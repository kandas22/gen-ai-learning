"""
Example test cases for form handling utilities using Playwright.
"""

import pytest
import asyncio
from playwright.async_api import async_playwright, Page
from playwright_basics import FormUtils, ValidationUtils, AjaxUtils

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

# FormUtils Tests
@pytest.mark.asyncio
async def test_fill_form(browser_page: Page):
    """Test form filling functionality."""
    # Set up a test form
    await browser_page.set_content("""
        <form id="test-form">
            <input type="text" id="name" name="name">
            <input type="email" id="email" name="email">
            <textarea id="message" name="message"></textarea>
            <button type="submit" id="submit">Submit</button>
        </form>
    """)

    # Test data
    form_data = {
        "#name": "Test User",
        "#email": "test@example.com",
        "#message": "Test message"
    }

    # Fill form
    result = await FormUtils.fill_form(
        browser_page,
        form_data,
        submit_selector="#submit"
    )

    # Verify fill was successful
    assert result is True

    # Verify field values
    assert await browser_page.input_value("#name") == "Test User"
    assert await browser_page.input_value("#email") == "test@example.com"
    assert await browser_page.input_value("#message") == "Test message"

# ValidationUtils Tests
@pytest.mark.asyncio
async def test_validate_field(browser_page: Page):
    """Test field validation functionality."""
    # Set up a test form with validation
    await browser_page.set_content("""
        <form id="test-form">
            <input type="email" id="email" name="email" class="valid">
        </form>
    """)

    # Set test value
    await browser_page.fill("#email", "test@example.com")

    # Validation rules
    rules = {
        "required": True,
        "pattern": r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",
        "min_length": 5
    }

    # Validate field
    result = await ValidationUtils.validate_field(
        browser_page,
        "#email",
        "invalid",
        rules
    )

    # Verify validation results
    assert result["required"] is True
    assert result["pattern"] is True
    assert result["min_length"] is True

# AjaxUtils Tests
@pytest.mark.asyncio
async def test_monitor_network(browser_page: Page):
    """Test network monitoring functionality."""
    # Set up test page with AJAX request
    await browser_page.set_content("""
        <script>
            async function makeRequest() {
                await fetch('/api/test', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({test: 'data'})
                });
            }
        </script>
        <button onclick="makeRequest()">Send Request</button>
    """)

    # Start monitoring
    requests_future = asyncio.create_task(
        AjaxUtils.monitor_network(browser_page, "**/api/test", timeout=1000)
    )

    # Trigger request
    await browser_page.click("button")

    # Get monitored requests
    requests = await requests_future

    # Verify request was captured
    assert len(requests) > 0
    assert requests[0]["method"] == "POST"
    assert requests[0]["url"].endswith("/api/test")