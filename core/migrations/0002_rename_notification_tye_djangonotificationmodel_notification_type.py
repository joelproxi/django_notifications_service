# Generated by Django 5.1.4 on 2024-12-27 11:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='djangonotificationmodel',
            old_name='notification_tye',
            new_name='notification_type',
        ),
    ]
