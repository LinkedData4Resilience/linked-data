# # https://geocoder.readthedocs.io/providers/GeoNames.html
# # enable free web service at (the bottome of the page at) https://www.geonames.org/manageaccount
import geocoder
import requests
import xmltodict
from xml.etree import ElementTree
import json


with open('output_ukr-civharm-2023-04-30(500-100).json', encoding="utf8") as f1:
    data = json.load(f1)

username = None

with open("userinfo.txt","r") as f:
    username = f.readline().strip()

geonames_base_url = "http://api.geonames.org/"
geonames_function = "findNearbyPostalCodes?"
def retrieve_location_info(lat, lng):
    
    api_url = geonames_base_url + geonames_function + 'lat=' + str(lat) + '&lng=' + str(lng) + '&username=' + username
    response = requests.get(api_url)
    if response.status_code == 200:
        result = ElementTree.fromstring(response.content)
        print(result)
        if len(result) > 0:
            place_name_element = result.find(".//placeName")
            place_name = place_name_element.text if place_name_element is not None else None

            postalcode_element = result.find(".//postalcode")
            postalcode = postalcode_element.text if postalcode_element is not None else None

            adminName1_element = result.find(".//adminName1")
            adminName1 = adminName1_element.text if adminName1_element is not None else None

            location_info = {
                "countryCode": place_name,
                "postalCode": postalcode,
                "region": adminName1
            }
            return location_info
    return None


i = 0
for d in data:
        
            if "latitude" in d and "longitude" in d:
                # Retrieve location information using the coordinates
                location_info = retrieve_location_info(d["latitude"], d["longitude"])
                if location_info is not None:
                    # Add the location information to the data
                    d.update(location_info)



with open('output_ukr-civharm-2023-04-30(900-1100).json', 'w', encoding="utf8") as f2:
    json.dump(data, f2)
