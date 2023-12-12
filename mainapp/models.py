from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class BicimadStation(models.Model):
    id = models.AutoField(primary_key=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    name = models.CharField(max_length=555)
    number = models.CharField(max_length=100)
    address = models.CharField(max_length=555)
    activate = models.IntegerField()
    no_available = models.IntegerField()
    total_bases = models.IntegerField()
    dock_bikes = models.IntegerField()
    free_bases = models.IntegerField()
    reservations_count = models.IntegerField()

    def __str__(self):
        return f"{self.name} ({self.number})"

class savedBICIMAD(models.Model):
    user=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    savedStation=models.ForeignKey(BicimadStation,null=True,on_delete=models.SET_NULL)


class Estacion(models.Model):
    IDESTACION = models.IntegerField(primary_key=True)
    DENOMINACION = models.CharField(max_length=255)
    LINEAS = models.CharField(max_length=255)
    longitude = models.FloatField()
    latitude = models.FloatField()
    ACONDICIONAMIENTOVIAJEROS=models.IntegerField()
    def __str__(self):
        return f"{self.IDESTACION} - {self.DENOMINACION}"
    
class savedStops(models.Model):
    user=models.ForeignKey(User,null=True,on_delete=models.SET_NULL)
    savedStop=models.ForeignKey(Estacion,null=True,on_delete=models.SET_NULL)