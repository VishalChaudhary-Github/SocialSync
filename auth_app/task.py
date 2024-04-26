from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from requests import get


@shared_task(name='send_email', ignore_result=True)
def send_email(recipient, otp, username):
    send_mail(subject="Reset Password: OTP for Verification",
              message="",
              from_email="SocialSync @Admin",
              recipient_list=[recipient],
              html_message=render_to_string('email_template.html',
                                            context={"otp": otp, 'username': username}))