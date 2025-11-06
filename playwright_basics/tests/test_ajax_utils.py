"""
Example test cases for AjaxUtils functionality.
"""

import pytest
import asyncio
from typing import Dict, Any, Optional
from playwright.async_api import async_playwright, Page
from playwright_basics import AjaxUtils
from aiohttp import web

@pytest.fixture(scope="module")
async def test_server(request):
    """Create a simple test server for API requests."""
    
    async def mock_api_handler(request):
        """Handle API requests with mock responses."""
        return web.json_response({"status": "success"})
    
    app = web.Application()
    app.router.add_post("/api/test", mock_api_handler)
    
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", 8000)
    await site.start()
    
    yield "http://localhost:8000"
    
    await runner.cleanup()

@pytest.fixture
async def browser_page():
    """Create a browser page fixture for tests."""
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context()
        page = await context.new_page()
        try:
            yield page
        finally:
            await context.close()
            await browser.close()

@pytest.mark.asyncio
async def test_monitor_network(browser_page: Page, test_server: str):
    """Test network request monitoring."""
    # Set up test page
    await browser_page.goto(test_server)
    await browser_page.set_content("""
        <button onclick="makeRequest()">Send Request</button>
        <script>
            async function makeRequest() {
                await fetch('/api/test', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({test: 'data'})
                });
            }
        </script>
    """)
    
    # Start monitoring
    monitor_task = asyncio.create_task(
        AjaxUtils.monitor_network(browser_page, "**/api/test", timeout=5000)
    )
    
    # Trigger request
    await browser_page.click("button")
    
    # Get monitored requests
    requests = await monitor_task
    
    # Verify request was captured
    assert len(requests) > 0
    request = requests[0]
    assert request["method"] == "POST"
    assert request["url"].endswith("/api/test")
    assert "Content-Type" in request["headers"]

@pytest.mark.asyncio
async def test_wait_for_response(browser_page: Page, test_server: str):
    """Test waiting for specific response."""
    # Set up test page
    await browser_page.goto(test_server)
    await browser_page.set_content("""
        <button onclick="makeRequest()">Send Request</button>
        <script>
            async function makeRequest() {
                await fetch('/api/test', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({test: 'data'})
                });
            }
        </script>
    """)
    
    # Start waiting for response
    response_future = asyncio.create_task(
        AjaxUtils.wait_for_response(browser_page, "**/api/test", timeout=5000)
    )
    
    # Trigger request
    await browser_page.click("button")
    
    # Get response
    response = await response_future
    
    # Verify response
    assert response is not None
    assert response["status"] == 200
    assert response["body"]["status"] == "success"

@pytest.mark.asyncio
async def test_request_interception(browser_page: Page, test_server: str):
    """Test request interception and mocking."""
    # Set up mock response
    mock_response = {
        "status": 200,
        "headers": {"Content-Type": "application/json"},
        "body": '{"status": "mocked"}'
    }
    
    # Set up interception
    success = await AjaxUtils.intercept_requests(
        browser_page,
        "**/api/test",
        mock_response
    )
    assert success is True
    
    # Set up test page
    await browser_page.goto(test_server)
    await browser_page.set_content("""
        <button onclick="makeRequest()">Send Request</button>
        <script>
            async function makeRequest() {
                const response = await fetch('/api/test');
                const data = await response.json();
                document.body.textContent = data.status;
            }
        </script>
    """)
    
    # Trigger request
    await browser_page.click("button")
    
    # Verify intercepted response
    content = await browser_page.text_content("body")
    assert content == "mocked"
    
    # Clear interception
    success = await AjaxUtils.clear_request_interception(
        browser_page,
        "**/api/test"
    )
    assert success is True