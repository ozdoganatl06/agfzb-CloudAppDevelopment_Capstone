import requests
import json
import logging
# import related models here
from requests.auth import HTTPBasicAuth
from . import models
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from ibm_watson.natural_language_understanding_v1 import Features, SentimentOptions,RelationsOptions


# Create a `get_request` to make HTTP GET requests
# e.g., response = requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))

# requests.get(url, params=params, headers={'Content-Type': 'application/json'},
#                                     auth=HTTPBasicAuth('apikey', api_key))
def get_request(url, **kwargs):
    #print(kwargs)
    print("GET from {} ".format(url))
    json_data={}
    try:
        if "apikey" in kwargs:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs, 
                       auth=HTTPBasicAuth("apikey", kwargs["apikey"]))
        else:
            response = requests.get(url, headers={'Content-Type':'application/json'}, params=kwargs)

        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.content)
        # service.get_all_dbs().get_result()
       
    except Exception as e:
        print("Error " ,e)
    
    return json_data



def post_request(url, json_payload, **kwargs):

    print("PAYLOAD", json_payload)
    try:
        response = requests.post(url, json=json_payload, params=kwargs)
        
    except Exception as e:
        print("Error" ,e)
    print("Status Code ", {response.status_code})
    data = json.loads(response.text)
    return data



# # # Create a get_dealers_from_cf method to get dealers from a cloud function
# # def get_dealers_from_cf(url, **kwargs):
# # - Call get_request() with specified arguments
# # - Parse JSON results into a CarDealer object list
def get_dealers_from_cf(url):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url)
    # print(json_result)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["rows"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = models.CarDealer(
                            address=dealer_doc["address"], 
                            city=dealer_doc["city"], 
                            full_name=dealer_doc["full_name"],
                            id=dealer_doc["id"], 
                            lat=dealer_doc["lat"], 
                            long=dealer_doc["long"],
                            short_name=dealer_doc["short_name"],
                            st=dealer_doc["st"], 
                            zip=dealer_doc["zip"],
                            id_=dealer_doc["_id"]
                            )
            results.append(dealer_obj)

    return results




# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
# def get_dealer_by_id_from_cf(url, dealerId):
# - Call get_request() with specified arguments
# - Parse JSON results into a DealerView object list
# Create a get_dealer_reviews_from_cf method to get reviews by dealer id from a cloud function
def get_dealers_id_from_cf(url, dealerId):
                  
    return get_request(url, dealerId=dealerId)

def get_dealer_reviews_from_cf(url, dealerId):
        results = []
        json_result = get_request(url, dealerId=dealerId)
        # print("json",json_result)
        dealers = json_result["rows"]

        try:
            for dealer in dealers:
                    # Get its content in `doc` object
                    dealer_doc = dealer["doc"]

                    review_obj =dealer_doc
                        
                        # models.DealerReview(
                        #                     id              = dealer_doc["id"], 
                        #                     name            = dealer_doc["name"], 
                        #                     dealership      = dealer_doc["dealership"], 
                        #                     review          = dealer_doc["review"], 
                        #                     purchase        = dealer_doc["purchase"],
                        #                     purchase_date   = dealer_doc["purchase_date"], 
                        #                     car_make        = dealer_doc['car_make'],
                        #                     car_model       = dealer_doc['car_model'], 
                        #                     car_year        = dealer_doc['car_year']
                                            
                                            # )
                       
                                      
                    review_obj["sentiment"]=analyze_review_sentiments(dealer_doc["review"])
                    results.append(review_obj)

        except:
            # print("hata 2")
            return results


        return results

def analyze_review_sentiments(texttoanalyze):
    print("geldi",texttoanalyze)
    api_key ="uj_r5rP5LeKqVQhtll2tzJOPFxSadY7ox9knj-Tf0e8j"
    url     ="https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/76036435-5a43-4136-91e2-6214909651b1"
    version = '2021-08-01'
    authenticator = IAMAuthenticator(api_key)
    # authenticator = IAMAuthenticator( api_key)
    
    natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2021-08-01',
    authenticator=authenticator
    )

    natural_language_understanding.set_service_url(url)
    try :
        response = natural_language_understanding.analyze(
            text=str(texttoanalyze),
        features=Features(relations=RelationsOptions())).get_result()

        # response = natural_language_understanding.analyze(
        # url=str(texttoanalyze),
        # features=Features(sentiment=SentimentOptions(targets=['bonds']))).get_result()

    except:
        # print("hata")
        return "neutral"
    

    # print(json.dumps(response, indent=2)["reations"])  
    # sentiment_score = str(response["sentiment"]["document"]["score"])
    # sentiment_label = response["sentiment"]["document"]["label"]
    # print(sentiment_score)
    # print(sentiment_label)
    # sentimentresult = sentiment_label
    
    return "neutral"


