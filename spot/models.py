from __future__ import unicode_literals
from django.db import models

class Spot(models.Model):
    #Already has an ID equivalent to models.AutoField(primary_key=True)
    lat        = models.DecimalField(max_digits=9, decimal_places=6)
    lon        = models.DecimalField(max_digits=9, decimal_places=6) 
    avail      = models.BooleanField(default=False)
    time_from  = models.FloatField()
    time_to    = models.FloatField()
