from django.db import models
from django.utils import timezone
import datetime


class Enterprise(models.Model):
    name = models.CharField(max_length=20)
    info = models.CharField(max_length=100)


class Zone(models.Model):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    letter = models.CharField(max_length=2)
    quantity = models.IntegerField(default=1)
    info = models.CharField(max_length=100)


class Place(models.Model):
    zone = models.ForeignKey(Zone, on_delete=models.CASCADE)
    place_number = models.IntegerField(blank=True)
    description = models.CharField(max_length=30, blank=True)
    car_number = models.CharField(max_length=9, default=None)
    booking_created = models.DateTimeField(blank=True)
    booking_start = models.DateTimeField(blank=True)
    booking_duration = models.IntegerField(default=40)
    place_type = models.IntegerField(blank=True, null=True)
    state = models.PositiveSmallIntegerField(default=1)
    completed = models.BooleanField(default=False)
    parent = models.IntegerField(blank=True, null=True)
    comment = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return "Zone:%s Place number:%s" % (self.zone.letter, self.place_number)

    def book(self):
        self.state = 2 if self.state == 1 else 2
        self.pk = None
        try:
            self.save()
        except Exception:
            pass

