# Flask Sample Application

This is a simple **Flask** web application that demonstrates how to create basic routes, return JSON responses, and handle user input using both **URL** and **query parameters**.

---

## 🚀 What is Flask?

**Flask** is a lightweight and flexible web framework for Python.  
It allows developers to quickly build web applications, APIs, and services with minimal setup.

Flask provides:
- A simple way to define routes and handle requests.
- Built-in development server and debugger.
- Easy integration with databases and templates.
- Flexibility for both small and large projects.

Official documentation: [https://flask.palletsprojects.com](https://flask.palletsprojects.com)

---

## 📁 Project Structure

flask_app/
│
├── app.py # Main Flask application file
├── requirements.txt # Python dependencies (Flask)
└── README.md # Documentation file


---

## ⚙️ Installation & Setup

### 1. Clone or download this repository

```bash
git clone https://github.com/yourusername/flask_app.git
cd flask_app

2. Create a virtual environment (recommended)
python -m venv venv
source venv/bin/activate      # For macOS/Linux
venv\Scripts\activate         # For Windows

3. Install dependencies
Create a requirements.txt file (if not present) with:
Flask==3.0.3
Then run:
pip install -r requirements.txt

▶️ Running the App
To start the Flask app, run:
 * python app.py


You should see output similar to:
 * Running on http://127.0.0.1:5000
 * Press CTRL+C to quit

🌐 Available Routes
1. Root Route

URL: /
Method: GET
Description: Returns a welcome message.
Example:
http://127.0.0.1:5000/

Response:

Welcome to the Flask App!

2. Health Check Route

URL: /health
Method: GET
Description: Simple health check endpoint for monitoring or testing.
Example:
http://127.0.0.1:5000/health

Response (JSON):

{
  "status": "healthy"
}

3. User Greeting (URL Parameter)

URL: /user/<name>
Method: GET
Description: Takes a user's name directly in the URL and returns a personalized greeting.
Example:
http://127.0.0.1:5000/user/Alice

Response (JSON):

{
  "message": "Hello, Alice!"
}

4. User Greeting (Query Parameter)

URL: /user?name=<name>
Method: GET
Description: Accepts the user's name as a query parameter instead.
Example:
http://127.0.0.1:5000/user?name=Bob

Response (JSON):

{
  "message": "Hello, Bob!"
}


If no name is provided:

{
  "message": "Hello, Guest!"
}


# Flask In-Memory Cache CRUD

A small example Flask application that implements CRUD (Create, Read, Update, Delete) operations backed by a thread-safe in-memory repository and a simple in-memory cache with optional TTL (time-to-live) per entry.

This repository is intended as a compact educational example for development and testing. It demonstrates cache priming, lazy TTL expiry, and cache invalidation on writes.

---

## Features

- Thread-safe in-memory repository for storing items (UUID keys).
- Thread-safe in-memory cache with per-entry TTL and manual invalidation.
- CRUD HTTP endpoints for `items`:
  - `POST   /items` — create an item
  - `GET    /items` — list all items (cached)
  - `GET    /items/<id>` — get single item (cached)
  - `PUT    /items/<id>` — update an item (invalidates cache)
  - `DELETE /items/<id>` — delete an item (invalidates cache)
- Endpoint to clear the cache: `POST /cache/clear`.
- Example priming of item-level cache after create/update.

---

## Requirements

- Python 3.8+
- Flask

You can install dependencies with:

```bash
pip install Flask
```

(Note: this example uses only the `flask` package — no external cache libraries required.)

---

## Running the app

Run the script directly for development:

```bash
python flask_in_memory_cache_crud.py
```

By default the app runs on `http://127.0.0.1:5000` with Flask's development server.

> **Important:** For production use a WSGI server (Gunicorn / uWSGI), and prefer an external/distributed cache (Redis) if you have multiple processes or machines.

---

## API — Endpoints & Examples

### Create an item

```bash
curl -X POST -H "Content-Type: application/json" \
  -d '{"name":"Alice","age":30}' \
  http://127.0.0.1:5000/items
```

Response: `201 Created` with the created item JSON (containing generated `id`).

### List items (cached)

```bash
curl http://127.0.0.1:5000/items
```

Response contains `{ "cached": <true|false>, "items": [...] }`. When `cached: true`, the items came from the list cache.

### Get single item (cached)

```bash
curl http://127.0.0.1:5000/items/<id>
```

Response contains `{ "cached": <true|false>, "item": { ... } }` or `404` if not found.

### Update an item

```bash
curl -X PUT -H "Content-Type: application/json" \
  -d '{"age":31}' \
  http://127.0.0.1:5000/items/<id>
```

This invalidates the list cache and the item cache, and re-primes the item cache with the updated value. Returns `200 OK` with the updated item.

### Delete an item

```bash
curl -X DELETE http://127.0.0.1:5000/items/<id>
```

Deletes the item, invalidates caches, and returns `200 OK`.

### Clear cache (manual)

```bash
curl -X POST http://127.0.0.1:5000/cache/clear
```

Clears the entire in-memory cache and returns `{ "ok": true }`.

---

## Cache behaviour & design notes

- **TTL (time-to-live):** Each cache entry can have a TTL in seconds. A TTL of `0` (or `None`) means "no expiry". The example script uses constants for `LIST_CACHE_TTL` and `ITEM_CACHE_TTL` that you can change.

- **Lazy expiry:** Expiration is checked lazily on access (when `get()` is called). Expired entries are removed on first access after expiration. The example does not include an active sweeper thread — add one if you need memory reclaimed promptly for cold keys.

- **Invalidate on writes:** The application invalidates related cache keys on `create`, `update`, and `delete` operations to keep list and item caches consistent with the repository.

- **Thread-safety:** Both the repository and cache use `threading.RLock` to ensure operations are atomic and free of races in a multi-threaded environment.

- **Priming:** After creating or updating an item the code primes the item-level cache with the new value so subsequent reads hit the cache.

---

## Improvements & Production considerations

If you plan to use a similar pattern in production consider:

- Replace the in-memory cache with a distributed cache (Redis, Memcached) to support multiple processes/hosts.
- Use `time.monotonic()` for TTL arithmetic to avoid issues with system clock changes.
- Add per-key request coalescing or mutexes to prevent cache stampede for expensive value computations.
- Add metrics (cache hits/misses, TTL expirations) and logging for observability.
- Consider a background sweeper if you must reclaim memory for expired keys promptly.
- Implement maximum-size eviction (LRU/LFU) if your memory footprint must be bounded — `cachetools` is helpful here.
- Return immutable/copy of cached objects to avoid accidental mutation by callers.

---

## Testing

You can write unit tests against `InMemoryRepository` and `InMemoryCache` directly. Example test ideas:

- Cache `set` + `get` with and without TTL.
- Cache expiry behavior for different TTL values.
- Concurrency tests: run many threads doing gets/sets/deletes and assert data consistency.
- API tests using Flask's test client to assert cache priming and invalidation behavior.

---

## Contributing

This is a small example — feel free to open issues or submit PRs to add features like:

- A configuration file or CLI flags for TTL values.
- A background sweeper implementation.
- Optional per-key locks to prevent stampedes.
- Integration with a real cache backend (Redis) behind a consistent API.

---
