# -*- coding: UTF-8 -*-
import os
import sys
import datetime
import urllib2
import urllib
import ephem # available from http://rhodesmill.org/pyephem
from xml.dom import minidom
from dateutil import tz
#from metar.Metar import Metar # available from http://python-metar.sourceforge.net
from django.db import models
from django_extensions.db import fields as ext_fields
from math import radians as rad,degrees as deg
from decimal import *

class StationManager(models.Model):
	def auto_update(self):
		sys.path[0] = os.path.normpath(os.path.join(sys.path[0], '..'))
		return self.filter(auto_update__exact=True)

class Station(models.Model):
	name = models.CharField(max_length=200, null=True, blank=True)
	code = models.CharField(max_length=20)
	source = models.CharField(max_length=200, null=True, blank=True)
#	url = models.URLField(null=True, blank=True) # observation url, METAR, XML...
#	country = CountryField()
	latitude = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
	longitude = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
	elevation = models.IntegerField(null=True, blank=True)
	auto_update = models.BooleanField(default=False)

	objects = StationManager()

	def get_name(self):
		return self.name
	
	def __unicode__(self):
		return u'%s' % self.code

class ObservationManager(models.Manager):
	def twenty_four_newest(self):
		return self.order_by('-timestamp')[:24]
	def all(self, limit=None):
		return self.order_by('-timestamp')

class Observation(models.Model):
	station = models.ForeignKey(Station)
	data = models.TextField() # Raw data generated from observation
	timestamp = models.DateTimeField(auto_now_add=True) # Add timestamp to observation

#**************************************************************
#---* Observation Data
#**************************************************************

	observation_type = models.CharField(max_length=5, null=True, blank=True) # METAR, SPECI, XML
	observation_cycle = models.IntegerField(null=True, blank=True) # a number between 0 and 23

	observation_time = models.DateTimeField(null=True, blank=True)

	wind_compass = models.CharField(max_length=4, null=True, blank=True)
	wind_speed = models.IntegerField(null=True, blank=True)
	wind_speed_gust = models.IntegerField(null=True, blank=True)
	wind_speed_max = models.IntegerField(null=True, blank=True)
	visibility = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
	temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
	dewpoint = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
	sky_conditions = models.TextField(null=True, blank=True)
	cloud_cover = models.IntegerField(null=True, blank=True) # Cloud cover in percentage
	weather_conditions = models.TextField(null=True, blank=True)
	sealevel_pressure = models.IntegerField(null=True, blank=True)
	relative_humidity = models.IntegerField(null=True, blank=True) # (RH = 100-5(temperature_celsius - dewpoint_celsius))
	precipitation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
	snc = models.TextField(null=True, blank=True)
	snd = models.IntegerField(null=True, blank=True)
	sed = models.TextField(null=True, blank=True)

	objects = ObservationManager()

	def get_metar_object(self):
		return Metar(self.data)

	def get_lunar_object(self):
		location = ephem.Observer()
		location.lon = self.station.longitude
		location.lat = self.station.latitude
		location.elevation = self.station.elevation
		return ephem.Moon(location)

	def save(self, **kwargs):
		super(Observation, self).save(**kwargs)

	def __unicode__(self):
		return u'%s' % self.data

		
	def updatemetar(self):
		metar = self.get_metar_object()
		self.observation_time = metar.time.replace(tzinfo=tz.gettz('UTC')) # provided in UTC, set that so it shows correctly later
		self.observation_cycle = metar.cycle
		self.observation_type = metar.type
		self.observation_mode = metar.mod
		self.temperature = '%s' % metar.temp.value(units='c')
		self.dewpoint = '%s' % metar.dewpt.value(units='c')	   
		self.visibility = '%s' % metar.vis.value(units='KM')
		if metar.wind_dir:
			#self.wind_direction = '%s' % int(metar.wind_dir.value())
			self.wind_compass = metar.wind_dir.compass()
		if metar.wind_speed:
			self.wind_speed = '%s' % int(round(metar.wind_speed.value(units='mps')))
		if metar.wind_gust:
			self.wind_speed_gust = '%s' % int(metar.wind_gust.value(units='mps'))
		self.sealevel_pressure = '%s' % int(metar.press.value(units="mb"))
		self.sky_conditions = '%s' % metar.sky_conditions()
		self.weather_conditions = '%s' % metar.present_weather()
		self.relative_humidity = 100-5*(metar.temp.value(units='c')-metar.dewpt.value(units='c'))
