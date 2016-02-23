# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-02-22 16:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_sample', models.BooleanField()),
                ('title', models.CharField(max_length=32)),
                ('description', models.TextField()),
                ('input_format', models.TextField()),
                ('output_format', models.TextField()),
                ('sample_input', models.TextField()),
                ('sample_output', models.TextField()),
                ('time_limit', models.IntegerField()),
                ('memory_limit', models.IntegerField()),
                ('deadline_datetime', models.DateTimeField()),
                ('judged_by', models.CharField(choices=[('F', 'File'), ('E', 'Executable')], max_length=1)),
                ('testcase_amount', models.IntegerField()),
            ],
            options={
                'ordering': ['pk'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('bitbucket_account', models.CharField(blank=True, max_length=32)),
                ('bitbucket_repository', models.CharField(blank=True, max_length=32)),
            ],
            options={
                'ordering': ['user__username'],
            },
        ),
        migrations.CreateModel(
            name='RequiredFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('via', models.CharField(choices=[('S', 'Submitted'), ('P', 'Provided')], max_length=1)),
                ('filename', models.CharField(max_length=32)),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='judge.Problem')),
            ],
            options={
                'ordering': ['problem__pk', 'via', 'filename'],
            },
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(blank=True, choices=[('SE', 'Submission Error'), ('JU', 'Judging'), ('AC', 'Accepted'), ('PA', 'Partially Accepted'), ('TL', 'Time Limit Exceeded'), ('ML', 'Memory Limit Exceeded'), ('RE', 'Runtime Error'), ('CE', 'Compile Error')], max_length=2)),
                ('score', models.IntegerField(blank=True, db_index=True, null=True)),
                ('running_time', models.IntegerField(blank=True, null=True)),
                ('submission_datetime', models.DateTimeField()),
                ('problem', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='judge.Problem')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='judge.Profile')),
            ],
            options={
                'ordering': ['-pk'],
            },
        ),
    ]