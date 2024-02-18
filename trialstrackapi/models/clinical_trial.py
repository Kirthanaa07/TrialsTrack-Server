from django.db import models
from .study_type import StudyType

class ClinicalTrial(models.Model):
  
  uid = models.CharField(max_length=50)
  nct_id = models.CharField(max_length=50)
  title = models.CharField(max_length=50)
  study_type = models.ForeignKey(StudyType, on_delete=models.CASCADE)
  overall_status = models.CharField(max_length=50)
  brief_summary = models.CharField(max_length=50)
  detail_description = models.CharField(max_length=50)
  phase = models.CharField(max_length=50)
  eligibility = models.CharField(max_length=50)
  study_first_submit_date = models.DateField()
  last_update_submit_date = models.DateField()