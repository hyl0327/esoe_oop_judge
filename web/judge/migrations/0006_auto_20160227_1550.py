# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-27 15:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('judge', '0005_auto_20160227_0036'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='problem',
            name='testcase_amount',
        ),
        migrations.AlterField(
            model_name='submission',
            name='score',
            field=models.DecimalField(blank=True, db_index=True, decimal_places=2, max_digits=5, null=True),
        ),
        migrations.AlterField(
            model_name='submission',
            name='status',
            field=models.CharField(choices=[('SU', 'Submitting'), ('SE', 'Submission Error'), ('JU', 'Judging'), ('CE', 'Compile Error'), ('AC', 'Accepted'), ('PA', 'Partially Accepted'), ('TL', 'Time Limit Exceeded'), ('ML', 'Memory Limit Exceeded'), ('RE', 'Runtime Error')], default='SU', max_length=2),
        ),
    ]