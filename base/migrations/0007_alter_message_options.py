# Generated by Django 3.2.20 on 2023-09-14 09:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_room_participants'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-updated', '-created']},
        ),
    ]
