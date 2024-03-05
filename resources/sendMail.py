import smtplib
import ssl
from email.message import EmailMessage

email_sender = "fahim.prime@gmail.com"
email_password = "mjai hixe ejho woju"
subject = "Registration Confirmation"
body = """
Congratulations! You have been successfully registered.
"""
def send_mail(receiver):
    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, receiver, em.as_string())
