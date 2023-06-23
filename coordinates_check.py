import json
from math import sqrt, sin, cos, atan2, radians
from rdflib import Graph, Literal, Namespace, RDF, XSD
def distance(lat1, lon1, lat2, lon2):
    """
    Calculate the distance between two points using the Haversine formula.
    """
    radius = 6371  # Radius of the Earth in kilometers
    
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    
    a = sin(dlat/2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2) ** 2
    c = 2 * atan2(sqrt(max(a, 0)), sqrt(max(1-a, 0)))
    distance = radius * c
    
    return distance


ns2 = Namespace("https://schema.org/")

g = Graph()
g.parse("converted_EOR-2023-04-30.ttl", format="turtle")
# g.parse("converted_ukr-civharm-2023-04-30.ttl", format="turtle")


# with open("datasets\enriched_original_EOR-2023-04-30.json", encoding="utf-8") as f:
for s, p, o in g:
    if p == RDF.type and o == ns2.GeoCoordinates:
        i = 0
        radius = 5  # 10km radius
        lat_literal = g.value(s, ns2.latitude, None)
        lon_literal = g.value(s, ns2.longitude, None)

        lat = float(lat_literal.value)
        lon = float(lon_literal.value)
        coord = (lat, lon)
        dist = distance(51.613451, 39.147331, lat, lon)
        
        if dist <= radius:
            
            print(f"Coordinate {coord} is within {radius}km radius.")
    

# Example usage



