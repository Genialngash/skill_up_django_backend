# Generated by Django 4.0.3 on 2022-03-15 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AnonymousUnlocksPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('unlocks', models.IntegerField(default=False)),
                ('stripe_product_id', models.CharField(max_length=64)),
                ('stripe_price_id', models.CharField(max_length=64)),
                ('expires_in', models.IntegerField()),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ProSubscriptionPackage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField()),
                ('recurring_payment', models.BooleanField(default=True)),
                ('stripe_product_id', models.CharField(max_length=64)),
                ('stripe_price_id', models.CharField(max_length=64)),
            ],
        ),
    ]