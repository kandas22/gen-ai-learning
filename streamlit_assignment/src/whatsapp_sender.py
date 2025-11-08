"""
WhatsApp PDF Sender using Twilio API
=====================================

This module provides a clean interface to send WhatsApp messages with PDF attachments
using Twilio's WhatsApp Business API.

Since Twilio requires PDFs to be hosted at publicly accessible HTTPS URLs, this module
includes helper functions to temporarily host files using multiple fallback services.

Environment Variables (Method 1):
  TWILIO_ACCOUNT_SID - Your Twilio Account SID
  TWILIO_AUTH_TOKEN - Your Twilio Auth Token
  TWILIO_WHATSAPP_FROM - Your Twilio WhatsApp number (e.g., whatsapp:+14155238886)

Streamlit Secrets (Method 2 - Recommended):
  In .streamlit/secrets.toml:
  [twilio]
  ACCOUNT_SID = "your_sid"
  AUTH_TOKEN = "your_token"
  WHATSAPP_FROM = "whatsapp:+14155238886"

Usage:
    from whatsapp_sender import send_whatsapp_pdf
    
    success, message = send_whatsapp_pdf(
        to_phone="+919711172197",
        pdf_bytes=pdf_data,
        message_text="Your lab report is ready!",
        pdf_filename="lab_report.pdf"
    )
    
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
"""

import os
import requests
from typing import Tuple, Optional

# Try to import streamlit for secrets support
try:
    import streamlit as st
    STREAMLIT_AVAILABLE = True
except ImportError:
    STREAMLIT_AVAILABLE = False


def get_twilio_credentials():
    """Get Twilio credentials from Streamlit secrets or environment variables."""
    # Try Streamlit secrets first
    if STREAMLIT_AVAILABLE:
        try:
            if hasattr(st, 'secrets') and 'twilio' in st.secrets:
                return (
                    st.secrets["twilio"]["ACCOUNT_SID"],
                    st.secrets["twilio"]["AUTH_TOKEN"],
                    st.secrets["twilio"]["WHATSAPP_FROM"]
                )
        except Exception:
            pass  # Fall back to environment variables
    
    # Fall back to environment variables (NO hardcoded defaults for security)
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    whatsapp_from = os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
    
    if not account_sid or not auth_token:
        raise ValueError(
            "Twilio credentials not found! Please set TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN environment variables."
        )
    
    return account_sid, auth_token, whatsapp_from


# Get credentials on module load
TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_WHATSAPP_FROM = get_twilio_credentials()


