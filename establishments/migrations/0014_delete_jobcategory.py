# Generated by Django 4.0.3 on 2022-04-11 13:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('establishments', '0013_alter_jobcard_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='JobCategory',
        ),
    ]