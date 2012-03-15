import sys
import urllib, urllib, urllib
import re
from xml.dom import minidom
from pprint import pprint


WSOI_WEATHER_URL   = 'http://xmlweather.vedur.is/?op_w=xml&type=obs&view=xml&params=T;TD;D;F;FX;FG;N;V;W;P;RH;R;SNC;SND;SED&ids=%s&time=%s&lang=%s'

def get_weather_from_wsoi(station_id, time, lang):
	url = WSOI_WEATHER_URL % (station_id, time, lang)
	
	handler = urllib.urlopen(url)
	dom = minidom.parse(handler)
	handler.close()

	data_structure = (
			'name',
			'time',
			'err',
			'link',
			'T',
			'TD',
			'D',
			'F',
			'FX',
			'FG',
			'N',
			'V',
			'W',
			'P',
			'RH',
			'R',
			'SNC',
			'SND',
			'SED'
			)
	weather_data = {}
    
	current_observation = dom.getElementsByTagName('station')
    
	for tag in data_structure:
		try:
			if (current_observation[0].getElementsByTagName(tag)[0]).childNodes.length != 0: #check if there is a value in the tag
				weather_data[tag] = (current_observation[0].getElementsByTagName(tag)[0]).childNodes[0].data
			else: # if no value then fill the tag with an empty string
				weather_data[tag] = None
		except IndexError:
			pass

	dom.unlink()
	pprint(url)
	return weather_data
