# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Notifier',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('model', models.CharField(max_length=32)),
                ('column', models.CharField(max_length=32, null=True)),
                ('column_val', models.TextField(null=True)),
                ('notify_text', models.TextField()),
                ('notify_interval', models.IntegerField()),
                ('notifies_left', models.IntegerField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NotifierNumber',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('phone_number', models.CharField(max_length=16)),
                ('notifier', models.ForeignKey(to='notifier.Notifier')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
