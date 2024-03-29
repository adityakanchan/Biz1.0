import pandas as pd
from math import radians, sin, cos, sqrt, atan2
import folium

# Function to calculate distance between two geographic coordinates
def calculate_distance(lat1, lon1, lat2, lon2):
    # Radius of the Earth in kilometers
    R = 6371.0
    
    # Convert latitude and longitude from degrees to radians
    lat1_rad, lon1_rad = radians(lat1), radians(lon1)
    lat2_rad, lon2_rad = radians(lat2), radians(lon2)
    
    # Calculate the differences
    dlon = lon2_rad - lon1_rad
    dlat = lat2_rad - lat1_rad
    
    # Haversine formula
    a = sin(dlat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    
    return distance

# Function to calculate distance to landmarks
def calculate_distance_to_landmarks(shop, landmarks):
    shop_lat, shop_lon = shop['Latitude'], shop['Longitude']
    distances = []
    for _, landmark in landmarks.iterrows():
        landmark_lat, landmark_lon = landmark['Latitude'], landmark['Longitude']
        distance = calculate_distance(shop_lat, shop_lon, landmark_lat, landmark_lon)
        distances.append(distance)
    return distances

# Prompt user for input
interested_business = input("Enter your interested type of business: ")

# Step 1: Load Data
existing_shops = pd.read_csv(r'E:\Bizlocation Project\biz2.0\py-app\Existing_shops.csv')
landmarks = pd.read_csv(r'E:\Bizlocation Project\biz2.0\py-app\Landmarks.csv')
available_shops = pd.read_csv(r'E:\Bizlocation Project\biz2.0\py-app\Available_shops.csv')

# Step 2: Filter Existing Shops based on user's interested business
filtered_existing_shops = existing_shops[existing_shops['TYPE'] == interested_business]

# Step 3: Calculate Distances for Existing Shops
existing_scores = []
for _, existing_shop in filtered_existing_shops.iterrows():
    # Calculate distance to landmarks
    existing_score = calculate_distance_to_landmarks(existing_shop, landmarks)
    existing_scores.append(existing_score)
print(existing_scores)
# Step 4: Calculate Distances for Available Shops
available_scores = []
for _, available_shop in available_shops.iterrows():
    # Calculate distance to landmarks
    available_score = calculate_distance_to_landmarks(available_shop, landmarks)
    available_scores.append(available_score)

# Step 5: Perform Landmark Calculations
# For demonstration purposes, let's assume a simple ranking based on the sum of distances to landmarks
existing_scores_sum = [sum(distances) for distances in existing_scores]
available_scores_sum = [sum(distances) for distances in available_scores]

# Rank available shops based on the calculated scores
sorted_available_shops_indices = sorted(range(len(available_scores_sum)), key=lambda k: available_scores_sum[k])

# Select top 3 potential locations
top_three_indices = sorted_available_shops_indices[:3]
top_three_locations = [available_shops.loc[index] for index in top_three_indices]

# Create a Folium map
m = folium.Map(location=[top_three_locations[0]['Latitude'], top_three_locations[0]['Longitude']], zoom_start=12)

# Add markers for each location
for location in top_three_locations:
    folium.Marker(
        location=[location['Latitude'], location['Longitude']],
        popup=f"{interested_business} Business Location",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)

# Save the map to an HTML file
m.save('top_three_locations_map.html')