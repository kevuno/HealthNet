# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-05 03:07
from __future__ import unicode_literals

import datetime
import django.core.validators
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0010_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patient',
            name='date_of_birth',
            field=models.DateField(default=datetime.datetime(2016, 12, 5, 3, 7, 17, 989101, tzinfo=utc), verbose_name='Birthday'),
        ),
        migrations.AlterField(
            model_name='patient',
            name='height',
            field=models.CharField(default='', max_length=6, validators=[django.core.validators.RegexValidator(message='Height needs to be in the form FEET\'INCHES" and needs to be at least 0\'0"', regex='(^[1-8]\'\\s?([0-9]|1[0-1])(\'\'|"))$|(^[0]\'\\s?([1-9]|1[0-1])(\'\'|"))$')]),
        ),
    ]
