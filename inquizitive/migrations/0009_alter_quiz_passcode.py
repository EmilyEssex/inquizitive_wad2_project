# Generated by Django 4.0.3 on 2022-03-24 08:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquizitive', '0008_alter_quiz_passcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='passcode',
            field=models.CharField(blank=True, max_length=128, null=True),
        ),
    ]
