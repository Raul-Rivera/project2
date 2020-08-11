from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.db.models import Max

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length = 70)
    description = models.CharField(max_length = 1000)
    img_url = models.URLField(blank = True)
    category = models.CharField(blank = True, max_length = 70)
    starting_bid = models.DecimalField(max_digits = 12, decimal_places = 2)
    user = models.ForeignKey(User, on_delete = models.CASCADE, blank = True, related_name = "Owner")
    active = models.BooleanField(blank = False, default = True)
    winner = models.ForeignKey(User, blank = True, on_delete = models.CASCADE, related_name = "New_Owner", null = True)

    def maximum_bid(self):
        return Bids.objects.all().filter(listing=self).aggregate(Max("bid"))

    def __str__(self):
        return (f"{self.title} - {self.description} \t Starting Bid: {self.starting_bid}")
