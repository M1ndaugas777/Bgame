# Generated by Django 5.0.4 on 2024-04-15 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgame', '0004_alter_player_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='player',
            name='username',
            field=models.CharField(default='Nothing', max_length=100, verbose_name='Username'),
        ),
    ]