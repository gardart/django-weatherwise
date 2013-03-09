# -*- coding: UTF-8 -*-
# usage : python manage.py get_weather_observations
from pprint import pprint
from datetime import datetime
from django.db import models
from django.core.management.base import NoArgsCommand
from pywsoi import get_weather_from_wsoi
import sys
import time
from socket import socket

CARBON_SERVER = '199.175.48.167'
CARBON_PORT = 2003

delay = 60 

Station = models.get_model("weatherwane", "Station")
Observation = models.get_model("weatherwane", "Observation")

SILENT, NORMAL, VERBOSE = 0, 1, 2

sock = socket()
try:
  sock.connect( (CARBON_SERVER,CARBON_PORT) )
except:
  print "Couldn't connect to %(server)s on port %(port)d, is carbon-agent.py running?" % { 'server':CARBON_SERVER, 'port':CARBON_PORT }
  sys.exit(1)


class Command(NoArgsCommand):
    help = "Aggregates data from weather feed"
    def handle_noargs(self, **options):
        verbosity = int(options.get('verbosity', VERBOSE))
        for observation in Observation.objects.all():
                 station='1'
		 sock = socket()
		 lines.append("%s %t %d" % (observation.station,observation.temperature,observation.observation_time))
		 message = '\n'.join(lines) + '\n' #all lines must end in a newline
		 print "sending message\n"
		 print '-' * 80
		 print message
		 print
		 sock.sendall(message)
  		 time.sleep(delay)

