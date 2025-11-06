"""Utility functions for form handling in Playwright."""

from typing import Dict, Any, Optional, List
from playwright.async_api import Page

class FormUtils:
    @staticmethod
    async def fill_form(
        page: Page,
        form_data: Dict[str, str],
        submit_selector: Optional[str] = None,
        delay: float = 0.0,
    ) -> bool:
        """
        Fill form fields with provided data.

        Args:
            page: Playwright async Page object
            form_data: dict mapping CSS selectors to values
            submit_selector: optional selector to click after filling
            delay: seconds to wait between filling fields

        Returns:
            True on success, False on error
        """
        try:
            for selector, value in form_data.items():
                await page.fill(selector, value)
                if delay > 0:
                    await page.wait_for_timeout(delay * 1000)

            if submit_selector:
                # Click the submit button but prevent the default navigation so tests
                # can still inspect the form fields on the page. We attach a one-time
                # submit handler that calls preventDefault(), then trigger the click.
                await page.evaluate(
                    """
                    (sel) => {
                        const btn = document.querySelector(sel);
                        if (!btn) return;
                        const form = btn.closest('form');
                        if (form) {
                            form.addEventListener('submit', e => e.preventDefault(), { once: true });
                        }
                        btn.click();
                    }
                    """,
                    submit_selector,
                )
            return True

        except Exception as e:
            print(f"Error filling form: {str(e)}")
            return False

    @staticmethod
    async def get_form_data(page: Page, form_selector: str) -> Dict[str, str]:
        """
        Get the current data from a form.
        
        Args:
            page: Playwright page object
            form_selector: Selector for the form element
            
        Returns:
            Dictionary of form field values
        """
        form_data = {}
        try:
            # Get all input elements
            inputs = await page.query_selector_all(f"{form_selector} input")
            textareas = await page.query_selector_all(f"{form_selector} textarea")
            selects = await page.query_selector_all(f"{form_selector} select")
            
            # Process inputs
            for input_el in inputs:
                name = await input_el.get_attribute("name")
                if name:
                    value = await input_el.input_value()
                    form_data[name] = value
                    
            # Process textareas
            for textarea in textareas:
                name = await textarea.get_attribute("name")
                if name:
                    value = await textarea.input_value()
                    form_data[name] = value
                    
            # Process selects
            for select in selects:
                name = await select.get_attribute("name")
                if name:
                    value = await select.input_value()
                    form_data[name] = value
                    
            return form_data
            
        except Exception as e:
            print(f"Error getting form data: {str(e)}")
            return {}

    @staticmethod
    async def clear_form(page: Page, form_selector: str) -> bool:
        """
        Clear all fields in a form.
        
        Args:
            page: Playwright page object
            form_selector: Selector for the form element
            
        Returns:
            bool: True if form was cleared successfully
        """
        try:
            # Clear inputs
            inputs = await page.query_selector_all(f"{form_selector} input")
            for input_el in inputs:
                input_type = await input_el.get_attribute("type")
                if input_type not in ["submit", "button", "reset"]:
                    await input_el.fill("")
            
            # Clear textareas
            textareas = await page.query_selector_all(f"{form_selector} textarea")
            for textarea in textareas:
                await textarea.fill("")
                
            # Reset selects to first option
            selects = await page.query_selector_all(f"{form_selector} select")
            for select in selects:
                options = await select.query_selector_all("option")
                if options:
                    first_value = await options[0].get_attribute("value")
                    if first_value:
                        await select.select_option(first_value)
                        
            return True
            
        except Exception as e:
            print(f"Error clearing form: {str(e)}")
            return False