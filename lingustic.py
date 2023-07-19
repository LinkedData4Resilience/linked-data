import requests
import json
from rdflib import Graph, Literal, Namespace, RDF, URIRef

fuser = open("userinfo.txt","r")
username = fuser.readline().strip()
# Load the RDF file
g = Graph()
# g.parse("converted_ukr-civharm-2023-04-30.ttl", format="ttl")
g.parse("converted_EOR-2023-04-30.ttl", format="ttl")
# Define the GeoNames namespace
gn = Namespace("http://sws.geonames.org/")

l4r = Namespace("https://linked4resilience.eu/ontology/")
# Load the existing city dictionary from the JSON file
with open("english_city_dict.json", "r") as file:
    city_dict = json.load(file)

# Iterate through the RDF data
for s, p, o in g:
    if p == l4r.addressCity:  # Assuming you have a specific RDF type for cities
        if o.startswith(gn):  # Check if the object is a GeoNames URI
            geoname_id = o.split("/")[-2]  # Extract the GeoName ID
            if geoname_id not in city_dict:  # Check if GeoName ID already exists in the dictionary
                api_url = f"http://api.geonames.org/getJSON?geonameId={geoname_id}&lang=en&username={username}"
                response = requests.get(api_url)
                if response.status_code == 200:
                    city_data = response.json()
                    translated_city_name = city_data["name"]
                    city_dict[geoname_id] = translated_city_name
                    print(translated_city_name)
                else:
                    print(f"Failed to retrieve data for GeoName ID: {geoname_id}")
            else:
                translated_city_name = city_dict[geoname_id]
            # g.set((s, p, Literal(translated_city_name, lang="fr")))

# Save the modified RDF file
# g.serialize("translated_rdf_file.rdf", format="xml")
with open("english_city_dict.json", "w") as file:
    json.dump(city_dict, file, indent=4)
# # Save the updated city dictionary back to the JSON file

# Print the city dictionary
print(city_dict)
