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

# UTM Zone 13N for Laramie, Wyoming
def assign_building_geometry_osm(df, path='./data/geojson/spaces.json', key='name', crs='EPSG:32613'):
    # Load the GeoJSON file containing building footprints and height data
    geo_df = gpd.read_file(path)

    # Set crs
    geo_df['geometry'] = geo_df['geometry'].to_crs(crs)
    
    # Create wall geometries by extruding the building footprint to the height
    geo_df['wall'] = gpd.GeoSeries([None] * len(geo_df), crs=crs)
    geo_df['floor'] = gpd.GeoSeries([None] * len(geo_df), crs=crs)
    geo_df['roof'] = gpd.GeoSeries([None] * len(geo_df), crs=crs)
    
    # Merge the geometries back into the original DataFrame
    df = df.merge(geo_df, on=key, how='inner')
    return df