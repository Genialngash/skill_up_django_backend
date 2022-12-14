# Generated by Django 4.0.3 on 2022-05-07 12:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0065_remove_jobseekerprofile_city'),
        ('utils', '0006_userzonemetadata_zone_seven_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='UserZoneMetadata',
            new_name='JobseekerZoneMetadata',
        ),
        migrations.RemoveField(
            model_name='jobseekerzonemetadata',
            name='user',
        ),
        migrations.AddField(
            model_name='jobseekerzonemetadata',
            name='profile',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='zone_metadata', to='users.jobseekerprofile'),
            preserve_default=False,
        ),
    ]
