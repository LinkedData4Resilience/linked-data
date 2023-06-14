# from rdflib import Graph, Literal, Namespace, RDF, URIRef
# from rdflib.namespace import RDFS, XSD
# from difflib import SequenceMatcher
# from geopy.distance import geodesic
# from difflib import SequenceMatcher
# from geopy.distance import geodesic
# from rdflib import Graph, Literal, Namespace, URIRef
# from rdflib.namespace import RDFS, XSD
# from itertools import groupby

# # Create a new RDF graph for the accepted pairs
# accepted_graph = Graph()

# # Define the namespaces used in the RDF files
# schema = Namespace("http://schema.org/")
# sem = Namespace("http://semanticweb.cs.vu.nl/2009/11/sem/")

# # Load the first RDF file
# g1 = Graph()
# g1.parse("EOR-2023-04-30.ttl", format="ttl")

# # Define a SPARQL query to extract the city, postalCode, lat, lng, and label values from each triple in the first RDF file
# query1 = """
#     PREFIX schema: <http://schema.org/>
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdfs:>
#     SELECT ?s ?city ?postalCode ?lat ?lng ?label ?date ?url
#     WHERE {
#         ?s rdfs:label ?label ;
#            schema:city ?city ;
#            schema:postalCode ?postalCode ;
#            schema:lat ?lat ;
#            schema:lng ?lng ;
#            schema:date ?date ;
#            schema:url ?url ;
           
#     }
# """

# # Execute the SPARQL query on the first RDF file and extract the results
# results1 = g1.query(query1)

# # Load the second RDF file
# g2 = Graph()
# g2.parse("CH-2023-04-30.ttl", format="ttl")

# # Define a SPARQL query to extract the city, postalCode, lat, lng, and label values from each triple in the second RDF file
# query2 = """
#     PREFIX schema: <http://schema.org/>
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdfs:>
#     SELECT ?s ?city ?postalCode ?lat ?lng ?label ?date ?url
#     WHERE {
#         ?s rdfs:label ?label ;
#            schema:city ?city ;
#            schema:postalCode ?postalCode ;
#            schema:lat ?lat ;
#            schema:lng ?lng ;
#            schema:date ?date ;
#            schema:url ?url ;
           
#     }
# """

# # Execute the SPARQL query on the second RDF file and extract the results
# results2 = g2.query(query2)

# # Create a namespace for the schema.org vocabulary
# schema = Namespace("http://schema.org/")

# # Create a namespace for the SEM namespace (assuming you have defined it)
# sem = Namespace("http://example.org/sem/")

# # Create an RDF graph to store the accepted pairs
# accepted_graph = Graph()


# # Create a dictionary to hold the triples from the first RDF file
# triple_dict1 = {}

# # Loop through the results from the first RDF file
# for row in results1:
#     # Extract the triple data
#     subject = row[0]
#     city = str(row[1])
#     postalCode = str(row[2])
#     lat = float(row[3])
#     lng = float(row[4])
#     label = str(row[5])
#     date = str(row[6])
#     url = str(row[7])
#     # Create a key for the triple based on city, postalCode, lat, and lng
#     key = (city, postalCode, lat, lng, date, url)
    
#     # Check if the key exists in the dictionary
#     if key in triple_dict1:
#         triple_dict1[key]["labels"].append((label, subject))
#     else:
#         # Create a new dictionary entry for this key
#         triple_dict1[key] = {"city": city, "date": date, "postalCode": postalCode, "lat": lat, "lng": lng, "labels": [(label, subject)], "url": url}

# # Create a dictionary to hold the triples from the second RDF file
# triple_dict2 = {}

# # Loop through the results from the second RDF file
# for row in results2:
#     # Extract the triple data
#     subject = row[0]
#     city = str(row[1])
#     postalCode = str(row[2])
#     lat = float(row[3])
#     lng = float(row[4])
#     label = str(row[5])
#     date = str(row[6])
#     url = str(row[7])
#     # Create a key for the triple based on city, postalCode, lat, and lng
#     key = (city, postalCode, lat, lng, date, url)
    
#     # Check if the key exists in the dictionary
#     if key in triple_dict2:
#         triple_dict2[key]["labels"].append((label, subject))
#     else:
#         # Create a new dictionary entry for this key
#         triple_dict2[key] = {"city": city, "date": date, "postalCode": postalCode, "lat": lat, "lng": lng, "labels": [(label, subject)], "url": url}

# matched_pairs = 0

# # Open a file to write the accepted pairs
# with open("duplicates_distance_2_similarity_55-95(url).txt", "w", encoding='utf-8') as f:
#     for key1 in triple_dict1:
#         # Loop through the keys in the second dictionary
#         for key2 in triple_dict2:
#             # Check if the city and date match
#             if triple_dict1[key1]["city"] == triple_dict2[key2]["city"] and triple_dict1[key1]["date"] == triple_dict2[key2]["date"]:
#                 # Calculate the distance between the coordinates
#                 coords1 = (triple_dict1[key1]['lat'], triple_dict1[key1]['lng'])
#                 coords2 = (triple_dict2[key2]['lat'], triple_dict2[key2]['lng'])
#                 distance_km = geodesic(coords1, coords2).kilometers
#                 # Calculate the similarity between the labels
#                 label_similarities = []
#                 for label1, subject1 in triple_dict1[key1]['labels']:
#                     for label2, subject2 in triple_dict2[key2]['labels']:
#                         similarity_ratio = SequenceMatcher(None, label1, label2).ratio()
#                         label_similarities.append((similarity_ratio, label1, subject1, label2, subject2))
#                 # Sort the label similarities in descending order
#                 label_similarities.sort(reverse=True)
                
