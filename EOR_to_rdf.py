from bs4 import BeautifulSoup
from rdflib import FOAF, RDFS, Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import XSD
import json
from datetime import datetime
import urllib.parse
import requests


with open("userinfo.txt","r") as fuser:
    username = fuser.readline().strip()

# Define the GeoNames API URL and username
GEONAMES_API_URL = 'http://api.geonames.org/searchJSON'
GEONAMES_USERNAME = username
# Define namespaces
my_namespace = Namespace("http://linked4resilience/data/eor/april2023/")
sem_namespace = Namespace("https://semanticweb.cs.vu.nl/2009/11/sem/")
SCHEMA = Namespace("http://schema.org/")

# Create an RDF graph
rdf_graph = Graph()

# Bind namespaces
rdf_graph.bind("res", my_namespace)
rdf_graph.bind("sem", sem_namespace)
rdf_graph.bind("xsd", XSD)

# Open the JSON file
with open("output_EOR-2023-04-30.json") as fjson:
    data = json.load(fjson)
with open('ukrainian_cities.json', 'r') as ukrainian_cities:
    city_uris = json.load(ukrainian_cities)
    # Initialize an event ID counter
    event_id = 'eor1'
    i = 0
    # Loop through the features in the JSON file
    for feature in data['features']:
        lng, lat = feature["geometry"]["coordinates"]
        # Create a URI for the event using the event ID
        if feature["properties"].get("country") == "Ukraine":
            event_URI = my_namespace + str(event_id)

            # Add triples to the graph
            verified_date_str = feature['properties']['verifiedDate']
            verified_date_obj = datetime.fromisoformat(verified_date_str)
            verified_date_str_no_time = verified_date_obj.date().isoformat()

            rdf_graph.add((URIRef(event_URI), SCHEMA.date, Literal(verified_date_str_no_time, datatype=XSD.date)))
            rdf_graph.add((URIRef(event_URI), SCHEMA.lat, Literal(lat, datatype=XSD.float)))
            rdf_graph.add((URIRef(event_URI), SCHEMA.lng, Literal(lng, datatype=XSD.float)))
            if feature["properties"].get("violenceLevel"):
                rdf_graph.add((URIRef(event_URI), SCHEMA.damageSeverity, Literal(feature['properties']['violenceLevel'], datatype=XSD.integer)))
            if feature["properties"].get("description"):
                rdf_graph.add((URIRef(event_URI), RDFS.label, Literal(feature["properties"]['description'])))

            if feature.get("postalCode"):
                rdf_graph.add((URIRef(event_URI), SCHEMA.postalCode, Literal(feature['postalCode'])))
            if feature["properties"].get("country"):
                city_name = feature['properties']['country']
                if city_name in city_uris:
                    city_uri = URIRef(city_uris[city_name])
                    rdf_graph.add((URIRef(event_URI), SCHEMA.addressCountry, city_uri))
                else:
                    rdf_graph.add((URIRef(event_URI), SCHEMA.addressCountry, Literal(feature["properties"]["country"])))
            if feature["properties"].get("province"):
                city_name = feature['properties']['province']
                if city_name in city_uris:
                    city_uri = URIRef(city_uris[city_name])
                    rdf_graph.add((URIRef(event_URI), SCHEMA.region, city_uri))
                else:
                    rdf_graph.add((URIRef(event_URI), SCHEMA.region, Literal(feature["properties"]["province"])))
            if feature["properties"].get("city"):

                city_name = feature['properties']['city']
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
                    rdf_graph.add((URIRef(event_URI), SCHEMA.city, city_uri))

            else:
                    geonames_url = f'http://api.geonames.org/searchJSON?q={city_name}&maxRows=1&username={username}'
                    response = requests.get(geonames_url).json()
                    if 'totalResultsCount' in response and response['totalResultsCount'] > 0:
                        geoname_id = response['geonames'][0]['geonameId']
                        city_uri = URIRef(f'http://sws.geonames.org/{geoname_id}/')
                        print('hi')
            for category in feature['properties']['categories']:
                rdf_graph.add((URIRef(event_URI), RDFS.comment, Literal(category)))

            if feature['properties'].get('url'):
                rdf_graph.add((URIRef(event_URI), SCHEMA.url, Literal(feature["properties"]['url'], datatype=XSD.anyURI)))

            rdf_graph.add((URIRef(event_URI), RDF.type, sem_namespace.Event))
            event_num = int(event_id[3:])
            event_id = f"event{event_num + 1}"



sorted_triples = sorted(rdf_graph, key=lambda triple: triple[0])
sorted_graph = Graph()
sorted_graph += sorted_triples

# serialize the sorted graph to a string in RDF/XML format
serialized = sorted_graph.serialize(format="ttl")
with open("output_EOR-2023-04-30.ttl", "wb") as f:
        f.write(serialized.encode('utf-8'))




with open("output_EOR-2023-04-30.ttl", 'r', encoding="utf8") as foutput:
    ttl = foutput.read()

