# Generated by Django 4.0.3 on 2022-04-09 22:07

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0005_alter_anonymousunlockspackage_tag'),
    ]

    operations = [
        migrations.AddField(
            model_name='anonymousunlockspackage',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(default='default.jpg', upload_to='payments/products/photos/%Y/'),
        ),
    ]
