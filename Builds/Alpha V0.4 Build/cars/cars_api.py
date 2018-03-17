import requests
from urllib.request import Request, urlopen
from urllib.error import URLError
import json


'''
APIT is a list that stores a list of all the criteria options.
Each criteria option is represented as a dictionary with the following information
{
'name' : User-friendly string with name of the criteria
'api_variable' : String containing the info that needs to be appended to the query to get that criteria info
'units' : String saying how that criteria is measured (for example tuition would be dollars, distance would be miles/inches/etc)
'is_num' : Bool saying whether the criteria is measured as a number. Used to see if automatic scoring is possible.
'needs_table' : Bool saying whether or not the information in the database is the actual information
                or represents different information. For example a criteria representing the institutions level
                (whether it is a 2 year school, 4 year, etc) might store the information as 1 for 2 year, 2 for 4 year,
                and 3 as other. Because of this you might need a table hardcoded here to translate the 1 to 2 year and 2
                to 4 year and 3 to other.
'table' : Dictionary mapping the criteria's database value to its actual value. Only used if needs_table is true
}
FOR COPY AND PASTE:
    {
    "name" : ,
    "api_variable" : ,
    "units" : ,
    "is_num" : ,
    "needs_table" : ,

    },
'''

APIT = [
    {
    "name" : "Year" ,
    "api_variable" : "year" ,
    "units" : "",
    "is_num" : True,
    "needs_table" : False,
    },
    {
    "name" : "Make",
    "api_variable" : "make",
    "units" : "",
    "is_num" : False,
    "needs_table" : False,
    },
    {
    "name" : "Model",
    "api_variable" : "model",
    "units" : "",
    "is_num" : False,
    "needs_table" : False,
    },
    {
    "name" : "Body Type" ,
    "api_variable" : " body_type" ,
    "units" : "",
    "is_num" : False,
    "needs_table" : False,

    },
    {
    "name" : "Transmission",
    "api_variable" : "transmission",
    "units" : "",
    "is_num" : False,
    "needs_table" : False,

    },
    {
    "name" : "Drivetrain",
    "api_variable" : "drivetrain",
    "units" : "",
    "is_num" : False,
    "needs_table" : False,

    },
    {
    "name" : "Engine",
    "api_variable" : "engine",
    "units" : "",
    "is_num" : False,
    "needs_table" : False,

    },
]


URL = "http://api.marketcheck.com/v1/search"

HEADERS = {'Host': 'marketcheck-prod.apigee.net'}

class CarsAPI:
    def __init__(self):
        self.params = [("api_key", "ArUGlu0Tj3lCqM0JJd2caRPwsobJde6U"), ("radius", "100"), ]

    def locationFilter(self,zipcode):
        google_api = "https://maps.googleapis.com/maps/api/geocode/json?key=AIzaSyC-enO3ECdoTTn5_L6p2q8CgKELVIhySm8&address="
        search = google_api + str(zipcode)
        request = Request(search)
        response = urlopen(request)
        json_obj = json.loads(response.read().decode('utf-8'))
        location = json_obj['results'][0]['geometry']['location']
        self.params += [
                    ('lat', str(location['lat'])),
                    ('lon', str(location['lng'])),
                ]

    def pull(self):
        response = requests.get(URL,headers=HEADERS,params=self.params)
        json_obj = response.json()
        return json_obj['']
