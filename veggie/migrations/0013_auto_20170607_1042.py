# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-07 10:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veggie', '0012_auto_20170607_0744'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='order_confirm_hash',
            field=models.CharField(max_length=64),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_edit_hash',
            field=models.CharField(max_length=64),
        ),
    ]