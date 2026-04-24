# Internal
import os

# Django
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.template.loader import render_to_string
from django.utils import timezone

# Email
from email.mime.image import MIMEImage


def send_reset_password_email(email, otp, user):
    subject = "Solicitud de cambio de contraseña"
    year_actual = timezone.now().year

    text_content = render_to_string(
        "email/reset_password.txt",
        {"email": email, "otp": otp, "user": user, "year_actual": year_actual},
    )
    html_content = render_to_string(
        "email/reset_password.html",
        {"email": email, "otp": otp, "user": user, "year_actual": year_actual},
    )

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    email.attach_alternative(html_content, "text/html")

    logo_path = os.path.join(settings.BASE_DIR, "api/static/images/logo.png")
    with open(logo_path, "rb") as f:
        logo = MIMEImage(f.read())
        logo.add_header("Content-ID", "<logo>")
        email.attach(logo)

    email.send()
