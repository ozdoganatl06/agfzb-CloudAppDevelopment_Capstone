from typing import ContextManager
from django.shortcuts import render

from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
# import requests
from .models import CarDealer, CarMake
from django.contrib import messages
from datetime import datetime
import logging
from . import restapis
from . import models


# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.

# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)

# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)

# Create a `registration_request` view to handle sign up request

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("/djangoapp/")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Create a `login_request` view to handle sign in request

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/djangoapp/')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)


# Create a `logout_request` view to handle sign out request

def logout_request(request):
    logout(request)
    return redirect('/djangoapp')


#
# Update the `get_dealerships` view to render the index page with a list of dealerships



def get_dealerships(request):
    if request.method == "GET":
        context={}
        url = "https://5aff4d7b.eu-gb.apigw.appdomain.cloud/api/dealership/api/dealership"
    
        context = {"dealerships": restapis.get_dealers_from_cf(url)}

        
        return render(request, 'djangoapp/index.html', context)        
      # Concat all dealer's short name
        
  


def get_dealer_details(request, dealer_id):

    context = {}
   
    print("reg",request.method)
    if request.method == "GET":
        url = "https://5aff4d7b.eu-gb.apigw.appdomain.cloud/api/review/api/review"
        # url = "https://5aff4d7b.eu-gb.apigw.appdomain.cloud/api/review/api/dealer_id?id={0}".format(dealer_id)
        reviews=restapis.get_dealer_reviews_from_cf(url, dealer_id)
        print("reviews",reviews)
        review=[]
        for rew in reviews:

            if rew["dealership"] ==int(dealer_id) or rew["dealership"] ==dealer_id:
               review.append(rew)


        context = {"reviews":  review}

        return render(request, 'djangoapp/dealer_details.html', context)



def add_review(request, dealer_id):
    context = {}
    # If it is a GET request, just render the add_review page
    if request.method == 'GET':
        
        context = {
            "dealer_id": dealer_id,
            # "dealer_name":"BMW", #restapis.get_dealers_id_from_cf(url,dealer_id)["name"],
            "cars": models.CarModel.objects.all()
        }
        
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':


        if (request.user.is_authenticated):
            review = dict()
            review["id"]=0#placeholder
            review["name"]=request.POST["name"]
            review["dealership"]=dealer_id
            review["review"]=request.POST["content"]
            if ("purchasecheck" in request.POST):
                review["purchase"]=True
            else:
                review["purchase"]=False
                # print(request.POST["car"])
            if review["purchase"] == True:
                car_parts=request.POST["car"].split("|")
                print("car parts",car_parts)
                print("car ",request.POST["car"] )
                review["purchase_date"]=request.POST["purchase_date"] 
                review["car_make"]="BMW"
                review["car_model"]=car_parts[1]
                review["car_year"]=car_parts[2]

            else:
                review["purchase_date"]=None
                review["car_make"]=None
                review["car_model"]=None
                review["car_year"]=None
 
            json_result = restapis.post_request("	https://5aff4d7b.eu-gb.apigw.appdomain.cloud/api/review/api/review_save", review, dealerId=dealer_id)
            # print(json_result)
            if "error" in json_result:
                context["message"] = "ERROR: Review was not submitted."
            else:
                context["message"] = "Review was submited"
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
