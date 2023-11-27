from apps.account.send_mail import send_confirmation_email
from apps.account.send_sms import send_activation_sms
from .celery import app
@app.task()
def send_confirmation_email_task(email, code):
    send_confirmation_email(email, code)

@app.task()
def send_activation_sms_task(phone_number, actvation_code):
    send_activation_sms(phone_number, actvation_code)