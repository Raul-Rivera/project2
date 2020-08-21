from django.contrib.auth.models import AbstractUser
from django.db import models
from django import forms
from django.db.models import Max

class User(AbstractUser):
    pass

class Listing(models.Model):
    name = models.CharField(max_length = 77, default="name")
    description = models.CharField(max_length = 1000)
    img_url = models.URLField(null = True)
    category = models.CharField(null = True, max_length = 70)
    starting_bid = models.IntegerField()
    owner = models.ForeignKey(User, on_delete = models.CASCADE, null = True, related_name = "Owner")
    active = models.BooleanField(default = True)
    new_owner = models.ForeignKey(User, on_delete = models.CASCADE, null = True, related_name = "New_Owner")

    def maximum_bid(self):
        return Bids.objects.all().filter(catalog=self).aggregate(Max("bid"))

    def __str__(self):
        return f"{self.name} - {self.description} \t Starting Bid: {self.starting_bid}"



class Bids(models.Model):
    catalog = models.ForeignKey(Listing, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    bid = models.IntegerField()



class Comment(models.Model):
    catalog = models.ForeignKey(Listing, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
    text = models.CharField(max_length = 1000)

    def __str__(self):
        return f"{self.text}"


class Watchlist(models.Model):
    catalog = models.ForeignKey(Listing, on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete = models.CASCADE)
