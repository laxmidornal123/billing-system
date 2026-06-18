from django.db import models


class Customer(models.Model):

    name = models.CharField(max_length=100)

    mobile = models.CharField(max_length=15)

    email = models.EmailField()

    address = models.TextField()

    def __str__(self):
        return self.name