import pandas as pd

# Step 1: Load Data
existing_shops = pd.read_csv(r'E:\Bizlocation Project\Bizlocation\Existing_shops.csv')
landmarks = pd.read_csv(r'E:\Bizlocation Project\Bizlocation\Landmarks.csv')
available_shops = pd.read_csv(r'e:\Bizlocation Project\Bizlocation\Available_shops.csv')


#define function calculate_distance
from math import radians, sin, cos, sqrt, atan2

def calculate_distance(location1, location2):
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1 = radians(location1['Latitude'])
    lon1 = radians(location1['Longitude'])
    lat2 = radians(location2['Latitude'])
    lon2 = radians(location2['Longitude'])
    
    # Haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    
    return distance

# define function 
from math import radians, sin, cos, sqrt, atan2

def calculate_competition_score(location, existing_shops, radius=1.0):
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1 = radians(location['Latitude'])
    lon1 = radians(location['Longitude'])
    
    # Count the number of existing shops within the competition radius
    competition_count = 0
    for index, shop in existing_shops.iterrows():
        lat2 = radians(shop['Latitude'])
        lon2 = radians(shop['Longitude'])
        
        # Calculate distance between potential location and existing shop
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        
        # Check if existing shop is within the competition radius
        if distance <= radius:
            competition_count += 1
    
    # Calculate competition score (inverse of competition count)
    competition_score = 1 / (competition_count + 1)
    
    return competition_score



# Step 2: Define Criteria and Weights
criteria_weights = {
    'proximity_to_landmarks': 0.6,
    'competition_level': 0.4
}

# Step 3: Calculate Scores for Available Locations
scores = []
for index, location in available_shops.iterrows():
    score = 0
    for landmark_index, landmark in landmarks.iterrows():
        # Calculate distance to landmarks and assign score based on proximity
        distance = calculate_distance(location, landmark)
        score += criteria_weights['proximity_to_landmarks'] * (1 / distance)
    
    # Calculate competition level score (for example, based on number of existing shops nearby)
    competition_score = calculate_competition_score(location, existing_shops)
    score += criteria_weights['competition_level'] * competition_score
    
    scores.append((index, score))

# Step 4: Rank Available Locations
ranked_locations = sorted(scores, key=lambda x: x[1], reverse=True)

# Step 5: Filter Top Three Locations
top_three_locations = [available_shops.loc[index] for index, _ in ranked_locations[:3]]

# Step 6: Present Results
print("Top three potential locations for starting a new business:")
for location in top_three_locations:
    print(location)
