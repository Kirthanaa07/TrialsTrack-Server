from django.db import models
from trialstrackapi.models.location import Location


class Trial(models.Model):
    class Meta:
        db_table = "trial"

    nct_id = models.CharField(max_length=50)
    title = models.CharField(max_length=50)
    brief_title = models.TextField()
    study_type = models.CharField(max_length=50)
    overall_status = models.CharField(max_length=50)
    brief_summary = models.TextField()
    detail_description = models.TextField()
    phase = models.CharField(max_length=50)
    eligibility = models.TextField()
    study_first_submit_date = models.DateField()
    last_update_submit_date = models.DateField()
    lead_sponsor_name = models.CharField(max_length=150)
    locations = models.ManyToManyField(
        Location, through="TrialLocation", related_name="trials"
    )
    imported_date = models.DateTimeField()
