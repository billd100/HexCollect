# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-11 22:20
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DailyCheckIn',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('excellent', 'excellent'), ('good', 'good'), ('neutral', 'neutral'), ('poor', 'poor'), ('abysmal', 'abysmal')], max_length=20)),
                ('status_detail', models.CharField(blank=True, max_length=1000)),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'userprofile.dailycheckin',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday', models.DateField(blank=True, null=True)),
                ('sex', models.CharField(blank=True, choices=[('', ''), ('Female', 'Female'), ('Male', 'Male')], default='', max_length=50)),
                ('gender_identity', models.CharField(blank=True, max_length=50)),
                ('race', models.CharField(blank=True, choices=[('', ''), ('Native American or Alaskan Native', 'Native American or Alaskan Native'), ('Asian', 'Asian'), ('Black', 'Black or African American'), ('Native Hawaiian or other Pacific Islander', 'Native Hawaiian or other Pacific Islander'), ('White', 'White')], default='', max_length=50)),
                ('about', models.TextField(blank=True, max_length=1000, verbose_name='Tell the community about yourself')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'UserProfile',
            },
        ),
    ]