ttl = ttl.replace('ns1:', 'schema:').replace('ns2:', 'sem:').replace('rdf-schema#', 'rdfs:')

with open("output_EOR-2023-04-30.ttl", 'w',encoding="utf8") as foutput:
    foutput.write(ttl)















































# from rdflib import FOAF, RDFS, Graph, Literal, Namespace, RDF, URIRef
# from rdflib.namespace import XSD
# import json

# # Define namespaces
# my_namespace = Namespace("http://resilience.vu.nl/manar/")
# sem_namespace = Namespace("http://semanticweb.cs.vu.nl/2009/11/sem/")
# SCHEMA = Namespace("http://schema.org/")

# # Create an RDF graph
# rdf_graph = Graph()

# # Bind namespaces
# rdf_graph.bind("res", my_namespace)
# rdf_graph.bind("sem", sem_namespace)
# rdf_graph.bind("xsd", XSD)

# # Open the JSON file
# with open("EOR-2023-04-30.geojson") as f:
#     data = json.load(f)
# with open('ukrainian_cities.json', 'r') as ukrainian_cities:
#     city_uris = json.load(ukrainian_cities)
#     # Initialize an event ID counter
#     event_id = 'eor1'

#     # Loop through the features in the JSON file
#     for feature in data['features']:
#             lng, lat = feature["geometry"]["coordinates"]
#             # Create a URI for the event using the event ID
#             event_URI = my_namespace + str(event_id)

#             # Add triples to the graph
#             # rdf_graph.add((URIRef(event_URI), SCHEMA.postalCode, Literal(feature['postal_code'])))

#             rdf_graph.add((URIRef(event_URI), SCHEMA.date, Literal(feature['properties']['verifiedDate'])))
#             rdf_graph.add((URIRef(event_URI), sem_namespace.event, URIRef(sem_namespace + 'Event')))
#             rdf_graph.add((URIRef(event_URI), SCHEMA.lat, Literal(lat)))
#             rdf_graph.add((URIRef(event_URI), SCHEMA.lng, Literal(lng)))

#             #rdf_graph.add((URIRef(event_URI), FOAF.page, URIRef(feature["properties"]['link'])))
#             if feature["properties"].get("country"):
#                 city_name = feature['properties']['country']
#                 if city_name in city_uris:
#                     city_uri = URIRef(city_uris[city_name])
#                     rdf_graph.add((URIRef(event_URI), SCHEMA.addressCountry, city_uri))
#                 else:
#                     rdf_graph.add((URIRef(event_URI), SCHEMA.addressCountry, Literal(feature["properties"]["country"])))
#             if feature["properties"].get("province"):
#                 city_name = feature['properties']['province']
#                 if city_name in city_uris:
#                     city_uri = URIRef(city_uris[city_name])
#                     rdf_graph.add((URIRef(event_URI), SCHEMA.region, city_uri))
#                 else:
#                     rdf_graph.add((URIRef(event_URI), SCHEMA.region, Literal(feature["properties"]["province"])))
#             if feature["properties"].get("city"):
#                 city_name = feature['properties']['city']
#                 if city_name in city_uris:
#                     city_uri = URIRef(city_uris[city_name])
#                     rdf_graph.add((URIRef(event_URI), SCHEMA.city, city_uri))
#                 else:
#                     rdf_graph.add((URIRef(event_URI), SCHEMA.city, Literal(feature["properties"]["city"])))
#             # rdf_graph.add((URIRef(event_URI), SCHEMA.district, Literal(feature["properties"]["district"])))
#             if feature["properties"].get("violence_level"):
#                 rdf_graph.add((URIRef(event_URI), SCHEMA.damageSeverity, Literal(feature['properties']['violenceLevel'], datatype=XSD.integer)))
#             # if feature["properties"].get("time"):
#             #     rdf_graph.add((URIRef(event_URI), SCHEMA.time, Literal(feature["properties"]["time"])))
#             for category in feature['properties']['categories']:
#                 rdf_graph.add((URIRef(event_URI), SCHEMA.additionalType, Literal(category)))
#         # Increment the event ID
#             event_num = int(event_id[3:])
#             event_id = f"eor{event_num + 1}"

# # Serialize the RDF graph to file
# with open("output_EOR-2023-04-30.ttl", "wb") as f:
#     f.write(rdf_graph.serialize(format="nt", encoding="utf-8"))


# from collections import defaultdict
# from rdflib import Graph, URIRef

# # Read triples from a file
# g = Graph()
# g.parse('output_EOR-2023-04-30.ttl', format='turtle')

# # Initialize dictionaries to store counts
# property_counts = defaultdict(int)
# unique_entity_counts = defaultdict(set)

# # Iterate over triples and count entities
# for s, p, o in g:
#     if isinstance(o, URIRef):
#         unique_entity_counts[p].add(o)
#     property_counts[p] += 1

# # Print results
# for p, count in property_counts.items():
#     unique_count = len(unique_entity_counts[p])
#     print(f"Property: {p} \tEntries: {count} \tUnique entities: {unique_count}")
