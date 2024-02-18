from django.db import models
from .clinical_trial import ClinicalTrial
from .location import Location

class ClinicalTrialLocation(models.Model):

    clinical_trial = models.ForeignKey(ClinicalTrial, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
