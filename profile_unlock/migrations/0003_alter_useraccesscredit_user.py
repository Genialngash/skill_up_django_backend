# Generated by Django 4.0.3 on 2022-05-29 15:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('profile_unlock', '0002_useraccesscredit_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='useraccesscredit',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]