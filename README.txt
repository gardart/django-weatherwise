# WeatherWise - Django model for weatherstations and observations
WeatherWise is a Django app that periodically recieves weather data from stations (XML).
Currently it only supports Icelandic Weather XML service
('http://xmlweather.vedur.is/?op_w=xml&type=obs&view=xml&params=T;TD;D;F;FX;FG;N;V;W;P;RH;R;SNC;SND;SED&ids=%s&time=%s&lang=%s')
If station model is defined, it automatically pulls data from xmlweather service and updates its observation model.
Each observation is recorded into the database.

# Installation
Start the new Django Weatherwane application with a fresh database  

python manage.py reset weatherwane 
python manage.py syncdb 
python manage.py schemamigration weatherwane --initial 
python manage.py migrate weatherwane 
python manage.py runserver

# Notes
The Icelandic XML weather service data is parsed with weatherwise/weatherwane/management/commands/pywsoi.py
