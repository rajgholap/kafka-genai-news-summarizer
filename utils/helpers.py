import json
import smtplib
from email.mime.text import MIMEText


def load_config(config_path):
    with open(config_path) as config_file:
        return json.load(config_file)


def send_email(smtp_config, recipient, subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = smtp_config['username']
    msg['To'] = recipient

    with smtplib.SMTP(smtp_config['server'], smtp_config['port']) as server:
        server.starttls()
        server.login(smtp_config['username'], smtp_config['password'])
        server.sendmail(smtp_config['username'], recipient, msg.as_string())
