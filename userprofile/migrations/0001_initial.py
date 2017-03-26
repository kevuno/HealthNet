# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-04 23:25
from __future__ import unicode_literals

import datetime
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Doctor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Hospital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='Hospital', max_length=50)),
                ('address', models.CharField(default='', max_length=30, validators=[django.core.validators.RegexValidator(message='Address should be formatted as [Number][Street name]', regex='^\\d+\\s[a-zA-z]+\\s[a-zA-z\\s]+')])),
            ],
        ),
        migrations.CreateModel(
            name='Nurse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Patient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_birth', models.DateField(default=datetime.datetime(2016, 12, 4, 23, 25, 37, 831357, tzinfo=utc), verbose_name='Birthday')),
                ('phone_number', models.CharField(default='', max_length=10, validators=[django.core.validators.RegexValidator(message='Phone number can only contain numbers', regex='^[0-9]+$')])),
                ('address', models.CharField(default='', max_length=30, validators=[django.core.validators.RegexValidator(message='Address should be formatted as [Number][Street name]', regex='^\\d+\\s[a-zA-z]+\\s[a-zA-z\\s]+')])),
                ('city', models.CharField(default='', max_length=20, validators=[django.core.validators.RegexValidator(message='City name can only contain letters, apostrophes, and/or dashes', regex="[a-zA-Z'-]")])),
                ('gender', models.CharField(choices=[('M', 'Male'), ('F', 'Female')], default='Male', max_length=1)),
                ('height', models.CharField(default='', max_length=6, validators=[django.core.validators.RegexValidator(message='Height needs to be in the form FEET\'INCHES"', regex='^(\\d{1,8})\'(\\s?)(-?)(\\s?)([0-9]|(1[0-1]))("|\'\')?$'), django.core.validators.RegexValidator(message="Height should be at least 0'1''", regex='^(\\d{1,8})\'(\\s?)(-?)(\\s?)([1-9]|(1[0-1]))("|\'\')?$')])),
                ('weight', models.CharField(default='', max_length=3, validators=[django.core.validators.RegexValidator(message='Weight must be greater than 0 lbs', regex='^[1-9][0-9]*$')], verbose_name='Weight(lb)')),
                ('emergency_contact', models.CharField(default='', max_length=30, validators=[django.core.validators.RegexValidator(message='Emergency contact should only contain letters, apostrophes, dashes, and/or periods', regex="[a-zA-Z'-.]")])),
                ('emergency_number', models.CharField(default='', max_length=10, validators=[django.core.validators.RegexValidator(message='Emergency number can only contain numbers', regex='^[0-9]+$')])),
                ('insurance_provider', models.CharField(default='', max_length=50)),
                ('insurance_number', models.CharField(default='', max_length=20)),
                ('doctor', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='userprofile.Doctor')),
                ('hospital', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='userprofile.Hospital')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='doctor',
            name='hospital',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='userprofile.Hospital'),
        ),
        migrations.AddField(
            model_name='doctor',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
