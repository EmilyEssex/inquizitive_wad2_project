# Generated by Django 4.0.3 on 2022-03-12 12:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquizitive', '0002_remove_quiz_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='numOfQue',
            field=models.IntegerField(default=1),
        ),
    ]