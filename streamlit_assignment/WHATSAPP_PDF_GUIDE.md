# How to Send PDF via WhatsApp with Twilio

## Quick Summary

To attach and send a PDF via WhatsApp using Twilio, you need:

1. **A publicly accessible HTTPS URL** for the PDF (Twilio requirement)
2. **Twilio Account** with WhatsApp enabled
3. **Media URL parameter** in your message

## The Problem

Twilio **CANNOT** send files directly from your local filesystem. You must provide a public HTTPS URL.

## The Solution

### Option 1: Temporary File Hosting (Easiest for Testing)

Use the `whatsapp_pdf_sender.py` helper I created:

```python
from whatsapp_pdf_sender import send_whatsapp_with_pdf

# Generate your PDF
pdf_bytes = generate_lab_report_pdf(patient_data, tests_df)

# Send via WhatsApp (it handles the upload automatically)
result = send_whatsapp_with_pdf(
    phone_number='+919711172197',
    pdf_bytes=pdf_bytes,
    message_text='Your lab report is ready!',
    filename='lab_report.pdf'
)

if result['success']:
    print(f"✅ Sent! Message SID: {result['message_sid']}")
else:
    print(f"❌ Error: {result['error']}")
```

**Services used** (automatic fallback):
- litterbox.catbox.moe (24-hour expiry) ✅ Working
- 0x0.st (24-hour expiry)
- file.io (expires after 1 download)

### Option 2: Direct Twilio API (If you have a PDF URL)

```python
from twilio.rest import Client

client = Client(account_sid, auth_token)

message = client.messages.create(
    from_='whatsapp:+14155238886',
    to='whatsapp:+919711172197',
    body='Here is your PDF report',
    media_url=['https://your-server.com/file.pdf']  # Must be HTTPS!
)
```

### Option 3: Upload to Twilio Assets (For Production)

1. Go to [Twilio Console](https://console.twilio.com/)
2. Navigate to **Runtime > Assets**
3. Click "Upload Asset"
4. Upload your PDF
5. Set visibility to **Public**
6. Copy the URL
7. Use it in `media_url`

Example URL: `https://your-runtime-xxxxx.twil.io/assets/report.pdf`

## Integration with Your Streamlit App

Replace the Playwright automation in `kavihealthcare.py`:

```python
# OLD: Complex Playwright automation
# NEW: Simple Twilio + temporary hosting

from whatsapp_pdf_sender import send_whatsapp_with_pdf

# In your WhatsApp send section:
with st.spinner("📱 Sending WhatsApp message with PDF..."):
    result = send_whatsapp_with_pdf(
        phone_number=clean_phone,
        pdf_bytes=pdf_bytes,
        message_text=message_text,
        filename=f"lab_report_patient_{patient_id}.pdf"
    )
    
    if result['success']:
        st.success(f"""
✅ WhatsApp message sent with PDF attachment!

**Details:**
- Message SID: {result['message_sid']}
- PDF uploaded to: {result['pdf_url']}
- Status: {result['status']}

The report has been delivered to the patient!
        """)
    else:
        st.error(f"❌ Error: {result['error']}")
```

## Test Files Created

1. **test.py** - Basic WhatsApp message test
2. **test_whatsapp_pdf.py** - Test with PDF URL
3. **whatsapp_pdf_sender.py** - Complete integration helper

## Run a Test

```bash
cd streamlit_assignment
export TWILIO_ACCOUNT_SID='your_sid'
export TWILIO_AUTH_TOKEN='your_token'
python whatsapp_pdf_sender.py
```

## Requirements

Add to your `requirements.txt`:
```
twilio==9.3.7
requests==2.32.5
```

## Benefits Over Playwright Approach

✅ **Simpler** - No browser automation needed
✅ **More reliable** - No UI changes breaking it  
✅ **Faster** - Direct API call vs browser
✅ **Works headless** - No display needed
✅ **Better errors** - Clear API error messages

## Limitations

⚠️ **Temporary URLs expire** (24 hours for free services)
⚠️ **File size limits**: 16MB max for documents
⚠️ **Must be HTTPS** - HTTP URLs won't work

## Production Recommendations

For production use:
1. Upload PDFs to AWS S3 with public HTTPS URLs
2. Or use Twilio Assets for small files
3. Or host on your own web server with HTTPS

Don't rely on temporary hosting services for critical reports!
