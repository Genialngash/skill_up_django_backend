# Generated by Django 4.0.3 on 2022-04-09 06:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('establishments', '0009_remove_employee_vacancy_applied'),
    ]

    operations = [
        migrations.RenameField(
            model_name='employee',
            old_name='created_on',
            new_name='joined_on',
        ),
    ]
