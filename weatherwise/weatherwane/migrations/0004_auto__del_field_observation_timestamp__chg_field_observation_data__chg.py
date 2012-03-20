# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Deleting field 'Observation.timestamp'
        db.delete_column('weatherwane_observation', 'timestamp')

        # Changing field 'Observation.data'
        db.alter_column('weatherwane_observation', 'data', self.gf('django.db.models.fields.TextField')(null=True))

        # Changing field 'Observation.observation_time'
        db.alter_column('weatherwane_observation', 'observation_time', self.gf('django.db.models.fields.DateTimeField')(default=''))


    def backwards(self, orm):
        
        # Adding field 'Observation.timestamp'
        db.add_column('weatherwane_observation', 'timestamp', self.gf('django.db.models.fields.DateTimeField')(default=datetime.date(2012, 3, 19)), keep_default=False)

        # Changing field 'Observation.data'
        db.alter_column('weatherwane_observation', 'data', self.gf('django.db.models.fields.TextField')(default=''))

        # Changing field 'Observation.observation_time'
        db.alter_column('weatherwane_observation', 'observation_time', self.gf('django.db.models.fields.DateTimeField')(null=True))


    models = {
        'weatherwane.observation': {
            'Meta': {'object_name': 'Observation'},
            'cloud_cover': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'dewpoint': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observation_cycle': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observation_time': ('django.db.models.fields.DateTimeField', [], {}),
            'observation_type': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'precipitation': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '5', 'decimal_places': '2', 'blank': 'True'}),
            'relative_humidity': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sealevel_pressure': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'sed': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'sky_conditions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'snc': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'snd': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'station': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['weatherwane.Station']"}),
            'temperature': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '1', 'blank': 'True'}),
            'visibility': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'weather_conditions': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'wind_compass': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'}),
            'wind_speed': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wind_speed_gust': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'wind_speed_max': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'})
        },
        'weatherwane.station': {
            'Meta': {'object_name': 'Station'},
            'auto_update': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'elevation': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6', 'blank': 'True'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '11', 'decimal_places': '6', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'})
        },
        'weatherwane.stationmanager': {
            'Meta': {'object_name': 'StationManager'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['weatherwane']
