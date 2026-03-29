"""
OrchestrAI - Email Service
Sends email notifications via SMTP (Gmail).
"""
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from core.config import get_settings

settings = get_settings()


async def send_email_notification(to_email: str, subject: str, body: str) -> bool:
    """Send email notification via SMTP."""
    if not settings.SMTP_USER or not settings.SMTP_PASSWORD:
        print(f"📧 [DEMO] Email to {to_email}: {subject} - {body}")
        return True

    try:
        msg = MIMEMultipart("alternative")
        msg["Subject"] = f"[OrchestrAI] {subject}"
        msg["From"] = settings.SMTP_FROM_EMAIL
        msg["To"] = to_email

        html_body = f"""
        <html>
        <body style="font-family: 'Inter', Arial, sans-serif; background: #0a0e27; color: #fff; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: rgba(255,255,255,0.05); border-radius: 16px; padding: 30px; border: 1px solid rgba(255,255,255,0.1);">
                <div style="text-align: center; margin-bottom: 20px;">
                    <h1 style="background: linear-gradient(135deg, #667eea, #764ba2); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 28px;">OrchestrAI</h1>
                </div>
                <h2 style="color: #00d4ff; font-size: 20px;">{subject}</h2>
                <p style="color: rgba(255,255,255,0.8); line-height: 1.6;">{body}</p>
                <hr style="border: 1px solid rgba(255,255,255,0.1); margin: 20px 0;">
                <p style="color: rgba(255,255,255,0.4); font-size: 12px;">This is an automated notification from OrchestrAI - TechNova Solutions</p>
            </div>
        </body>
        </html>
        """

        msg.attach(MIMEText(body, "plain"))
        msg.attach(MIMEText(html_body, "html"))

        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_FROM_EMAIL, to_email, msg.as_string())

        print(f"✅ Email sent to {to_email}: {subject}")
        return True
    except Exception as e:
        print(f"❌ Email error: {e}")
        return False
