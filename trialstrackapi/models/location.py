from django.db import models


class Location(models.Model):
    class Meta:
        db_table = "location"

    name = models.CharField(max_length=100)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=50)
    zip = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    geo_lat = models.CharField(max_length=100)
    geo_lon = models.CharField(max_length=100)
    created_date = models.DateTimeField()
