# Generated by Django 5.0.4 on 2024-04-29 08:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgame', '0049_wiseelder'),
    ]

    operations = [
        migrations.AddField(
            model_name='wiseelder',
            name='player',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wise_elder', to='bgame.player'),
        ),
    ]