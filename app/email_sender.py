import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(sender, password, receiver, subject, body):
    try:
        # Create message object
        msg = MIMEMultipart()
        msg["From"] = sender
        msg["To"] = receiver
        msg["Subject"] = subject

        # Attach body
        msg.attach(MIMEText(body, "plain"))

        # Connect to SMTP server (Gmail)
        server = smtplib.SMTP("smtp.gmail.com", 587)

        # Start secure connection
        server.starttls()

        
        server.login(sender, password)

        # Send email
        server.send_message(msg)

        
        server.quit()

        print(f" Email sent to {receiver}")
        return True

    except Exception as e:
        print(f" Failed to send email to {receiver}: {e}")
        return False