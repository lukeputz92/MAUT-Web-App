# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 20:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decisions', '0006_auto_20171102_2038'),
    ]

    operations = [
        migrations.RenameField(
            model_name='userdecisionmodel',
            old_name='user',
            new_name='decision_user',
        ),
    ]
