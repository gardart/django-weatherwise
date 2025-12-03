import urllib.request
from pprint import pprint
from xml.dom import minidom

WSOI_WEATHER_URL = (
    "http://xmlweather.vedur.is/?op_w=xml&type=obs&view=xml&params="
    "T;TD;D;F;FX;FG;N;V;W;P;RH;R;SNC;SND;SED&ids=%s&time=%s&lang=%s"
)


def get_weather_from_wsoi(station_id, time_period, lang):
    url = WSOI_WEATHER_URL % (station_id, time_period, lang)

    with urllib.request.urlopen(url) as handler:
        dom = minidom.parse(handler)

    data_structure = (
        "name",
        "time",
        "err",
        "link",
        "T",
        "TD",
        "D",
        "F",
        "FX",
        "FG",
        "N",
        "V",
        "W",
        "P",
        "RH",
        "R",
        "SNC",
        "SND",
        "SED",
    )
    weather_data = {}

    current_observation = dom.getElementsByTagName("station")

    for tag in data_structure:
        try:
            value_node = current_observation[0].getElementsByTagName(tag)[0]
            if value_node.childNodes and value_node.childNodes[0].data:
                weather_data[tag] = value_node.childNodes[0].data
            else:
                weather_data[tag] = None
        except IndexError:
            weather_data[tag] = None

    dom.unlink()
    pprint(url)
    return weather_data
