# Generated by Django 4.2.7 on 2023-12-02 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Tracker', '0011_scoreset_nbr'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scoreset',
            name='nbr',
            field=models.IntegerField(),
        ),
    ]
