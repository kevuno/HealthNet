# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-05 00:20
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('log', '0007_auto_20161204_1915'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='time',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 5, 0, 20, 23, 378926, tzinfo=utc)),
        ),
    ]
