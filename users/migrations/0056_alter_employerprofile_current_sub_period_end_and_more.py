# Generated by Django 4.0.3 on 2022-04-11 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0055_rename_sub_end_date_employerprofile_current_sub_period_end_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employerprofile',
            name='current_sub_period_end',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='employerprofile',
            name='current_sub_period_start',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
