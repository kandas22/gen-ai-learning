import pytest
from playwright.async_api import Page
from playwright_basics import FormUtils


@pytest.mark.asyncio
async def test_fill_form(page: Page):
    """Test the form filling functionality (async)."""
    # Navigate to a test page with a form
    await page.goto('data:text/html,<form id="testForm"><input id="name"><input id="email"><textarea id="message"></textarea><button id="submit">Submit</button></form>')

    form_data = {
        "#name": "John Doe",
        "#email": "john@example.com",
        "#message": "Hello, World!"
    }

    # Use the async FormUtils API
    result = await FormUtils.fill_form(page, form_data, "#submit")

    # Verify result
    assert result is True

    # Verify field values
    assert await page.input_value("#name") == "John Doe"
    assert await page.input_value("#email") == "john@example.com"
    assert await page.input_value("#message") == "Hello, World!"