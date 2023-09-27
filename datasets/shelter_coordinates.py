import json
import xml.etree.ElementTree as ET

def extract_coordinates(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()

    coordinates_list = []

    for placemark in root.findall('.//{http://www.opengis.net/kml/2.2}Placemark'):
        coordinates = placemark.find('.//{http://www.opengis.net/kml/2.2}Point/{http://www.opengis.net/kml/2.2}coordinates')

        if coordinates is not None:
            coordinates_text = coordinates.text.strip()
            longitude, latitude, _ = map(float, coordinates_text.split(','))

            # Appending data to the coordinates_list as a tuple (lat, lng)
            coordinates_list.append((latitude, longitude))

    return coordinates_list

# Provide the path to the XML file
file_path = 'datasets\shelterinfo.kml'
coordinates_data = extract_coordinates(file_path)

# Output coordinates data to a JSON file
output_file_path = 'shelter_coordinates.json'
with open(output_file_path, 'w') as json_file:
    json.dump(coordinates_data, json_file, indent=4)

print(f"Coordinates data has been saved to '{output_file_path}'.")