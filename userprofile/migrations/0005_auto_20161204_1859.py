# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-04 23:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0004_auto_20161204_1858'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime(2016, 12, 4, 23, 59, 9, 993029, tzinfo=utc), verbose_name='Birthday'),
        ),
    ]
