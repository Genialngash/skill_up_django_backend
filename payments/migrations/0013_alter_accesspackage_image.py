# Generated by Django 4.0.3 on 2022-05-04 18:56

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('payments', '0012_alter_accesspackage_stripe_price_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accesspackage',
            name='image',
            field=imagekit.models.fields.ProcessedImageField(default='default.jpg', upload_to='media/payments/products/photos/%Y/'),
        ),
    ]
