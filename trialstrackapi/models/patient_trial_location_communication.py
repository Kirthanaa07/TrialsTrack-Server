from django.db import models

from trialstrackapi.models.patient_trial_location import PatientTrialLocation
from .researcher import Researcher
from .trial_location import TrialLocation


class PatientTrialLocationCommunication(models.Model):
    class Meta:
        db_table = "patient_trial_location_communication"

    patient_trial_location = models.ForeignKey(
        PatientTrialLocation,
        related_name="trial_location_researchers",
        on_delete=models.CASCADE,
    )
    message = models.TextField()
    created_by = models.CharField(max_length=100)
    created_date = models.DateTimeField()
    