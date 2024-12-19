import csv

from nautobot.apps.jobs import register_jobs, Job, TextVar



class LocationJob(Job):
    class Meta:
        name = "Create Locations from CSV"

    csv_file = TextVar(description="CSV input file.")

    def run(self, csv_file):
        reader = csv.DictReader(csv_file.splitlines())
        for row in reader:
            self.logger.info(row)


register_jobs(LocationJob)
