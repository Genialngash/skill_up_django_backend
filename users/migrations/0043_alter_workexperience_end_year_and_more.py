# Generated by Django 4.0.3 on 2022-04-01 22:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0042_rename_jobseeker_workexperience_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workexperience',
            name='end_year',
            field=models.PositiveIntegerField(verbose_name='End year'),
        ),
        migrations.AlterField(
            model_name='workexperience',
            name='start_year',
            field=models.PositiveIntegerField(verbose_name='Start year'),
        ),
    ]