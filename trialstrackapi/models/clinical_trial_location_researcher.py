from django.db import models
from .researcher import Researcher
from .clinical_trial_location import ClinicalTrialLocation


class ClinicalTrialLocationResearcher(models.Model):
    clinical_trial_location = models.ForeignKey(
        ClinicalTrialLocation, on_delete=models.CASCADE
    )
    researcher = models.ForeignKey(Researcher, on_delete=models.CASCADE)
