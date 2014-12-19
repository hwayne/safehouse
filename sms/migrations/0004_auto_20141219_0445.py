# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0003_storedcommand'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='StoredCommand',
            new_name='DelayedCommand',
        ),
    ]
