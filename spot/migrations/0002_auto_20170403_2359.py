# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-03 23:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('spot', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='spot',
            old_name='time_end',
            new_name='time_to',
        ),
    ]
