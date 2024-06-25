import math
import geopandas as gpd
from shapely.geometry import Polygon
from shapely.ops import transform, unary_union

def add_z_to_geometry(geom, z):
    """
    Adds Z-coordinate to a 2D geometry, converting it to 3D.
    """
    def add_z_coord(x, y, z=z):
        return (x, y, z)
    return transform(add_z_coord, geom)

def assign_building_geometry_osm(df, path='./data/geojson/spaces.json', key='name'):
    # Load the GeoJSON file containing building footprints and height data
    geo_df = gpd.read_file(path)
    
    # Convert geometries to 3D using the height property
    geo_df['geometry_3d'] = geo_df.apply(lambda row: add_z_to_geometry(row['geometry'], row.get('height', 10.668)), axis=1)
    
    # Create wall geometries assuming height is divided uniformly across the height
    geo_df['wall'] = geo_df['geometry_3d']
    
    # # The floor and roof geometries could be approximations (bottom and top planes)
    geo_df['floor'] = geo_df.apply(lambda row: add_z_to_geometry(row['geometry'], 0), axis=1)
    geo_df['roof'] = geo_df['geometry_3d']
    
    # Create wall geometries by extruding the building footprint to the height
    # geo_df['wall'] = gpd.GeoSeries([None] * len(geo_df), crs=geo_df.crs)
    # geo_df['floor'] = gpd.GeoSeries([None] * len(geo_df), crs=geo_df.crs)
    # geo_df['roof'] = gpd.GeoSeries([None] * len(geo_df), crs=geo_df.crs)

    # Prepare geo_df to merge
    # geo_df = geo_df[[key, 'floor', 'wall', 'roof', 'geometry']]
    # geo_df.rename(columns={'geometry_3d': 'geometry'}, inplace=True)
    
    # Merge the geometries back into the original DataFrame
    df = df.merge(geo_df, on=key, how='inner')
    
    return df

# def assign_building_geometry_osm(df, path='./data/geojson/spaces.json', key='name'):
#     # Load the GeoJSON file containing building footprints and height data
#     geo_df = gpd.read_file(path)
    
#     # Convert geometries to 3D using the height property
#     geo_df['geometry_3d'] = geo_df.apply(lambda row: add_z_to_geometry(row['geometry'], row['height']), axis=1)
    
#     # Create wall geometries assuming height is divided uniformly across the height
#     geo_df['wall'] = geo_df['geometry_3d']
    
#     # The floor and roof geometries could be approximations (bottom and top planes)
#     geo_df['floor'] = geo_df.apply(lambda row: add_z_to_geometry(row['geometry'], 0), axis=1)
#     geo_df['roof'] = geo_df['geometry_3d']
    
#     # Prepare geo_df to merge
#     geo_df = geo_df[[key, 'floor', 'wall', 'roof', 'geometry_3d']]
#     geo_df.rename(columns={'geometry_3d': 'geometry'}, inplace=True)
    
#     # Merge the geometries back into the original DataFrame
#     df = df.merge(geo_df, on=key, how='left')
#     df = df.dropna(subset=['roof', 'floor', 'wall'])
#     return df
