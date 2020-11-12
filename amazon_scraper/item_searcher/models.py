from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=100)
    current_price = models.FloatField()
    url = models.CharField(max_length=100, default='')


    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item_searcher_detail', kwargs={'pk': self.pk}) #reverse returns the full path as a string. kwargs part returns the instance of the specifc posts primary key



class TrackingDetails(models.Model):
    target_price = models.FloatField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Price(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    price = models.FloatField()
    date = models.DateTimeField()

