"""
WhatsApp PDF Attachment via Playwright (Local Automation)
==========================================================

This script provides a browser automation approach using Playwright to send a
WhatsApp message and attach a LOCAL PDF file directly through the WhatsApp Web UI.

Use cases:
- Rapid prototyping / internal workflows
- Sending a locally generated PDF (e.g., Streamlit lab report) manually assisted

NOTES & LIMITATIONS:
- This is UI automation and is more brittle than official APIs. DOM changes may break selectors.
- You MUST be logged in to WhatsApp Web (the script waits so you can scan QR).
- Respect WhatsApp Terms of Service. Don't spam users.

Environment Variables (recommended):
  export WHATSAPP_PHONE='+919711172197'     # Destination phone (country code required, '+' optional)
  export MESSAGE_TEXT='Your lab report is ready!'
  export PDF_PATH='/absolute/path/to/report.pdf'
  export USER_DATA_DIR='~/.playwright/whatsapp'   # (Optional) persistent Chromium profile

CLI Usage (macOS / zsh):
  python test_whatsapp_pdf_playwright.py \
    --phone '+919711172197' \
    --pdf ./report.pdf \
    --message 'Here is your report'

First Run Flow:
1. Launches Chromium (non-headless) with persistent user data dir.
2. Opens https://web.whatsapp.com/ and waits for login (QR scan).
3. Navigates to chat using ?phone=<number>.
4. Inserts message text.
5. Attaches the PDF.
6. Attempts to click send (fallback: press Enter).

Install Requirements:
  pip install playwright
  python -m playwright install chromium

Integrating with Streamlit PDF Generation:
After generating PDF bytes in your app, write to a file and call this script
(in a subprocess) pointing PDF_PATH to that file OR adapt the helper function
`send_whatsapp_pdf(phone, pdf_path, message)`.

DISCLAIMER: Use responsibly. For production-grade messaging integrate with
WhatsApp Business API providers instead of UI automation.
"""

from __future__ import annotations

import os
import sys
import time
import argparse
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
except ImportError as _e:  # pragma: no cover - import branch
    print("\n❌ Playwright is not installed.")
    print("Install and set up browsers first:")
    print("  pip install playwright")
    print("  python -m playwright install chromium")
    sys.exit(1)


DEFAULT_MESSAGE = (
    "📄 Your lab report is ready!\n"
    "Please review the attached PDF.\n\n"
    "Regards,\nKaviHealthCare Lab"
)


def normalize_phone(raw: str) -> str:
    """Return digits-only phone with optional leading '+'. Accepts '+91...', '9197...', '0971...'."""
    if not raw:
        raise ValueError("Phone number is empty")
    raw = raw.strip()
    plus = raw.startswith('+')
    digits = ''.join(ch for ch in raw if ch.isdigit())
    if not digits:
        raise ValueError("Phone number must contain digits")
    if not plus:
        # assume international format; keep as digits only (WhatsApp 'send' endpoint tolerates both)
        return digits
    return '+' + digits


def wait_for_login(page, timeout_ms: int = 180_000):
    """Wait until the main chat composer is visible, indicating login complete (QR scanned)."""
    print("🔐 Waiting for WhatsApp Web login (scan QR if prompted)...")
    try:
        page.wait_for_selector("div[role='textbox'][contenteditable='true'], div[contenteditable='true']", timeout=timeout_ms)
    except PlaywrightTimeoutError:
        raise RuntimeError(
            "Timed out waiting for WhatsApp login. Please run script again after ensuring you are logged in."
        )
    print("✅ Login confirmed.")


def open_chat(page, phone_digits: str):
    chat_url = f"https://web.whatsapp.com/send?phone={phone_digits}"
    print(f"🌐 Navigating to chat URL: {chat_url}")
    page.goto(chat_url, wait_until="domcontentloaded")
    # Wait again for message box specific to the chat
    page.wait_for_selector("div[role='textbox'][contenteditable='true'], div[contenteditable='true']", timeout=60_000)
    print("💬 Chat interface ready.")


def type_message(page, message: str):
    print("⌨️ Inserting message text...")
    locator = page.locator("div[role='textbox'][contenteditable='true'], div[contenteditable='true']").first
    try:
        locator.click()
        locator.fill(message)
    except Exception:
        # fallback to keyboard typing
        locator.click()
        page.keyboard.type(message)
    print("✅ Message prepared.")


def attach_pdf(page, pdf_path: Path) -> bool:
    print(f"📎 Attaching PDF: {pdf_path}")
    candidates_clip = [
        "span[data-icon='clip']",
        "div[title='Attach']",
        "button[aria-label='Attach']",
        "div[data-testid='attach'][role='button']",
    ]
    opened_menu = False
    for sel in candidates_clip:
        try:
            page.click(sel, timeout=2000)
            opened_menu = True
            break
        except Exception:
            continue
    if not opened_menu:
        print("⚠️ Could not open attachment menu (paperclip).")
        return False

    # Document attach button candidates
    doc_candidates = [
        "span[data-icon='document']",
        "div[title='Document']",
        "button[aria-label='Document']",
        "div[data-testid='attach-document']",
    ]
    file_chooser = None
    try:
        with page.expect_file_chooser(timeout=8000) as fc_info:
            clicked_doc = False
            for sel in doc_candidates:
                try:
                    page.click(sel, timeout=2000)
                    clicked_doc = True
                    break
                except Exception:
                    continue
            if not clicked_doc:
                print("⚠️ Document option not found in menu.")
                return False
        file_chooser = fc_info.value
        file_chooser.set_files(str(pdf_path))
        print("✅ File selected via file chooser.")
        return True
    except Exception as e:
        print(f"⚠️ File chooser method failed: {e}. Trying direct input[type=file]...")
        try:
            inputs = page.locator("input[type='file']")
            if inputs.count() > 0:
                inputs.first.set_input_files(str(pdf_path))
                print("✅ File attached using direct file input fallback.")
                return True
            print("⚠️ No file inputs found for fallback.")
        except Exception as inner:
            print(f"❌ Fallback attach failed: {inner}")
    return False


