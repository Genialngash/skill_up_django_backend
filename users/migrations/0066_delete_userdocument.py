# Generated by Django 4.0.3 on 2022-05-13 10:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0065_remove_jobseekerprofile_city'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserDocument',
        ),
    ]