import json
from shapely.geometry import shape

# Read the geojson file
with open('asset_geometry.geojson', 'r') as file:
    geojson_data = json.load(file)

# Initialize an empty list to store all WKT geometries
all_geometries = []

# Loop through each feature in the geojson
for feature in geojson_data['features']:
    # Convert the geometry of each feature to a shapely geometry
    geometry = shape(feature['geometry'])
    # Append the WKT representation of the geometry to the list
    all_geometries.append(geometry.wkt)

# Concatenate all geometries into a single string
big_wkt = ''.join(all_geometries)

# Open a new file to store the big WKT data
with open('output.wkt', 'w') as wkt_file:
    # Write the single big WKT string to the file
    wkt_file.write(big_wkt)