def upload_pdf_to_temporary_hosting(pdf_bytes: bytes, filename: str = "report.pdf") -> Tuple[bool, str]:
    """
    Upload PDF to a temporary hosting service with multiple fallback options.
    Tries: tmpfiles.org -> 0x0.st -> file.io
    
    Args:
        pdf_bytes: PDF file content as bytes
        filename: Name for the PDF file
    
    Returns:
        Tuple of (success: bool, url_or_error_message: str)
    """
    errors = []
    
    # Option 1: Try tmpfiles.org (more reliable than file.io)
    try:
        response = requests.post(
            'https://tmpfiles.org/api/v1/upload',
            files={'file': (filename, pdf_bytes, 'application/pdf')},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('status') == 'success':
                # tmpfiles returns URL in format: https://tmpfiles.org/12345
                # But the actual download URL is: https://tmpfiles.org/dl/12345
                raw_url = data.get('data', {}).get('url', '')
                if raw_url:
                    # Convert to direct download link
                    pdf_url = raw_url.replace('tmpfiles.org/', 'tmpfiles.org/dl/')
                    return True, pdf_url
        errors.append(f"tmpfiles.org: {response.status_code}")
    except Exception as e:
        errors.append(f"tmpfiles.org: {str(e)}")
    
    # Option 2: Try 0x0.st (simple and reliable)
    try:
        response = requests.post(
            'https://0x0.st',
            files={'file': (filename, pdf_bytes, 'application/pdf')},
            timeout=30
        )
        
        if response.status_code == 200:
            pdf_url = response.text.strip()
            if pdf_url.startswith('https://'):
                return True, pdf_url
        errors.append(f"0x0.st: {response.status_code}")
    except Exception as e:
        errors.append(f"0x0.st: {str(e)}")
    
    # Option 3: Try file.io (fallback, but often rate-limited)
    try:
        response = requests.post(
            'https://file.io',
            files={'file': (filename, pdf_bytes, 'application/pdf')},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                pdf_url = data.get('link')
                if pdf_url:
                    return True, pdf_url
        errors.append(f"file.io: {response.status_code}")
    except Exception as e:
        errors.append(f"file.io: {str(e)}")
    
    # All services failed
    error_summary = "; ".join(errors)
    return False, f"All upload services failed. Errors: {error_summary}"


def send_whatsapp_message_via_twilio(
    to_phone: str,
    message_text: str,
    pdf_url: Optional[str] = None
) -> Tuple[bool, str]:
    """
    Send WhatsApp message via Twilio API.
    
    Args:
        to_phone: Recipient phone number with country code (e.g., +919711172197)
        message_text: Message content
        pdf_url: Optional HTTPS URL to PDF file to attach
    
    Returns:
        Tuple of (success: bool, message_or_error: str)
    """
    try:
        from twilio.rest import Client
    except ImportError:
        return False, "Twilio library not installed. Run: pip install twilio"
    
    try:
        # Ensure phone number has proper format
        clean_phone = to_phone.strip()
        if not clean_phone.startswith('+'):
            clean_phone = '+' + ''.join(filter(str.isdigit, clean_phone))
        
        # Format for Twilio WhatsApp
        whatsapp_to = f"whatsapp:{clean_phone}"
        
        # Initialize Twilio client
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        
        # Prepare message parameters
        message_params = {
            'from_': TWILIO_WHATSAPP_FROM,
            'to': whatsapp_to,
            'body': message_text
        }
        
        # Add PDF attachment if URL provided
        if pdf_url:
            message_params['media_url'] = [pdf_url]
        
        # Send message
        message = client.messages.create(**message_params)
        
        return True, f"Message sent successfully! SID: {message.sid}"
    
    except Exception as e:
        return False, f"Twilio API error: {str(e)}"


def send_whatsapp_pdf(
    to_phone: str,
    pdf_bytes: bytes,
    message_text: str,
    pdf_filename: str = "report.pdf"
) -> Tuple[bool, str]:
    """
    Complete workflow: Upload PDF and send via WhatsApp using Twilio.
    
    This is the main function you should use. It handles:
    1. Uploading PDF to temporary hosting (file.io)
    2. Getting a public HTTPS URL
    3. Sending WhatsApp message with PDF via Twilio
    
    Args:
        to_phone: Recipient phone number with country code (e.g., +919711172197)
        pdf_bytes: PDF file content as bytes
        message_text: Message to send with the PDF
        pdf_filename: Name for the PDF file (default: report.pdf)
    
    Returns:
        Tuple of (success: bool, message: str)
        
    Example:
        success, msg = send_whatsapp_pdf(
            to_phone="+919711172197",
            pdf_bytes=pdf_data,
            message_text="Your lab report is ready!",
            pdf_filename="lab_report_12345.pdf"
        )
    """
    # Step 1: Upload PDF to get public URL
    upload_success, pdf_url_or_error = upload_pdf_to_temporary_hosting(pdf_bytes, pdf_filename)
    
    if not upload_success:
        return False, f"Failed to upload PDF: {pdf_url_or_error}"
    
    pdf_url = pdf_url_or_error
    
    # Step 2: Send WhatsApp message with PDF URL
    send_success, send_message = send_whatsapp_message_via_twilio(
        to_phone=to_phone,
        message_text=message_text,
        pdf_url=pdf_url
    )
    
    if not send_success:
        return False, f"Failed to send WhatsApp: {send_message}"
    
    return True, f"✅ WhatsApp message with PDF sent successfully to {to_phone}"


def send_whatsapp_text_only(to_phone: str, message_text: str) -> Tuple[bool, str]:
    """
    Send a text-only WhatsApp message (no PDF attachment).
    
    Args:
        to_phone: Recipient phone number with country code
        message_text: Message content
    
    Returns:
        Tuple of (success: bool, message: str)
    """
    return send_whatsapp_message_via_twilio(to_phone, message_text, pdf_url=None)


# Test function for development
if __name__ == "__main__":
    import sys
    
    print("🧪 Twilio WhatsApp Sender Test")
    print("=" * 50)
    
    # Check if Twilio credentials are set
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        print("❌ ERROR: Twilio credentials not set!")
        print("\nPlease set environment variables:")
        print("  export TWILIO_ACCOUNT_SID='your_account_sid'")
        print("  export TWILIO_AUTH_TOKEN='your_auth_token'")
        print("  export TWILIO_WHATSAPP_FROM='whatsapp:+14155238886'")
        sys.exit(1)
    else:
        print(f"✅ Using custom TWILIO_ACCOUNT_SID: {TWILIO_ACCOUNT_SID[:10]}...")
    
    print(f"📱 From: {TWILIO_WHATSAPP_FROM}")
    
    # Test with a simple text message
    test_phone = os.getenv("TEST_PHONE", "+919711172197")
    test_message = "🧪 Test message from KaviHealthCare Lab"
    
    print(f"\n📤 Sending test message to: {test_phone}")
    success, message = send_whatsapp_text_only(test_phone, test_message)
    
    if success:
        print(f"✅ {message}")
    else:
        print(f"❌ {message}")
    
    sys.exit(0 if success else 1)
