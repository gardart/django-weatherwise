import sys
import urllib, urllib, urllib
import re
from xml.dom import minidom


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
			#weather_data[tag] = (current_observation[0].getElementsByTagName(tag)[0]).childNodes[0].data.encode('utf-8')
			weather_data[tag] = (current_observation[0].getElementsByTagName(tag)[0]).childNodes[0].data
		except IndexError:
			pass

	dom.unlink()
	return weather_data
