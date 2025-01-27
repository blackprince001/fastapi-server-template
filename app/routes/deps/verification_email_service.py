import resend

from app.core.config import settings

resend.api_key = settings.resend_api_key


def send_verification_email(email: str, verification_code: str):
    params: resend.Emails.SendParams = {
        "from": settings.email_sender,
        "to": [email],
        "subject": "Your Verification Code",
        "html": f"<p>Your verification code is: <strong>{verification_code}</strong></p>",
    }

    try:
        resend.Emails.send(params)

    except Exception as e:
        print(f"Failed to send email: {e}")
        raise


def send_single_signon_code(email: str, single_sign_on_code: str):
    params: resend.Emails.SendParams = {
        "from": settings.email_sender,
        "to": [email],
        "subject": "Your Sign In Code",
        "html": f"<p>Your Sigin code is: <strong>{single_sign_on_code}</strong></p>",
    }

    try:
        resend.Emails.send(params)

    except Exception as e:
        print(f"Failed to send email: {e}")
        raise
