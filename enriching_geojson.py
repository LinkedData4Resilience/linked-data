# # https://geocoder.readthedocs.io/providers/GeoNames.html
# # enable free web service at (the bottome of the page at) https://www.geonames.org/manageaccount
import geocoder
import requests
import xmltodict
from xml.etree import ElementTree
import json

with open('output_EOR-2023-04-30.json', encoding="utf8") as f1:
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
        #print(result)
        if len(result) > 0:

            postalcode_element = result.find(".//postalcode")
            postalcode = postalcode_element.text if postalcode_element is not None else None

            location_info = {
                "postalCode": postalcode,
            }
            return location_info
    return None


i = 0
for d in data["features"]:
        
    if 'postalCode' in d:
        #if i <=5000:
            if (d['postalCode'] == None):
                #print(d['postalCode'])
                longitude,latitude = d["geometry"]["coordinates"]
                # Retrieve location information using the coordinates
                location_info = retrieve_location_info(latitude, longitude)
                if location_info is not None:
                    # Add the location information to the data
                    d.update(location_info)
                    print(i)
            i += 1


with open('output_EOR-2023-04-30.json', 'w', encoding="utf8") as f2:
    json.dump(data, f2)



