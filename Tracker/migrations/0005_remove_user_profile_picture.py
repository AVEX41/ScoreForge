# Generated by Django 4.2.7 on 2023-11-24 07:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0004_alter_user_profile_picture'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='profile_picture',
        ),
    ]
