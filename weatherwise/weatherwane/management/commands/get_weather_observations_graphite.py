import calendar
import socket
import time
from pprint import pprint

from django.core.management.base import BaseCommand

from ...models import Station
from ..pywsoi import get_weather_from_wsoi

CARBON_SERVER = "199.175.48.167"
CARBON_PORT = 2003
DELAY = 15  # secs

SILENT, NORMAL, VERBOSE = 0, 1, 2


def send_msg(message, server, port):
    print(f"sending message to {server}:{port}\n{message}")
    sock = socket.socket()
    sock.connect((server, port))
    sock.sendall(message.encode("utf-8"))
    sock.close()


class Command(BaseCommand):
    help = "Aggregates data from weather feed and forwards to Graphite"

    def add_arguments(self, parser):
        parser.add_argument("--server", default=CARBON_SERVER, help="Graphite Carbon server")
        parser.add_argument("--port", default=CARBON_PORT, type=int, help="Graphite Carbon port")

    def handle(self, *args, **options):
        verbosity = int(options.get("verbosity", VERBOSE))
        server = options["server"]
        port = options["port"]

        for station in Station.objects.all():
            weather = get_weather_from_wsoi(station.code, "3h", "en")
            if verbosity > NORMAL:
                pprint(weather)
            timestamp = weather.get("time")
            if not timestamp:
                continue
            timestamp_struct = time.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            timestamp_epoch = calendar.timegm(timestamp_struct)
            lines = [
                "stations.%s.T %s %d" % (station.code, weather.get("T"), timestamp_epoch),
                "stations.%s.TD %s %d" % (station.code, weather.get("TD"), timestamp_epoch),
                "stations.%s.RH %s %d" % (station.code, weather.get("RH"), timestamp_epoch),
                "stations.%s.F %s %d" % (station.code, weather.get("F"), timestamp_epoch),
                "stations.%s.FG %s %d" % (station.code, weather.get("FG"), timestamp_epoch),
                "stations.%s.FX %s %d" % (station.code, weather.get("FX"), timestamp_epoch),
                "stations.%s.V %s %d" % (station.code, weather.get("V"), timestamp_epoch),
                "stations.%s.N %s %d" % (station.code, weather.get("N"), timestamp_epoch),
                "stations.%s.P %s %d" % (station.code, weather.get("P"), timestamp_epoch),
                "stations.%s.R %s %d" % (station.code, weather.get("R"), timestamp_epoch),
                "stations.%s.SNC %s %d" % (station.code, weather.get("SNC"), timestamp_epoch),
                "stations.%s.SND %s %d" % (station.code, weather.get("SND"), timestamp_epoch),
                "stations.%s.SED %s %d" % (station.code, weather.get("SED"), timestamp_epoch),
            ]
            message = "\n".join(lines) + "\n"
            send_msg(message, server, port)
            time.sleep(DELAY)
