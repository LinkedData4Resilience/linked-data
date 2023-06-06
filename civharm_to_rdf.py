from rdflib import FOAF, RDFS, Graph, Literal, Namespace, RDF, URIRef
import rdflib
from rdflib.namespace import XSD
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup


# Define namespaces
my_namespace = Namespace("http://linked4resilience/data/ch/april2023/")
sem_namespace = Namespace("http://semanticweb.cs.vu.nl/2009/11/sem/")
SCHEMA = Namespace("http://schema.org/")

# Create an RDF graph
rdf_graph = Graph()

# Bind namespaces
rdf_graph.bind("res", my_namespace)
rdf_graph.bind("sem", sem_namespace)
rdf_graph.bind("xsd", XSD)

with open('ukrainian_cities.json', 'r') as ukrainian_cities:
    city_uris = json.load(ukrainian_cities)
# Open the JSON file
with open("output_ukr-civharm-2023-04-30.json",encoding="utf-8") as f:
    data = json.load(f)

with open("userinfo.txt","r") as fuser:
    username = fuser.readline().strip()

    # Initialize an event ID counter
    event_id = 'civ1'
	
    # Loop through the features in the JSON file
    for d in data:
        latitude = d['latitude']
        longitude = d['longitude']
        date = d['date']
        city_list = d['location'].split(",")
        city = city_list[0]
        description = d['description'] 
        if 'postalCode' in d:
            postal_code = d['postalCode']
            region = d['region']
        if d.get('sources') and d['sources'][0].get('path'):
            path = d['sources'][0]['path']
        if 'countryCode' in d:
            
            country = "Ukraine"
            geo_country_URI = rdflib.URIRef("http://sws.geonames.org/690791/")
            # Create a URI for the event using the event ID
        event_URI = my_namespace + str(event_id)

        # Add triples to the graph
        rdf_graph.add((URIRef(event_URI), SCHEMA.addressCountry, geo_country_URI))
        rdf_graph.add((URIRef(event_URI), RDF.type, sem_namespace.Event))
        rdf_graph.add((URIRef(event_URI), SCHEMA.lat, Literal(latitude, datatype=XSD.float)))
        rdf_graph.add((URIRef(event_URI), SCHEMA.lng, Literal(longitude, datatype=XSD.float)))
        rdf_graph.add((URIRef(event_URI), RDFS.label, Literal(description)))
        rdf_graph.add((URIRef(event_URI), SCHEMA.url, Literal(path, datatype=XSD.anyURI)))
        # rdf_graph.add((URIRef(event_URI), SCHEMA.addressCountry, Literal(country)))
        if region:
            region_name = region
            if region_name in city_uris:
                    city_uri = URIRef(city_uris[region_name])
                    rdf_graph.add((URIRef(event_URI), SCHEMA.region, city_uri))
            else:
                rdf_graph.add((URIRef(event_URI), SCHEMA.region, Literal(region)))
        
        if city:
            city_name = city
            if city_name in city_uris:
                    city_uri = URIRef(city_uris[city_name])
                    rdf_graph.add((URIRef(event_URI), SCHEMA.city, city_uri))
            else:
                          
                geonames_url = f'http://api.geonames.org/searchJSON?q={city_name}&maxRows=1&username={username}'
                response = requests.get(geonames_url).json()
                if 'totalResultsCount' in response and response['totalResultsCount'] > 0:
                    geoname_id = response['geonames'][0]['geonameId']
                    city_uri = URIRef(f'http://sws.geonames.org/{geoname_id}/')
                    print('hi')
                    city_uris[city_name] = str(city_uri)
                    with open('ukrainian_cities.json', 'w') as uri_new:
                        json.dump(city_uris, uri_new, indent=4)
                else:
                    city_uri = Literal(city_name)
                rdf_graph.add((URIRef(event_URI), SCHEMA.city, Literal(city_uri)))
                
        date_obj = datetime.strptime(date, "%m/%d/%Y")
        formatted_date_str = datetime.strftime(date_obj, "%Y-%m-%d")
        rdf_graph.add((URIRef(event_URI), SCHEMA.date, Literal(formatted_date_str, datatype=XSD.date)))
        
        rdf_graph.add((URIRef(event_URI), SCHEMA.postalCode, Literal(postal_code)))
        # Increment the event ID
        event_num = int(event_id[3:])
        event_id = f"event{event_num + 1}"



sorted_triples = sorted(rdf_graph, key=lambda triple: triple[0])
sorted_graph = Graph()
sorted_graph += sorted_triples

# serialize the sorted graph to a string in RDF/XML format
serialized = sorted_graph.serialize(format="ttl")
# Serialize the RDF graph to file
with open("output_ukr-civharm-2023-04-30.ttl", "wb") as f:
    f.write(serialized.encode('utf-8'))


with open("output_ukr-civharm-2023-04-30.ttl", 'r', encoding="utf8") as foutput:
    ttl = foutput.read()
    
ttl = ttl.replace('ns1:', 'schema:').replace('ns2:', 'sem:').replace('rdf-schema#', 'rdfs:')

with open("output_ukr-civharm-2023-04-30.ttl", 'w',encoding="utf8") as foutput:
    foutput.write(ttl)

# import re

# # Define the properties to extract and count
# properties = [
#     "schema:addressCountry",
#     "schema:city",
#     "schema:date",
#     "schema:lat",
#     "schema:lng",
#     "schema:postalCode",
#     "schema:region",
#     "schema:url",
#     "rdfs:label"
# ]

# # Read in the triples file
# with open("output_ukr-civharm-2023-04-30.ttl", "r", encoding='utf-8') as f:
#     data = f.read()

# # Iterate over the properties and count the unique entities
# for property_name in properties:
#     # Extract the property values using a regular expression pattern
#     pattern = re.compile(rf"{property_name}\s+(.*?)\s*;")
#     matches = pattern.findall(data)

#     # Count the number of unique entities
#     unique_entities = set(matches)
#     count = len(unique_entities)

#     # Print the results
#     print(f"{property_name}: {count} unique entities")
