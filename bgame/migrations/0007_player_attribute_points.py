# Generated by Django 5.0.4 on 2024-04-16 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgame', '0006_alter_player_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='attribute_points',
            field=models.IntegerField(default=3, verbose_name='Attribute_points'),
        ),
    ]