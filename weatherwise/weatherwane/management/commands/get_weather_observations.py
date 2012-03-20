# -*- coding: UTF-8 -*-
# usage : python manage.py get_weather_observations
from pprint import pprint
from datetime import datetime
from django.db import models
from django.core.management.base import NoArgsCommand
from pywsoi import get_weather_from_wsoi

Station = models.get_model("weatherwane", "Station")
Observation = models.get_model("weatherwane", "Observation")

SILENT, NORMAL, VERBOSE = 0, 1, 2



class Command(NoArgsCommand):
    help = "Aggregates data from weather feed"
    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', VERBOSE))
        created_count = 0
        for station in Station.objects.all():
	    weather = get_weather_from_wsoi(station.code,'3h','en')
	    pprint(weather)
            if verbosity > NORMAL:
                pprint(weather)
            log, created = Observation.objects.get_or_create(
                 station=station,
                 observation_time=weather['time'],
                 defaults={
					'temperature': weather['T'],
					'dewpoint': weather['TD'],
					'relative_humidity': weather['RH'],
					'wind_compass': weather['D'],
					'wind_speed': weather['F'],
					'wind_speed_gust': weather['FG'],
					'wind_speed_max': weather['FX'],
					'visibility': weather['V'],
					'cloud_cover': weather['N'],
					'weather_conditions': weather['W'],
					'sealevel_pressure': weather['P'],
					'precipitation': weather['R'],
					'snc': weather['SNC'],
					'snd': weather['SND'],
					'sed': weather['SED'],
                    }
                 )
            if created:
                created_count += 1
        if verbosity > NORMAL:
            print "New weather observations: %d" % created_count
	    print log
	else:
	    print "No new weather observations"
