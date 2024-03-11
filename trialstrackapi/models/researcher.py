from django.db import models
from .user import User
from .location import Location


class Researcher(models.Model):
    class Meta:
        db_table = "researcher"

    user = models.OneToOneField(
        User, related_name="researcher", on_delete=models.CASCADE
    )
    location = models.ForeignKey(
        Location, related_name="location_researchers", on_delete=models.CASCADE
    )
    department = models.CharField(max_length=50)
