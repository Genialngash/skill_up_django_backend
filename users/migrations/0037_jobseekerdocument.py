# Generated by Django 4.0.3 on 2022-04-01 06:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0036_alter_jobseekerprofile_options'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobseekerDocument',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=128)),
                ('file', models.FileField(upload_to='media/documents/%Y/%m/%d/', verbose_name='Document')),
                ('jobseeker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobseeker_documents', to='users.jobseekerprofile')),
            ],
        ),
    ]