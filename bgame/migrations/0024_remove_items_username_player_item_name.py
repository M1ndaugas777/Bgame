# Generated by Django 5.0.4 on 2024-04-17 09:42

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgame', '0023_consumablesmarketplace'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='items',
            name='username',
        ),
        migrations.AddField(
            model_name='player',
            name='item_name',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bgame.items'),
        ),
    ]
