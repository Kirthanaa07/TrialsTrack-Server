from django.db import models

class Sponsor(models.Model):
  name = models.CharField(max_length=50)