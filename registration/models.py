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

    def __str__(self):
        return self.name
