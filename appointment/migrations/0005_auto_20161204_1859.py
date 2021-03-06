# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-04 23:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('appointment', '0004_auto_20161204_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='date',
            field=models.DateField(default=datetime.datetime(2016, 12, 4, 23, 59, 9, 994522, tzinfo=utc), verbose_name='Appointment Date'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='endTime',
            field=models.TimeField(default=datetime.datetime(2016, 12, 5, 0, 59, 9, 994588, tzinfo=utc), verbose_name='Ending Appointment Time'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='time',
            field=models.TimeField(default=datetime.datetime(2016, 12, 4, 23, 59, 9, 994554, tzinfo=utc), verbose_name='Starting Appointment Time'),
        ),
    ]
