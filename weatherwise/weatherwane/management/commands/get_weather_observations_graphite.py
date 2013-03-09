# -*- coding: UTF-8 -*-
# usage : python manage.py get_weather_observations
from pprint import pprint
from datetime import datetime
from django.db import models
from django.core.management.base import NoArgsCommand
from pywsoi import get_weather_from_wsoi
import socket
import time
import calendar

CARBON_SERVER = '199.175.48.167'
CARBON_PORT = 2003
DELAY = 15  # secs

Station = models.get_model("weatherwane", "Station")
Observation = models.get_model("weatherwane", "Observation")

SILENT, NORMAL, VERBOSE = 0, 1, 2

def send_msg(message):
    print 'sending message:\n%s' % message
    sock = socket.socket()
    sock.connect((CARBON_SERVER, CARBON_PORT))
    sock.sendall(message)
    sock.close()

class Command(NoArgsCommand):
    help = "Aggregates data from weather feed"
    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', VERBOSE))
        created_count = 0
        for station in Station.objects.all():
		weather = get_weather_from_wsoi(station.code,'3h','en')
                pprint(weather)
		node = station
                timestamp=weather['time']
		timestamp_struct = time.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
		timestamp_epoch = calendar.timegm(timestamp_struct)
		timestamp = timestamp_epoch
		print 'Time Epoch:\n%s' % timestamp
        	lines = [
			'stations.%s.T %s %d' % (node, weather['T'], timestamp),
			'stations.%s.TD %s %d' % (node, weather['TD'], timestamp),
			'stations.%s.RH %s %d' % (node, weather['RH'], timestamp),
			'stations.%s.F %s %d' % (node, weather['F'], timestamp),
			'stations.%s.FG %s %d' % (node, weather['FG'], timestamp),
			'stations.%s.FX %s %d' % (node, weather['FX'], timestamp),
			'stations.%s.V %s %d' % (node, weather['V'], timestamp),
			'stations.%s.N %s %d' % (node, weather['N'], timestamp),
			'stations.%s.P %s %d' % (node, weather['P'], timestamp),
			'stations.%s.R %s %d' % (node, weather['R'], timestamp),
			'stations.%s.SNC %s %d' % (node, weather['SNC'], timestamp),
			'stations.%s.SND %s %d' % (node, weather['SND'], timestamp),
			'stations.%s.SED %s %d' % (node, weather['SED'], timestamp)
        	]
        	message = '\n'.join(lines) + '\n'
	        send_msg(message)
	        time.sleep(DELAY)
#        if verbosity > NORMAL:
#	    print "Test"
#	else:
#	    print "Notest"
