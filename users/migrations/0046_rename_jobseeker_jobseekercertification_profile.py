# Generated by Django 4.0.3 on 2022-04-04 21:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0045_rename_jobseeker_jobseekerlanguage_profile'),
    ]

    operations = [
        migrations.RenameField(
            model_name='jobseekercertification',
            old_name='jobseeker',
            new_name='profile',
        ),
    ]