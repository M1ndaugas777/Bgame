# Generated by Django 5.0.4 on 2024-04-25 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgame', '0045_totem'),
    ]

    operations = [
        migrations.AddField(
            model_name='totem',
            name='prayer_price',
            field=models.IntegerField(default=1000, verbose_name='Pray'),
        ),
    ]
