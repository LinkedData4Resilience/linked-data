




import json
import requests
with open("userinfo.txt","r") as fuser:
    username = fuser.readline().strip()


with open('datasets/original_ukrainian_geoname_uri_mappings.json', 'r') as original_ukrainian_cities:
    original_geoname_uri_mappings = json.load(original_ukrainian_cities)
    with open('datasets/extended-ukrainian-geoname-uri-mappings.json', 'r') as extended_ukrainian_cities:
        extended_geoname_uri_mappings = json.load(extended_ukrainian_cities)

        original_geoname_uri_mappings.update(extended_geoname_uri_mappings)
        geoname_uri_mappings = original_geoname_uri_mappings
    with open("datasets/EOR-2023-04-30-enriched.geojson") as fjson:
        data = json.load(fjson) 

    i = 0    
    for feature in data['features']:

        if feature['geometry'].get('coordinates'):
            
            lng, lat = feature["geometry"]["coordinates"]
            # print ('\t lng: ', lng)
            # print ('\t lat: ', lat)
        if feature["properties"].get("city"):
            
            city_name = feature['properties']['city']
            if city_name in geoname_uri_mappings:
                geonames_url = f'http://api.geonames.org/findNearbyPlaceNameJSON?lat={lat}&lng={lng}&username={username}'
                
                response = requests.get(geonames_url).json()
                request = requests.get(geonames_url)
                if request.ok == True:
                    print(response)
                    if 'name' in response['geonames'][0]:
                        feature['properties']['city'] = response['geonames'][0]['name']
                        print(response['geonames'][0]['name'])
                        i += 1
                        print(i)
                

                
fjson.write(json.dumps(data))
                