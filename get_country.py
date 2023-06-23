import json
import pandas as pd
import io
from geopy.geocoders import Nominatim
import requests




def get_country_name(latitude, longitude):
    url = f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}"
    response = requests.get(url)
    data = response.json()
    # print(response)
    if 'address' in data:
        if 'country' in data['address']:
            country_name = data['address']['country']
            # print(country_name)
            return country_name

    return None

with open("datasets\enriched_original_EOR-2023-04-30.json", encoding="utf-8") as f:
        data = json.load(f)
        i = 0
        for feature in data['features']:
            if feature['geometry'].get('coordinates'):        
                longitude, latitude = feature["geometry"]["coordinates"]
                country = get_country_name(latitude, longitude)
                
                if country == 'Україна': 
                    i +=1 
                    print(i)
        print(i)

# with open("datasets/enriched_original_ukr-civharm-2023-04-30.json", encoding="utf-8") as f:
#         data = json.load(f)
#         i = 0
#         for d in data:
#             latitude = d['latitude']
#             longitude = d['longitude']
#             country = get_country_name(latitude, longitude)
#             if country == 'Україна': 
#                 i +=1 
#         print(i)