# Generated by Django 5.1.6 on 2025-02-20 13:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth_app', '0005_useract'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='useract',
            name='reminder_access_count',
        ),
    ]
