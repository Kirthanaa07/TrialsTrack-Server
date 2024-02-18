from django.db import models

class Location(models.Model):
  
  uid = models.CharField(max_length=50)
  name = models.CharField(max_length=50)
  address = models.CharField(max_length=50)
  city = models.CharField(max_length=50)
  state = models.CharField(max_length=50)
  zip = models.IntegerField()
  country = models.CharField(max_length=50)
  