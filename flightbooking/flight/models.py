from django.db import models

# Create your models here.

class Customer(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=20, null=True)
    firstname = models.CharField(max_length=100, null=True)
    birthday = models.DateField(null=True)
    phonenumber = models.CharField(max_length=10, null=True)
    class Meta:
        db_table = "customer"
        managed = False


class Flightclass(models.Model):
    flight_class = models.CharField(max_length=50,primary_key=True)
    price = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = "flight_class"
        managed = False
    def __str__(self):
        return self.flight_class


