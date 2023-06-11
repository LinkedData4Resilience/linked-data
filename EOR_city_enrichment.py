import json
import requests

with open("userinfo.txt", "r") as fuser:
    username = fuser.readline().strip()

with open('datasets/original_ukrainian_geoname_uri_mappings.json', 'r') as original_ukrainian_cities:
    original_geoname_uri_mappings = json.load(original_ukrainian_cities)

with open('datasets/extended-ukrainian-geoname-uri-mappings.json', 'r', encoding='utf-8') as extended_ukrainian_cities:
    extended_geoname_uri_mappings = json.load(extended_ukrainian_cities)

    original_geoname_uri_mappings.update(extended_geoname_uri_mappings)
    geoname_uri_mappings = original_geoname_uri_mappings

with open("datasets/EOR-2023-04-30.geojson") as fjson:
    data = json.load(fjson)

# Load existing results from the file
with open("datasets/city_coordinates.json") as fresult:
    existing_results = json.load(fresult)

result = [] # Store the city data with coordinates

i = 0
for feature in data['features']:
    if feature['geometry'].get('coordinates'):
        lng, lat = feature["geometry"]["coordinates"]
        new_coordinates = [lng, lat]
        # Check if coordinates already exist in the existing results
        if any(d["coordinates"] == new_coordinates for d in existing_results):
            print('I am already there')  # Skip coordinates if already present in existing results
        else:
            if feature["properties"].get("city"):
                city_name = feature['properties']['city']
            if city_name not in geoname_uri_mappings:
                geonames_url = f'http://api.geonames.org/findNearbyPlaceNameJSON?lat={lat}&lng={lng}&username={username}'
                #request = requests.get(geonames_url)
                
                response = requests.get(geonames_url).json()
                print(response)
                if i < 200:
                    if 'name' in response['geonames'][0] and 'geonameId' in response['geonames'][0]:
                        city_name = response['geonames'][0]['name']
                        geoname_id = response['geonames'][0]['geonameId']
                        result.append({"city": city_name, "coordinates": [lng, lat], "URI": f'http://sws.geonames.org/{geoname_id}/' })
                        i += 1
                        updated_results = existing_results + result

                        # Save the result to a new JSON file
                        with open("datasets/city_coordinates.json", "w") as fresult:
                            json.dump(updated_results, fresult)
                        
        if 'city' not in feature['properties']:
                geonames_url = f'http://api.geonames.org/findNearbyPlaceNameJSON?lat={lat}&lng={lng}&username={username}'
                #request = requests.get(geonames_url)
                
                response = requests.get(geonames_url).json()
                print(response)
                if i < 200:
                    if 'name' in response['geonames'][0] and 'geonameId' in response['geonames'][0]:
                        city_name = response['geonames'][0]['name']
                        geoname_id = response['geonames'][0]['geonameId']
                        result.append({"city": city_name, "coordinates": [lng, lat], "URI": f'http://sws.geonames.org/{geoname_id}/' })
                        i += 1
                        updated_results = existing_results + result

                        # Save the result to a new JSON file
                        with open("datasets/city_coordinates.json", "w") as fresult:
                            json.dump(updated_results, fresult)


