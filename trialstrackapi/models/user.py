from django.db import models


class User(models.Model):
    class Meta:
        db_table = "user"

    uid = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=50)
