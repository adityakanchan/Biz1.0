# %%
import folium

# Create a map object with initial location and zoom level
mapObj = folium.Map(location=[18.51594970496859, 73.8488336933151], zoom_start=18)

# Add a marker to the map
marker = folium.Marker(
    location=[18.51594970496859, 73.8488336933151],
    popup="Kesari Wada"  # Add popup text if needed
)

# Add the marker to the map object
marker.add_to(mapObj)

# Display the map
mapObj
# %%