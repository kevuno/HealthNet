# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-04 23:51
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('medrecord', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalrecord',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2016, 12, 4, 23, 51, 15, 690680, tzinfo=utc), editable=False),
        ),
    ]
