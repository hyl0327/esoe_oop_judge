# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-17 00:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0013_remove_problem_time_limit'),
    ]

    operations = [
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(choices=[('SU', 'Submitting'), ('SE', 'Submission Error'), ('CO', 'Compiling'), ('CE', 'Compilation Error'), ('JU', 'Judging'), ('AC', 'Accepted'), ('NA', 'Not Accepted'), ('RE', 'Runtime Error')], db_index=True, default='SU', max_length=2),
        ),
    ]
