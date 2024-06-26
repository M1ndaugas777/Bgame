# Generated by Django 5.0.4 on 2024-04-30 14:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgame', '0053_alter_wiseelder_variable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='totem',
            name='defense_prayer_price',
            field=models.IntegerField(default=100, verbose_name='Pray defense'),
        ),
        migrations.AlterField(
            model_name='totem',
            name='health_prayer_price',
            field=models.IntegerField(default=100, verbose_name='Pray health'),
        ),
        migrations.AlterField(
            model_name='totem',
            name='strength_prayer_price',
            field=models.IntegerField(default=100, verbose_name='Pray strength'),
        ),
    ]
