import csv

from nautobot.apps.jobs import Job, register_jobs
from nautobot.extras.jobs import TextVar


class LocationJob(Job):
    csv_file = TextVar(description="CSV input file.")

    def run(self, csv_file):
        reader = csv.DictReader(csv_file)
        for row in reader:
            self.logger.info(row)

register_jobs([LocationJob])
