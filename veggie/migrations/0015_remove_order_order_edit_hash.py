# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-18 09:54
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('veggie', '0014_item_item_unitsize'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='order_edit_hash',
        ),
    ]