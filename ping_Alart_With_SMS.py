import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from ping3 import ping
import time
import requests

# Configuration
EMAIL_ADDRESS = 'Enter you mail'
EMAIL_PASSWORD = 'Mail_Password'
RECIPIENT_EMAIL = 'mail to'
SMTP_SERVER = 'mail server'
SMTP_PORT = 587
SUBJECT = 'Ping Alert'
PING_INTERVAL = 3600  # Interval between pings in seconds

# SMS Gateway Configuration
SMS_API_URL = "https://bulkSMS_API/api.php"
SMS_TOKEN = "API TOken"  # Replace with your actual token
SMS_RECIPIENTS = "+880XXXXXXXX"  # Replace with actual phone numbers

# List of IPs and corresponding hostnames to check
IP_ADDRESSES = [
    ('192.168.100.2','Core Switch Server Room'),
    ('192.168.100.3','Esxi Server 1'),
]

def send_email(subject, body):
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECIPIENT_EMAIL
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECIPIENT_EMAIL, msg.as_string())

def send_sms(message):
    data = {
        'token': SMS_TOKEN,
        'to': SMS_RECIPIENTS,
        'message': message
    }
    response = requests.post(url=SMS_API_URL, data=data)
    print(f'SMS response: {response.text}')

def check_ping(ip):
    response = ping(ip)
    return response is not None

def main():
    while True:
        for ip, hostname in IP_ADDRESSES:
            if not check_ping(ip):
                body = f'Ping to {hostname} ({ip}) failed. Please check on this host.'
                # Send email notification
                send_email(SUBJECT, body)
                print(f'Email alert sent for {hostname} ({ip})')
                # Send SMS notification
                send_sms(body)
                print(f'SMS alert sent for {hostname} ({ip})')
        time.sleep(PING_INTERVAL)

if __name__ == "__main__":
    main()
