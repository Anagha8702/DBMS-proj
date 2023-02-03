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
            models.UniqueConstraint(fields=['Customer_ID', 'Customer_Review'], name='unique_host_migration'),
        ]

class Car(models.Model):
    Car_ID= models.IntegerField(primary_key= True)


    




