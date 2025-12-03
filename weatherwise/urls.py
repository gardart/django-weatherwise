from django.contrib import admin
from django.urls import path

from weatherwise.weatherwane.views import observations_list

urlpatterns = [
    path("", observations_list, name="observations_list"),
    path("admin/", admin.site.urls),
]
