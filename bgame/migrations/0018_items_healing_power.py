# Generated by Django 5.0.4 on 2024-04-16 13:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgame', '0017_remove_items_item_remove_items_player_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='healing_power',
            field=models.IntegerField(blank=True, default=4, null=True, verbose_name='Healing power'),
        ),
    ]