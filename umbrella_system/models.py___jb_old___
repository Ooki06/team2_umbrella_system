from __future__ import unicode_literals

from django.db import models


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name

class User(models.Model):
    password = models.CharField(max_length=8)
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name

class Order(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    time_zone_id = models.IntegerField(default=0)
    order_day = models.DateTimeField('date published')
    charge_lv = models.IntegerField(default=0)
    order_flg = models.IntegerField(default=0)
