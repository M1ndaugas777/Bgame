# Generated by Django 5.0.4 on 2024-04-25 06:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgame', '0042_alter_player_experience_threshold'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enemy',
            old_name='gold_pieces',
            new_name='minimum_gold_pieces',
        ),
        migrations.AddField(
            model_name='enemy',
            name='maximum_gold_pieces',
            field=models.IntegerField(default=20, verbose_name='Gold_pieces'),
        ),
    ]
