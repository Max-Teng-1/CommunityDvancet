import smtplib
import requests
import pytz
import re
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timedelta
from typing import List, Dict, Union, Any

from src.backend.config import config
from src.backend.core import security
from src.backend.db.models.user import User
from src.backend.common import response


def str_to_datetime(date: str):
    return datetime.strptime(date, '%Y-%m-%d %H')


def datetime_to_str(date: datetime):
    d = date.strftime('%Y-%m-%d %H:%M:%S')
    return d


def send_email(email: str, reset_code: str = None, auto_accept: bool = False):
    sender_address = '123456@gmail.com'
    sender_pass = '666666'
    receiver_address = email
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    if reset_code:
        message['Subject'] = 'Reset Password'
        message.attach(MIMEText(reset_pwd_email_content(reset_code), 'html', 'utf-8'))

    file_image = open(r'src/backend/static/logo.png', 'rb')
    data_image = file_image.read()
    file_image.close()
    image = MIMEImage(data_image)
    image.add_header('Content-ID', '<image_Greater>')
    message.attach(image)

    connection = smtplib.SMTP('smtp.gmail.com', 587)

    connection.starttls()
    connection.login(sender_address, sender_pass)
    text = message.as_string()
    connection.sendmail(sender_address, receiver_address, text)
    connection.quit()


def reset_pwd_email_content(reset_code: str):
    return f'''
            <h1>
                Hello Dear!<br>
                How are you today?
            </h1>
            <hr>
            <h4>
                We've detected someone trying to change your password.<br>
                Please make sure it is your own operation.<br>
                Your reset code is <strong>{reset_code}</strong>.<br>
                Please don't tell this code to others.<br>
                Hope you successfully reset your password.<br>
            </h4>
            <hr>
            <h4>
                Best regards,<br>
                CommunityDvancet Team.
            </h4>
            '''


def calculate_time_delte_hour(start_date: str, end_date: str):
    time_delta = str_to_datetime(end_date) - str_to_datetime(start_date)
    return time_delta.total_seconds() / 3600


def calculate_time_delte_day(start_date: str, end_date: str):
    time_delta = str_to_datetime(end_date) - str_to_datetime(start_date)
    return time_delta.total_seconds() / 86400


def security_key_check(data: Any, user: User):
    if not security.check_security_key(data.security_key):
        if data.password == "":
            return response.resp_403(message="You need to enter your password for following operations")
        if data.password != "" and not User.verify_password(data.password, user.password):
            return response.resp_403(message="Wrong password")
    security_key = security.create_security_key(expires_delta=timedelta(minutes=config.SECURITY_KEY_EXPIRE_MINUTES))
    return security_key


def get_aus_time_str():
    return datetime_to_str(datetime.now(pytz.timezone('Australia/Sydney')))[0:13]

