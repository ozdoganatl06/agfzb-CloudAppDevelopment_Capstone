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

    name = models.CharField(max_length=20, default="name")
    description =models.CharField(max_length=20, default="description")


    def __str__(self):
        return "Name: " + self.name + "," + \
               "Description: " + self.description
  
class CarModel(models.Model):


    
    carmake = models.ForeignKey(CarMake, null= True, on_delete=models.CASCADE)
    name = models.CharField(null= False, max_length=30, default='Audi X8')
 
  
    year = models.DateField(null= True)
    dealer_id= models.AutoField(primary_key=True)
  
 
    
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
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip,id_):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        
        self.id_ = id_

        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    
    def __init__(self,dealership,name,purchase,review,purchase_date,car_make,car_model,car_year,sentiment,id,id_):
        # Dealer address
        self.dealership = dealership
        # Dealer city
        self.purchase = purchase
        # Dealer Full Name
        self.review = review
        # Dealer id
        self.id = id
        # Location lat
        self.purchase_date = purchase_date
        # Location long
        self.name = name
        # Dealer state
        self.car_make = car_make
        # Dealer zip
        self.car_model = car_model
        # Dealer state
        self.car_year = car_year
        # Dealer zip
        self.sentiment = sentiment
        self.id_ = id_

    def __str__(self):
        return "Dealer dealership: " + self.dealership