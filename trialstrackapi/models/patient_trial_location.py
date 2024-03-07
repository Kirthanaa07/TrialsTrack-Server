from django.db import models

from trialstrackapi.models.researcher import Researcher
from .patient import Patient
from .trial_location import TrialLocation


class PatientTrialLocation(models.Model):
    class Meta:
        db_table = "patient_trial_location"

    trial_location = models.ForeignKey(
        TrialLocation,
        related_name="trial_location_patients",
        on_delete=models.CASCADE,
    )
    patient = models.ForeignKey(
        Patient,
        related_name="patient_trial_locations",
        on_delete=models.CASCADE,
    )
    researcher = models.ForeignKey(
        Researcher,
        related_name="researcher_patient_trial_locations",
        on_delete=models.CASCADE,
    )
    status = models.CharField(max_length=50)
