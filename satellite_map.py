import pandas as pd
import numpy as np
import folium
import requests
import webbrowser
from folium.plugins import MarkerCluster
import os

# Read in your questionaire samples
data = pd.read_csv("resources/position_sample.csv") # Note we do not provide a sample 

# Define the bounding box for the region of interest (Southern Germany).
bbox = [47.270, 5.866, 50.517, 15.041]

YOUR_INSTANCE_ID = None
if not YOUR_INSTANCE_ID:
    raise ValueError("You need to login to sentinel hub and set your instance ID before you can use this script."
                    )

# Sentinel Hub API endpoint and request parameters
sentinel_hub_url = f"https://services.sentinel-hub.com/ogc/wms/{YOUR_INSTANCE_ID}"
params = {
    'REQUEST': 'GetMap',
    'SERVICE': 'WMS',
    'VERSION': '1.3.0',
    'LAYERS': 'TRUE-COLOR-S2-L1C',
    'FORMAT': 'image/png',
    'CRS': 'EPSG:4326',
    'BBOX': ','.join(map(str, bbox)),
    'WIDTH': 512,
    'HEIGHT': 512,
    'MAXCC': 20,
    'TIME': '2020-01-01/2024-12-31',
}

# Get the satellite image from Sentinel Hub
response = requests.get(sentinel_hub_url, params=params)
if response.status_code == 200:
    with open('resources/southern_germany.png', 'w+') as file:
        file.write(response.content)
else:
    raise ValueError(f"response was {response.status_code}. Could not download satellite data.")

# Create a folium map centered on Southern Germany
m = folium.Map(location=[48.5, 10.5], zoom_start=6)

# Add the satellite image as an overlay
folium.raster_layers.ImageOverlay(
    image='resources/southern_germany.png',
    bounds=[[47.270, 5.866], [50.517, 15.041]],
    opacity=0.6
).add_to(m)

lat = data["LocationLatitude"].iloc[2:].values
lon = data["LocationLongitude"].iloc[2:].values
points = np.array([lat, lon]).T

def generate_random_coordinates(center, radius, num_points):
    lat, lon = center
    radius_in_degrees = radius / 111  # 1 degree is approximately 111 km
    return [
        (
            lat + np.random.uniform(-radius_in_degrees, radius_in_degrees),
            lon + np.random.uniform(-radius_in_degrees, radius_in_degrees)
        )
        for _ in range(num_points)
    ]

marker_cluster = MarkerCluster().add_to(m)
for point in points:
    folium.Marker(location=point, popup=f'Point: {point}').add_to(marker_cluster)

m.save('southern_germany_map.html')

webbrowser.open('southern_germany_map.html')
webbrowser.open(f"file://{os.path.abspath('southern_germany_map.html')}")


