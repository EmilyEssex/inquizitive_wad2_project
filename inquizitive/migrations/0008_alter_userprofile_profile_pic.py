# Generated by Django 3.2.3 on 2022-03-24 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inquizitive', '0007_remove_quiz_likes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='profile_pic',
            field=models.ImageField(default='default.jpg', upload_to='media/profile_images'),
        ),
    ]
