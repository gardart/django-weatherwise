from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import render

from ..models import Observation

def weather_chart_view(request):
    try:
        from chartit import Chart, DataPool
    except ImportError as exc:
        raise ImproperlyConfigured("django-chartit must be installed to render charts.") from exc

    weatherdata = DataPool(
        series=[
            {
                "options": {"source": Observation.objects.all()},
                "terms": ["observation_time", "wind_speed"],
            }
        ]
    )

    #Step 2: Create the Chart object
    cht = Chart(
        datasource=weatherdata,
        series_options=[
            {
                "options": {"type": "line", "stacking": False},
                "terms": {"observation_time": ["wind_speed"]},
            }
        ],
        chart_options={"title": {"text": "Weather Data"}, "xAxis": {"title": {"text": "Date"}}},
    )

    return render(request, "weatherchart.html", {"weatherchart": cht})
