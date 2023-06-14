from bs4 import BeautifulSoup
from rdflib import FOAF, RDFS, Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import XSD, RDFS, RDF
import json
from datetime import datetime
import urllib.parse
import requests
import validators
import requests

from rdflib.namespace import NamespaceManager


# username for GeoNames
fuser = open("userinfo.txt","r")
username = fuser.readline().strip()

with open("datasets/city_coordinates.json") as fresult:
    existing_results = json.load(fresult)

# Define the GeoNames API URL and username
GEONAMES_API_URL = 'http://api.geonames.org/searchJSON'
GEONAMES_USERNAME = username
# Define namespaces
# Registratie: linked4resilience.eu
l4r_eor_namespace_event = Namespace("https://linked4resilience.eu/data/EOR/April2023/event/")
l4r_eor_namespace_location = Namespace("https://linked4resilience.eu/data/EOR/April2023/location/")
l4r_eor_namespace_geo = Namespace("https://linked4resilience.eu/data/EOR/April2023/geo/")
l4r_o_namespace = Namespace("https://linked4resilience.eu/ontology/")


sem_namespace = Namespace("http://semanticweb.cs.vu.nl/2009/11/sem/")

gno_namespace = Namespace('http://www.geonames.org/ontology#')
gni_namespace = Namespace ('https://sws.geonames.org/')


sdo_namespace = Namespace("https://schema.org/")

# Create an RDF graph
rdf_graph = Graph()

# Bind namespaces
# Appraoch 1
rdf_graph.bind("l4revent", l4r_eor_namespace_event)
rdf_graph.bind("l4rlocation", l4r_eor_namespace_location)
rdf_graph.bind("l4rgeo", l4r_eor_namespace_geo)
rdf_graph.bind("l4ro", l4r_o_namespace)

rdf_graph.bind("xsd", XSD)
rdf_graph.bind('gno', gno_namespace)
rdf_graph.bind('gni', gni_namespace)
rdf_graph.bind('sem', sem_namespace)
rdf_graph.bind('sdo', sdo_namespace)
rdf_graph.bind('rdfs', RDFS)

# Appraoch 2
# namespace_manager = NamespaceManager(rdf_graph)
# namespace_manager.bind("l4r", l4r_eor_namespace_event, override=False)
# namespace_manager.bind("l4ro", l4r_o_namespace, override=False)
# namespace_manager.bind("xsd", XSD, override=False)
# namespace_manager.bind('gno', gno_namespace, override=False)
# namespace_manager.bind('gni', gni_namespace, override=False)
# namespace_manager.bind('sem', sem_namespace, override=False)
# namespace_manager.bind('sdo', sdo_namespace, override=False)
# namespace_manager.bind('rdfs', RDFS, override=False)
# rdf_graph.namespace_manager = namespace_manager



num_entry = 0
num_vio = 0
num_date = 0
num_label = 0
num_postalCode = 0
num_country = 0
num_coordinates = 0

num_prov = 0
# cities
num_city = 0
num_cities_original_EoR = 0
cities_not_found = set()
# social media content
num_url = 0
num_validated_url = 0
num_broken_url_link = 0


event_id = 1
location_id = 1
geo_id = 1


