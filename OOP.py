import random
import smtplib
from twilio.rest import Client
from dotenv import load_dotenv
import os
import re
# Regular expression pattern for email validation
email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

class EmailManager:
    def __init__(self, smtp_server, smtp_port, smtp_username, smtp_password):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.smtp_username = smtp_username
        self.smtp_password = smtp_password

    def send_otp(self, email, otp):
        subject = 'Your OTP'
        message = f'''Thank you for using. To enhance the security of your account, we have generated a one-time password (OTP) for you:

Your OTP: {otp}

Please use this OTP to verify your identity. This code is valid for the next 5 minutes, after which it will expire.
'''

        try:
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            msg = f'Subject: {subject}\n\n{message}'
            server.sendmail(self.smtp_username, email, msg)
            server.quit()
            print('OTP sent successfully via email!')
        except Exception as e:
            print(f'Error sending OTP via email: {str(e)}')

class MobileManager:
    def __init__(self, twilio_account_sid, twilio_auth_token):
        self.twilio_account_sid = twilio_account_sid
        self.twilio_auth_token = twilio_auth_token

    def send_otp(self, phone_number, otp):
        if self.twilio_account_sid is None or self.twilio_auth_token is None:
            print("Twilio credentials not found.")
            return

        try:
            client = Client(self.twilio_account_sid, self.twilio_auth_token)
            message = client.messages.create(
                to=phone_number,
                from_='+15418358453',  # Replace with your Twilio phone number
                body=f'''Thank you for using. To enhance the security of your account, we have generated a one-time password (OTP) for you:

Your OTP: {otp}

Please use this OTP to verify your identity. This code is valid for the next 5 minutes, after which it will expire.
'''
            )
            print('OTP sent successfully via Twilio!')
        except Exception as e:
            print(f'Error sending OTP via Twilio: {str(e)}')

class OTPManager:
    def __init__(self):
        load_dotenv('.env')
        self.email_manager = EmailManager(
            smtp_server='smtp.gmail.com',
            smtp_port=587,
            smtp_username='jyjawale2003@gmail.com',
            smtp_password=os.getenv('SMTP_PASSWORD')
        )
        self.mobile_manager = MobileManager(
            twilio_account_sid=os.getenv('TWILIO_ACCOUNT_SID'),
            twilio_auth_token=os.getenv('TWILIO_AUTH_TOKEN')
        )

    def generate_otp(self):
        return str(random.randint(100000, 999999))

    def validate_email(self, email):
        return re.match(email_pattern, email) is not None

    def validate_mobile(self, mobile):
        return len(mobile) == 10 and mobile.isdigit()

    def send_otp_email(self, email, otp):
        if self.validate_email(email):
            self.email_manager.send_otp(email, otp)
        else:
            print('Invalid email address!')

    def send_otp_mobile(self, mobile, otp):
        if self.validate_mobile(mobile):
            self.mobile_manager.send_otp('+91' + mobile, otp)
        else:
            print('Invalid mobile number!')

if __name__ == "__main__":
    otp_manager = OTPManager()

    # User input for email
    email = input('Enter your email address: ')
    otp = otp_manager.generate_otp()
    otp_manager.send_otp_email(email, otp)

    # User input for mobile number (Twilio)
    use_twilio = input('Do you want to send OTP via Twilio? (yes/no): ')
    if use_twilio.lower() == 'yes':
        mobile = input('Enter your mobile number: ')
        otp_manager.send_otp_mobile(mobile, otp)


