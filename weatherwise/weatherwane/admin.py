from django.contrib import admin
from weatherwane.models import Station, Observation

class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'auto_update')
    list_filter = ('auto_update',)
    search_fields = ('code',)

class ObservationAdmin(admin.ModelAdmin):
    list_display = ('station', 'observation_time', 'temperature', 'wind_speed', 'wind_compass', 'visibility', 'sealevel_pressure', 'sky_conditions', 'weather_conditions')
    date_hierarchy = 'observation_time'


admin.site.register(Station, StationAdmin)
admin.site.register(Observation, ObservationAdmin)

