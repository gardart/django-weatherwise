import time
from socket import create_connection

from django.core.management.base import BaseCommand

from ...models import Observation

CARBON_SERVER = "199.175.48.167"
CARBON_PORT = 2003


class Command(BaseCommand):
    help = "Send observations to Graphite"

    def add_arguments(self, parser):
        parser.add_argument("--server", default=CARBON_SERVER, help="Graphite Carbon server")
        parser.add_argument("--port", default=CARBON_PORT, type=int, help="Graphite Carbon port")
        parser.add_argument("--delay", default=60, type=int, help="Delay between batches in seconds")

    def handle(self, *args, **options):
        server = options["server"]
        port = options["port"]
        delay = options["delay"]

        observations = Observation.objects.all()
        if not observations.exists():
            self.stdout.write("No observations to send")
            return

        try:
            sock = create_connection((server, port))
        except OSError:
            self.stderr.write(f"Couldn't connect to {server} on port {port}, is carbon-agent.py running?")
            return

        lines = []
        for observation in observations:
            if observation.temperature is None:
                continue
            station_code = observation.station.code
            timestamp = (
                int(observation.observation_time.timestamp())
                if observation.observation_time
                else int(time.time())
            )
            metric_name = f"stations.{station_code}.temperature"
            lines.append(f"{metric_name} {observation.temperature} {timestamp}")

        if not lines:
            self.stdout.write("No metrics created from observations")
            sock.close()
            return

        message = "\n".join(lines) + "\n"
        sock.sendall(message.encode("utf-8"))
        sock.close()
        self.stdout.write(f"Sent {len(lines)} metrics to {server}:{port}")

        if delay:
            time.sleep(delay)
