from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.

class Item(models.Model):
    name = models.CharField(max_length=100)
    #description = models.TextField()
    price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('item_searcher_detail', kwargs={'pk': self.pk}) #reverse returns the full path as a string. kwargs part returns the instance of the specifc posts primary key


class TrackingDetails(models.Model):
    current_price = models.FloatField()
    start_price = models.FloatField()
    target_price = models.FloatField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.PROTECT)
