# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contact',
            name='created_at',
            field=models.DateTimeField(default=datetime.date(2014, 9, 25), auto_now_add=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='contact',
            name='updated_at',
            field=models.DateTimeField(default=datetime.date(2014, 9, 25), auto_now=True),
            preserve_default=False,
        ),
    ]
