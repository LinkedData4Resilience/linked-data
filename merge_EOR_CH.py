# This file is used to preform the integrating step of the converted Eyes On Russia and Civilian Harm datasets.
# The output will be a .ttl file of the relation of integration between the two datasets.

from rdflib import Graph, Literal, Namespace, RDF, URIRef
from rdflib.namespace import RDFS, XSD
from difflib import SequenceMatcher
from geopy.distance import geodesic
import urllib.parse

import validators

# Define the namespaces used in the RDF files
l4r_eor_namespace_event = Namespace("https://linked4resilience.eu/data/EOR/April2023/event/")
l4r_integrated_namespace_event = Namespace("https://linked4resilience.eu/data/integrated/April2023/event/")

l4r_o_namespace = Namespace("https://linked4resilience.eu/ontology/")


sem_namespace = Namespace("http://semanticweb.cs.vu.nl/2009/11/sem/")

gno_namespace = Namespace('http://www.geonames.org/ontology#')
gni_namespace = Namespace ('https://sws.geonames.org/')


sdo_namespace = Namespace("https://schema.org/")



# Load the first RDF file
g1 = Graph()
g1.parse("converted_EOR-2023-04-30.ttl", format="ttl")

# Load the second RDF file
g2 = Graph()
g2.parse("converted_ukr-civharm-2023-04-30.ttl", format="ttl")

# Define a SPARQL query to extract the city, postalCode, lat, lng, and label values from each triple in the first RDF file
query1 = """
    
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
    PREFIX ns2: <https://linked4resilience.eu/ontology/> 
    PREFIX ns3: <http://purl.org/dc/terms/> 
    PREFIX ns1: <https://schema.org/> 
    SELECT ?city ?lat ?lng ?label ?date ?url ?s ?loc
    WHERE {
        ?s rdfs:label ?label ;
           ns2:addressCity ?city ;
           ns1:location ?loc;
           ns3:date ?date ;
           ns1:url ?url .
        ?loc ns1:geo ?geo.
        ?geo ns1:latitude ?lat .
        ?geo ns1:longitude ?lng .
    }
"""

# Execute the SPARQL query on the first RDF file and extract the results
results1 = g1.query(query1)
row_count = len(results1)
print("Number of rows:", row_count)

# Define a SPARQL query to extract the city, postalCode, lat, lng, and label values from each triple in the second RDF file
query2 = """
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#> 
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#> 
    PREFIX ns2: <https://linked4resilience.eu/ontology/> 
    PREFIX ns3: <http://purl.org/dc/terms/> 
    PREFIX ns1: <https://schema.org/> 
    SELECT ?city ?lat ?lng ?label ?date ?url ?s ?loc
    WHERE {
        ?s rdfs:label ?label ;
           ns2:addressCity ?city ;
           ns1:location ?loc;
           ns3:date ?date ;
           ns1:url ?url .
        ?loc ns1:geo ?geo.
        ?geo ns1:latitude ?lat .
        ?geo ns1:longitude ?lng .

    }
"""

        #    ns1:latitude ?lat ;
        #    ns1:longitude ?lng ;

# Execute the SPARQL query on the second RDF file and extract the results
results2 = g2.query(query2)
row_count = len(results2)
print("Number of rows:", row_count)
# Create a dictionary to hold the groups
group_dict = {}
keyword_list = ['central','bridge','college','market','Theater','tanks','cars','car','residential','zoo', 'church','supermarket', 'University', 'playground', 'center', 'hotel','university','school', 'hospital', 'building', 'complex', 'house', 'clinic', 'museum', 'block', 'flat', 'station', 'factory']

# Loop through the results from the first RDF file
for row1 in results1:
    # Extract the triple data
    city1 = str(row1[0])
    lat1 = float(row1[1])
    lng1 = float(row1[2])
    label1 = str(row1[3])
    date1 = str(row1[4])
    url1 = str(row1[5])
    subject1 = str(row1[6])
    # Create a key for the group based on city, postalCode, lat, and lng
    key = (subject1, city1, lat1, lng1, date1,label1)
    # Check if the key exists in the dictionary
    if key not in group_dict:
        # Create a new dictionary entry for this key
        group_dict[key] = {"subjects":[subject1], "city": city1, "date": date1,
                            "lat": lat1, "lng": lng1, "url1": [url1], "labels": [label1]}
        
