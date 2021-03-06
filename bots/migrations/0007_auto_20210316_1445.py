# Generated by Django 3.1.4 on 2021-03-16 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0006_auto_20210316_1421'),
    ]

    operations = [
        migrations.CreateModel(
            name='CommandType',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('description', models.CharField(max_length=128)),
            ],
            options={
                'db_table': 'command_types',
            },
        ),
        migrations.RemoveField(
            model_name='command',
            name='reply_data_url',
        ),
        migrations.AddField(
            model_name='command',
            name='reply_img_url',
            field=models.TextField(blank=True, default='', help_text='Url to image'),
        ),
        migrations.AlterField(
            model_name='command',
            name='reply_text',
            field=models.TextField(blank=True, default='', help_text='Text to be sent when command is triggered'),
        ),
    ]
