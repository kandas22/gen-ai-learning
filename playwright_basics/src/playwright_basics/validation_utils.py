"""Utility functions for form validation in Playwright."""

from typing import Dict, Any, Optional, List
from playwright.async_api import Page

class ValidationUtils:
    @staticmethod
    async def validate_field(
        page: Page,
        selector: str,
        error_class: str,
        rules: Dict[str, Any]
    ) -> Dict[str, bool]:
        """
        Validate a form field against given rules.
        
        Args:
            page: Playwright page object
            selector: Field selector
            error_class: Class name for error state
            rules: Dictionary of validation rules
            
        Returns:
            Dictionary of validation results
        """
        validation = {}
        
        try:
            element = await page.query_selector(selector)
            if not element:
                return {"exists": False}
                
            value = await element.input_value()
            
            # Required field
            if rules.get("required"):
                validation["required"] = bool(value.strip())
                
            # Minimum length
            if "min_length" in rules:
                validation["min_length"] = len(value) >= rules["min_length"]
                
            # Maximum length
            if "max_length" in rules:
                validation["max_length"] = len(value) <= rules["max_length"]
                
            # Pattern matching
            if "pattern" in rules:
                import re
                validation["pattern"] = bool(re.match(rules["pattern"], value))
                
            # Custom validation function
            if "custom_validation" in rules:
                validation["custom"] = await rules["custom_validation"](value)
                
            return validation
                
        except Exception as e:
            print(f"Error validating field: {str(e)}")
            return {"error": str(e)}

    @staticmethod
    async def check_form_validation(
        page: Page,
        form_selector: str,
        error_class: str = "invalid"
    ) -> Dict[str, List[str]]:
        """
        Check validation state of all form fields.
        
        Args:
            page: Playwright page object
            form_selector: Selector for the form
            error_class: Class name indicating invalid state
            
        Returns:
            Dictionary mapping field names to error messages
        """
        validation_state = {}
        
        try:
            # Get all form fields
            fields = await page.query_selector_all(
                f"{form_selector} input, {form_selector} textarea, {form_selector} select"
            )
            
            for field in fields:
                name = await field.get_attribute("name")
                if not name:
                    continue
                    
                # Check for error class
                has_error = await field.evaluate(
                    f"el => el.classList.contains('{error_class}')"
                )
                
                # Get error message if present
                error_message = None
                if has_error:
                    # Try to find associated error message
                    error_el = await page.query_selector(
                        f"[data-error-for='{name}'], #{name}-error, .{name}-error"
                    )
                    if error_el:
                        error_message = await error_el.text_content()
                        
                validation_state[name] = error_message if error_message else []
                
            return validation_state
            
        except Exception as e:
            print(f"Error checking form validation: {str(e)}")
            return {"error": [str(e)]}

    @staticmethod
    async def wait_for_validation(
        page: Page,
        selector: str,
        timeout: float = 5000
    ) -> bool:
        """
        Wait for field validation to complete.
        
        Args:
            page: Playwright page object
            selector: Field selector
            timeout: Maximum time to wait in milliseconds
            
        Returns:
            bool: True if validation completed successfully
        """
        try:
            # Wait for validation classes to be applied
            await page.wait_for_selector(
                f"{selector}:not(.validating)",
                timeout=timeout
            )
            return True
            
        except Exception as e:
            print(f"Error waiting for validation: {str(e)}")
            return False