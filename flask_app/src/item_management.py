"""
Flask app implementing CRUD operations backed by an in-memory cache + in-memory repository.

Features:
- Thread-safe in-memory repository (dict) to store items.
- Thread-safe in-memory cache with optional TTL per entry.
- Automatic cache invalidation on writes (create/update/delete).
- Endpoints:
    POST   /items        -> create item (JSON body)
    GET    /items        -> list all items (cached)
    GET    /items/<id>   -> get single item (cached)
    PUT    /items/<id>   -> update item (invalidates cache)
    DELETE /items/<id>   -> delete item (invalidates cache)
- Simple JSON responses with proper HTTP status codes.

Usage:
    python flask_in_memory_cache_crud.py

Example curl commands:
  Create:
    curl -X POST -H "Content-Type: application/json" -d '{"name":"Alice","age":30}' http://127.0.0.1:5000/items

  List:
    curl http://127.0.0.1:5000/items

  Get one:
    curl http://127.0.0.1:5000/items/<id>

  Update:
    curl -X PUT -H "Content-Type: application/json" -d '{"age":31}' http://127.0.0.1:5000/items/<id>

  Delete:
    curl -X DELETE http://127.0.0.1:5000/items/<id>

Notes:
- This is an example in-memory approach suitable for development and testing. For production use a persistent DB + distributed cache.
- TTL = 0 means "no expiry".
"""

from flask import Flask, request, jsonify, abort
from uuid import uuid4
from threading import RLock
from time import time
from typing import Any, Dict, Optional, Tuple

app = Flask(__name__)


class InMemoryCache:
    """Simple thread-safe in-memory cache with TTL support and manual invalidation."""

    def __init__(self):
        self._store: Dict[str, Tuple[Any, float]] = {}
        self._lock = RLock()

    def set(self, key: str, value: Any, ttl_seconds: float = 0) -> None:
        """Store value with optional TTL. ttl_seconds=0 means no expiry."""
        expiry = time() + ttl_seconds if ttl_seconds and ttl_seconds > 0 else 0
        with self._lock:
            self._store[key] = (value, expiry)

    def get(self, key: str) -> Optional[Any]:
        with self._lock:
            entry = self._store.get(key)
            if not entry:
                return None
            value, expiry = entry
            if expiry and time() > expiry:
                # expired
                del self._store[key]
                return None
            return value

    def delete(self, key: str) -> None:
        with self._lock:
            if key in self._store:
                del self._store[key]

    def clear(self) -> None:
        with self._lock:
            self._store.clear()


class InMemoryRepository:
    """Thread-safe in-memory repository for storing items."""

    def __init__(self):
        self._data: Dict[str, Dict[str, Any]] = {}
        self._lock = RLock()

    def create(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        with self._lock:
            _id = str(uuid4())
            item = {"id": _id, **payload}
            self._data[_id] = item
            return item

    def list_all(self) -> Dict[str, Dict[str, Any]]:
        with self._lock:
            # Return a shallow copy to avoid accidental mutation.
            return {k: v.copy() for k, v in self._data.items()}

    def get(self, _id: str) -> Optional[Dict[str, Any]]:
        with self._lock:
            item = self._data.get(_id)
            return item.copy() if item else None

    def update(self, _id: str, patch: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        with self._lock:
            item = self._data.get(_id)
            if not item:
                return None
            # update fields in place
            item.update(patch)
            return item.copy()

    def delete(self, _id: str) -> bool:
        with self._lock:
            if _id in self._data:
                del self._data[_id]
                return True
            return False


# Instantiate global repository and cache
repo = InMemoryRepository()
cache = InMemoryCache()

# Cache configuration
LIST_CACHE_KEY = "items:list"
LIST_CACHE_TTL = 30  # seconds (set to 0 to disable expiry)
ITEM_CACHE_PREFIX = "item:"
ITEM_CACHE_TTL = 60  # seconds


def cache_item_key(item_id: str) -> str:
    return ITEM_CACHE_PREFIX + item_id


# --- Flask routes ---

@app.route("/items", methods=["POST"])
def create_item():
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400
    payload = request.get_json()
    if not isinstance(payload, dict):
        return jsonify({"error": "JSON payload must be an object"}), 400

    item = repo.create(payload)

    # Invalidate list cache because collection changed
    cache.delete(LIST_CACHE_KEY)

    # Prime the cache for the newly created item
    cache.set(cache_item_key(item["id"]), item, ttl_seconds=ITEM_CACHE_TTL)

    return jsonify(item), 201


@app.route("/items", methods=["GET"])
def list_items():
    # Try to read from cache
    cached = cache.get(LIST_CACHE_KEY)
    if cached is not None:
        return jsonify({"cached": True, "items": list(cached.values())}), 200

    # Not in cache: read from repository and set cache
    data = repo.list_all()
    cache.set(LIST_CACHE_KEY, data, ttl_seconds=LIST_CACHE_TTL)
    return jsonify({"cached": False, "items": list(data.values())}), 200


@app.route("/items/<item_id>", methods=["GET"])
def get_item(item_id):
    key = cache_item_key(item_id)
    cached = cache.get(key)
    if cached is not None:
        return jsonify({"cached": True, "item": cached}), 200

    item = repo.get(item_id)
    if not item:
        return jsonify({"error": "Item not found"}), 404

    cache.set(key, item, ttl_seconds=ITEM_CACHE_TTL)
    return jsonify({"cached": False, "item": item}), 200


@app.route("/items/<item_id>", methods=["PUT"])
def update_item(item_id):
    if not request.is_json:
        return jsonify({"error": "Request body must be JSON"}), 400
    patch = request.get_json()
    if not isinstance(patch, dict):
        return jsonify({"error": "JSON payload must be an object"}), 400

    updated = repo.update(item_id, patch)
    if not updated:
        return jsonify({"error": "Item not found"}), 404

    # Invalidate caches
    cache.delete(cache_item_key(item_id))
    cache.delete(LIST_CACHE_KEY)

    # Re-prime item cache with updated value
    cache.set(cache_item_key(item_id), updated, ttl_seconds=ITEM_CACHE_TTL)

    return jsonify(updated), 200


@app.route("/items/<item_id>", methods=["DELETE"])
def delete_item(item_id):
    deleted = repo.delete(item_id)
    if not deleted:
        return jsonify({"error": "Item not found"}), 404

    # Invalidate caches
    cache.delete(cache_item_key(item_id))
    cache.delete(LIST_CACHE_KEY)

    return jsonify({"ok": True}), 200


@app.route("/cache/clear", methods=["POST"])
def clear_cache():
    cache.clear()
    return jsonify({"ok": True}), 200


if __name__ == "__main__":
    # For development use only. In production, use a WSGI server and consider process-local caches
    app.run(debug=True)
