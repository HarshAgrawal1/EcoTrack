from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.contrib.auth.models import User






class Registration(models.Model):
    email=models.CharField(max_length=50)
    name=models.CharField(max_length=50)
    address=models.CharField(max_length=100)
    password=models.CharField(max_length=60,null=True,blank=True)
    work=models.CharField(max_length=50)

    points=models.IntegerField()

    
    def __str__(self):
        return self.name

class Additem(models.Model):
    email=models.CharField(max_length=50)

    type=models.CharField(max_length=100)

    quantity=models.FloatField()

    measure=models.CharField(max_length=50)
    waste_id=models.IntegerField()


    def __str__(self):
        return self.email


class OrderDetail(models.Model):
    company_email=models.CharField(max_length=50)
    user_email=models.CharField(max_length=50)

    type=models.CharField(max_length=100)

    quantity=models.FloatField()

    measure=models.CharField(max_length=50)
    waste_id=models.IntegerField()

    def __str__(self):
        return self.company_email




