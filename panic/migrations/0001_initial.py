# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Contact'
        db.create_table('panic_contact', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=128)),
            ('phone_number', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('panic', ['Contact'])

        # Adding model 'Incident'
        db.create_table('panic_incident', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('incident_date', self.gf('django.db.models.fields.DateTimeField')()),
            ('contact_size', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('panic', ['Incident'])


    def backwards(self, orm):
        # Deleting model 'Contact'
        db.delete_table('panic_contact')

        # Deleting model 'Incident'
        db.delete_table('panic_incident')


    models = {
        'panic.contact': {
            'Meta': {'object_name': 'Contact'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'phone_number': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'panic.incident': {
            'Meta': {'object_name': 'Incident'},
            'contact_size': ('django.db.models.fields.IntegerField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'incident_date': ('django.db.models.fields.DateTimeField', [], {})
        }
    }

    complete_apps = ['panic']