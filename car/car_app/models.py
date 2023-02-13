from msilib.schema import Property
from django.db import models
from  django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
#User.admin = Property(lambda p: Admin.objects.get_or_create(user = p))


class Admin(models.Model):
    Admin_ID = models.OneToOneField(User,on_delete=models.CASCADE,primary_key= True)
    address= models.CharField(max_length=100)
    salary= models.FloatField()
    Phone_no= models.CharField(max_length=14)


class Customer(models.Model):
    Customer_ID = models.IntegerField(primary_key= True)
    Customer_Name= models.CharField(max_length=25)
    License_No = models.IntegerField()
    age = models.IntegerField()
    gender = models.CharField(max_length=1)

class Cylinder(models.Model):
    id = models.IntegerField(primary_key= True)
    no_of_cylinders = models.IntegerField()
    valves_per_cylinder = models.IntegerField()
    config = models.CharField(max_length=20)
    class Meta:
            constraints = [
                models.UniqueConstraint(fields=['valves_per_cylinder', 'config'], name='unique_host_migration2'),
            ]


class Engine(models.Model):
    Engine_ID= models.IntegerField(primary_key= True)
    cc = models.IntegerField()
    fuel_system_type = models.CharField(max_length=20)
    capacity = models.IntegerField()
    fuel_type = models.CharField(max_length=20)
    id = models.ForeignKey(Cylinder, on_delete=models.SET_NULL, null=True)

class Body(models.Model):
    Body_ID = models.IntegerField(primary_key= True)
    no_of_doors = models.IntegerField()
    boot_space = models.IntegerField()
    ground_clearance = models.IntegerField()
    body_type = models.CharField(max_length=20)


class Car(models.Model):
    Car_ID= models.IntegerField(primary_key= True)
    variant=models.CharField(max_length=10)
    Model=models.CharField(max_length=20)
    Mileage = models.FloatField()
    Make = models.CharField(max_length=20)
    kerb_weight = models.IntegerField()
    Type=models.CharField(max_length=10)
    Admin_ID =  models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    Engine_ID = models.ForeignKey(Engine, on_delete=models.SET_NULL, null=True)
    Body_ID = models.ForeignKey(Body, on_delete=models.SET_NULL, null=True)
  

class Bought_by(models.Model):
    Customer_ID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Car_ID = models.ForeignKey(Car, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Customer_ID', 'Car_ID'], name='unique_host_migration3'),
        ]


    