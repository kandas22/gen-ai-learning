"""
Integration Example: Streamlit KaviHealthcare + Twilio WhatsApp + PDF Attachment

This shows how to integrate PDF sending with attachments into your Streamlit app.

Key Challenge: Twilio requires a publicly accessible HTTPS URL for media.
Solution: Use a temporary file hosting service to upload the PDF.
"""

import os
import requests
from io import BytesIO
from twilio.rest import Client

def upload_pdf_to_temp_hosting(pdf_bytes, filename="report.pdf"):
    """
    Upload PDF to a temporary hosting service and get a public URL.
    
    Options:
    1. 0x0.st - Free, expires in 30 days
    2. tmpfiles.org - Free, expires after 1 hour
    3. file.io - Free, 1 download limit
    
    Returns:
        str: Public HTTPS URL of the uploaded PDF
    """
    try:
        # Option 1: 0x0.st (most reliable, expires in 30 days)
        print("  Trying 0x0.st...")
        response = requests.post(
            'https://0x0.st',
            files={'file': (filename, pdf_bytes, 'application/pdf')},
            data={'expires': 24},  # Expire in 24 hours
            timeout=30
        )
        
        if response.status_code == 200 and response.text.startswith('http'):
            url = response.text.strip()
            print(f"  ✅ Uploaded to 0x0.st")
            return url
        
    except Exception as e:
        print(f"  ⚠️  0x0.st failed: {e}")
    
    try:
        # Option 2: file.io (expires after first download)
        print("  Trying file.io...")
        response = requests.post(
            'https://file.io',
            files={'file': (filename, pdf_bytes, 'application/pdf')},
            data={'expires': '1d'},
            timeout=30
        )
        
        if response.status_code == 200:
            try:
                data = response.json()
                if data.get('success'):
                    url = data['link']
                    print(f"  ✅ Uploaded to file.io")
                    return url
            except:
                pass
        
    except Exception as e:
        print(f"  ⚠️  file.io failed: {e}")
    
    try:
        # Option 3: litterbox (expires in 24 hours)
        print("  Trying litterbox...")
        response = requests.post(
            'https://litterbox.catbox.moe/resources/internals/api.php',
            files={'fileToUpload': (filename, pdf_bytes, 'application/pdf')},
            data={'time': '24h', 'reqtype': 'fileupload'},
            timeout=30
        )
        
        if response.status_code == 200 and response.text.startswith('http'):
            url = response.text.strip()
            print(f"  ✅ Uploaded to litterbox")
            return url
            
    except Exception as e:
        print(f"  ⚠️  litterbox failed: {e}")
    
    raise Exception("All upload services failed. Please check your internet connection or try again later.")


def send_whatsapp_with_pdf(
    phone_number,
    pdf_bytes,
    message_text,
    filename="lab_report.pdf",
    account_sid=None,
    auth_token=None,
    from_number='whatsapp:+14155238886'
):
    """
    Send a WhatsApp message with PDF attachment via Twilio.
    
    Args:
        phone_number: Recipient phone with country code (e.g., '+919711172197')
        pdf_bytes: PDF file content as bytes
        message_text: Message to send with the PDF
        filename: Name for the PDF file
        account_sid: Twilio Account SID
        auth_token: Twilio Auth Token
        from_number: Twilio WhatsApp number (default: sandbox)
    
    Returns:
        dict: Result with success status and message SID or error
    """
    try:
        # Format phone number for WhatsApp
        if not phone_number.startswith('whatsapp:'):
            # Remove any spaces or special chars except +
            clean_phone = ''.join(c for c in phone_number if c.isdigit() or c == '+')
            phone_number = f'whatsapp:{clean_phone}'
        
        # Step 1: Upload PDF to get public URL
        print("📤 Uploading PDF to temporary hosting...")
        pdf_url = upload_pdf_to_temp_hosting(pdf_bytes, filename)
        print(f"✅ PDF uploaded: {pdf_url}")
        
        # Step 2: Send via Twilio WhatsApp
        print("📱 Sending WhatsApp message with attachment...")
        
        # Use provided credentials or environment variables
        account_sid = account_sid or os.getenv('TWILIO_ACCOUNT_SID')
        auth_token = auth_token or os.getenv('TWILIO_AUTH_TOKEN')
        
        if not account_sid or not auth_token:
            raise Exception("Twilio credentials not provided")
        
        client = Client(account_sid, auth_token)
        
        message = client.messages.create(
            from_=from_number,
            body=message_text,
            media_url=[pdf_url],
            to=phone_number
        )
        
        return {
            'success': True,
            'message_sid': message.sid,
            'status': message.status,
            'pdf_url': pdf_url
        }
        
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }


# ============================================
# Example usage in Streamlit app
# ============================================
"""
Add this to your kavihealthcare.py where you handle WhatsApp sending:

# After generating PDF
pdf_bytes = generate_lab_report_pdf(patient_data, filtered_tests)

# In the WhatsApp send section, replace the Playwright automation with:
result = send_whatsapp_with_pdf(
    phone_number=clean_phone,
    pdf_bytes=pdf_bytes,
    message_text=message_text,
    filename=f"lab_report_patient_{patient_id}.pdf",
    account_sid=os.getenv('TWILIO_ACCOUNT_SID'),
    auth_token=os.getenv('TWILIO_AUTH_TOKEN')
)

if result['success']:
    st.success(f'''
✅ WhatsApp message sent with PDF attachment!

**Details:**
- Message SID: {result['message_sid']}
- Status: {result['status']}
- PDF URL: {result['pdf_url']}

The report has been delivered to the patient.
    ''')
else:
    st.error(f"❌ Error: {result['error']}")
"""


# Test function
if __name__ == "__main__":
    # Example: Create a simple test PDF
    from reportlab.lib.pagesizes import letter
    from reportlab.pdfgen import canvas
    from io import BytesIO
    
    # Create a simple PDF for testing
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.drawString(100, 750, "Test Lab Report")
    c.drawString(100, 730, "Patient: John Doe")
    c.drawString(100, 710, "This is a test PDF sent via WhatsApp")
    c.save()
    
    pdf_bytes = buffer.getvalue()
    
    # Send via WhatsApp
    result = send_whatsapp_with_pdf(
        phone_number='+919008333222',
        pdf_bytes=pdf_bytes,
        message_text='🏥 Test Lab Report\n\nThis is a test message with PDF attachment.',
        filename='test_report.pdf'
    )
    
    if result['success']:
        print(f"\n✅ Success!")
        print(f"Message SID: {result['message_sid']}")
        print(f"PDF URL: {result['pdf_url']}")
        print(f"\n💡 Check your WhatsApp to see the PDF!")
    else:
        print(f"\n❌ Error: {result['error']}")
