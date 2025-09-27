from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class ClothType(models.Model):
    clothtypes = models.CharField(max_length=25)
    
    def __str__(self):
        return self.clothtypes

class ServiceType(models.Model):
    servicetypes = models.CharField(max_length=25)
    price = models.IntegerField()
    
    def __str__(self):
        return f"{self.servicetypes} - ₹{self.price}"

class Address(models.Model):
    address = models.CharField(max_length=250)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)

class OrderNumber(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    orders = models.IntegerField(default=0)

class Status(models.Model):
    status = models.CharField(max_length=25)
    
    def __str__(self):
        return self.status

class Orders(models.Model):
    date = models.DateTimeField()
    clothtype = models.CharField(max_length=25,default=None)
    noofclothes = models.IntegerField()
    cost = models.IntegerField(default=0)
    discound = models.IntegerField(default=0)
    totalcost = models.IntegerField(default=0)
    statusid = models.ForeignKey(Status, on_delete=models.PROTECT)
    servicetypes = models.CharField(max_length=25,default=0)
    homedelivery = models.BooleanField(default=False)
    serviceid = models.ForeignKey(ServiceType, on_delete=models.PROTECT)
    userid = models.ForeignKey(User, on_delete=models.CASCADE)

class Discounds(models.Model):
    discounds = models.IntegerField(default=0)
    orders = models.IntegerField(default=0)

class Payment(models.Model):
    payed = models.BooleanField()
    orderid = models.ForeignKey(Orders, on_delete=models.CASCADE)

class Feedback(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.CharField(max_length=500,default=0)