# Generated by Django 4.0.3 on 2022-04-27 11:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('establishments', '0016_alter_company_website_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='city',
            field=models.CharField(default='London', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='company',
            name='website_url',
            field=models.URLField(null=True),
        ),
    ]
