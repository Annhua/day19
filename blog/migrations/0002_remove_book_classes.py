# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-08-29 07:22
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='book',
            name='classes',
        ),
    ]
