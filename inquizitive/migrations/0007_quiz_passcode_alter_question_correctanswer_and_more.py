# Generated by Django 4.0.3 on 2022-03-24 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquizitive', '0006_alter_question_correctanswer_alter_question_optiona_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='quiz',
            name='passcode',
            field=models.CharField(max_length=128, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='correctAnswer',
            field=models.CharField(max_length=500),
        ),
        migrations.AlterField(
            model_name='question',
            name='optiona',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='optionb',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='optionc',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='optiond',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='question',
            name='questionMarks',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='question',
            name='questionText',
            field=models.CharField(max_length=500, unique=True),
        ),
    ]