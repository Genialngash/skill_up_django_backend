# Generated by Django 4.0.3 on 2022-10-23 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('establishments', '0033_coursecard_lessonsmodule_completed'),
        ('users', '0082_user_last_email_notification'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobseekerprofile',
            name='courses',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='establishments.coursecard'),
        ),
    ]
