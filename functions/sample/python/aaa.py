# {
#   "apikey": "ydVWNgFsFGSZB9i4AGqDdr-wrBawa4hDsVj5v1PSgi4J",
#   "host": "344acfc1-c258-4a55-89e7-ac8a0053bf52-bluemix.cloudantnosqldb.appdomain.cloud",
#   "iam_apikey_description": "Auto-generated for key c1973931-12f4-41f0-9ff4-6ea173bd9093",
#   "iam_apikey_name": "Service credentials-1",
#   "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
#   "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/43f8179a69304810bb916e8113e313f0::serviceid:ServiceId-059fd6c6-9225-458c-a628-f96d6483ebc6",
#   "password": "946c31c00a2625fe2fac8ecbd4805245",
#   "port": 443,
#   "url": "https://apikey-v2-73krvc8err7vghn84lgsdx8j5k61zrqpyf4cht5upoi:946c31c00a2625fe2fac8ecbd4805245@344acfc1-c258-4a55-89e7-ac8a0053bf52-bluemix.cloudantnosqldb.appdomain.cloud",
#   "username": "apikey-v2-73krvc8err7vghn84lgsdx8j5k61zrqpyf4cht5upoi"
# }
{
  "apikey": "ydVWNgFsFGSZB9i4AGqDdr-wrBawa4hDsVj5v1PSgi4J",
  "host": "344acfc1-c258-4a55-89e7-ac8a0053bf52-bluemix.cloudantnosqldb.appdomain.cloud",
  "iam_apikey_description": "Auto-generated for key c1973931-12f4-41f0-9ff4-6ea173bd9093",
  "iam_apikey_name": "Service credentials-1",
  "iam_role_crn": "crn:v1:bluemix:public:iam::::serviceRole:Manager",
  "iam_serviceid_crn": "crn:v1:bluemix:public:iam-identity::a/43f8179a69304810bb916e8113e313f0::serviceid:ServiceId-059fd6c6-9225-458c-a628-f96d6483ebc6",
  "password": "946c31c00a2625fe2fac8ecbd4805245",
  "port": 443,
  "url": "https://apikey-v2-73krvc8err7vghn84lgsdx8j5k61zrqpyf4cht5upoi:946c31c00a2625fe2fac8ecbd4805245@344acfc1-c258-4a55-89e7-ac8a0053bf52-bluemix.cloudantnosqldb.appdomain.cloud",
  "username": "apikey-v2-73krvc8err7vghn84lgsdx8j5k61zrqpyf4cht5upoi"
}

import time

import requests

API_KEY = "ydVWNgFsFGSZB9i4AGqDdr-wrBawa4hDsVj5v1PSgi4J"
ACCOUNT = "344acfc1-c258-4a55-89e7-ac8a0053bf52"

def get_access_token(api_key):
    """Retrieve an access token from the IAM token service."""
    token_response = requests.post(
        "https://iam.cloud.ibm.com/identity/token",
        data={
            "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
            "response_type": "cloud_iam",
            "apikey": api_key
        },
        headers={
            "Accept": "application/json"
        }
    )
    if token_response.status_code == 200:
        print ("Got access token from IAM")
        return token_response.json()['access_token']
    else:
        # print( token_response.status_code, token_response.json())
        return None

def main(api_key, account):
    access_token = None
    while True:
        if not access_token:
            access_token = get_access_token(api_key)
            print(1)
            print(access_token)
        if access_token:
            response = requests.get(
                "https://{0}.cloudant.com/_all_dbs".format(account),
                headers={
                    "Accept": "application/json",
                    "Authorization": "Bearer {0}".format(access_token)
                }
            )
            print ("Got Cloudant response, status code", response.status_code)
            if response.status_code == 401:
                print ("Token has expired.")
                access_token = None

        time.sleep(1)

if __name__ == "__main__":
    main(API_KEY, ACCOUNT)