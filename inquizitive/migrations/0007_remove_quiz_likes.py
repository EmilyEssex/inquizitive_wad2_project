# Generated by Django 3.2.3 on 2022-03-24 11:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('inquizitive', '0006_merge_20220324_1135'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quiz',
            name='likes',
        ),
    ]
