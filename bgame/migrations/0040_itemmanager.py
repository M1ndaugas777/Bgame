# Generated by Django 5.0.4 on 2024-04-24 09:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bgame', '0039_items_health_modifier'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemManager',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]