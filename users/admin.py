from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _
from jobseekers.models import JobseekerCertification, JobseekerLanguage, WorkExperience
from rest_framework_simplejwt import token_blacklist

from . import models


class EmployerProfileAdmin(admin.ModelAdmin):
  list_display = ('id', 'user', 'stripe_customer_id')
  list_display_links = ('user',)
  list_per_page = 25

admin.site.register(models.EmployerProfile, EmployerProfileAdmin)

class LanguageInline(admin.TabularInline):
    model = JobseekerLanguage

class CertificationInline(admin.TabularInline):
    model = JobseekerCertification

class WorkExperienceInline(admin.StackedInline):
    model = WorkExperience

@admin.register(models.JobseekerProfile)
class JobseekerProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user',)
    list_display_links = ('user',)
    list_per_page = 25
    # inlines = [
    #     WorkExperienceInline,
    #     CertificationInline
    # ]

@admin.register(models.User)
class UserAdmin(DjangoUserAdmin):
    """Define admin model for custom User model with no email field."""
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (_("Personal info"), {
            "fields": (
                "first_name", 
                "last_name", 
                "u_type", 
                'avatar',
                'birthday',
                'phone_number',
                'contact_is_verified',
                'logged_in_as',
                'gender',
                'publish_jobseeker_profile',
                'unread_notifications',
                'last_email_notification'
            )}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
    )
    list_display_links = ('email',)
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "first_name",
                    "last_name",
                    "password1",
                    "password2",
                    "u_type",
                    "publish_jobseeker_profile"
                ),
            },
        ),
    )
    list_display = (
        "id",
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_superuser",
    )
    search_fields = ("email", "first_name", "last_name",)
    ordering = ("email",)
    list_per_page = 25

class OutstandingTokenAdmin(token_blacklist.admin.OutstandingTokenAdmin):

    def has_delete_permission(self, *args, **kwargs):
        return True # or whatever logic you want

admin.site.unregister(token_blacklist.models.OutstandingToken)
admin.site.register(token_blacklist.models.OutstandingToken, OutstandingTokenAdmin)
