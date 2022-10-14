# Generated by Django 4.0.3 on 2022-05-17 17:32

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0076_remove_jobseekerprofile_is_published_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='avatar',
            field=imagekit.models.fields.ProcessedImageField(default='default.jpg', upload_to='users/photos/%Y/%m/'),
        ),
    ]