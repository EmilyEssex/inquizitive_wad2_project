# Generated by Django 2.2.26 on 2022-03-07 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquizitive', '0002_remove_quiz_creator'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='quizName',
            field=models.CharField(default='default value', max_length=128),
        ),
    ]
