# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-05-20 16:53
from __future__ import unicode_literals

import concurrency.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_auto_20180520_1652'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='version',
            field=concurrency.fields.IntegerVersionField(default=0, help_text='record revision number'),
        ),
        migrations.AddField(
            model_name='price',
            name='version',
            field=concurrency.fields.IntegerVersionField(default=0, help_text='record revision number'),
        ),
    ]
