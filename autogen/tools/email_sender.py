"""Email delivery functionality"""
import aiosmtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Dict, Any
from config import Config
try:
    import markdown2
except ImportError:
    markdown2 = None

async def send_email(
    recipient: str,
    subject: str,
    content: str,
    seo_score: str
) -> Dict[str, Any]:
    """
    Send email with SEO content
    
    Args:
        recipient: Recipient email address
        subject: Email subject
        content: Generated content (markdown)
        seo_score: SEO analysis report
    
    Returns:
        Status dictionary
    """
    try:
        # Convert markdown to HTML if available
        if markdown2:
            content_html = markdown2.markdown(content)
        else:
            content_html = content.replace('\n', '<br>')
        
        # Create message
        message = MIMEMultipart("alternative")
        message["From"] = Config.SMTP_USERNAME
        message["To"] = recipient
        message["Subject"] = f"📝 {subject}"
        
        # HTML body
        html_body = f"""
<!DOCTYPE html>
<html>
<head>
    <style>
        body {{ font-family: Arial, sans-serif; line-height: 1.6; }}
        .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                  color: white; padding: 20px; text-align: center; }}
        .content {{ padding: 20px; }}
        .seo-score {{ background: #f5f5f5; padding: 15px; margin: 20px 0; 
                     border-left: 4px solid #667eea; }}
        pre {{ background: #f9f9f9; padding: 10px; overflow-x: auto; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>SEO-Optimized Content Delivery</h1>
    </div>
    <div class="content">
        <h2>📊 SEO Analysis</h2>
        <div class="seo-score">
            <pre>{seo_score}</pre>
        </div>
        
        <h2>📝 Generated Content</h2>
        <div>
            {content_html}
        </div>
    </div>
</body>
</html>
"""
        
        html_part = MIMEText(html_body, "html")
        message.attach(html_part)
        
        # Send email
        await aiosmtplib.send(
            message,
            hostname=Config.SMTP_SERVER,
            port=Config.SMTP_PORT,
            username=Config.SMTP_USERNAME,
            password=Config.SMTP_PASSWORD,
            start_tls=True
        )
        
        return {
            "status": "success",
            "message": f"Email sent successfully to {recipient}"
        }
    
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to send email: {str(e)}"
        }
