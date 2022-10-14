from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template, render_to_string


def send_developer_cron_update(context_data):
    """Send the developer a report after the cron job runs"""
    html = render_to_string('email/dev_cron_update.html', context_data)
    text = render_to_string('email/dev_cron_update.txt', context_data)

    return send_mail(
        'Update Unlock Codes Cron Job',
        message=text,
        html_message=html,
        recipient_list=[settings.BACKEND_DEV_EMAIL],
        from_email=settings.DEFAULT_FROM_EMAIL,
        fail_silently=settings.FAIL_SILENTLY,
    )
