# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-19 15:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20180519_1437'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='booking',
            name='day',
        ),
    ]
