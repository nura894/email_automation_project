import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender, password, receiver, subject, body):
    try:
        # 1. Create message object
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = subject

        # 2. Attach body
        msg.attach(MIMEText(body, "plain"))

        # 3. Connect to SMTP server (Gmail)
        server = smtplib.SMTP("smtp.gmail.com", 587)

        # 4. Start secure connection
        server.starttls()

        # 5. Login
        server.login(sender, password)

        # 6. Send email
        server.send_message(msg)

        # 7. Close connection
        server.quit()

        print(f" Email sent to {receiver}")
        return True

    except Exception as e:
        print(f" Failed to send email to {receiver}: {e}")
        return False