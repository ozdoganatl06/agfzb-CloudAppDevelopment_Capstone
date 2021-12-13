#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#
from cloudant.client import Cloudant
from cloudant.error import CloudantException
import requests

    


def main(dict):
    databaseName = "dealerships"
    print("Databases: ")
    print(dict["IAM_API_KEY"])
 
    
    try:
        client = Cloudant.iam(
            account_name=dict["COUCH_USERNAME"],
            # url=dict["COUCH_URL"],
            api_key=dict["IAM_API_KEY"],
            connect=True,
        )
        print("Databases: {0}".format(client.all_dbs()))
    except CloudantException as ce:
        print("unable to connect")
        print(ce)
        return {"error": ce}
    except (requests.exceptions.RequestException, ConnectionResetError) as err:
        print("connection error")
        return {"error": err}

    return {"dbs": client.all_dbs()}

if __name__ == '__main__':
    a={"COUCH_URL": "https://5aff4d7b.eu-gb.apigw.appdomain.cloud/api/dealership",
    "IAM_API_KEY": "ydVWNgFsFGSZB9i4AGqDdr-wrBawa4hDsVj5v1PSgi4J",
    "COUCH_USERNAME": "344acfc1-c258-4a55-89e7-ac8a0053bf52"}

    # API_KEY = "ydVWNgFsFGSZB9i4AGqDdr-wrBawa4hDsVj5v1PSgi4J"
    # ACCOUNT = "344acfc1-c258-4a55-89e7-ac8a0053bf52"

    main(a)
  
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