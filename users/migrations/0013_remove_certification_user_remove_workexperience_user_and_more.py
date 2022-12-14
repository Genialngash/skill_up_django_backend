# Generated by Django 4.0.3 on 2022-03-24 07:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_rename_total_raters_jobseekerprofile_total_ratings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='certification',
            name='user',
        ),
        migrations.RemoveField(
            model_name='workexperience',
            name='user',
        ),
        migrations.AddField(
            model_name='certification',
            name='jobseeker',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='jobseeker_certifications', to='users.jobseekerprofile'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='workexperience',
            name='jobseeker',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='jobseeker_experience', to='users.jobseekerprofile'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='jobseekerdocument',
            name='jobseeker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobseeker_legal_docs', to='users.jobseekerprofile'),
        ),
        migrations.AlterField(
            model_name='language',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobseeker_spoken_languages', to='users.jobseekerprofile'),
        ),
    ]
