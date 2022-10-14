from datetime import date

from django.conf import settings
from django_extensions.management.jobs import DailyJob
from profile_unlock.models import UserAccessCredit
from profile_unlock.profile_unlock_utilities import check_code_expiry
from profile_unlock.tasks import send_developer_cron_update


class Job(DailyJob):
    help = "Check for expired unlock codes and mark them as inactive"

    def execute(self):
        total_codes_updated = 0
        error = None
        today = date.today()
        formatted_date = today.strftime("%B %d, %Y")

        try:
            print('Running Cron Job')
            # Check Anonymous Codes
            access_credits = UserAccessCredit.objects.filter(is_valid=True)
            for access_credit in access_credits:
                # Check if the Code has Expired
                credit_is_expired = check_code_expiry(access_credit)

                if credit_is_expired:
                    access_credit.is_valid = False
                    access_credit.save()
                    total_codes_updated += 1
                    print(f"Updated {access_credit.email}'s Expired Access Code")

            print('Finish running Cron Job')
            context_data = {
                'total_codes_updated': total_codes_updated,
                'date': formatted_date,
                'server_name': settings.SERVER_ALIAS
            }
    
            return send_developer_cron_update.delay(context_data)
        except:
            error = True
            context_data = {
                'total_codes_updated': total_codes_updated,
                'date': formatted_date,
                'server_name': settings.SERVER_ALIAS,
                'error': error,
            }
            return send_developer_cron_update.delay(context_data)
