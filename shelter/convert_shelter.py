
import csv
import time
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


with open("shelter_coordinates.json") as fresult:
    shelter_coords = json.load(fresult)

l4r_shelter_namespace_location = Namespace("https://linked4resilience.eu/data/Shelter/July2023/location/")

l4r_shelter_namespace_geo = Namespace("https://linked4resilience.eu/data/Shelter/July2023/geo/")
l4r_o_namespace = Namespace("https://linked4resilience.eu/ontology/")
sdo_namespace = Namespace("https://schema.org/")


rdf_graph = Graph()

rdf_graph.bind("shelterlocation", l4r_shelter_namespace_location)
rdf_graph.bind("sheltergeo", l4r_shelter_namespace_geo)
rdf_graph.bind("l4ro", l4r_o_namespace)


location_id = 1
geo_id = 1

for latitude, longtiude in shelter_coords:
    lat = latitude
    lng = longtiude
    location_URI = l4r_shelter_namespace_location + str(location_id).zfill(8)
    location_id += 1


    geo_URI = l4r_shelter_namespace_geo + str(geo_id).zfill(8)
    geo_id += 1

    rdf_graph.add((URIRef(location_URI), RDF.type, l4r_o_namespace.Shelter)) #
    rdf_graph.add((URIRef(location_URI), sdo_namespace.geo, URIRef(geo_URI))) #

    rdf_graph.add((URIRef(geo_URI), RDF.type, sdo_namespace.GeoCoordinates)) #

    rdf_graph.add((URIRef(geo_URI), sdo_namespace.latitude, Literal(lat, datatype=XSD.float))) # updated from lat

    rdf_graph.add((URIRef(geo_URI), sdo_namespace.longitude, Literal(lng, datatype=XSD.float))) # updated from lng



serialized = rdf_graph.serialize(format="ttl")
with open("converted_shelter_coords.ttl", "wb") as f:
        f.write(serialized.encode('utf-8'))