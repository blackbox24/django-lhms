from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import pyotp

def generate_otp():
    secret_code = pyotp.random_base32()
    totp = pyotp.TOTP(secret_code,interval=86400)
    return totp, secret_code

def verify_otp(secret_code,otp):
    totp = pyotp.TOTP(secret_code,interval=86400)
    return totp.verify(otp)

def send_email_verification(username,email,otp_code):
    subject = 'Email Verification'
    from_email = settings.EMAIL_HOST
    to_email = email

    context = {"username":username,"email":email,"otp_code":otp_code}
    html_content = render_to_string("email_verification.html",context)


    mail = EmailMessage(
        subject,
        html_content,
        from_email,
        [to_email],
        
    )
    mail.content_subtype = 'html'
    mail.send()

    return True

def send_password_reset(username,email,otp_code):
    subject = 'Password Reset'
    from_email = settings.EMAIL_HOST
    to_email = email

    context = {"username":username,"email":email,"otp_code":otp_code}
    html_content = render_to_string("password_reset.html",context)


    mail = EmailMessage(
        subject,
        html_content,
        from_email,
        [to_email],
        
    )
    mail.content_subtype = 'html'
    mail.send()

    return True

def send_thankyou_email(username,email):
    subject = 'Account is active'
    from_email = settings.EMAIL_HOST
    to_email = email

    context = {"username":username,"email":email}
    html_content = render_to_string("thankyou.html",context)


    mail = EmailMessage(
        subject,
        html_content,
        from_email,
        [to_email],
        
    )
    mail.content_subtype = 'html'
    mail.send()

    return True