#                 # Check if there are any label similarities
#                 if label_similarities:
#                     # Group the label similarities by the first label
#                     grouped_similarities = groupby(label_similarities, key=lambda x: x[1])
                    
#                     # Loop through the groups
#                     for _, group in grouped_similarities:
#                         group = list(group)
#                         # Get the maximum similarity within the group
#                         max_similarity = max(group, key=lambda x: x[0])[0]
#                         # Get the pairs with the maximum similarity
#                         max_similarity_pairs = [(label1, subject1, label2, subject2) for _, label1, subject1, label2, subject2 in group if _ == max_similarity]
#                         # Check if the maximum similarity is above the threshold
#                         if max_similarity >= 0.55:
#                             # Get the pair with the largest label length
#                             max_pair = max(max_similarity_pairs, key=lambda x: len(x[0]))
#                             max_label1, max_subject1, max_label2, max_subject2 = max_pair
#                             # Add the accepted triple to the graph
#                             max_label_subject = URIRef(max_subject1)
#                             accepted_graph.add((max_label_subject, RDFS.label, Literal(max_label1)))
#                             accepted_graph.add((max_label_subject, schema.city, Literal(triple_dict1[key1]["city"])))
#                             accepted_graph.add((max_label_subject, schema.postalCode, Literal(triple_dict1[key1]["postalCode"])))
#                             accepted_graph.add((max_label_subject, schema.lat, Literal(triple_dict1[key1]["lat"], datatype=XSD.float)))
#                             accepted_graph.add((max_label_subject, schema.lng, Literal(triple_dict1[key1]["lng"], datatype=XSD.float)))
#                             accepted_graph.add((max_label_subject, schema.date, Literal(triple_dict1[key1]["date"], datatype=XSD.date)))
#                             accepted_graph.add((max_label_subject, schema.url, Literal(triple_dict1[key1]["url"], datatype=XSD.anyURI)))
#                             accepted_graph.add((max_label_subject, sem.hasSimilarity, Literal(max_similarity, datatype=XSD.float)))
#                             accepted_graph.add((max_label_subject, sem.hasDistance, Literal(distance_km, datatype=XSD.float)))
    
#                             # Write the accepted pair to the file
#                             f.write(f"{max_label1} ({max_subject1}) - {max_label2} ({max_subject2})\n")
#                             matched_pairs += 1

# # Save the accepted pairs in TTL format
# accepted_graph.serialize("accepted_pairs.ttl", format="ttl")

# print(f"{matched_pairs} pairs were matched.")




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
    SELECT ?city ?lat ?lng ?label ?date ?url ?s
    WHERE {
        ?s rdfs:label ?label ;
           ns2:addressCity ?city ;
           ns1:latitude ?lat ;
           ns1:longitude ?lng ;
           ns3:date ?date ;
           ns1:url ?url ;

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
    SELECT ?city ?lat ?lng ?label ?date ?url ?s
    WHERE {
        ?s rdfs:label ?label ;
           ns2:addressCity ?city ;
           ns1:latitude ?lat ;
           ns1:longitude ?lng ;
           ns3:date ?date ;
           ns1:url ?url ;

    }
"""



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
        
        
        if city2 == value["city"] and date2 == value["date"]:
            
            
                
                similarity_ratio = SequenceMatcher(None, label2, value["labels"][0]).ratio()
                
                coords1 = (group_dict[key]['lat'], group_dict[key]['lng'])
                
                coords2 = (lat2, lng2)
                
                distance_km = geodesic(coords1, coords2).km
                if group_dict[key]["url1"][0] == url2 and similarity_ratio > 0.55 and distance_km <= 2 and len(value["labels"]) == 1: 
                    
                    value["labels"].append(label2)
                    value["subjects"].append(subject2)
                    value["url1"].append(url2)
                    sub_present = True
                    break

                # elif distance_km <= 1:
                #     if similarity_ratio > 0.55 and similarity_ratio < 0.97:
                        
                #         value["labels"].append(label2)
                #         value["subjects"].append(subject2)

                elif ("area" in value["labels"][0].lower()) or ("area" in label2.lower()):
                    if (distance_km <= 2) and (similarity_ratio > 0.75) and len(value["labels"]) == 1:
                    
                                value["labels"].append(label2)
                                value["subjects"].append(subject2)
                                value["url1"].append(url2)
                                sub_present = True
                                break


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





# # Add the remaining triples from the first RDF file to the output graph
# for triple in g1:
#     output_graph.add(triple)

# # Add the remaining triples from the second RDF file to the output graph
# for triple in g2:
#     output_graph.add(triple)

# Save the output graph to a TTL file
output_graph.serialize("Merged-2023-04-30.ttl", format="ttl")

print("Total number of groups:", match_count)
print("Total number of merged:", id_count)
print("Output file saved as 'Merged-2023-04-30.ttl'")
print(len(group_dict))
print(len(ch_list))
# with open("Merged-2023-04-30.ttl", 'r', encoding="utf8") as foutput:
#     ttl = foutput.read()
    
# ttl = ttl.replace('ns1:', 'schema:').replace('ns2:', 'rdfs:').replace('rdf-schema#', 'rdfs:')

# with open("Merged-2023-04-30.ttl", 'w',encoding="utf8") as foutput:
#     foutput.write(ttl)
