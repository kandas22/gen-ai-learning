"""
Twilio WhatsApp Test Script

Prerequisites:
1. Sign up for Twilio: https://www.twilio.com/try-twilio
2. Get your Account SID and Auth Token from Twilio Console
3. Join the Twilio WhatsApp Sandbox:
   - Go to: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn
   - Send the code shown (e.g., "join <word>-<word>") to the WhatsApp Sandbox number
   - Wait for confirmation message
4. Set environment variables or update credentials below

IMPORTANT: For WhatsApp, you MUST use the Twilio WhatsApp Sandbox number (default: +14155238886)
           NOT your regular Twilio phone number!

Usage:
    export TWILIO_ACCOUNT_SID='your_account_sid'
    export TWILIO_AUTH_TOKEN='your_auth_token'
    export TWILIO_WHATSAPP_FROM='whatsapp:+14155238886'
    export RECIPIENT_PHONE='whatsapp:+919008333222'
    python test.py
"""

import os
from twilio.rest import Client

# Option 1: Use environment variables (recommended for security)
account_sid = os.getenv('TWILIO_ACCOUNT_SID', 'your_account_sid')
auth_token = os.getenv('TWILIO_AUTH_TOKEN', 'your_auth_token')
# IMPORTANT: Use Twilio's WhatsApp Sandbox number, NOT your regular SMS number
twilio_whatsapp_from = os.getenv('TWILIO_WHATSAPP_FROM', 'whatsapp:+14155238886')
recipient_phone = os.getenv('RECIPIENT_PHONE', 'whatsapp:+919711172197')

# Option 2: Hardcode credentials (NOT recommended for production)
# Uncomment and fill in your actual credentials:
# account_sid = "ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
# auth_token = "your_auth_token_here"
# twilio_whatsapp_from = "whatsapp:+14155238886"  # Twilio sandbox number
# recipient_phone = "whatsapp:+919711172197"      # Your WhatsApp number with country code

try:
    # Validate credentials are set
    if account_sid == 'your_account_sid' or auth_token == 'your_auth_token':
        print("❌ ERROR: Please set your Twilio credentials!")
        print("\nOption 1 - Set environment variables:")
        print("  export TWILIO_ACCOUNT_SID='ACxxxxx...'")
        print("  export TWILIO_AUTH_TOKEN='your_token'")
        print("  export TWILIO_WHATSAPP_FROM='whatsapp:+14155238886'")
        print("  export RECIPIENT_PHONE='whatsapp:+919711172197'")
        print("\nOption 2 - Edit test.py and uncomment lines 27-30")
        print("\nGet credentials from: https://console.twilio.com/")
        exit(1)
    
    if 'xxxxxxxxxx' in recipient_phone:
        print("❌ ERROR: Please set a valid recipient phone number!")
        print("Update RECIPIENT_PHONE with your WhatsApp number (with country code)")
        print("Example: whatsapp:+919711172197")
        exit(1)
    
    # Create Twilio client
    client = Client(account_sid, auth_token)
    
    # Optional: Show your Twilio phone numbers
    print("📋 Fetching your Twilio WhatsApp configuration...")
    print(f"Using WhatsApp From: {twilio_whatsapp_from}")
    print(f"Sending to: {recipient_phone}")
    
    # Important note about WhatsApp Sandbox
    if '+14155238886' in twilio_whatsapp_from:
        print("\n⚠️  You're using the WhatsApp Sandbox number.")
        print("   Make sure you've sent 'join <code>' to this number on WhatsApp first!")
        print("   Visit: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn")
    
    try:
        incoming_phone_numbers = client.incoming_phone_numbers.list(limit=5)
        if incoming_phone_numbers:
            print("\n📱 Your Twilio SMS numbers (NOT for WhatsApp):")
            for number in incoming_phone_numbers:
                print(f"  - {number.phone_number}")
    except Exception:
        pass
    
    # Send WhatsApp message with PDF attachment
    print("\n📱 Sending WhatsApp message with PDF...")
    
    # Option 1: Attach a local PDF file
    pdf_path = os.getenv('PDF_PATH', '/Users/kanda/Downloads/lab_report_patient_2_20251107_220929.pdf')  # Set this to your PDF file path
    
    # Option 2: Use a publicly accessible URL for the PDF
    # pdf_url = "https://www.example.com/your-file.pdf"
    
    message_params = {
        'from_': twilio_whatsapp_from,
        'body': 'Hello! 📄 Here is your PDF report attached.',
        'to': recipient_phone
    }
    
    # If you have a local PDF file, you need to upload it to a publicly accessible URL first
    # Twilio requires media URLs to be publicly accessible (https://)
    if pdf_path and os.path.exists(pdf_path):
        print(f"⚠️  Local file found: {pdf_path}")
        print("⚠️  Note: Twilio requires a publicly accessible HTTPS URL for media.")
        print("⚠️  You need to upload this file to a web server or use a service like:")
        print("    - AWS S3 with public URL")
        print("    - Twilio Assets (https://www.twilio.com/docs/runtime/assets)")
        print("    - Any web hosting service")
        print("\nFor now, sending message without attachment...")
    else:
        # Example: If you have a publicly accessible PDF URL
        pdf_url = os.getenv('PDF_URL', '')
        if pdf_url:
            message_params['media_url'] = [pdf_url]
            print(f"📎 Attaching PDF from URL: {pdf_url}")
    
    message = client.messages.create(**message_params)
    
    print(f"✅ Message sent successfully!")
    print(f"Message SID: {message.sid}")
    print(f"Status: {message.status}")
    print(f"From: {message.from_}")
    print(f"To: {message.to}")

except Exception as e:
    print(f"❌ Error sending message: {str(e)}")
    print("\nTroubleshooting:")
    print("1. Are you using the WhatsApp Sandbox number? (whatsapp:+14155238886)")
    print("   Your regular Twilio number (+19123965292) does NOT work for WhatsApp!")
    print("2. Have you joined the WhatsApp Sandbox?")
    print("   - Open WhatsApp and send the join code to +1 415 523 8886")
    print("   - Visit: https://console.twilio.com/us1/develop/sms/try-it-out/whatsapp-learn")
    print("3. Verify the recipient number is registered with WhatsApp")
    print("4. Check your Twilio account balance/trial status")
    print("\nFor more help, visit: https://www.twilio.com/docs/whatsapp")
