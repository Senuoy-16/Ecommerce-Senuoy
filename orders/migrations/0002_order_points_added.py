# Generated by Django 5.2.1 on 2025-06-12 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='points_added',
            field=models.BooleanField(default=False),
        ),
    ]
