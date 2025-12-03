from decimal import Decimal
from math import radians as rad, degrees as deg

import ephem  # available from http://rhodesmill.org/pyephem
from dateutil import tz
from django.core.exceptions import ImproperlyConfigured
from django.db import models


class StationManager(models.Manager):
    def auto_update(self):
        return self.filter(auto_update=True)


class Station(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True)
    code = models.CharField(max_length=20)
    source = models.CharField(max_length=200, null=True, blank=True)
    latitude = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=6, null=True, blank=True)
    elevation = models.IntegerField(null=True, blank=True)
    auto_update = models.BooleanField(default=False)

    objects = StationManager()

    class Meta:
        ordering = ["code"]

    def get_name(self):
        return self.name

    def __str__(self):
        return self.name or self.code


class ObservationManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().order_by("-observation_time")

    def twenty_four_newest(self):
        return self.get_queryset()[:24]


class Observation(models.Model):
    station = models.ForeignKey(Station, on_delete=models.CASCADE)
    data = models.TextField(null=True, blank=True)
    observation_type = models.CharField(max_length=5, null=True, blank=True)
    observation_cycle = models.IntegerField(null=True, blank=True)
    observation_time = models.DateTimeField(null=True, blank=True)
    wind_compass = models.CharField(max_length=4, null=True, blank=True, verbose_name="WC")
    wind_speed = models.IntegerField(null=True, blank=True, verbose_name="WS")
    wind_speed_gust = models.IntegerField(null=True, blank=True, verbose_name="WSG")
    wind_speed_max = models.IntegerField(null=True, blank=True, verbose_name="WSM")
    visibility = models.CharField(max_length=5, null=True, blank=True, verbose_name="VIS")
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="T")
    dewpoint = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True, verbose_name="DEW")
    sky_conditions = models.TextField(null=True, blank=True, verbose_name="SKY")
    cloud_cover = models.IntegerField(null=True, blank=True, verbose_name="CLC")
    weather_conditions = models.TextField(null=True, blank=True, verbose_name="CON")
    sealevel_pressure = models.IntegerField(null=True, blank=True, verbose_name="P")
    relative_humidity = models.IntegerField(null=True, blank=True, verbose_name="RH")
    precipitation = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, verbose_name="PRE")
    snc = models.TextField(null=True, blank=True)
    snd = models.IntegerField(null=True, blank=True)
    sed = models.TextField(null=True, blank=True)

    objects = ObservationManager()

    class Meta:
        ordering = ["-observation_time"]

    def get_metar_object(self):
        if not self.data:
            return None
        try:
            from metar.Metar import Metar  # Imported lazily to avoid hard dependency unless used
        except ImportError as exc:
            raise ImproperlyConfigured("Install python-metar to parse METAR data.") from exc

        return Metar(self.data)

    def get_lunar_object(self):
        location = ephem.Observer()
        location.lon = rad(self.station.longitude)
        location.lat = rad(self.station.latitude)
        location.elevation = self.station.elevation
        location.date = self.observation_time
        return ephem.Moon(location)

    def __str__(self):
        if self.observation_time:
            return f"{self.station} @ {self.observation_time}"
        return f"{self.station} observation"

    def updatemetar(self):
        metar = self.get_metar_object()
        if not metar:
            return
        self.observation_time = metar.time.replace(tzinfo=tz.gettz("UTC"))
        self.observation_cycle = metar.cycle
        self.observation_type = metar.type
        self.observation_mode = metar.mod  # type: ignore[attr-defined]
        self.temperature = Decimal(str(metar.temp.value(units="c")))
        self.dewpoint = Decimal(str(metar.dewpt.value(units="c")))
        self.visibility = str(metar.vis.value(units="KM"))
        if metar.wind_dir:
            self.wind_compass = metar.wind_dir.compass()
        if metar.wind_speed:
            self.wind_speed = int(round(metar.wind_speed.value(units="mps")))
        if metar.wind_gust:
            self.wind_speed_gust = int(metar.wind_gust.value(units="mps"))
        self.sealevel_pressure = int(metar.press.value(units="mb"))
        self.sky_conditions = str(metar.sky_conditions())
        self.weather_conditions = str(metar.present_weather())
        self.relative_humidity = int(
            100 - 5 * (metar.temp.value(units="c") - metar.dewpt.value(units="c"))
        )

    def moon_dec(self):
        moon = self.get_lunar_object()
        return round(deg(moon.dec), 1)

    def moon_alt(self):
        moon = self.get_lunar_object()
        return round(deg(moon.alt), 1)

    def moon_phase(self):
        moon = self.get_lunar_object()
        return round(moon.phase, 1)
