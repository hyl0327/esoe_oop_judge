# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-27 00:36
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0004_auto_20160225_2110'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='running_time',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='score',
            field=models.IntegerField(blank=True, db_index=True, null=True),
        ),
    ]
