# Generated by Django 4.0.3 on 2022-05-14 15:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('utils', '0007_rename_userzonemetadata_jobseekerzonemetadata_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='jobcardzonemetadata',
            options={'verbose_name': 'Job Card Zone Metadata', 'verbose_name_plural': 'Job Card Zone Metadata'},
        ),
        migrations.AlterModelOptions(
            name='jobseekerzonemetadata',
            options={'verbose_name': 'Jobseeker Zone Metadata', 'verbose_name_plural': 'Jobseeker Zone Metadata'},
        ),
    ]
