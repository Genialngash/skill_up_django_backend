# Generated by Django 4.0.3 on 2022-06-04 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0010_rename_last_sent_on_emailnotificationlog_sent_on'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailnotificationlog',
            name='sent_on',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
