# Generated by Django 4.0.3 on 2022-05-18 18:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0077_alter_user_avatar'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobseekerlanguage',
            name='profile',
        ),
        migrations.RemoveField(
            model_name='workexperience',
            name='profile',
        ),
        migrations.DeleteModel(
            name='JobseekerCertification',
        ),
        migrations.DeleteModel(
            name='JobseekerLanguage',
        ),
        migrations.DeleteModel(
            name='WorkExperience',
        ),
    ]
