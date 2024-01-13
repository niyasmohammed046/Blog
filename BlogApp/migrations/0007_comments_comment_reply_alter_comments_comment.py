# Generated by Django 5.0.1 on 2024-01-12 10:11

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BlogApp', '0006_remove_comments_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='comments',
            name='comment_reply',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='replies', to='BlogApp.comments'),
        ),
        migrations.AlterField(
            model_name='comments',
            name='comment',
            field=models.TextField(),
        ),
    ]