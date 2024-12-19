import csv

from nautobot.apps.jobs import register_jobs, Job, TextVar
from nautobot.dcim.models.locations import Location, LocationType
from nautobot.extras.models.statuses import Status

# Maps abbreviated US state names to their long forms
STATE_ABBREVIATION_MAPPING = {
    "CA": "California",
    "VA": "Virginia",
    "NJ": "New Jersey",
    "IL": "Illinois",
}


class LocationJob(Job):
    class Meta:
        name = "Create Locations from CSV"

    csv_file = TextVar(description="CSV input file.")

    def run(self, csv_file):
        reader = csv.DictReader(csv_file.splitlines(), delimiter=",")
        state_location_type = LocationType.objects.get(name="State")
        city_location_type = LocationType.objects.get(name="City")
        data_center_location_type = LocationType.objects.get(name="Data Center")
        branch_location_type = LocationType.objects.get(name="Branch")
        default_status = Status.objects.get(name="Active")
        for row in reader:
            state_name = row["state"] if len(row["state"]) > 2 else STATE_ABBREVIATION_MAPPING.get(row["state"], None)
            if not state_name:
                self.logger.warning("Unknown state '%s' - skipping.", row["state"])
                continue
            state, _ = Location.objects.get_or_create(
                name=state_name,
                location_type=state_location_type,
                defaults={"status": default_status},
            )
            city, _ = Location.objects.get_or_create(
                name=row["city"],
                parent=state,
                location_type=city_location_type,
                defaults={"status": default_status},
            )
            Location.objects.get_or_create(
                name=row["name"],
                parent=city,
                location_type=branch_location_type if row["name"].endswith("BR") else data_center_location_type,
                defaults={"status": default_status},
            )
            self.logger.info(row)


register_jobs(LocationJob)
