# Generated by Django 5.0.2 on 2024-02-13 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SwadeshChat', '0002_remove_message_receiver_id_message_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='slug',
            field=models.SlugField(max_length=10),
        ),
    ]
