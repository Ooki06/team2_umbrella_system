from __future__ import unicode_literals
from django.db import models
from django.utils.encoding import python_2_unicode_compatible


# Create your models here.
class Room(models.Model):
    name = models.CharField(max_length=200)
    seats = models.IntegerField(default=0)
    def __unicode__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name

class User(models.Model):
    user_ids = models.CharField(max_length=20)
    user_name = models.CharField(max_length=20,default='')
    password = models.CharField(max_length=8)
    def __unicode__(self):
        return self.user_name

class Order(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    time_zone_id = models.IntegerField(default=0)
    order_day = models.DateTimeField('date published')
    charge_lv = models.IntegerField(default=0)
    def __unicode__(self):
        return self.room.name