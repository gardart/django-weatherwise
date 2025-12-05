#!/usr/bin/env sh
set -e

INTERVAL_SECONDS="${FETCH_INTERVAL:-3600}"

STATION_CODE="${STATION_CODE:-1}"
STATION_NAME="${STATION_NAME:-Reykjavík}"
STATION_LAT="${STATION_LAT:-64.12888}"
STATION_LON="${STATION_LON:--21.90819}"
STATION_ELEVATION="${STATION_ELEVATION:-60}"
STATION_SOURCE="${STATION_SOURCE:-0-20000-0-04030}"

# Ensure the default station exists, then do one fetch before the loop.
python weatherwise/manage.py shell <<'PY'
import os
from decimal import Decimal, InvalidOperation
from weatherwise.weatherwane.models import Station

def parse_decimal(value):
    if value in (None, ""):
        return None
    try:
        return Decimal(value)
    except InvalidOperation:
        print(f"[station-init] Invalid decimal value: {value!r}; storing as NULL")
        return None

def parse_int(value):
    if value in (None, ""):
        return None
    try:
        return int(float(value))
    except (ValueError, TypeError):
        print(f"[station-init] Invalid integer value: {value!r}; storing as NULL")
        return None

defaults = dict(
    name=os.environ.get("STATION_NAME", "Reykjavík"),
    latitude=parse_decimal(os.environ.get("STATION_LAT", "64.12888")),
    longitude=parse_decimal(os.environ.get("STATION_LON", "-21.90819")),
    elevation=parse_int(os.environ.get("STATION_ELEVATION", "60")),
    source=os.environ.get("STATION_SOURCE", "0-20000-0-04030"),
)

station, created = Station.objects.update_or_create(
    code=os.environ.get("STATION_CODE", "1"),
    defaults=defaults,
)
print(f"[station-init] Station {'created' if created else 'updated'}: {station}")
PY

python weatherwise/manage.py get_weather_observations --verbosity 2

while true; do
    python weatherwise/manage.py get_weather_observations --verbosity 2
    sleep "${INTERVAL_SECONDS}"
done
