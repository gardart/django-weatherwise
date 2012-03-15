# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'StationManager'
        db.create_table('weatherwane_stationmanager', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('weatherwane', ['StationManager'])

        # Adding model 'Station'
        db.create_table('weatherwane_station', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('code', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6, blank=True)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=11, decimal_places=6, blank=True)),
            ('elevation', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('auto_update', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('weatherwane', ['Station'])

        # Adding model 'Observation'
        db.create_table('weatherwane_observation', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('station', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['weatherwane.Station'])),
            ('data', self.gf('django.db.models.fields.TextField')()),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')()),
            ('observation_type', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('observation_cycle', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('observation_time', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('wind_compass', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
            ('wind_speed', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('wind_speed_gust', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('wind_speed_max', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('visibility', self.gf('django.db.models.fields.CharField')(max_length=5, null=True, blank=True)),
            ('temperature', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=1, blank=True)),
            ('dewpoint', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=4, decimal_places=1, blank=True)),
            ('sky_conditions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('cloud_cover', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('weather_conditions', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('sealevel_pressure', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('relative_humidity', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('precipitation', self.gf('django.db.models.fields.DecimalField')(null=True, max_digits=5, decimal_places=2, blank=True)),
            ('snc', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('snd', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('sed', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('weatherwane', ['Observation'])


    def backwards(self, orm):
        
        # Deleting model 'StationManager'
        db.delete_table('weatherwane_stationmanager')

        # Deleting model 'Station'
        db.delete_table('weatherwane_station')

        # Deleting model 'Observation'
        db.delete_table('weatherwane_observation')


    models = {
        'weatherwane.observation': {
            'Meta': {'object_name': 'Observation'},
            'cloud_cover': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'data': ('django.db.models.fields.TextField', [], {}),
            'dewpoint': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '4', 'decimal_places': '1', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observation_cycle': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'observation_time': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
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
            'timestamp': ('django.db.models.fields.DateTimeField', [], {}),
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
