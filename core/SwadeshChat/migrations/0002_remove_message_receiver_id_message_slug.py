# Generated by Django 5.0.2 on 2024-02-13 06:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SwadeshChat', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='message',
            name='receiver_id',
        ),
        migrations.AddField(
            model_name='message',
            name='slug',
            field=models.SlugField(default=1, max_length=10, unique=True),
            preserve_default=False,
        ),
    ]