# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-06 13:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('veggie', '0005_auto_20170606_1318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='orderdate',
            name='order',
        ),
        migrations.AddField(
            model_name='order',
            name='order_date',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='veggie.OrderDate'),
            preserve_default=False,
        ),
    ]
