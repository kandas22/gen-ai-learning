"""Core browser and page manipulation utilities."""
from typing import Optional, Dict, Any
from playwright.sync_api import Page, Browser, BrowserContext

class BrowserUtils:
    """Browser utility functions for common operations."""
    
    @staticmethod
    async def get_browser_info(browser: Browser) -> Dict[str, Any]:
        """Get information about the current browser."""
        return {
            "browser_type": browser.browser_type.name,
            "version": await browser.version(),
            "contexts": len(browser.contexts),
            "is_connected": browser.is_connected()
        }

    @staticmethod
    def get_page_info(page: Page) -> Dict[str, str]:
        """Get information about the current page."""
        return {
            "url": page.url,
            "title": page.title(),
            "viewport": page.viewport_size,
            "content_size": {
                "width": page.evaluate("document.documentElement.scrollWidth"),
                "height": page.evaluate("document.documentElement.scrollHeight")
            }
        }

class NavigationUtils:
    """Navigation and URL manipulation utilities."""
    
    @staticmethod
    async def navigate_and_wait(page: Page, url: str, wait_for: Optional[str] = None) -> Dict[str, Any]:
        """Navigate to URL and optionally wait for selector."""
        response = await page.goto(url)
        if wait_for:
            await page.wait_for_selector(wait_for)
        
        return {
            "status": response.status if response else None,
            "url": page.url,
            "title": await page.title()
        }

    @staticmethod
    async def back_forward(page: Page, steps_back: int = 1, steps_forward: int = 0) -> Dict[str, Any]:
        """Navigate back and forward in history."""
        for _ in range(steps_back):
            await page.go_back()
        
        for _ in range(steps_forward):
            await page.go_forward()
        
        return {
            "current_url": page.url,
            "can_go_back": page.evaluate("window.history.length > 1"),
            "can_go_forward": page.evaluate("window.history.length > window.history.state + 1")
        }

class ElementUtils:
    """Element interaction and manipulation utilities."""
    
    @staticmethod
    async def get_element_info(page: Page, selector: str) -> Dict[str, Any]:
        """Get information about an element."""
        element = await page.wait_for_selector(selector)
        if not element:
            return {"error": f"Element not found: {selector}"}
        
        return {
            "text": await element.text_content(),
            "tag_name": await element.evaluate("el => el.tagName.toLowerCase()"),
            "attributes": await element.evaluate("el => Object.assign({}, ...Array.from(el.attributes).map(a => ({[a.name]: a.value})))"),
            "is_visible": await element.is_visible(),
            "bbox": await element.bounding_box()
        }

    @staticmethod
    async def interact_with_element(page: Page, selector: str, action: str, value: Optional[str] = None) -> Dict[str, Any]:
        """Perform common interactions with elements."""
        element = await page.wait_for_selector(selector)
        if not element:
            return {"error": f"Element not found: {selector}"}
        
        result = {"action": action, "selector": selector}
        
        if action == "click":
            await element.click()
        elif action == "type":
            await element.type(value or "")
        elif action == "select":
            await element.select_option(value or "")
        elif action == "check":
            await element.check()
        elif action == "uncheck":
            await element.uncheck()
        
        result["success"] = True
        return result

class ScreenshotUtils:
    """Screenshot and visual verification utilities."""
    
    @staticmethod
    async def take_screenshots(page: Page, name: str, full_page: bool = False) -> Dict[str, str]:
        """Take various types of screenshots."""
        results = {}
        
        # Full page or viewport screenshot
        results["page"] = await page.screenshot(
            path=f"{name}_page.png",
            full_page=full_page
        )
        
        # PDF (only works in headless Chrome)
        if "chromium" in page.browser_type.name.lower():
            results["pdf"] = await page.pdf(path=f"{name}.pdf")
        
        return results

    @staticmethod
    async def element_screenshot(page: Page, selector: str, name: str) -> Dict[str, Any]:
        """Take screenshot of specific element."""
        element = await page.wait_for_selector(selector)
        if not element:
            return {"error": f"Element not found: {selector}"}
        
        screenshot = await element.screenshot(path=f"{name}_element.png")
        return {
            "selector": selector,
            "screenshot": screenshot
        }