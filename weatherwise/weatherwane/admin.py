
import unicodecsv as csv
import datetime
from django.contrib import admin
from weatherwane.models import Station, Observation

from django.contrib import admin
from django.contrib.admin import util as admin_util
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse


def export_model_as_csv(modeladmin, request, queryset):
    if hasattr(modeladmin, 'exportable_fields'):
        field_list = modeladmin.exportable_fields
    else:
        # Copy modeladmin.list_display to remove action_checkbox
        field_list = modeladmin.list_display[:]
        field_list.remove('action_checkbox')

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=%s-%s-export-%s.csv' % (
        __package__.lower(),
        queryset.model.__name__.lower(),
        datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )

    writer = csv.writer(response)
    writer.writerow(
        [admin_util.label_for_field(f, queryset.model, modeladmin) for f in field_list],
    )

    for obj in queryset:
        csv_line_values = []
        for field in field_list:
            field_obj, attr, value = admin_util.lookup_field(field, obj, modeladmin)
            csv_line_values.append(value)

        writer.writerow(csv_line_values)

    return response
export_model_as_csv.short_description = _('Export to CSV')


#class MyModelAdmin(admin.ModelAdmin):
#    actions = (export_model_as_csv,)
#    exportable_fields = ('name', 'description',)

class StationAdmin(admin.ModelAdmin):
    list_display = ('name', 'latitude', 'longitude', 'auto_update')
    list_filter = ('auto_update',)
    search_fields = ('code',)
#    actions = (export_model_as_csv,)

class ObservationAdmin(admin.ModelAdmin):
    list_filter = ('station', 'observation_time', 'wind_compass', 'wind_speed')
    list_display = ('station', 
		'observation_time', 
		'temperature', 
#		'dewpoint',
		'wind_speed', 
		'wind_compass',
		'wind_speed_gust',
		'wind_speed_max',
#		'visibility', 
		'sealevel_pressure',
		'relative_humidity',
		'precipitation',
		'cloud_cover',
#		'sky_conditions',
		'weather_conditions',
#		'snc',
#		'snd',
#		'sed',
		'moon_alt',
		'moon_phase',
     		'moon_dec'
)
    date_hierarchy = 'observation_time'
    actions = (export_model_as_csv,)	## Action to export data as csv (fields given in exportable_fields arrey)
    exportable_fields = ('observation_time','temperature','wind_speed','wind_compass','wind_speed_gust','wind_speed_max','sealevel_pressure','relative_humidity','precipitation','cloud_cover','weather_conditions','moon_alt','moon_phase','moon_dec',)


admin.site.register(Station, StationAdmin)
admin.site.register(Observation, ObservationAdmin)
