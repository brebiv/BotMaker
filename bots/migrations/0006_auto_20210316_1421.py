# Generated by Django 3.1.4 on 2021-03-16 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0005_auto_20210315_1632'),
    ]

    operations = [
        migrations.AddField(
            model_name='command',
            name='reply_data_url',
            field=models.TextField(default='', help_text='Url to fetch data from'),
        ),
        migrations.AlterField(
            model_name='message',
            name='text',
            field=models.TextField(),
        ),
    ]
