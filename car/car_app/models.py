from django.db import models

# Create your models here.
class Admin(models.Model):
    Admin_ID = models.IntegerField(primary_key= True)
    Admin_Name= models.CharField(max_length=25)
    address= models.CharField(max_length=100)
    salary= models.FloatField()
    Phone_no= models.CharField(max_length=14)

class Customer(models.Model):
    Customer_ID = models.IntegerField(primary_key= True)
    Customer_Name= models.CharField(max_length=25)
    License_No = models.IntegerField()

class Customer_Review(models.Model):
    Customer_Review= models.CharField(max_length=100)
    Customer_ID = models.ForeignKey(Customer, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['Customer_ID', 'Customer_Review'], name='unique_host_migration1'),
        ]

class Engine(models.Model):
    Engine_ID= models.IntegerField(primary_key= True)
    cc = models.IntegerField()
    fuel_system_type = models.CharField(max_length=20)
    capacity = models.IntegerField()
    fuel_type = models.CharField(max_length=20)

class Car(models.Model):
    Car_ID= models.IntegerField(primary_key= True)
    variant=models.CharField(max_length=10)
    Model=models.CharField(max_length=20)
    Mileage = models.FloatField()
    Make = models.CharField(max_length=20)
    kerb_weight = models.IntegerField()
    Type=models.CharField(max_length=10)
    Admin_ID = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    Engine_ID = models.ForeignKey(Engine, on_delete=models.SET_NULL, null=True)
  
class Cylinder(models.Model):
    no_of_cylinders = models.IntegerField()
    valves_per_cylinder = models.IntegerField()
    config = models.CharField(max_length=20)
    class Meta:
            constraints = [
                models.UniqueConstraint(fields=['valves_per_cylinder', 'config'], name='unique_host_migration2'),
            ]

class Bought_by(models.Model):
    Customer_ID = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Car_ID = models.ForeignKey(Car, on_delete=models.CASCADE)

class Body(models.Model):
    Body_ID = models.IntegerField(primary_key= True)
    no_of_doors = models.IntegerField()
    boot_space = models.IntegerField()
    ground_clearance = models.IntegerField()
    body_type = models.CharField(max_length=20)