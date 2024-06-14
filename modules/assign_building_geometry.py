import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
from shapely.ops import unary_union, transform

def add_z_to_geometry(geom, z):
    """
    Adds Z-coordinate to a 2D geometry, converting it to 3D.
    """
    def add_z_coord(x, y, z=z):
        return (x, y, z)

    return transform(add_z_coord, geom)

def assign_building_geometry(df):
    # Dictionary to store GeoDataFrames for each floor
    floor_geometries = {}
    building_extremes = {}

    # Load GeoJSON files for each floor and collect building extremes
    for i in range(7):  # Assuming floors 0 to 6
        path = f'./data/geojson/{i}.json'
        geo_df = gpd.read_file(path)

        # Convert geometries to 3D by adding Z-coordinate
        geo_df['geometry'] = geo_df['geometry'].apply(lambda geom: add_z_to_geometry(geom, 35 * i))

        # Update extremes and store GeoDataFrames
        for building in geo_df['UW_Building_Name'].unique():
            if building in building_extremes:
                building_extremes[building]['top'] = max(building_extremes[building]['top'], i)
                building_extremes[building]['bottom'] = min(building_extremes[building]['bottom'], i)
            else:
                building_extremes[building] = {'top': i, 'bottom': i}

        floor_geometries[i] = geo_df

    # Assign floor, wall, roof, and all geometries to the DataFrame
    df['floor'] = None
    df['wall'] = None
    df['roof'] = None
    df['geometry'] = None

    for index, row in df.iterrows():
        building_name = row['UW_Building_Name']
        if building_name in building_extremes:
            bottom_floor = building_extremes[building_name]['bottom']
            top_floor = building_extremes[building_name]['top']

            # Assign floor geometry with Z data
            df.at[index, 'floor'] = add_z_to_geometry(floor_geometries[bottom_floor][floor_geometries[bottom_floor]['UW_Building_Name'] == building_name].geometry.iloc[0], 0)

            # Assign roof geometry with Z data
            df.at[index, 'roof'] = add_z_to_geometry(floor_geometries[top_floor][floor_geometries[top_floor]['UW_Building_Name'] == building_name].geometry.iloc[0], 35 * top_floor)

            # Collect and store wall geometries as a MultiPolygon, adding Z data
            wall_geometries = [add_z_to_geometry(floor_geometries[i][floor_geometries[i]['UW_Building_Name'] == building_name].geometry.iloc[0], 35 * i) for i in range(bottom_floor, top_floor + 1) if not floor_geometries[i][floor_geometries[i]['UW_Building_Name'] == building_name].empty]
            combined_geometry = unary_union(wall_geometries)  # Combining all geometries into one MultiPolygon
            df.at[index, 'wall'] = combined_geometry
            df.at[index, 'geometry'] = combined_geometry  # Ensure this is updated as well

    return df
