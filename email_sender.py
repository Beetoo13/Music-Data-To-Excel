import ssl, smtplib
from email.message import EmailMessage


def send_success_email(es, ep, er, music_error_list):
    email_sender = es
    email_password = ep
    email_receiver = er
    subject = "Songs excel created correctly"
    body = f"""
    The information of the songs was obtained successfully.
    Not found songs: {music_error_list}
    """
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())


def send_error_email(es, ep, er, error_message):
    email_sender = es
    email_password = ep
    email_receiver = er
    subject = "There was an error obtaining the songs"
    body = f"""
    There was an error getting the songs information:
    {error_message}
    """
    em = EmailMessage()
    em["From"] = email_sender
    em["To"] = email_receiver
    em["subject"] = subject
    em.set_content(body)

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())