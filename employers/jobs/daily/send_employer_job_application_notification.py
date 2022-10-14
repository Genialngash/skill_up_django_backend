from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from django_extensions.management.jobs import DailyJob
from employers.tasks import send_employer_email_notification
from notifications.models import EmailNotificationSubscription, Notification

User = get_user_model()


class Job(DailyJob):
    help = "Send employers email notifications if they have subscribed to email notifications."

    def execute(self):
        try:
            users = User.objects.all()

            for user in users:
                sub_status = EmailNotificationSubscription.objects.get(user=user)
   
                if sub_status.new_job_application:
                    if user.last_email_notification:
                        last_sent_on = user.last_email_notification
                        todays_date = timezone.now()
                        days_since = ((last_sent_on - todays_date).days + 1)

                        print('Days since is ' + str(days_since))

                        if days_since >= 0 and user.unread_notifications >= 3:
                            # Send the user the email
                            print(f'Sending email NTF to {user.email}')
                            print('DONE ONE')

                            job_application_notifications = Notification.objects.filter(
                                user=user,
                                mark_as_read=False,
                                tag='new_job_application',
                            )

                            last_applicant = job_application_notifications[0].jobcard_notification_metadata.jobseeker
                            last_applicant_name = f'{last_applicant.first_name} {last_applicant.last_name}'

                            context_data = {
                                'last_applicant_name': last_applicant_name,
                                'employer_first_name': user.first_name,
                                'employer_email': user.email,
                                'site_name': "Veeta UK",
                                'employer_dashboard_url': 'https://veeta.co.uk/employer/dashboard/'
                            }

                            send_employer_email_notification.delay(context_data)

                            user.last_email_notification = timezone.now()
                            user.save()

                    if not user.last_email_notification and user.unread_notifications >= 3:
                        # Send the user the email
                        print(f'Sending email NTF to {user.email}')
                        print('DONE TWO')

                        job_application_notifications = Notification.objects.filter(
                            user=user,
                            mark_as_read=False,
                            tag='new_job_application',
                        )


                        last_applicant = job_application_notifications[0].jobcard_notification_metadata.jobseeker
                        last_applicant_name = f'{last_applicant.first_name} {last_applicant.last_name}'

                        context_data = {
                            'last_applicant_name': last_applicant_name,
                            'employer_first_name': user.first_name,
                            'employer_email': user.email,
                            'site_name': "Veeta UK",
                            'employer_dashboard_url': 'https://veeta.co.uk/employer/dashboard/'
                        }
                
                        send_employer_email_notification.delay(context_data)

                        user.last_email_notification = timezone.now()
                        user.save()
        except:
            pass
