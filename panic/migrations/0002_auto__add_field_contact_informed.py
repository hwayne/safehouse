# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Contact.informed'
        db.add_column('panic_contact', 'informed',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Contact.informed'
        db.delete_column('panic_contact', 'informed')


    models = {
        'panic.contact': {
            'Meta': {'object_name': 'Contact'},
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'informed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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