from django.db import models
from .user import User
from .location import Location

class Researcher(models.Model):
  
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  location = models.ForeignKey(Location, on_delete=models.CASCADE)
  department = models.CharField(max_length=50)