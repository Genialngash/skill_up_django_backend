# Generated by Django 4.0.3 on 2022-10-23 12:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('establishments', '0035_remove_completed_by_enrolments_completed_enrolment'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checker',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('enrolment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='establishments.enrolments')),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='establishments.lessonsmodule')),
            ],
        ),
    ]
