from nautobot.apps.jobs import register_jobs

from jobs.locations import LocationJob

register_jobs([LocationJob])
