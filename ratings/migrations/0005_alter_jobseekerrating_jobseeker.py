# Generated by Django 4.0.3 on 2022-04-18 06:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ratings', '0004_alter_companyrating_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseekerrating',
            name='jobseeker',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobseeker_rating', to=settings.AUTH_USER_MODEL),
        ),
    ]
