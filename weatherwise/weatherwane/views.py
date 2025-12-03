from django.shortcuts import render

from .models import Observation


def observations_list(request):
    observations = Observation.objects.select_related("station")[:200]
    return render(
        request,
        "observations_list.html",
        {
            "observations": observations,
        },
    )
