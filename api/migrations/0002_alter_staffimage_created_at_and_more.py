# Generated by Django 4.1.6 on 2025-05-09 05:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffimage',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now, null=True, verbose_name='Created At|Создано'),
        ),
        migrations.AlterField(
            model_name='studentimage',
            name='created_at',
            field=models.DateTimeField(default=datetime.datetime.now, null=True, verbose_name='Created At|Создано'),
        ),
    ]
