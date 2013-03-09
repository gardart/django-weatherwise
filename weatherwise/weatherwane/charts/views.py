from chartit import DataPool, Chart
from weatherwane.models import Observation

def weather_chart_view(request):
    #Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = DataPool(
           series=
            [{'options': {
               'source': Observation.objects.all()},
              'terms': [
		'observation_time',
                'wind_speed']}
             ])

    #Step 2: Create the Chart object
    cht = Chart(
            datasource = weatherdata,
            series_options =
              [{'options':{
                  'type': 'line',
                  'stacking': False},
                'terms':{
                  'observation_time': [
                    'wind_speed']
                  }}],
            chart_options =
              {'title': {
                   'text': 'Weather Data'},
               'xAxis': {
                    'title': {
                       'text': 'Date'}}})

    #Step 3: Send the chart object to the template.
    return render_to_response({'weatherchart': cht})
