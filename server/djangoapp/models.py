from django.db import models
import sys
from django.utils.timezone import now
try:
    from django.db import models
except Exception:
    print("There was an error loading django modules. Do you have django installed?")
    sys.exit()

from django.conf import settings
import uuid


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
# Lesson model
class CarMake(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, default="name")
    description =models.CharField(max_length=20, default="description")


    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description
  
class CarModel(models.Model):
    modelle = models.CharField(max_length=200, default="modelle")
    modelle = models.ManyToManyField(CarMake)
    modelle = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    dealer_id= models.AutoField(primary_key=True)
    name =models.CharField(max_length=20, default="name")
 
    
    RED = 'Red'
    BLUE = 'Blue'
    YELLOW = 'Yellow'
    WHITE= 'White'
    BLACK= 'Black'
    COLOR_CHOICES = [
        (RED, 'Red'),
        (BLUE, 'Blue'),
        (YELLOW, 'Yellow'),
        (WHITE,'White'),
        (BLACK,'Black')
        ]
    color = models.CharField(max_length=6, choices=COLOR_CHOICES, default=WHITE)
    year =  models.DateField()

    SUV = 'Suv'
    SEDAN = 'Sedan'
    WAGON = 'Wagon'
    TYPE_CHOICES = [
        (RED, 'Suv'),
        (BLUE, 'Sedan'),
        (YELLOW, 'wagon')
    ]
    type = models.CharField(max_length=6, choices=TYPE_CHOICES, default=SUV)

    def __str__(self):
        return "Name: " + self.name 

# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object


# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
