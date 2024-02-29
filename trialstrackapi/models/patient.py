from django.db import models
from .user import User

class Patient(models.Model):
  
  user = models.ForeignKey(User, on_delete=models.CASCADE)
  age = models.IntegerField()
  gender = models.CharField(max_length=50)
  dob = models.DateField()