import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header
import os

def send_email(subject, body, attachment_path=None, attachment_filename=None):
    to_email = os.getenv('RECIPIENT_EMAIL')
    from_email = os.getenv('BOT_EMAIL_ADDRESS')
    password = os.getenv('BOT_EMAIL_PASSWORD')

    msg = MIMEMultipart()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = Header(subject, 'utf-8')

    msg.attach(MIMEText(body, 'plain', 'utf-8'))

    if attachment_path is not None:
        attachment = open(attachment_path, 'rb')
        part = MIMEBase('application', 'octet-stream')
        part.set_payload(attachment.read())
        encoders.encode_base64(part)
        
        filename = attachment_filename if attachment_filename else os.path.basename(attachment_path)
        # Используем RFC 2231 для кодирования имён файлов с Кириллицей
        encoded_filename = Header(filename, 'utf-8').encode()
        part.add_header('Content-Disposition', 'attachment', filename=filename)
        msg.attach(part)

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, password)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully")

    except Exception as e:

        print(f"Failed to send email: {e}")
