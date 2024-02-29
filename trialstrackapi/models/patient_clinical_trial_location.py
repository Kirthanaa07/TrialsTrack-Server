from django.db import models
from .patient import Patient
from .clinical_trial_location import ClinicalTrialLocation

class PatientClinicalTrialLocation(models.Model):
  clinical_trial_location = models.ForeignKey(ClinicalTrialLocation, on_delete=models.CASCADE)
  patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
  status = models.CharField(max_length=50)