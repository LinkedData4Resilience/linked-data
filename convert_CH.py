# This file is used to convert the structered data of Civilian Harm dataset to linked data

from rdflib import FOAF, RDFS, Graph, Literal, Namespace, RDF, URIRef
import rdflib
from rdflib.namespace import XSD
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import validators


# Define namespaces
l4r_ch_namespace_event = Namespace("https://linked4resilience.eu/data/CH/April2023/event/")
l4r_o_namespace = Namespace("https://linked4resilience.eu/ontology/")
l4r_ch_namespace_location = Namespace("https://linked4resilience.eu/data/CH/April2023/location/")
l4r_ch_namespace_geo = Namespace("https://linked4resilience.eu/data/CH/April2023/geo/")

sem_namespace = Namespace("http://semanticweb.cs.vu.nl/2009/11/sem/")

gno_namespace = Namespace('http://www.geonames.org/ontology#')
gni_namespace = Namespace ('https://sws.geonames.org/')


sdo_namespace = Namespace("https://schema.org/")

# Create an RDF graph
rdf_graph = Graph()
# Bind namespaces
# Appraoch 1
rdf_graph.bind("l4r", l4r_ch_namespace_event)
rdf_graph.bind("l4ro", l4r_o_namespace)
rdf_graph.bind("xsd", XSD)
rdf_graph.bind('gno', gno_namespace)
rdf_graph.bind('gni', gni_namespace)
rdf_graph.bind('sem', sem_namespace)
rdf_graph.bind('sdo', sdo_namespace)
rdf_graph.bind('rdfs', RDFS)


# initiating entries counter 
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
num_cities_found_in_geonames_mapping = 0
cities_not_found = set()
provinces_not_found = set()
# social media content
num_url = 0
num_validated_url = 0
num_403_url = 0
num_404_url = 0
num_broken_url_link = 0

# username for GeoNames
fuser = open("userinfo.txt","r")
username = fuser.readline().strip()
with open("datasets\ch_coordinates.json") as fresult:
    existing_results = json.load(fresult)
# Define the GeoNames API URL and username
GEONAMES_API_URL = 'http://api.geonames.org/searchJSON'
GEONAMES_USERNAME = username

# open enrichment files
with open('datasets/original_ukrainian_geoname_uri_mappings.json', 'r') as original_ukrainian_cities:
    original_geoname_uri_mappings = json.load(original_ukrainian_cities)
    with open('datasets/extended-ukrainian-geoname-uri-mappings.json', 'r', encoding="utf8") as extended_ukrainian_cities:
        extended_geoname_uri_mappings = json.load(extended_ukrainian_cities)

        original_geoname_uri_mappings.update(extended_geoname_uri_mappings)
        geoname_uri_mappings = original_geoname_uri_mappings

    # Initialize an event ID counter
    event_id = 1
    location_id = 1
    geo_id = 1

