# Generated by Django 5.0.2 on 2024-02-15 10:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_alter_game_image'),
    ]

    operations = [
        migrations.RenameField(
            model_name='game',
            old_name='desciption',
            new_name='description',
        ),
    ]
