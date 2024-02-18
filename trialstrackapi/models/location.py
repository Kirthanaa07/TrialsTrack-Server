from django.db import models
from .user import User

class Location(models.Model):
  
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  address = models.CharField(max_length=50)
  city = models.CharField(max_length=50)
  state = models.CharField(max_length=50)
  zip = models.IntegerField()
  country = models.CharField(max_length=50)
  