# accessing the enriched original data
    with open("datasets/enriched_original_ukr-civharm-2023-04-30.json", encoding="utf-8") as f:
        data = json.load(f)
        # with open("CH_url_count.csv", "w", newline="") as csvfile:
        #     writer = csv.writer(csvfile)
        #     writer.writerow(["URL", "Response", "Request Duration"])
        # Loop through the features in the JSON file
        for d in data:
                # ensure that events are only in Ukraine
                if d['countryCode'] == "UA":
                    num_entry +=1
                    event_URI = l4r_ch_namespace_event + str(event_id).zfill(8)
                    latitude = d['latitude']
                    longitude = d['longitude']
                    coordinates = [longitude, latitude]

                    comment_in_preparation = ''

                    # converting coorinates
                    if 'latitude'in d and 'longitude' in d:
                        latitude = d['latitude']
                        longitude = d['longitude']
                        num_coordinates += 1

                        location_URI = l4r_ch_namespace_location + str(location_id).zfill(8)
                        location_id += 1
                        rdf_graph.add((URIRef(event_URI), sdo_namespace.location, URIRef(location_URI))) # updated from lat
                        geo_URI = l4r_ch_namespace_geo + str(geo_id).zfill(8)
                        geo_id += 1
                        rdf_graph.add((URIRef(location_URI), RDF.type, sdo_namespace.Place)) #
                        rdf_graph.add((URIRef(location_URI), sdo_namespace.geo, URIRef(geo_URI))) #

                        rdf_graph.add((URIRef(geo_URI), RDF.type, sdo_namespace.GeoCoordinates)) #

                        rdf_graph.add((URIRef(geo_URI), sdo_namespace.latitude, Literal(latitude, datatype=XSD.float))) # updated from lat
                            # print ('\tlat', Literal(lat, datatype=XSD.float))

                        rdf_graph.add((URIRef(geo_URI), sdo_namespace.longitude, Literal(longitude, datatype=XSD.float))) # updated from lng

                    # convert the date
                    if 'date' in d:                 
                        date = d['date']
                        date_obj = datetime.strptime(date, "%m/%d/%Y")
                        formatted_date_str = datetime.strftime(date_obj, "%Y-%m-%d")
                        rdf_graph.add((URIRef(event_URI), URIRef('http://purl.org/dc/terms/date'), Literal(formatted_date_str, datatype=XSD.date)))
                        num_date += 1

                    
                    # convert description
                    if 'description' in d:
                        description = d['description']
                        rdf_graph.add((URIRef(event_URI), RDFS.label, Literal(description)))
                        num_label += 1
                    # convet the postal code
                    if 'postalCode' in d:
                        postal_code = d['postalCode']
                        rdf_graph.add((URIRef(event_URI), sdo_namespace.postalCode, Literal(postal_code)))
                        num_postalCode +=1

                    if d.get('sources') and d['sources'][0].get('path'):
                        url = d['sources'][0]['path']
                        rdf_graph.add((URIRef(event_URI), sdo_namespace.url, Literal(url, datatype=XSD.anyURI)))
                        num_url += 1
                        

                    if 'countryCode' in d:
                            
                            country = "Ukraine"
                            country_uri = rdflib.URIRef("http://sws.geonames.org/690791/")

                            rdf_graph.add((URIRef(event_URI), l4r_o_namespace.addressCountry, country_uri))
                            num_country += 1


                    # Initiate Event 

                    rdf_graph.add((URIRef(event_URI), RDF.type, sem_namespace.Event))
                    # rdf_graph.add((URIRef(event_URI), sdo_namespace.latitude, Literal(latitude, datatype=XSD.float)))
                    # rdf_graph.add((URIRef(event_URI), sdo_namespace.longitude, Literal(longitude, datatype=XSD.float)))


                    

                    # convert Region
                    if 'region' in d:
                        region = d['region']
                        if region in geoname_uri_mappings:
                                city_uri = URIRef(geoname_uri_mappings[region])
                                rdf_graph.add((URIRef(event_URI), l4r_o_namespace.addressRegion, city_uri))
                                num_prov += 1
                        else:
                            print ('The province not found!', region)
                            provinces_not_found.add(region)
                        
                    # exctract city infomation
                    if 'location' in d:
                        city_list = d['location'].split(",")
                        city = city_list[0] # the informaiton comes in the format of "city, town, street"
                        city_name = city
                        if city_name in geoname_uri_mappings:
                                city_uri = URIRef(geoname_uri_mappings[city_name])
                                rdf_graph.add((URIRef(event_URI), l4r_o_namespace.addressCity, city_uri))
                            
                                num_city += 1
                                

                        else:
                            
                            for c in existing_results:
                                
                                if coordinates == c['coordinates']:
                                    
                                    city_uri = URIRef(c['URI'])
                                    rdf_graph.add((URIRef(event_URI), l4r_o_namespace.addressCity, city_uri))
                                    
                                    num_city += 1
                                    break
                            


                    # Increment the event ID

                    event_id += 1




sorted_triples = sorted(rdf_graph, key=lambda triple: triple[0])
sorted_graph = Graph()
sorted_graph += sorted_triples

# serialize the sorted graph to a string in RDF/XML format
serialized = sorted_graph.serialize(format="ttl")
# Serialize the RDF graph to file
with open("converted_ukr-civharm-2023-04-30.ttl", "wb") as f:
    f.write(serialized.encode('utf-8'))

# print the numbers
print ('#Entry ', num_entry)
print ('#rdfs:label ', num_label)
print ('#postalCode ', num_postalCode)
print ('#country', num_country)
print ('#date ', num_date)
print ('#coordinates ', num_coordinates)
print ('#province ', num_prov)
print ('#city ', num_city)
print ('num_cities_found_in_geonames_mapping ', num_cities_found_in_geonames_mapping)
print ('#(set of) cities not found ', len(cities_not_found))
for c in cities_not_found:
    print (c)
print ('#(set of) provinces not found ', len(provinces_not_found))

print ('count URL: ', num_url)
print ('count URL: ', num_403_url)
print ('count URL: ', num_404_url)


