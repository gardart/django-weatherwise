# WeatherWise - Django model for weatherstations and observations
WeatherWise is a Django app that periodically receives weather data from stations (XML). It currently targets the Icelandic Weather XML service
(`http://xmlweather.vedur.is/?op_w=xml&type=obs&view=xml&params=T;TD;D;F;FX;FG;N;V;W;P;RH;R;SNC;SND;SED&ids=%s&time=%s&lang=%s`).
If the station model is defined, it automatically pulls data from xmlweather service and updates its observation model. Each observation is recorded into the database.

## Installation (Django 5.x)
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## Notes
- The Icelandic XML weather service data is parsed with `weatherwise/weatherwane/management/commands/pywsoi.py`.
- The chart view in `weatherwane/charts/views.py` expects `django-chartit` (or a compatible fork) to be installed. Install it separately if you need the chart page. 
- The `Observation.updatemetar` helper requires the `python-metar` package; it is not pinned in `requirements.txt` because compatibility with Django 5/Python 3 may vary.
