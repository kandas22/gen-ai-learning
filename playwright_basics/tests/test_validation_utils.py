"""
Example test cases for validation utilities.
"""

import pytest
import asyncio
from typing import Dict, Any
from playwright.async_api import async_playwright, Page
from playwright_basics import ValidationUtils

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
async def test_field_validation(browser_page: Page):
    """Test field validation with various rules."""
    # Set up test form
    await browser_page.set_content("""
        <form id="test-form">
            <input type="text" id="username" name="username">
            <span id="username-error"></span>
        </form>
    """)
    
    # Set up validation rules
    rules = {
        "required": True,
        "min_length": 3,
        "max_length": 20,
        "pattern": r"^[a-zA-Z0-9_]+$"
    }
    
    # Test empty field
    result = await ValidationUtils.validate_field(
        browser_page,
        "#username",
        "invalid",
        rules
    )
    assert result["required"] is False
    
    # Test valid input
    await browser_page.fill("#username", "valid_username123")
    result = await ValidationUtils.validate_field(
        browser_page,
        "#username",
        "invalid",
        rules
    )
    assert all(result.values())
    
    # Test invalid pattern
    await browser_page.fill("#username", "invalid@username")
    result = await ValidationUtils.validate_field(
        browser_page,
        "#username",
        "invalid",
        rules
    )
    assert not result["pattern"]

@pytest.mark.asyncio
async def test_form_validation(browser_page: Page):
    """Test form-wide validation checks."""
    # Set up test form
    await browser_page.set_content("""
        <form id="test-form">
            <input type="text" id="name" name="name" class="valid">
            <span id="name-error"></span>
            
            <input type="email" id="email" name="email" class="invalid">
            <span id="email-error">Invalid email format</span>
            
            <input type="password" id="password" name="password" class="invalid">
            <span id="password-error">Password too short</span>
        </form>
    """)
    
    # Check validation state
    validation_state = await ValidationUtils.check_form_validation(
        browser_page,
        "#test-form",
        "invalid"
    )
    
    # Verify results
    assert "name" in validation_state
    assert len(validation_state["name"]) == 0  # No errors
    
    assert "email" in validation_state
    assert validation_state["email"] == ["Invalid email format"]
    
    assert "password" in validation_state
    assert validation_state["password"] == ["Password too short"]

@pytest.mark.asyncio
async def test_validation_waiting(browser_page: Page):
    """Test waiting for validation to complete."""
    # Set up test form with async validation
    await browser_page.set_content("""
        <form id="test-form">
            <input type="email" id="email" name="email">
            <script>
                const emailInput = document.getElementById('email');
                emailInput.addEventListener('input', async () => {
                    emailInput.classList.add('validating');
                    await new Promise(resolve => setTimeout(resolve, 1000));
                    emailInput.classList.remove('validating');
                    emailInput.classList.add('valid');
                });
            </script>
        </form>
    """)
    
    # Trigger validation
    await browser_page.fill("#email", "test@example.com")
    
    # Wait for validation
    result = await ValidationUtils.wait_for_validation(
        browser_page,
        "#email",
        timeout=2000
    )
    
    # Verify validation completed
    assert result is True
    
    # Verify final state
    has_valid = await browser_page.evaluate(
        "el => el.classList.contains('valid')",
        await browser_page.query_selector("#email")
    )
    assert has_valid