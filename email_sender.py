import csv
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import smtplib

def send_email(output_file):

    subject = "Agency timesheets"
    body = "Attached is the CSV with timesheets for last month"
    sender_email = {sender_email}
    recipient_email = {recipient_email}
    sender_password = {sender_password}
    smtp_server = {smtp_server}
    smtp_port = {smtp_port}

    message = MIMEMultipart()
    message['Subject'] = subject
    message['From'] = sender_email
    message['To'] = recipient_email
    body_part = MIMEText(body)
    message.attach(body_part)

    with open(output_file, 'rb') as file:
        message.attach(MIMEApplication(file.read(), Name=output_file))

    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, recipient_email, message.as_string())

    print("Email sent successfully!")

def main():
    output_file = 'Timesheets.csv'  
    send_email(output_file)


if __name__ == "__main__":
    main()
