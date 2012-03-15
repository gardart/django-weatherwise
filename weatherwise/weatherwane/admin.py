from django.contrib import admin
from weatherwane.models import Station, Observation

class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'auto_update')
    list_filter = ('auto_update',)
    search_fields = ('code',)

class ObservationAdmin(admin.ModelAdmin):
    list_display = ('station', 
		'observation_time', 
		'temperature', 
		'dewpoint',
		'wind_speed', 
		'wind_compass',
		'wind_speed_gust',
		'wind_speed_max',
		'visibility', 
		'sealevel_pressure',
		'relative_humidity',
		'precipitation',
		'cloud_cover',
		'sky_conditions',
		'weather_conditions',
		'snc',
		'snd',
		'sed'
)
    date_hierarchy = 'observation_time'


admin.site.register(Station, StationAdmin)
admin.site.register(Observation, ObservationAdmin)

