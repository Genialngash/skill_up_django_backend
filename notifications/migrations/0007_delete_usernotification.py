# Generated by Django 4.0.3 on 2022-06-01 17:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0006_remove_usernotification_sent_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserNotification',
        ),
    ]
