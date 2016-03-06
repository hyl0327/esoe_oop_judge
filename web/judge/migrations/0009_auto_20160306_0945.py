# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-06 09:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0008_auto_20160229_2333'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='submission',
            name='running_time',
        ),
        migrations.RemoveField(
            model_name='submission',
            name='score',
        ),
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(choices=[('SU', 'Submitting'), ('SE', 'Submission Error'), ('CO', 'Compiling'), ('CE', 'Compilation Error'), ('JU', 'Judging'), ('AC', 'Accepted'), ('NA', 'Not Accepted'), ('TL', 'Time Limit Exceeded'), ('ML', 'Memory Limit Exceeded'), ('RE', 'Runtime Error')], db_index=True, default='SU', max_length=2),
        ),
    ]
