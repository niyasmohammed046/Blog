# Generated by Django 5.0.1 on 2024-01-14 06:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0008_subscribe'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='is_featured',
            field=models.BooleanField(default=False),
        ),
    ]