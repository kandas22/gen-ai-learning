"""Pytest configuration helpers for the tests folder.

This file provides test-wide pytest hooks and fixtures. Keep it minimal so that
pytest can import it reliably.
"""

import pytest

import asyncio


@pytest.fixture(scope="module")
def event_loop():
    """Create an event loop for module-scoped async fixtures.

    pytest-asyncio provides a function-scoped event_loop by default. Tests that
    declare module-scoped async fixtures (like a test server) require a module
    scoped event loop; defining it here ensures those fixtures can run.
    """
    loop = asyncio.new_event_loop()
    try:
        yield loop
    finally:
        loop.close()


def pytest_configure(config):
    """Register custom markers programmatically (keeps pytest quiet on unknown markers)."""
    config.addinivalue_line("markers", "asyncio: mark a test as an async test")
