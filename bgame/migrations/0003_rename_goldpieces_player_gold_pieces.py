# Generated by Django 5.0.4 on 2024-04-12 10:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bgame', '0002_player_username'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='goldpieces',
            new_name='gold_pieces',
        ),
    ]