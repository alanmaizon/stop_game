# Generated by Django 4.2.16 on 2024-12-22 23:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='notification',
            name='is_archived',
            field=models.BooleanField(default=False),
        ),
    ]