with open('datasets/original_ukrainian_geoname_uri_mappings.json', 'r') as original_ukrainian_cities:
    original_geoname_uri_mappings = json.load(original_ukrainian_cities)
    with open('datasets/extended-ukrainian-geoname-uri-mappings.json', 'r', encoding='utf-8') as extended_ukrainian_cities:
        extended_geoname_uri_mappings = json.load(extended_ukrainian_cities)

        original_geoname_uri_mappings.update(extended_geoname_uri_mappings)
        geoname_uri_mappings = original_geoname_uri_mappings

    # Open the JSON file
    with open("datasets\enriched_original_EOR-2023-04-30.json") as fjson:
        data = json.load(fjson)

        # Initialize an event ID counter


        # Loop through the features in the JSON file
        for feature in data['features']:
            # print ('event id ', event_id)

            # Create a URI for the event using the event ID
            if feature["properties"].get("country") == "Ukraine":

                num_entry +=1
                event_URI = l4r_eor_namespace_event + str(event_id).zfill(8)
                comment_in_preparation = ''
                # print ('this event has URI: ', event_URI)
                # print ('event id = ', event_id)

                #
                if feature['properties'].get('verifiedDate'):

                    verified_date_str = feature['properties']['verifiedDate']
                    verified_date_obj = datetime.fromisoformat(verified_date_str)
                    verified_date_str_no_time = verified_date_obj.date().isoformat()
                    # print ('\tverified date: ', verified_date_str)
                    # print ('\tverified obj: ', verified_date_obj)
                    # print ('\tdate of event: ', verified_date_str_no_time)

                    rdf_graph.add((URIRef(event_URI), URIRef('http://purl.org/dc/terms/date'), Literal(verified_date_str_no_time, datatype=XSD.date)))
                    num_date += 1

                if feature['geometry'].get('coordinates'):
                    num_coordinates += 1
                    lng, lat = feature["geometry"]["coordinates"]
                    # print ('\t lng: ', lng)
                    # print ('\t lat: ', lat)

                    # event schema:location L
                    location_URI = l4r_eor_namespace_location + str(location_id).zfill(8)
                    location_id += 1
                    rdf_graph.add((URIRef(event_URI), sdo_namespace.location, URIRef(location_URI))) # updated from lat

                    geo_URI = l4r_eor_namespace_geo + str(geo_id).zfill(8)
                    geo_id += 1
                    rdf_graph.add((URIRef(location_URI), RDF.type, sdo_namespace.Place)) #
                    rdf_graph.add((URIRef(location_URI), sdo_namespace.geo, URIRef(geo_URI))) #

                    rdf_graph.add((URIRef(geo_URI), RDF.type, sdo_namespace.GeoCoordinates)) #

                    rdf_graph.add((URIRef(geo_URI), sdo_namespace.latitude, Literal(lat, datatype=XSD.float))) # updated from lat
                    # print ('\tlat', Literal(lat, datatype=XSD.float))

                    rdf_graph.add((URIRef(geo_URI), sdo_namespace.longitude, Literal(lng, datatype=XSD.float))) # updated from lng


                    # rdf_graph.add((URIRef(event_URI), sdo_namespace.latitude, Literal(lat, datatype=XSD.float))) # updated from lat
                    # # print ('\tlat', Literal(lat, datatype=XSD.float))

                    # rdf_graph.add((URIRef(event_URI), sdo_namespace.longitude, Literal(lng, datatype=XSD.float))) # updated from lng
                    # # print ('\tlng', Literal(lng, datatype=XSD.float))


                if feature["properties"].get("violenceLevel"):
                    # rdf_graph.add((URIRef(event_URI), l4r_o_namespace.hasViolenceLevel, Literal(feature['properties']['violenceLevel'], datatype=XSD.integer))) # nonNegativeInteger
                    # print ('\thasViolenceLevel: ', Literal(feature['properties']['violenceLevel'], datatype=XSD.integer)) # nonNegativeInteger
                    comment_in_preparation += 'Editors of the Eyes on Russia project assigned a violence level to this event as ' + str(feature['properties']['violenceLevel']) + '. '
                    num_vio += 1

                if feature["properties"].get("description"):
                    rdf_graph.add((URIRef(event_URI), RDFS.label, Literal(feature["properties"]['description'], lang="en")))
                    # print ('\thas rdfs:label: ', Literal(feature["properties"]['description']))
                    num_label += 1
                else:
                    rdf_graph.add((URIRef(event_URI), RDFS.label, Literal('no description', lang="en")))

                if feature.get("postalCode"):
                    rdf_graph.add((URIRef(event_URI), sdo_namespace.postalCode, Literal(feature['postalCode'])))
                    #print ('\thas postalcode: ', Literal(feature['postalCode']))
                    num_postalCode +=1

                if 'postalCode' not in feature:
                    geonames_url = f'http://api.geonames.org/findNearbyPostalCodesJSON?lat=47&lng=9&username={username}'
                    response = requests.get(geonames_url).json()
                    
                    if 'postalCode' in response['postalCodes'][0]:
                        postalCode = response['postalCodes'][0]['postalCode']
                        rdf_graph.add((URIRef(event_URI), sdo_namespace.postalCode, Literal(postalCode)))
                        num_postalCode +=1
                    # if 'totalResultsCount' in response and response['totalResultsCount'] > 0:
                    #     geoname_id = response['geonames'][0]['geonameId']
                    #     city_uri = URIRef(f'http://sws.geonames.org/{geoname_id}/')
                    #     print('hi')
                    #     geoname_uri_mappings[city_name] = str(city_uri)
                    #     rdf_graph.add((URIRef(event_URI), sdo_namespace.addressLocality, city_uri))
                    #     print ('the city URI ', city_uri)


                if feature["properties"].get("country"):
                    country_name = feature['properties']['country']
                    # print ('\tcountry: ', country_name)
                    if country_name in geoname_uri_mappings:
                        country_uri = URIRef(geoname_uri_mappings[country_name])
                        rdf_graph.add((URIRef(event_URI), l4r_o_namespace.addressCountry, country_uri))
                        # print ('\tCountry URI: ', country_uri)
                        num_country += 1
                    else:
                        rdf_graph.add((URIRef(event_URI), l4r_o_namespace.addressCountry, Literal(feature["properties"]["country"])))
                        print ('ERROR: the URI is not in the saved Geonames mapping: ', country_name)
                        print ('this event has URI: ', event_URI)

                if feature["properties"].get("province"):
                    prov_name = feature['properties']['province']
                    if prov_name in geoname_uri_mappings:
                        prov_uri = URIRef(geoname_uri_mappings[prov_name])
                        rdf_graph.add((URIRef(event_URI), l4r_o_namespace.addressRegion, prov_uri))
                        # print ('\tProvince URI: ', prov_uri)
                        num_prov += 1
                    else:
                        rdf_graph.add((URIRef(event_URI), l4r_o_namespace.addressRegion, Literal(feature["properties"]["province"])))
                        print ('ERROR: the URI is not in the saved Geonames mapping: ', prov_name)
                        print ('this event has URI: ', event_URI)

                if feature["properties"].get("city"):
                    num_cities_original_EoR += 1
                    city_name = feature['properties']['city']
                    if city_name in geoname_uri_mappings:
                        city_uri = URIRef(geoname_uri_mappings[city_name])
                        rdf_graph.add((URIRef(event_URI), l4r_o_namespace.addressCity, city_uri))
                        
                        num_city += 1
                    else:
                        for c in existing_results:

                            if feature["geometry"]["coordinates"] == c['coordinates']:
                                city_uri = URIRef(c['URI'])
                                rdf_graph.add((URIRef(event_URI), l4r_o_namespace.addressCity, city_uri))
                                
                                num_city += 1
                                break
                        # geonames_url = f'http://api.geonames.org/searchJSON?q={city_name}&maxRows=1&username={username}'
                        # response = requests.get(geonames_url).json()
                        # if 'totalResultsCount' in response and response['totalResultsCount'] > 0:
                        #     geoname_id = response['geonames'][0]['geonameId']
                        #     city_uri = URIRef(f'http://sws.geonames.org/{geoname_id}/')
                        #     print('hi')
                        #     geoname_uri_mappings[city_name] = str(city_uri)
                        #     rdf_graph.add((URIRef(event_URI), sdo_namespace.addressLocality, city_uri))
                        #     print ('the city URI ', city_uri)
                        # else:
                        # print ('Failed to find the city: ', city_name)
                            # else:  
                            #     cities_not_found.add(city_name)
                            #     comment_in_preparation += 'According to Eyes on Russia, this event happened in '+ city_name +'. '
                        # city_uri = Literal(city_name)

                if 'city' not in feature["properties"]: 
                    for c in existing_results:

                            if feature["geometry"]["coordinates"] == c['coordinates']:
                                city_uri = URIRef(c['URI'])
                                rdf_graph.add((URIRef(event_URI), l4r_o_namespace.addressCity, city_uri))
                                
                                num_city += 1
                                break
                                
                for category in feature['properties']['categories']:
                    # Eyes on Russia provides some extra information as the category of the event. We decide to keep this in the comment
                    comment_in_preparation += 'According to Eyes on Russia, this event is of type '+ category +'. '
                    # print ('comment: ', comment_in_preparation + 'The type of event could be ' +category)

                if feature['properties'].get('url'):
                    social_media_content_url = feature["properties"]['url']
                    rdf_graph.add((URIRef(event_URI), sdo_namespace.url, Literal(social_media_content_url, datatype=XSD.anyURI)))
                    num_url += 1

                        
                        #         num_validated_url +=1
                        # TODO:
                    try:
                        x = requests.get(social_media_content_url)
                        if int(x.status_code >= 200 and x.status_code <= 299):
                            num_validated_url +=1
                            print(x.status_code)
                        else:
                            print(social_media_content_url)
                            print(x.status_code)
                    except Exception as e:
                        print (e)

                rdf_graph.add((URIRef(event_URI), RDF.type, sem_namespace.Event))
                if comment_in_preparation != '':
                    rdf_graph.add((URIRef(event_URI), RDFS.comment, Literal(comment_in_preparation, lang="en")))

                event_id += 1