ch_list = []
# Loop through the results from the second RDF file
for row2 in results2:
    # Extract the triple data
    city2 = str(row2[0])
    lat2 = float(row2[1])
    lng2 = float(row2[2])
    label2 = str(row2[3])
    date2 = str(row2[4])
    url2 = str(row2[5])
    subject2 = str(row2[6])
    sub_present = False
    # Iterate over the existing groups

    for key, value in group_dict.items():
        # Compare the cities dates
        
    # start comparing to merge the events.    
        if city2 == value["city"] and date2 == value["date"]:
            
                       
                similarity_ratio = SequenceMatcher(None, label2, value["labels"][0]).ratio()
                
                coords1 = (group_dict[key]['lat'], group_dict[key]['lng'])
                
                coords2 = (lat2, lng2)
                
                distance_km = geodesic(coords1, coords2).km
                # condition 1 
                if group_dict[key]["url1"][0] == url2 and similarity_ratio > 0.55 and distance_km <= 2 and len(value["labels"]) == 1: 
                    
                    value["labels"].append(label2)
                    value["subjects"].append(subject2)
                    value["url1"].append(url2)
                    sub_present = True
                    break
                # condition 2
                elif ("area" in value["labels"][0].lower()) or ("area" in label2.lower()):
                    if (distance_km <= 2) and (similarity_ratio > 0.75) and len(value["labels"]) == 1:
                    
                                value["labels"].append(label2)
                                value["subjects"].append(subject2)
                                value["url1"].append(url2)
                                sub_present = True
                                break

                # condition 3                 
                elif any((keyword in value["labels"][0].lower()) or (keyword in label2.lower()) for keyword in keyword_list):
                    if (distance_km < 1) and (similarity_ratio >= 0.55) and len(value["labels"]) == 1:
                 
                                value["labels"].append(label2)
                                value["subjects"].append(subject2)
                                value["url1"].append(url2)
                                sub_present = True
                                break
    if not sub_present:        
        ch_list.append(subject2)
                            
# Create the output graph
output_graph = Graph()

# Iterate over the grouped events
id_count = 0
match_count = 0
for key, value in group_dict.items():
    if len(value["labels"]) == 2:
        id_count += 1
        match_count +=1
        # Generate a new subject URI for the group
        subject_uri = URIRef(l4r_integrated_namespace_event + str(id_count).zfill(8))
        # Add the triples for the group to the output graph
        
        
        output_graph.add((subject_uri, RDF.type, sem_namespace.Event))        
        output_graph.add((subject_uri, URIRef('http:www.w3.org/ns/prov#wasDerivedFrom'), URIRef(value['subjects'][0])))
        if validators.url(value["url1"][0]) and validators.url(value["url1"][1]):
            if value["labels"][0] >= value["labels"][1]:
                output_graph.add((subject_uri, l4r_o_namespace.hasPrimarySource, URIRef(value['subjects'][0])))
            else:
                output_graph.add((subject_uri, l4r_o_namespace.hasPrimarySource, URIRef(value['subjects'][1])))
        elif validators.url(value["url1"][0]):
            output_graph.add((subject_uri, l4r_o_namespace.hasPrimarySource, URIRef(value['subjects'][0])))
        elif validators.url(value["url1"][1]):
            output_graph.add((subject_uri, l4r_o_namespace.hasPrimarySource, URIRef(value['subjects'][1])))

        else:
            if value["labels"][0] >= value["labels"][1]:
                output_graph.add((subject_uri, l4r_o_namespace.hasPrimarySource, URIRef(value['subjects'][0])))
            else:
                output_graph.add((subject_uri, l4r_o_namespace.hasPrimarySource, URIRef(value['subjects'][1]))) 
                
        output_graph.add((subject_uri, URIRef('http:www.w3.org/ns/prov#wasDerivedFrom'), URIRef(value['subjects'][1])))
        
for key, value in group_dict.items():
    if len(value["labels"]) == 1:
        id_count += 1
        subject_uri = URIRef(l4r_integrated_namespace_event + str(id_count).zfill(8))
        # Add the triples for the group to the output graph
        

        output_graph.add((subject_uri, RDF.type, sem_namespace.Event))        
        output_graph.add((subject_uri, URIRef('http:www.w3.org/ns/prov#wasDerivedFrom'), URIRef(value['subjects'][0])))
        output_graph.add((subject_uri, l4r_o_namespace.hasPrimarySource, URIRef(value['subjects'][0])))

for subject in ch_list:    
        id_count += 1
        subject_uri = URIRef(l4r_integrated_namespace_event + str(id_count).zfill(8))
    # Add the triples for the group to the output graph
    

        output_graph.add((subject_uri, RDF.type, sem_namespace.Event))        
        output_graph.add((subject_uri, URIRef('http:www.w3.org/ns/prov#wasDerivedFrom'), URIRef(subject)))
        output_graph.add((subject_uri, l4r_o_namespace.hasPrimarySource, URIRef(subject)))









# Save the output graph to a TTL file
output_graph.serialize("integ-2023-04-30.ttl", format="ttl")
# print the output numbers 
print("Total number of groups:", match_count)
print("Total number of merged:", id_count)
print("Output file saved as 'Merged-2023-04-30.ttl'")
print(len(group_dict))
print(len(ch_list))
