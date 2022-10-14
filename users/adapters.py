from allauth.account.adapter import DefaultAccountAdapter
from django.conf import settings

from .tasks import (
    send_user_email_activation_after_signup,
    send_user_password_reset_email,
)


class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        """
        Saves a new `User` instance using information provided in the
        signup form.
        """
        from allauth.account.utils import user_email, user_field, user_username

        data = form.cleaned_data
        first_name = data.get("first_name")
        last_name = data.get("last_name")
        email = data.get("email")
        username = data.get("username")
        u_type = data.get("u_type")

        user_email(user, email)
        user_username(user, username)

        if first_name:
            user_field(user, "first_name", first_name)
        if u_type:
            user_field(user, "u_type", u_type)
        if last_name:
            user_field(user, "last_name", last_name)
        if "password1" in data:
            user.set_password(data["password1"])
        else:
            user.set_unusable_password()
        self.populate_username(request, user)
        if commit:
            # ability not to commit makes it easier to derive from this adapter by adding
            user.save()
        return user


    def send_mail(self, template_prefix, email, context):
        # account_confirl_email => link that will be in the confirmation email that will point 
        # to the frontend page for confirming the email

        account_confirm_email = 'signup/verify/'
        account_password_reset_email = 'account/password-reset/'

        if ('password_reset_url' in context):
            # if someone is trying to reset their password, we send a password reset email
            default_url = context['password_reset_url']
            splits = default_url.split('/')
            reset_uid = splits[-3]
            reset_token = splits[-2]

            context['password_reset_url'] = (
                account_password_reset_email + reset_uid + '/' + reset_token
            )

            to_email = email
            cleaned_data = {
                'protocol': settings.PROTOCOL,
                'domain': settings.FRONTEND_DOMAIN_URL,
                'url': context['password_reset_url'],
                'site_name': 'Veeta',
                'user': {
                    'first_name': context['user'].first_name,
                    'last_name': context['user'].last_name,
                }
            }

            current_site = context['current_site'].domain

            # send emails via celery
            send_user_password_reset_email.delay(to_email, cleaned_data)

        if ('activate_url' in context):
            # if someone just signed up, we send the activation email
            context['activate_url'] = (
                account_confirm_email + context['key']
            )
            to_email = email
            cleaned_data = {
                'protocol': settings.PROTOCOL,
                'domain': settings.FRONTEND_DOMAIN_URL,
                'url': context['activate_url'],
                'site_name': 'Veeta',
                'user': {
                    'first_name': context['user'].first_name,
                    'last_name': context['user'].last_name,
                }
            }

            # send emails via celery
            send_user_email_activation_after_signup.delay(to_email, cleaned_data)


# clean_data = {'protocol': 'https','domain': settings.FRONTEND_DOMAIN_URL,'url': 'asdasdasd','site_name': 'Veeta','user': {'first_name':'Mike','last_name':'Foo',},}
# tasks.send_user_email_activation_after_signup.delay('mazindev.tech@gmail.com', clean_data)
