from django.db import models
from .trial import Trial
from .location import Location


class TrialLocation(models.Model):
    class Meta:
        db_table = "trial_location"

    trial = models.ForeignKey(
        Trial, related_name="trial_locations", on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        Location, related_name="location_trials", on_delete=models.CASCADE
    )
    contact_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=50)
    contact_email = models.CharField(max_length=100)
    pi_name = models.CharField(max_length=50)
    status = models.CharField(max_length=50)
