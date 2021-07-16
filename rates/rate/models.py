from django.db import models


class City(models.Model):
    city_name = models.CharField(max_length=200)
    rate = models.FloatField(default=0)

    def __str__(self):
        return f"{self.city_name} -> {self.rate}"


class Reservation(models.Model):
    reservation = models.CharField(max_length=200, unique=True)
    checkin_date = models.DateTimeField()
    checkout_date = models.DateTimeField()
    flat = models.CharField(max_length=200)
    income = models.FloatField()
    city = models.ForeignKey(City, on_delete=models.DO_NOTHING)

    def __str__(self):
        return f"RID={self.reservation}\tin={self.checkin_date}\tout={self.checkout_date}\tincome={self.income}"
