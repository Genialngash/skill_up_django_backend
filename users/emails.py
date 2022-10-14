from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template, render_to_string


def send_user_activation_email(user_email, context_data):
    """Send user an activation email after signup"""
    message = get_template("email/activation.html").render(
        context_data
    )

    to_email = user_email

    email = EmailMessage(
        subject="Activate your account",
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )

    email.content_subtype = "html"
    return email.send(fail_silently=settings.FAIL_SILENTLY)


def send_user_password_reset_email(user_email, context_data):
    """Send user a password reset email"""
    message = get_template("email/password_reset.html").render(
        context_data
    )

    to_email = user_email

    email = EmailMessage(
        subject="Reset your password",
        body=message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[to_email],
    )

    email.content_subtype = "html"
    return email.send(fail_silently=settings.FAIL_SILENTLY)


def send_employer_signup_credits(user_email, context_data):
    """Send user their unlock code after successful email activation"""
    to_email = user_email
    html = render_to_string('email/sign_up_credits.html', context_data)
    text = render_to_string('email/sign_up_credits.txt', context_data)

    return send_mail(
        'Your Unlock Code!',
        message=text,
        html_message=html,
        recipient_list=[to_email],
        from_email=settings.DEFAULT_FROM_EMAIL,
        fail_silently=settings.FAIL_SILENTLY,
    )
