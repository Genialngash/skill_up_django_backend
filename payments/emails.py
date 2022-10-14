from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template, render_to_string


def send_user_their_unlock_code(user_email, context_data):
    """Send user their unlock code after successful payment"""
    to_email = user_email
    html = render_to_string('email/unlock_code.html', context_data)
    text = render_to_string('email/unlock_code.txt', context_data)

    return send_mail(
        'Your Unlock Code!',
        message=text,
        html_message=html,
        recipient_list=[to_email],
        from_email=settings.DEFAULT_FROM_EMAIL,
        fail_silently=settings.FAIL_SILENTLY,
    )
