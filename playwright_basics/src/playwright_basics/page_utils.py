"""Page interaction and form handling utilities."""
from typing import Dict, Any, List, Optional
from playwright.sync_api import Page

class FormUtils:
    """Form handling and validation utilities."""
    
    def __init__(self, page: Page):
        """Initialize with a Playwright page."""
        self.page = page
    
    def fill_form(self, form_data: dict, submit_selector: str = None) -> bool:
        """Fill form fields with provided data."""
        try:
            for selector, value in form_data.items():
                self.page.fill(selector, value)
            
            if submit_selector:
                self.page.click(submit_selector)
            
            return True
        except Exception as e:
            print(f"Error filling form: {str(e)}")
            return False

    @staticmethod
    async def get_form_data(page: Page, form_selector: str) -> Dict[str, Any]:
        """Get current form field values."""
        return await page.evaluate("""(formSelector) => {
            const form = document.querySelector(formSelector);
            if (!form) return {};
            
            const data = {};
            const elements = form.elements;
            for (let i = 0; i < elements.length; i++) {
                const el = elements[i];
                if (el.name) {
                    if (el.type === 'checkbox' || el.type === 'radio') {
                        data[el.name] = el.checked;
                    } else {
                        data[el.name] = el.value;
                    }
                }
            }
            return data;
        }""", form_selector)

class ValidationUtils:
    """Input validation and error handling utilities."""
    
    @staticmethod
    async def validate_field(page: Page, selector: str, value: str, rules: Dict[str, Any]) -> Dict[str, Any]:
        """Validate input field against rules."""
        results = {"selector": selector, "value": value, "valid": True, "errors": []}
        
        # Fill the field
        await page.fill(selector, value)
        
        # Check length rules
        if "min_length" in rules and len(value) < rules["min_length"]:
            results["valid"] = False
            results["errors"].append(f"Length must be at least {rules['min_length']}")
        
        if "max_length" in rules and len(value) > rules["max_length"]:
            results["valid"] = False
            results["errors"].append(f"Length must be at most {rules['max_length']}")
        
        # Check pattern rule
        if "pattern" in rules:
            is_valid = await page.evaluate("""(selector, pattern) => {
                const el = document.querySelector(selector);
                return new RegExp(pattern).test(el.value);
            }""", selector, rules["pattern"])
            
            if not is_valid:
                results["valid"] = False
                results["errors"].append("Value does not match required pattern")
        
        return results

    @staticmethod
    async def check_form_validation(page: Page, form_selector: str) -> Dict[str, Any]:
        """Check HTML5 form validation state."""
        return await page.evaluate("""(formSelector) => {
            const form = document.querySelector(formSelector);
            if (!form) return { error: 'Form not found' };
            
            const invalidElements = Array.from(form.querySelectorAll(':invalid'));
            return {
                valid: form.checkValidity(),
                invalidFields: invalidElements.map(el => ({
                    name: el.name,
                    type: el.type,
                    validationMessage: el.validationMessage
                }))
            };
        }""", form_selector)

class AjaxUtils:
    """AJAX request handling and monitoring utilities."""
    
    @staticmethod
    async def wait_for_response(page: Page, url_pattern: str, timeout: int = 30000) -> Dict[str, Any]:
        """Wait for and capture specific AJAX response."""
        try:
            response = await page.wait_for_response(url_pattern, timeout=timeout)
            return {
                "status": response.status,
                "headers": response.headers,
                "body": await response.json()
            }
        except Exception as e:
            return {"error": str(e)}

    @staticmethod
    async def monitor_network(page: Page, url_pattern: str = None) -> List[Dict[str, Any]]:
        """Monitor network requests matching pattern."""
        requests = []
        
        page.on("request", lambda request: requests.append({
            "url": request.url,
            "method": request.method,
            "headers": request.headers,
            "resource_type": request.resource_type
        }))
        
        page.on("response", lambda response: requests[-1].update({
            "status": response.status,
            "response_headers": response.headers
        }))
        
        return requests