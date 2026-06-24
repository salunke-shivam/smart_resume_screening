import smtplib
from email.message import EmailMessage
import config

def send_email(to_email, to_name, subject, body):
    msg = EmailMessage()
    msg["From"] = config.EMAIL_FROM
    msg["To"] = to_email
    msg["Subject"] = subject
    msg.set_content(f"Hi {to_name},\n\n{body}")

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(config.EMAIL_FROM, config.GMAIL_APP_PASSWORD)
            server.send_message(msg)
        return True, "OK"
    except Exception as e:
        return False, str(e)

def send_interview_invite(candidate_name, candidate_email, company_name="Our Company"):
    subject = f"Interview Invitation - {company_name}"
    body = (
        f"Congratulations! We reviewed your resume and would like to invite you "
        f"for an interview for the role you applied for. Please reply to this email "
        f"with your availability."
    )
    return send_email(candidate_email, candidate_name, subject, body)

def send_rejection(candidate_name, candidate_email, company_name="Our Company"):
    subject = f"Application Update - {company_name}"
    body = (
        f"Thank you for your interest and the time you took to apply. "
        f"Unfortunately, we have decided to move forward with other candidates "
        f"at this time. We wish you the best in your job search."
    )
    return send_email(candidate_email, candidate_name, subject, body)
