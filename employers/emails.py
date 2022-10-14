

def send_employer_job_application_notification_email():
    pass


from django.conf import settings
from django.core.mail import EmailMessage, send_mail
from django.template.loader import get_template, render_to_string


def send_employer_job_application_notification_email(context_data):
    """
    Send the employer a notification if people have reacted or 
    shown interest in their job card.
    """

    html = render_to_string('email/employer_job_application_notification.html', context_data)
    text = render_to_string('email/employer_job_application_notification.txt', context_data)

    return send_mail(
        'New applicants for your job card',
        message=text,
        html_message=html,
        recipient_list=[context_data['employer_email']],
        from_email=settings.DEFAULT_FROM_EMAIL,
        fail_silently=settings.FAIL_SILENTLY,
    )
