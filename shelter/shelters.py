import math

def euclidean_distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0]) ** 2 + (coord1[1] - coord2[1]) ** 2)

def find_nearest_shelter(attacking_event, available_shelters, max_distance):
    nearest_shelter = None
    min_distance = max_distance

    for shelter in available_shelters:
        distance = euclidean_distance(attacking_event, shelter)
        if distance < min_distance:
            nearest_shelter = shelter
            min_distance = distance

    return nearest_shelter

def suggest_new_shelter(attacking_events, existing_shelters, max_distance):
    new_shelter = None

    for event in attacking_events:
        nearest_shelter = find_nearest_shelter(event, existing_shelters, max_distance)
        if nearest_shelter is None:
            # If no shelter found within the max_distance, create a new shelter
            new_shelter = event
            existing_shelters.append(new_shelter)
        else:
            # Check if the new shelter is within max_distance of the nearest shelter
            if euclidean_distance(event, nearest_shelter) > max_distance:
                new_shelter = event
                existing_shelters.append(new_shelter)

    return new_shelter

# Ukrainian locations' coordinates
ukrainian_locations = [
    (50.4501, 30.5234),  # Kyiv
    (49.8397, 24.0297),  # Lviv
    (46.4825, 30.7233),  # Odessa
    (49.5500, 25.6000),  # Ternopil
    (48.9226, 24.7111),  # Ivano-Frankivsk
    (49.2331, 28.4682),  # Vinnytsia
    (48.6208, 22.2879),  # Uzhhorod
    (46.9742, 31.9948),  # Mykolaiv
    (48.4647, 35.0462),  # Dnipro
    (49.5535, 25.5948),  # Kamianets-Podilskyi

    # Additional Ukrainian locations
    (50.4000, 30.3000),  # Bila Tserkva
    (49.8333, 24.0167),  # Brody
    (48.8833, 24.7000),  # Kolomyia
    (48.7167, 26.5833),  # Khmelnytskyi
    (49.0667, 33.4167),  # Kropyvnytskyi
]

# Existing shelter locations' coordinates
shelter_locations = [
    (50.2304, 30.5103),  # Shelter near Kyiv
    (49.8412, 24.0125),  # Shelter near Lviv
    (46.4775, 30.7256),  # Shelter near Odessa
    (49.5550, 25.6000),  # Shelter near Ternopil
]

max_distance = 2  # Maximum distance for shelters to be considered nearby

for location in ukrainian_locations:
    nearest_shelter = find_nearest_shelter(location, shelter_locations, max_distance)
    if nearest_shelter is not None:
        shelter_locations.append(nearest_shelter)

new_shelter_location = suggest_new_shelter(ukrainian_locations, shelter_locations, max_distance)
if new_shelter_location:
    print("Suggested new shelter location:", new_shelter_location)

print("All shelter locations:", shelter_locations)
