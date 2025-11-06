import asyncio
from playwright.async_api import async_playwright, Playwright
import time
from typing import List, Dict, Any
import csv
from datetime import datetime

# Define the list of critical websites (same as before)
TARGET_SITES: List[Dict] = [
    {"url": "https://www.google.com/", "expected_load_time_sec": 2.0, "critical_element": "img[alt='Google']"},
    {"url": "https://playwright.dev/python/", "expected_load_time_sec": 3.5, "critical_element": "text=Playwright"},
]

CSV_FILE = "website_health_report.csv"

async def check_site_health(playwright: Playwright, target: Dict) -> Dict[str, Any]:
    """
    Performs the health check and returns a dictionary of the results.
    """
    url = target['url']
    expected_time = target['expected_load_time_sec']
    critical_element = target['critical_element']
    
    # Initialize the results dictionary
    result: Dict[str, Any] = {
        'timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        'url': url,
        'status_code': 0,
        'load_time_sec': 0.0,
        'time_alert': False,
        'content_check': False,
        'error_message': None,
    }
    
    # 1. Launch Browser and Context
    browser = await playwright.chromium.launch()
    page = await browser.new_page()
    
    try:
        # 2. Navigate and Measure Load Time
        start_time = time.time()
        
        response = await page.goto(url, timeout=30000, wait_until='networkidle')
        
        end_time = time.time()
        load_time = round(end_time - start_time, 2)
        
        result['load_time_sec'] = load_time
        result['status_code'] = response.status if response else 0
        
        print(f"--- Check Summary for {url} ---")

        # 3. Check Status Code and Performance
        if result['status_code'] != 200:
            print(f"❌ Status: {result['status_code']} FAILURE")
            # Set a clear error message for the log
            result['error_message'] = f"HTTP Status {result['status_code']}"
        
        if load_time > expected_time:
            print(f"⚠️ Performance Alert: {load_time}s > {expected_time}s")
            result['time_alert'] = True

        # 4. Content Check (Only if successful HTTP status)
        if result['status_code'] == 200:
            try:
                locator = page.get_by_text(critical_element, exact=False)
                await locator.wait_for(timeout=5000)
                result['content_check'] = True
                print(f"✔️ Content Check: Element '{critical_element}' found.")
            except Exception:
                result['content_check'] = False
                result['error_message'] = "Critical element missing."
                print(f"❌ Content Alert: Element '{critical_element}' NOT found.")

    except Exception as e:
        # Catch any critical navigation or timeout errors
        error_msg = str(e).split('\n')[0] # Keep the error message concise
        result['error_message'] = f"CRITICAL: {error_msg}"
        print(f"🔥 Critical Error: {error_msg}")
        
    finally:
        await browser.close()
        return result # Return the structured data

async def main() -> None:
    # ... (Setup code for 'screenshots' directory remains the same)
    
    async with async_playwright() as playwright:
        # 1. Run all checks concurrently
        tasks = [check_site_health(playwright, target) for target in TARGET_SITES]
        # Collect the list of result dictionaries
        all_results: List[Dict[str, Any]] = await asyncio.gather(*tasks)

    # 2. CSV Reporting
    if not all_results:
        print("\nNo results to report.")
        return

    # Use the keys from the first result dictionary as the CSV header
    fieldnames = list(all_results[0].keys())

    # 'a' means append, which is crucial for trend analysis over time
    with open(CSV_FILE, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        # Check if the file is new (or empty) and write the header only once
        if csvfile.tell() == 0:
            writer.writeheader()
        
        # Write all gathered rows
        writer.writerows(all_results)
    
    print(f"\n--- Monitoring Complete ---")
    print(f"📊 Results appended successfully to **{CSV_FILE}** for trend analysis.")

if __name__ == "__main__":
    print("--- Starting Website Health Monitor ---")
    asyncio.run(main())