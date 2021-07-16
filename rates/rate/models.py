from django.db import models


class City(models.Model):
    city_name = models.CharField(max_length=200)
    rate = models.FloatField(default=0)


class Reservation(models.Model):
    reservation = models.CharField(max_length=200)
    checkin_date = models.DateTimeField()
    checkin_date = models.DateTimeField()
    flat = models.CharField(max_length=200)
    income = models.FloatField()
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)
