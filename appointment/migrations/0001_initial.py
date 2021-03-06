# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-04 23:25
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userprofile', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Appointment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=50)),
                ('date', models.DateField(default=datetime.datetime(2016, 12, 4, 23, 25, 37, 832935, tzinfo=utc), verbose_name='Appointment Date')),
                ('time', models.TimeField(default=datetime.datetime(2016, 12, 4, 23, 25, 37, 833018, tzinfo=utc), verbose_name='Starting Appointment Time')),
                ('endTime', models.TimeField(default=datetime.datetime(2016, 12, 5, 0, 25, 37, 833089, tzinfo=utc), verbose_name='Ending Appointment Time')),
                ('description', models.CharField(default='', max_length=100)),
                ('doctor_ID', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='userprofile.Doctor')),
                ('patient_ID', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='userprofile.Patient')),
            ],
        ),
    ]
