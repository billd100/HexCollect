# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-21 19:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('UserProfile', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='ethnicity',
            field=models.CharField(blank=True, choices=[('', ''), ('Hispanic or Latino', 'Hispanic'), ('Not Hispanic or Latino', 'Not Hispanic or Latino')], default='', max_length=25),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='race',
            field=models.CharField(blank=True, choices=[('', ''), ('Am. Indian, N. Alaskan', 'Native American or Alaskan Native'), ('Asian', 'Asian'), ('Black', 'Black or African American'), ('Pacific Islander', 'Native Hawaiian or other Pacific Islander'), ('White', 'White'), ('Two or more', 'Two or more races'), ('Other', 'Other')], default='', max_length=50),
        ),
    ]
