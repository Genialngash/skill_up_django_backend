# Generated by Django 4.0.3 on 2022-05-22 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobseekers', '0006_rename_user_jobseekerlanguage_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workexperience',
            name='end_year',
            field=models.PositiveIntegerField(null=True, verbose_name='End year'),
        ),
    ]