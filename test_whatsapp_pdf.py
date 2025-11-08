"""
Twilio WhatsApp PDF Attachment Example

This script shows how to send a PDF via WhatsApp using Twilio.

IMPORTANT: Twilio requires media files to be hosted at a publicly accessible HTTPS URL.
           You CANNOT send files directly from your local filesystem.

Solutions for PDF attachment:
1. Upload to Twilio Assets (recommended for small files)
2. Use AWS S3 with public URL
3. Use any web hosting service that provides HTTPS URLs
4. Use a temporary file hosting service (for testing)

Prerequisites:
1. Twilio Account SID and Auth Token
2. WhatsApp Sandbox activated (or WhatsApp Business API number)
3. PDF file uploaded to a publicly accessible URL

Usage:
    export TWILIO_ACCOUNT_SID='your_account_sid'
    export TWILIO_AUTH_TOKEN='your_auth_token'
    export TWILIO_WHATSAPP_FROM='whatsapp:+14155238886'
    export RECIPIENT_PHONE='whatsapp:+919008333222'
    export PDF_URL='https://your-server.com/report.pdf'
    python test_whatsapp_pdf.py
"""

import os
from twilio.rest import Client

# Credentials - NO hardcoded defaults
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
twilio_whatsapp_from = os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
recipient_phone = os.getenv('RECIPIENT_PHONE', 'whatsapp:+919008333222')

# Validate credentials
if not account_sid or not auth_token:
    print("❌ ERROR: Missing Twilio credentials!")
    print("\nPlease set environment variables:")
    print("  export TWILIO_ACCOUNT_SID='your_account_sid'")
    print("  export TWILIO_AUTH_TOKEN='your_auth_token'")
    exit(1)

# PDF URL (must be publicly accessible HTTPS)
pdf_url = os.getenv('PDF_URL', '')

# Example PDF URLs you can test with:
# pdf_url = "https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf"
# pdf_url = "https://www.africau.edu/images/default/sample.pdf"

try:
    client = Client(account_sid, auth_token)
    
    print("📋 Configuration:")
    print(f"  From: {twilio_whatsapp_from}")
    print(f"  To: {recipient_phone}")
    
    if not pdf_url:
        print("\n❌ No PDF URL provided!")
        print("\nTo send a PDF, you need to:")
        print("1. Upload your PDF to a web server (HTTPS required)")
        print("2. Set the PDF_URL environment variable:")
        print("   export PDF_URL='https://your-server.com/your-file.pdf'")
        print("\nExample with a test PDF:")
        print("   export PDF_URL='https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf'")
        print("   python test_whatsapp_pdf.py")
        exit(1)
    
    print(f"  PDF: {pdf_url}")
    print("\n📱 Sending WhatsApp message with PDF attachment...")
    
    message = client.messages.create(
        from_=twilio_whatsapp_from,
        body='📄 Hey Alice, your mobile is hacked ;) Let\'s be more funny!.',
        media_url=[pdf_url],  # This is how you attach media - must be a public HTTPS URL
        to=recipient_phone
    )
    
    print(f"\n✅ Message sent successfully!")
    print(f"Message SID: {message.sid}")
    print(f"Status: {message.status}")
    # print(f"Media attached: {len(message.media_url) if hasattr(message, 'media_url') else 'N/A'}")
    
    print("\n💡 Tip: Check your WhatsApp to see the PDF attachment!")

except Exception as e:
    print(f"\n❌ Error: {str(e)}")
    print("\nCommon issues:")
    print("1. PDF URL must be HTTPS (not HTTP)")
    print("2. URL must be publicly accessible (not behind authentication)")
    print("3. File size limits: 5MB for images, 16MB for other media")
    print("4. Supported formats: PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX")
    print("\nFor more info: https://www.twilio.com/docs/whatsapp/api#sending-media")


# ============================================
# Solution 1: Upload PDF to Twilio Assets
# ============================================
"""
Step-by-step to upload to Twilio Assets:

1. Go to Twilio Console: https://console.twilio.com/
2. Navigate to: Runtime > Assets
3. Click "Upload Asset"
4. Select your PDF file
5. Set visibility to "Public"
6. Copy the provided URL
7. Use that URL in the PDF_URL variable

Example:
export PDF_URL='https://your-runtime-xxxxx.twil.io/assets/report.pdf'
"""


# ============================================
# Solution 2: Use a local web server (for testing)
# ============================================
"""
For quick testing, you can use ngrok to expose a local file:

1. Install ngrok: https://ngrok.com/
2. Start a simple Python web server:
   python -m http.server 8000
3. In another terminal, expose it with ngrok:
   ngrok http 8000
4. Place your PDF in the same directory
5. Use the ngrok URL:
   export PDF_URL='https://xxxx-xx-xx-xxx-xxx.ngrok.io/your-file.pdf'

Note: This is only for testing! Use a proper hosting solution for production.
"""


# ============================================
# Solution 3: Integrate with your Streamlit app
# ============================================
"""
To integrate with your KaviHealthcare Streamlit app:

Option A: Upload to Twilio Assets first
1. Generate PDF in Streamlit
2. Save to local file
3. Upload to Twilio Assets (manual or via API)
4. Use the Assets URL with Twilio WhatsApp API

Option B: Use a cloud storage service
1. Generate PDF in Streamlit
2. Upload to AWS S3 / Google Cloud Storage with public access
3. Get the public HTTPS URL
4. Use that URL with Twilio

Option C: Host files temporarily
1. Use a service like file.io or tmpfiles.org
2. Upload the PDF programmatically
3. Get the temporary public URL
4. Send via WhatsApp (URL expires after use)

Example for Option C:
import requests

# Generate your PDF
pdf_bytes = generate_lab_report_pdf(patient_data, tests_df)

# Upload to temporary hosting
response = requests.post(
    'https://file.io',
    files={'file': ('report.pdf', pdf_bytes, 'application/pdf')}
)
pdf_url = response.json()['link']

# Send via WhatsApp
message = client.messages.create(
    from_='whatsapp:+14155238886',
    body='Your lab report is ready!',
    media_url=[pdf_url],
    to=recipient_phone
)
"""
