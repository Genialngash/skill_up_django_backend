# Generated by Django 4.0.3 on 2022-10-23 17:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('establishments', '0036_checker'),
    ]

    operations = [
        migrations.AlterField(
            model_name='enrolments',
            name='course',
            field=models.ForeignKey(db_constraint=False, on_delete=django.db.models.deletion.CASCADE, to='establishments.coursecard'),
        ),
    ]
