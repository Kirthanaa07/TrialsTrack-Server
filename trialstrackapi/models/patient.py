from django.db import models
from .user import User


class Patient(models.Model):
    class Meta:
        db_table = "patient"
        
    user = models.OneToOneField(User, related_name="patient", on_delete=models.CASCADE)
    age = models.IntegerField()
    gender = models.CharField(max_length=50)
    dob = models.DateField()
