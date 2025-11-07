# search_scorecard.py
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import time
import sys

QUERY = "sa vs ind final scorecard"

def main(headless: bool = False):
    with sync_playwright() as p:
        # Choose browser: chromium, firefox or webkit
        browser = p.chromium.launch(headless=headless, slow_mo=50)   # slow_mo helps you watch the steps
        context = browser.new_context(
            viewport={"width": 1280, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36",
            locale="en-US",
            accept_downloads=True
        )

        page = context.new_page()

        try:
            # 1) Go to Bing (more stable in headless)
            page.goto("https://www.bing.com", wait_until="domcontentloaded", timeout=15000)

            # Try to accept consent if shown
            try:
                for sel in ["#bnp_btn_accept", "button:has-text('I agree')", "button:has-text('Accept')"]:
                    loc = page.locator(sel)
                    if loc.count() > 0:
                        loc.first.click()
                        page.wait_for_timeout(500)
                        break
            except Exception:
                pass

            # 2) Wait for Bing search box, type the query and press Enter
            try:
                search_box = page.wait_for_selector("input[name='q']", timeout=6000)
            except PlaywrightTimeoutError:
                # fallback to common Bing id
                search_box = page.wait_for_selector("#sb_form_q", timeout=6000)
            search_box.fill(QUERY)
            search_box.press("Enter")

            # 3) Wait for results to load (Bing result links are typically li.b_algo h2 a)
            page.wait_for_selector("li.b_algo h2 a", timeout=10000)

            # 4) Find best candidate among result links on Bing
            results = page.locator("li.b_algo h2 a")
            count = results.count()
            chosen_index = None
            chosen_href = None
            chosen_title = None

            # Heuristics for picking a scorecard:
            # - 'scorecard' in href or title
            # - OR known cricket sites (espncricinfo, cricbuzz) in href
            # - fallback: first result
            for i in range(count):
                link = results.nth(i)
                # title is the anchor text itself on Bing
                try:
                    title = link.inner_text().strip()
                except Exception:
                    title = ""
                href = link.get_attribute("href") or ""

                low_href = href.lower()
                low_title = title.lower()

                if ("scorecard" in low_href) or ("scorecard" in low_title) \
                   or ("espncricinfo" in low_href) or ("cricbuzz" in low_href) \
                   or ("cricket" in low_title) or ("cricket" in low_href):
                    chosen_index = i
                    chosen_href = href
                    chosen_title = title
                    break

            # fallback to first result if none matched heuristics
            if chosen_index is None and count > 0:
                chosen_index = 0
                chosen_href = results.nth(0).get_attribute("href")
                try:
                    chosen_title = results.nth(0).locator("h3").inner_text().strip()
                except Exception:
                    chosen_title = ""

            if chosen_index is None:
                print("No search results found. Exiting.")
                browser.close()
                return

            print(f"Clicking result #{chosen_index + 1}: {chosen_title}\n{chosen_href}")

            # 5) Click the chosen link and wait for navigation
            results.nth(chosen_index).click()
            try:
                # Wait for network to be idle or timeout after 15s
                page.wait_for_load_state("networkidle", timeout=15000)
            except PlaywrightTimeoutError:
                # continue even if networkidle times out
                pass

            # Small pause to let dynamic content render
            page.wait_for_timeout(1200)

            # 6) Save a screenshot of the scorecard page and print page title/URL
            timestamp = int(time.time())
            screenshot_path = f"scorecard_{timestamp}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"Screenshot saved to: {screenshot_path}")

            page_title = page.title()
            page_url = page.url
            print(f"Final page title: {page_title}")
            print(f"Final page URL: {page_url}")

            # Optional: Save HTML snapshot for later inspection
            html_path = f"scorecard_{timestamp}.html"
            with open(html_path, "w", encoding="utf-8") as f:
                f.write(page.content())
            print(f"HTML saved to: {html_path}")

        except PlaywrightTimeoutError as e:
            print("A timeout occurred while performing steps:", str(e))
        except Exception as e:
            print("An unexpected error occurred:", str(e))
        finally:
            browser.close()


if __name__ == "__main__":
    # Run with headful to see the browser, pass --headless to run headless
    headless_flag = False
    if "--headless" in sys.argv:
        headless_flag = True
    main(headless=headless_flag)