# Generated by Django 5.0.4 on 2024-04-16 12:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bgame', '0012_rename_current_healh_player_health_threshold'),
    ]

    operations = [
        migrations.RenameField(
            model_name='player',
            old_name='health_threshold',
            new_name='maximum_health',
        ),
    ]