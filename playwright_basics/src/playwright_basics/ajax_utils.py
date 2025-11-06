"""Utility functions for monitoring AJAX requests in Playwright."""

from typing import List, Optional, Dict, Any
import asyncio
import fnmatch
from playwright.async_api import Page, Request, Response

class AjaxUtils:
    @staticmethod
    async def monitor_network(
        page: Page,
        url_pattern: str,
        timeout: float = 30000
    ) -> List[Dict[str, Any]]:
        """
        Wait for a network request matching a pattern and return its details.

        This is implemented using Playwright's wait_for_request which supports
        string patterns (including globs) or predicates.
        """
        # Fall back to an event-listener approach which works across contexts.
        requests: List[Dict[str, Any]] = []
        loop = asyncio.get_event_loop()
        future = loop.create_future()

        def _on_request(req: Request):
            try:
                if fnmatch.fnmatch(req.url, url_pattern.replace('**', '*')):
                    info = {
                        "url": req.url,
                        "method": req.method,
                        "headers": req.headers,
                        "post_data": req.post_data,
                    }
                    requests.append(info)
                    if not future.done():
                        future.set_result(requests)
            except Exception:
                pass

        page.on("request", _on_request)

        try:
            results = await asyncio.wait_for(future, timeout=timeout / 1000)
            return results
        except asyncio.TimeoutError:
            return requests
        finally:
            try:
                # Playwright uses `off` to remove event listeners
                page.off("request", _on_request)
            except Exception:
                pass

    @staticmethod
    async def wait_for_response(
        page: Page,
        url_pattern: str,
        timeout: float = 30000
    ) -> Optional[Dict[str, Any]]:
        """
        Wait for a response matching a URL pattern.
        
        Args:
            page: Playwright page object
            url_pattern: URL pattern to match
            timeout: Maximum time to wait in milliseconds
            
        Returns:
            Response data if found, None otherwise
        """
        try:
            # Wait for response
            pattern = url_pattern.replace('**', '*')
            response = await page.wait_for_response(
                lambda r: fnmatch.fnmatch(r.url, pattern),
                timeout=timeout
            )
            
            # Get response data
            status = response.status
            headers = response.headers
            
            try:
                body = await response.json()
            except:
                try:
                    body = await response.text()
                except:
                    body = None
                    
            return {
                "status": status,
                "headers": headers,
                "body": body
            }
            
        except Exception as e:
            print(f"Error waiting for response: {str(e)}")
            return None

    @staticmethod
    async def intercept_requests(
        page: Page,
        url_pattern: str,
        mock_response: Dict[str, Any]
    ) -> bool:
        """
        Intercept and mock responses for matching requests.
        
        Args:
            page: Playwright page object
            url_pattern: URL pattern to match
            mock_response: Response data to return
            
        Returns:
            bool: True if interception was set up successfully
        """
        try:
            async def _handler(route):
                await route.fulfill(**mock_response)

            await page.route(url_pattern, _handler)
            return True
            
        except Exception as e:
            print(f"Error setting up request interception: {str(e)}")
            return False

    @staticmethod
    async def clear_request_interception(
        page: Page,
        url_pattern: str
    ) -> bool:
        """
        Clear request interception for a URL pattern.
        
        Args:
            page: Playwright page object
            url_pattern: URL pattern to unroute
            
        Returns:
            bool: True if interception was cleared successfully
        """
        try:
            await page.unroute(url_pattern)
            return True
            
        except Exception as e:
            print(f"Error clearing request interception: {str(e)}")
            return False