print ('#Entry ', num_entry)
print ('#violence level ', num_vio)
print ('#rdfs:label ', num_label)
print ('#postalCode ', num_postalCode)
print ('#country', num_country)
print ('#date ', num_date)
print ('#coordinates ', num_coordinates)
print ('#province ', num_prov)
print ('num_cities_original_EoR ', num_cities_original_EoR)
print ('#city (found in Geonames)', num_city)
print ('#(unique) cities not found ', len(cities_not_found))
# for r in cities_not_found:
#      print (r)
print ('count URL: ', num_url)
print ('valid URL: ', num_url)
sorted_triples = sorted(rdf_graph, key=lambda triple: triple[0])
sorted_graph = Graph()
sorted_graph += sorted_triples

# serialize the sorted graph to a string in RDF/XML format
serialized = sorted_graph.serialize(format="ttl")
with open("converted_EOR-2023-04-30.ttl", "wb") as f:
        f.write(serialized.encode('utf-8'))




# with open("output_EOR-2023-04-30.ttl", 'r', encoding="utf8") as foutput:
#     ttl = foutput.read()

# ttl = ttl.replace('ns1:', 'schema:').replace('ns2:', 'sem:').replace('rdf-schema#', 'rdfs:')
#
# with open("output_EOR-2023-04-30.ttl", 'w',encoding="utf8") as foutput:
#     foutput.write(ttl)
