import os
import smtplib
from email.message import EmailMessage
from email.utils import formataddr
from pathlib import Path
import ssl

from dotenv import load_dotenv # pip3 install python_dotenv

PORT = 465
EMAIL_SERVER = "smtp.gmail.com"

# load the env variables
current_dir = Path(__file__).resolve().parent if "__file__" in locals() else Path.cwd()
envars = current_dir / ".env"
load_dotenv(envars)

# read env variables
# sender_email = os.getenv("EMAIL")
# password_email = os.getenv("PASSWORD")

sender_email = "swarupdas.mails@gmail.com"
GMAIL_APP_PASSWORD = "wonplzmtcengwihq"

def send_email(subject, receiver_email, name, due_date, invoice_no, amount):
    # create base text message
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = formataddr(("Swarup Code Ltd.", f"{sender_email}"))
    msg["To"] = receiver_email
    msg["BCC"] = sender_email

    msg.set_content(
        f"""\
        Hi {name},
        I hope you are doing well.
        This is a reminder that your {amount} INR in respect of our invoice {invoice_no} is due for
        payment on {due_date}.
        Best Regards,
        Swarup Das.
        """
    )

    msg.add_alternative(
        f"""\
    <html>
        <body>
            <p>Hi {name},</p>
            <p>I hope you are doing well.</p>
            <p>This is a reminder that your <strong>{amount} INR</strong> in respect of our invoice <strong>{invoice_no}</strong> is due for
        payment on <strong>{due_date}</strong>.</p>
            <p>Best Regards,</p>
            <p>Swarup Das.</p>
        </body>
    </html>
        """,
        subtype="html"
    )

    simple_email_context = ssl.create_default_context

    print(f"Connecting to server...")
    with smtplib.SMTP_SSL(EMAIL_SERVER,PORT) as server:
        # server.starttls()
        server.login(sender_email, GMAIL_APP_PASSWORD)
        print(f"Connected to server...")
        server.sendmail(sender_email, receiver_email, msg.as_string())
    

if __name__ == "__main__":
    print(f"Sending email")
    try:
        send_email(
            subject="Invoice Reminder",
            name="Swarup Das",
            receiver_email="julius.swr9@gmail.com",
            due_date="05 May, 2024",
            invoice_no="INV-01-44-33",
            amount="100"
        )
        print(f"Email sent successfully!")
    except Exception as ex:
        print(ex)

