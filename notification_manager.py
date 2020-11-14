from twilio.rest import Client
from config import account_sid, auth_token, FROM_NUM, TO_NUM


class NotificationManager:

    def __init__(self):
        self.client = Client(account_sid, auth_token)

    def send_sms(self, message):
        message = self.client.messages.create(
            body=message,
            from_=FROM_NUM,
            to=TO_NUM,
        )
        print(message.sid)
