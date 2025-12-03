from datetime import datetime, timezone
from pprint import pformat

from django.core.management.base import BaseCommand

from ...models import Observation, Station
from .pywsoi import get_weather_from_wsoi

SILENT, NORMAL, VERBOSE = 0, 1, 2


class Command(BaseCommand):
    help = "Aggregates data from weather feed"

    def handle(self, *args, **options):
        verbosity = int(options.get("verbosity", VERBOSE))
        created_count = 0
        last_log = None

        for station in Station.objects.all():
            weather = get_weather_from_wsoi(station.code, "3h", "en")
            if verbosity > NORMAL:
                self.stdout.write(pformat(weather))

            observation_time = self._parse_timestamp(weather.get("time"))
            log, created = Observation.objects.get_or_create(
                station=station,
                observation_time=observation_time,
                defaults={
                    "temperature": weather.get("T"),
                    "dewpoint": weather.get("TD"),
                    "relative_humidity": weather.get("RH"),
                    "wind_compass": weather.get("D"),
                    "wind_speed": weather.get("F"),
                    "wind_speed_gust": weather.get("FG"),
                    "wind_speed_max": weather.get("FX"),
                    "visibility": weather.get("V"),
                    "cloud_cover": weather.get("N"),
                    "weather_conditions": weather.get("W"),
                    "sealevel_pressure": weather.get("P"),
                    "precipitation": weather.get("R"),
                    "snc": weather.get("SNC"),
                    "snd": weather.get("SND"),
                    "sed": weather.get("SED"),
                },
            )
            if created:
                created_count += 1
            last_log = log

        if verbosity > NORMAL:
            self.stdout.write(f"New weather observations: {created_count}")
            if last_log:
                self.stdout.write(str(last_log))
        elif verbosity > SILENT:
            message = "No new weather observations" if created_count == 0 else f"New weather observations: {created_count}"
            self.stdout.write(message)

    def _parse_timestamp(self, value):
        if not value:
            return None
        try:
            return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").replace(tzinfo=timezone.utc)
        except (TypeError, ValueError):
            return None
