# WeatherWise - Django model for weatherstations and observations using Icelandic Met Office
WeatherWise is a Django app that periodically receives weather data from stations (XML). It currently targets the Icelandic Weather XML service
(`http://xmlweather.vedur.is/?op_w=xml&type=obs&view=xml&params=T;TD;D;F;FX;FG;N;V;W;P;RH;R;SNC;SND;SED&ids=%s&time=%s&lang=%s`).
If the station model is defined, it automatically pulls data from xmlweather service and updates its observation model. Each observation is recorded into the database.

## Quickstart

### 1) Install
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Optional extras:
- Charts page: `pip install django-chartit`
- METAR parsing helper: `pip install python-metar`

### 2) Configure (optional)
- If needed, create `weatherwise/local_settings.py` to override database or secrets. Defaults use SQLite at `weatherwise/weather.db`.

### 3) Migrate database
```bash
python weatherwise/manage.py migrate
```

### 4) Run health check
```bash
python weatherwise/manage.py check
```

### 5) Create admin user
```bash
python weatherwise/manage.py createsuperuser
```

### 6) Run the server
```bash
python weatherwise/manage.py runserver
```
Admin is available at `http://127.0.0.1:8000/admin/`.

### 7) Add a weather station in the admin
1. Visit `http://127.0.0.1:8000/admin/` and log in with your superuser.
2. Open “Stations” and click “Add station”.
3. Fill required fields:
   - Name (e.g., Akureyri)
   - Code from the XML feed (e.g., 3471)
4. Optional fields:
   - Source/provider note
   - Latitude/Longitude in decimal degrees (e.g., 63.962800 / -20.566900)
   - Elevation in meters
5. Save. You can now fetch observations for this station via the management command or cron.

### Fetch observations from the XML service
From the project root:
```bash
python weatherwise/manage.py get_weather_observations --verbosity 2
```
Wrapper script (uses `.venv` if present) at `scripts/fetch_observations.sh`:
```bash
chmod +x scripts/fetch_observations.sh
scripts/fetch_observations.sh
```
Example cron entry to run hourly (adjust cadence as needed):
```
0 * * * * /path/to/django-weatherwise/scripts/fetch_observations.sh >> /var/log/weatherwise.log 2>&1
```

## Docker Compose (app + hourly fetcher)
Quick way to run the app and a sidecar that pulls new observations every hour. Uses SQLite stored on a Docker volume.

```bash
# Build and start
docker compose up --build -d

# Stop
docker compose down
```

Defaults (override in `docker-compose.yml` or with `--env-file`):
- DB path: `/data/weather.db` (persisted in `weatherwise_data` volume)
- App: Gunicorn on `0.0.0.0:8000` (exposed to host)
- Scheduler: runs `get_weather_observations` every 3600s (`FETCH_INTERVAL` to change)
- Env: `DJANGO_SECRET_KEY=change-me`, `DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1`, `DJANGO_DEBUG=False`
- Static files are served by WhiteNoise (no extra reverse proxy needed).
- On scheduler start we seed/update a default station and do an initial fetch. Override via envs (`STATION_CODE`, `STATION_NAME`, `STATION_LAT`, `STATION_LON`, `STATION_ELEVATION`, `STATION_SOURCE`).
- Superuser auto-created on web start: set `ADMIN_USERNAME`, `ADMIN_EMAIL`; leave `ADMIN_PASSWORD` empty to auto-generate (password is printed in web container logs on first create).
- Use an external host path for the DB volume by replacing the volume lines in `docker-compose.yml` with `- /opt/weatherwise:/data` for both `web` and `scheduler`, and remove the `weatherwise_data` volume declaration.

If you want to inspect the database on the host:
```bash
docker compose exec web python weatherwise/manage.py dbshell
```

### Podman Compose (rootless-friendly)
Same stack using Podman:
```bash
podman compose -f podman-compose.yml up --build -d
# Stop
podman compose -f podman-compose.yml down
```
Notes:
- Volume `weatherwise_data` is created automatically and stores `/data/weather.db`.
- If running rootless, ensure your user can bind to port 8000 or adjust the mapping.
- Environment variables mirror the Docker Compose setup; override via `-f` overlays or `--env-file`.
- Scheduler seeds the default Reykjavík station on start and runs an initial fetch (envs configurable as above).
- Superuser auto-created in the web container; password is logged if `ADMIN_PASSWORD` is unset.
- To bind the DB to a host path, change both service volume entries in `podman-compose.yml` to `- /opt/weatherwise:/data` and remove the `weatherwise_data` volume at the bottom.

## Notes
- The Icelandic XML weather service data is parsed with `weatherwise/weatherwane/management/commands/pywsoi.py`.
- The chart view in `weatherwane/charts/views.py` expects `django-chartit` (or a compatible fork) to be installed. Install it separately if you need the chart page. 
- The `Observation.updatemetar` helper requires the `python-metar` package; it is not pinned in `requirements.txt` because compatibility with Django 5/Python 3 may vary.
