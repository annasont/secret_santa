# Generated by Django 3.2.2 on 2021-08-26 16:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('draw', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='participant',
            name='user',
        ),
    ]
