# Generated by Django 3.1.4 on 2021-03-16 17:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0010_inlinekeyboard_inlinkeyboardbutton'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='inline_keyboard',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, to='bots.inlinekeyboard'),
            preserve_default=False,
        ),
    ]
