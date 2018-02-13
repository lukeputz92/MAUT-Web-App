from urllib.request import Request, urlopen
from urllib.error import URLError
import json

#This is the link for the College API used with the key
REQUEST_URL = "https://api.data.gov/ed/collegescorecard/v1/schools.json?api_key=XR0O0IAXgeNIPZKCyBnjCLODxG4MZwnpyfkOiz3g"
#State abbreviations matched with their FIPS number
STATE_CODES = {
    'WA': '53', 'DE': '10', 'DC': '11', 'WI': '55', 'WV': '54', 'HI': '15',
    'FL': '12', 'WY': '56', 'PR': '72', 'NJ': '34', 'NM': '35', 'TX': '48',
    'LA': '22', 'NC': '37', 'ND': '38', 'NE': '31', 'TN': '47', 'NY': '36',
    'PA': '42', 'AK': '02', 'NV': '32', 'NH': '33', 'VA': '51', 'CO': '08',
    'CA': '06', 'AL': '01', 'AR': '05', 'VT': '50', 'IL': '17', 'GA': '13',
    'IN': '18', 'IA': '19', 'MA': '25', 'AZ': '04', 'ID': '16', 'CT': '09',
    'ME': '23', 'MD': '24', 'OK': '40', 'OH': '39', 'UT': '49', 'MO': '29',
    'MN': '27', 'MI': '26', 'RI': '44', 'KS': '20', 'MT': '30', 'MS': '28',
    'SC': '45', 'KY': '21', 'OR': '41', 'SD': '46'
}
#API Variable name translation. Go from our variable names to the API's
APIT = {'institution_level' : 'school.institutional_characteristics.level', 'out_of_state_tuition' : '2013.cost.tuition.out_of_state',
                    'in_state_tuition' : '2013.cost.tuition.in_state', 'retention_rate' : '2013.student.retention_rate.four_year.full_time',
                    'avg_age' : '2013.student.demographics.age_entry', 'num_students' : '2013.student.size',
                    'admission_rate' : '2013.admissions.admission_rate.overall'}

class CollegeAPI:
    def __init__(self):
        self.request_filter = "&_fields=id,school.name"
        self.location_filter = ""

    def criteriaFilter(self,criteria):
        for key, value in criteria.items():
            if value[0]:
                self.request_filter += "," + APIT[key]


    '''
    Returns schools from/near a certain location.

    Depending on the filter used a different location variable type will be given.

    If filter is "ZIP" then results within 'distance' miles of the zip code 'location' will be returned
    If filter is "STATE" then results within state 'location' will be returned
    If filter is "REGION then results within state 'location' will be returned
    If filter is "NONE" then all results will be returned
    '''
    def locationFilter(self,location="NONE",distance=0,filter="NONE"):
        if filter == "ZIP":
            self.location_filter = "&_zip=" + str(location) + "&_distance=" + str(distance)
        elif filter == "STATE":
            self.location_filter = "&school.state_fips=" + STATE_CODES[location]
        elif filter == "REGION":
            self.location_filter = "&school.region_id=" + str(location)
        else:
            self.location_filter = ""

    '''
    Pulls all the schools that match the current search query
    '''
    def pull(self):
        url = REQUEST_URL + self.location_filter + self.request_filter
        request = Request(url)
        response = urlopen(request)
        json_obj = json.loads(response.read().decode('utf-8'))
        return json_obj['results']
