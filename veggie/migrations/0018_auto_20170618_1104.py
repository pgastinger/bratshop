# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-18 11:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veggie', '0017_auto_20170618_1004'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='confirm_date',
            field=models.DateTimeField(default=None),
        ),
    ]