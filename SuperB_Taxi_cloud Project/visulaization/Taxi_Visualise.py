#!/usr/bin/env python
# coding: utf-8

# In[1]:


import random
import folium
from folium import plugins
import matplotlib.pyplot as plt
import time

# Define the geographical boundaries (latitude and longitude)
boundary = {
    "min_lat": 40.70,  # Minimum latitude
    "max_lat": 40.80,  # Maximum latitude
    "min_lon": -74.00,  # Minimum longitude
    "max_lon": -73.90,  # Maximum longitude
}

# Initialize the map
m = folium.Map(
    location=[(boundary["min_lat"] + boundary["max_lat"]) / 2, (boundary["min_lon"] + boundary["max_lon"]) / 2],
    zoom_start=14,
)

# Create a marker for the taxi's starting position
start_location = [random.uniform(boundary["min_lat"], boundary["max_lat"]), random.uniform(boundary["min_lon"], boundary["max_lon"])]
start_marker = folium.Marker(location=start_location, icon=folium.Icon(color='blue', icon='taxi', prefix='fa'))
start_marker.add_to(m)

# Initialize a list to store the taxi's movement history
movement_history = [start_location]

# Define the number of simulation steps
num_steps = 50

# Simulate taxi movement
for _ in range(num_steps):
    # Generate random movement
    delta_lat = random.uniform(-0.001, 0.001)  # Adjust the range for latitude as needed
    delta_lon = random.uniform(-0.001, 0.001)  # Adjust the range for longitude as needed

    # Update the taxi's current location
    current_location = [
        max(boundary["min_lat"], min(boundary["max_lat"], movement_history[-1][0] + delta_lat)),
        max(boundary["min_lon"], min(boundary["max_lon"], movement_history[-1][1] + delta_lon)),
    ]

    # Add the current location to the movement history
    movement_history.append(current_location)

    # Create a marker for the current location
    current_marker = folium.Marker(location=current_location, icon=folium.Icon(color='green'))
    current_marker.add_to(m)

    # Delay to visualize movement (adjust as needed)
    time.sleep(1)

# Create a line to show the taxi's movement
movement_line = folium.PolyLine(locations=movement_history, color='red', weight=5)
movement_line.add_to(m)

# Save the map to an HTML file
m.save('taxi_movement_map.html')

# Display the map
plt.figure(figsize=(10, 10))
plugins.FastMarkerCluster([tuple(location) for location in movement_history]).add_to(m)
m.save('taxi_movement_map_clustered.html')
plt.show()


# In[2]:


import random
import folium
from folium import plugins
import matplotlib.pyplot as plt
import time


# In[3]:


import folium


# In[4]:


get_ipython().system('pip install folium')


# In[3]:


import random
import folium
from folium import plugins
import matplotlib.pyplot as plt
import time

# Define the geographical boundaries (latitude and longitude)
boundary = {
    "min_lat": 28.00,  # Minimum latitude
    "max_lat": 28.80,  # Maximum latitude
    "min_lon": 77.00,  # Minimum longitude
    "max_lon": 77.90,  # Maximum longitude
}

# Initialize the map
m = folium.Map(
    location=[(boundary["min_lat"] + boundary["max_lat"]) / 2, (boundary["min_lon"] + boundary["max_lon"]) / 2],
    zoom_start=14,
)

# Create a marker for the taxi's starting position
start_location = [random.uniform(boundary["min_lat"], boundary["max_lat"]), random.uniform(boundary["min_lon"], boundary["max_lon"])]
start_marker = folium.Marker(location=start_location, icon=folium.Icon(color='blue', icon='taxi', prefix='fa'))
start_marker.add_to(m)

# Initialize a list to store the taxi's movement history
movement_history = [start_location]

# Define the number of simulation steps
num_steps = 30

# Simulate taxi movement
for _ in range(num_steps):
    # Generate random movement
    delta_lat = random.uniform(-0.01, 0.01)  # Adjust the range for latitude as needed
    delta_lon = random.uniform(-0.01, 0.01)  # Adjust the range for longitude as needed

    # Update the taxi's current location
    current_location = [
        max(boundary["min_lat"], min(boundary["max_lat"], movement_history[-1][0] + delta_lat)),
        max(boundary["min_lon"], min(boundary["max_lon"], movement_history[-1][1] + delta_lon)),
    ]

    # Add the current location to the movement history
    movement_history.append(current_location)

    # Create a marker for the current location
    current_marker = folium.Marker(location=current_location, icon=folium.Icon(color='green'))
    current_marker.add_to(m)

    # Delay to visualize movement (adjust as needed)
    time.sleep(1)

# Create a line to show the taxi's movement
movement_line = folium.PolyLine(locations=movement_history, color='red', weight=5)
movement_line.add_to(m)

# Save the map to an HTML file
m.save('taxi_movement_map.html')

# Display the map
plt.figure(figsize=(10, 10))
plugins.FastMarkerCluster([tuple(location) for location in movement_history]).add_to(m)
m.save('taxi_movement_map_clustered.html')
plt.show()


# In[ ]:





# In[ ]:




