# Generated by Django 4.0.3 on 2022-03-24 08:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0013_remove_certification_user_remove_workexperience_user_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Language',
            new_name='JobseekerLanguage',
        ),
    ]