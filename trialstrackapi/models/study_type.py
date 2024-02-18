from django.db import models

class StudyType(models.Model):
  
  name = models.CharField(max_length=50)