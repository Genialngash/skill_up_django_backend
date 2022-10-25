# Generated by Django 4.0.3 on 2022-10-23 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0082_user_last_email_notification'),
        ('establishments', '0032_rename_card_jobapplication_job_card_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='CourseCard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('course_name', models.CharField(max_length=32)),
                ('course_description', models.TextField()),
                ('proffesional', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.employerprofile')),
            ],
        ),
        migrations.CreateModel(
            name='LessonsModule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('lesson_name', models.CharField(max_length=32)),
                ('lesson_description', models.TextField()),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='establishments.coursecard')),
            ],
        ),
        migrations.CreateModel(
            name='Completed',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='establishments.employee')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.jobseekerprofile')),
            ],
        ),
    ]