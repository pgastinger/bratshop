# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-19 09:43
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('veggie', '0020_auto_20170619_0935'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_image',
            field=models.ImageField(null=True, upload_to=''),
        ),
    ]
