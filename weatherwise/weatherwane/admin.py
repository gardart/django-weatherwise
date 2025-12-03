import csv
import datetime

from django.contrib import admin
from django.contrib.admin.utils import label_for_field, lookup_field
from django.http import HttpResponse
from django.utils.translation import gettext_lazy as _

from .models import Observation, Station


def export_model_as_csv(modeladmin, request, queryset):
    if hasattr(modeladmin, "exportable_fields"):
        field_list = list(modeladmin.exportable_fields)
    else:
        field_list = list(modeladmin.list_display)
        if "action_checkbox" in field_list:
            field_list.remove("action_checkbox")

    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = "attachment; filename=%s-%s-export-%s.csv" % (
        __package__.lower(),
        queryset.model.__name__.lower(),
        datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S"),
    )

    writer = csv.writer(response)
    writer.writerow([label_for_field(f, queryset.model, modeladmin) for f in field_list])

    for obj in queryset:
        csv_line_values = []
        for field in field_list:
            _, _, value = lookup_field(field, obj, modeladmin)
            csv_line_values.append(value)

        writer.writerow(csv_line_values)

    return response


export_model_as_csv.short_description = _("Export to CSV")


class StationAdmin(admin.ModelAdmin):
    list_display = ("name", "latitude", "longitude")
    search_fields = ("code",)


class ObservationAdmin(admin.ModelAdmin):
    list_filter = ("station", "observation_time", "wind_compass", "wind_speed")
    list_display = (
        "station",
        "observation_time",
        "temperature",
        "wind_speed",
        "wind_compass",
        "wind_speed_gust",
        "wind_speed_max",
        "sealevel_pressure",
        "relative_humidity",
        "precipitation",
        "cloud_cover",
        "weather_conditions",
        "moon_alt",
        "moon_phase",
        "moon_dec",
    )
    date_hierarchy = "observation_time"
    actions = (export_model_as_csv,)
    exportable_fields = (
        "observation_time",
        "temperature",
        "wind_speed",
        "wind_compass",
        "wind_speed_gust",
        "wind_speed_max",
        "sealevel_pressure",
        "relative_humidity",
        "precipitation",
        "cloud_cover",
        "weather_conditions",
        "moon_alt",
        "moon_phase",
        "moon_dec",
    )


admin.site.register(Station, StationAdmin)
admin.site.register(Observation, ObservationAdmin)
