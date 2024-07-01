import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from shapely.ops import transform, unary_union

def add_z_to_geometry(geom, z):
    """
    Adds Z-coordinate to a 2D geometry, converting it to 3D.
    """
    def add_z_coord(x, y, z=z):
        return (x, y, z)
    return transform(add_z_coord, geom)

def extrude(geom, height):
    """
    Creates 3D wall geometry by extruding the 2D geometry to the given height.
    """
    if geom.is_empty or height == 0:
        return geom
    base = [(x, y, 0) for x, y in geom.exterior.coords]
    top = [(x, y, height) for x, y in geom.exterior.coords]
    wall_polygons = []
    for i in range(len(base)-1):
        wall_polygons.append(Polygon([base[i], base[i+1], top[i+1], top[i]]))
    return unary_union(wall_polygons)

def combine_geometries(floor, wall, roof):
    """
    Combines floor, wall, and roof geometries into a single MultiPolygon.
    """
    return unary_union([floor, wall, roof])

def assign_building_geometry_osm(df, path='./data/geojson/spaces.json', key='name'):
    # Load the GeoJSON file containing building footprints and height data
    geo_df = gpd.read_file(path)

    # Create floor, wall, and roof geometries
    geo_df['floor'] = geo_df.apply(lambda row: add_z_to_geometry(row['geometry'], 0), axis=1)
    geo_df['wall'] = geo_df.apply(lambda row: extrude(row['geometry'], row['height']), axis=1)
    geo_df['roof'] = geo_df.apply(lambda row: add_z_to_geometry(row['geometry'], row['height']), axis=1)
    
    # Combine floor, wall, and roof into a single geometry column
    geo_df['geometry'] = geo_df.apply(lambda row: combine_geometries(row['floor'], row['wall'], row['roof']), axis=1)

    print(geo_df['geometry'])
    # Merge the geometries back into the original DataFrame
    df = df.merge(geo_df[[key, 'floor', 'wall', 'roof', 'geometry']], on=key, how='left')
    df = df.dropna(subset=['geometry'])
    
    return df
