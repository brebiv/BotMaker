# Generated by Django 3.1.4 on 2021-03-16 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0008_command_type_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='command',
            old_name='type_id',
            new_name='type',
        ),
    ]
