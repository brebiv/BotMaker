# Generated by Django 3.1.4 on 2021-03-16 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0011_command_inline_keyboard'),
    ]

    operations = [
        migrations.AlterField(
            model_name='command',
            name='inline_keyboard',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='bots.inlinekeyboard'),
        ),
    ]
