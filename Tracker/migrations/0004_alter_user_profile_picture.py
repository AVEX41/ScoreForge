# Generated by Django 4.2.7 on 2023-11-23 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0003_user_profile_picture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='profile_picture',
            field=models.BinaryField(blank=True, null=True),
        ),
    ]