def click_send(page) -> bool:
    print("🚀 Attempting to send message + attachment...")
    send_candidates = [
        "span[data-icon='send']",
        "div[aria-label='Send']",
        "button[data-testid='compose-btn-send']",
        "button[aria-label='Send']",
        "div[data-testid='dm-send']",
    ]
    for sel in send_candidates:
        try:
            page.click(sel, timeout=2000)
            print("✅ Send button clicked.")
            return True
        except Exception:
            continue
    # fallback: press Enter
    try:
        page.keyboard.press("Enter")
        print("↩️ Enter key pressed as fallback.")
        return True
    except Exception:
        print("❌ Unable to send message.")
        return False


def send_whatsapp_pdf(phone: str, pdf_path: Path, message: str, user_data_dir: Path) -> None:
    normalized = normalize_phone(phone)
    digits_only = ''.join(ch for ch in normalized if ch.isdigit())
    if not pdf_path.exists():
        raise FileNotFoundError(f"PDF path does not exist: {pdf_path}")

    with sync_playwright() as p:
        print("🧪 Launching Chromium (persistent context)...")
        user_data_dir = user_data_dir.expanduser().resolve()
        user_data_dir.mkdir(parents=True, exist_ok=True)
        try:
            context = p.chromium.launch_persistent_context(
                user_data_dir=str(user_data_dir),
                headless=False,
            )
        except Exception as e:
            raise RuntimeError(
                "Failed to launch Chromium persistent context. Run: python -m playwright install chromium"
            ) from e

        page = context.pages[0] if context.pages else context.new_page()
        page.set_default_timeout(30_000)

        print("🌐 Opening WhatsApp Web homepage...")
        page.goto("https://web.whatsapp.com/", wait_until="load")
        wait_for_login(page)
        open_chat(page, digits_only)
        type_message(page, message)
        attached = attach_pdf(page, pdf_path)
        if not attached:
            print("⚠️ Proceeding without attachment (attachment failed).")
        sent = click_send(page)
        if sent:
            print("\n✅ Message workflow completed.")
        else:
            print("\n❌ Message may NOT have been sent. Please check the UI manually.")
        print("⏳ Keeping browser open for 3s before closing context...")
        time.sleep(3)
        context.close()


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Send a WhatsApp message with PDF via Playwright automation.")
    parser.add_argument("--phone", dest="phone", help="Destination phone with country code (e.g. +919711172197).", default=os.getenv("WHATSAPP_PHONE"))
    parser.add_argument("--pdf", dest="pdf", help="Path to local PDF file.", default=os.getenv("PDF_PATH"))
    parser.add_argument("--message", dest="message", help="Message text.", default=os.getenv("MESSAGE_TEXT", DEFAULT_MESSAGE))
    parser.add_argument("--user-data-dir", dest="user_data_dir", help="Persistent Chromium profile dir.", default=os.getenv("USER_DATA_DIR", "~/.playwright/whatsapp"))
    parser.add_argument("--no-attach", action="store_true", help="Skip attempting to attach the PDF (debug).")
    return parser.parse_args(argv)


def main():  # pragma: no cover - CLI entry
    args = parse_args()

    if not args.phone:
        print("❌ Phone number required. Provide --phone or WHATSAPP_PHONE env var.")
        sys.exit(2)
    if not args.pdf and not args.no_attach:
        print("❌ PDF path required. Provide --pdf or PDF_PATH env var (or use --no-attach).")
        sys.exit(2)

    pdf_path = Path(args.pdf) if args.pdf else Path("/dev/null")
    if not args.no_attach and not pdf_path.exists():
        print(f"❌ PDF file not found at: {pdf_path}")
        sys.exit(3)

    print("""
============================
WhatsApp Automation Summary
============================
Phone:        {phone}
PDF:          {pdf}
Attach PDF?:  {attach}
Message:
-----------
{message}
-----------
    """.format(phone=args.phone, pdf=str(pdf_path), attach=not args.no_attach, message=args.message))

    try:
        if args.no_attach:
            # Create a temp zero-byte file to simplify flow if skipping attach
            pdf_path = Path("/dev/null")
        send_whatsapp_pdf(args.phone, pdf_path, args.message, Path(args.user_data_dir))
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting tips:")
        print(" - Ensure 'python -m playwright install chromium' was executed")
        print(" - Verify internet connectivity and WhatsApp Web availability")
        print(" - Check phone format (+<country><number>)")
        print(" - DOM changes may require updating selectors in this script")
        sys.exit(1)


if __name__ == "__main__":  # pragma: no cover
    main()
