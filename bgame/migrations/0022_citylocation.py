# Generated by Django 5.0.4 on 2024-04-17 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgame', '0021_rename_location_enemy_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='CityLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Location')),
            ],
        ),
    ]
