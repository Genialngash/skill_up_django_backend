# Generated by Django 4.0.3 on 2022-06-05 19:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('establishments', '0030_alter_jobcard_is_published'),
        ('notifications', '0018_rename_jobseeker_jobapplicationnotificationmetadata_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobapplicationnotificationmetadata',
            name='job_card',
        ),
        migrations.RemoveField(
            model_name='jobapplicationnotificationmetadata',
            name='user',
        ),
        migrations.AddField(
            model_name='jobapplicationnotificationmetadata',
            name='job_application',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='establishments.jobapplication'),
            preserve_default=False,
        ),
    ]
