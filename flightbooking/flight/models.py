from django.db import models

# Create your models here.

class Customer(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    password = models.CharField(max_length=20, null=True)
    firstname = models.CharField(max_length=100, null=True)
    lastname = models.CharField(max_length=100, null=True)
    birthday = models.DateField(null=True)
    phonenumber = models.CharField(max_length=10, null=True)
    class Meta:
        db_table = "customer"
        managed = False


class Flightclass(models.Model):
    flight_class = models.CharField(max_length=50,primary_key=True)
    price = models.FloatField(null=True, blank=True)
    class Meta:
        db_table = "flightclass"
        managed = False
    def __str__(self):
        return self.flight_class

class Flight(models.Model):
    flight_id  = models.CharField(max_length=10,primary_key=True)
    departure = models.CharField(max_length=100)
    destination = models.CharField(max_length=10)
    gate = models.CharField(max_length=10)
    boarding_time = models.TimeField(null=True)
    boarding_date = models.DateField(null=True)
    class Meta:
        db_table = "flight"
        managed = False
    def __str__(self):
        return self.flight_id

class Ticket(models.Model):
    ticket_id  = models.CharField(max_length=10,primary_key=True)
    flightid  =  models.ForeignKey(Flight, on_delete=models.CASCADE, db_column='flight_id')
    flight_class = models.ForeignKey(Flightclass, on_delete=models.CASCADE, db_column='flight_class')
    username = models.ForeignKey(Customer, on_delete=models.CASCADE, db_column='username')
    seat = models.CharField(max_length=10)
    class Meta:
        db_table = "ticket"
        managed = False
    def __str__(self):
        return self.ticket_id

