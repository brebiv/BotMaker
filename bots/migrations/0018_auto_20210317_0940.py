# Generated by Django 3.1.4 on 2021-03-17 09:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bots', '0017_callbackhandler'),
    ]

    operations = [
        migrations.AlterField(
            model_name='callbackhandler',
            name='reply_text',
            field=models.TextField(blank=True, default=''),
        ),
    ]
