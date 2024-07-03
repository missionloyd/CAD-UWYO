# -*- coding: utf-8 -*-
"""
Created on Fri Jun 16 17:16:28 2023

@author: Olivier Chavanne

Modified June 2024
@author: Luke Macy
"""
from modules.create_building_dataframe import create_building_dataframe
from modules. assign_building_geometry_osm import  assign_building_geometry_osm
from modules.assign_building_type import assign_building_type

import geopandas as gpd
import pandas as pd
from shapely import box
from shapely.ops import unary_union
import os
import matplotlib.pyplot as plt
from shapely import wkt

# Local libraries
from enerCAD.building import generate_envelope
from enerCAD.building import generate_buildings
import enerCAD.xml as xml
import enerCAD.result as result
import enerCAD.network as network
import enerCAD.production as prod
import enerCAD.KPI as KPI

# URL for RegBL API request
GEOADMIN_BASE_URL = "https://api.geo.admin.ch/rest/services/ech/MapServer/ch.bfs.gebaeude_wohnungs_register/"

def create_xml_root(xml_file_to_copy, climate_file, horizon_file):
    '''
    Parameters                                                          
    ----------
    xml_file_to_copy : TYPE
        DESCRIPTION.
    climate_file : TYPE
        DESCRIPTION.
    horizon_file : TYPE
        DESCRIPTION.

    Returns
    -------
    root : TYPE
        DESCRIPTION.
    district : TYPE
        DESCRIPTION.
    '''
    
    # Write XML file for CitySim :
    print("Writing XML file...")    
    # Add Root 
    root = xml.add_root()
    # Add Simulation days
    xml.add_simulation_days(root)
    # Add Climate
    # xml.add_climate(root, climate_file)
    # Add District
    district = xml.add_district(root)
    
    # Horizon
    # read in the tab-separated file as a dataframe
    # horizon_df = pd.read_csv(horizon_file)    
    # assign column names to the dataframe
    # horizon_df.rename(columns={'latitude': 'phi', 'longitude': 'theta'}, inplace=True)
    # Add Far field obstructions
    # xml.add_far_field_obstructions(district, horizon_df)
    
    # Add all the composites and profiles, taken from a source XML
    xml.add_child_from_xml_to_district(district, xml_file_to_copy, 'Composite')
    xml.add_child_from_xml_to_district(district, xml_file_to_copy, 'OccupancyDayProfile')
    xml.add_child_from_xml_to_district(district, xml_file_to_copy, 'OccupancyYearProfile')
    xml.add_child_from_xml_to_district(district, xml_file_to_copy, 'DeviceType')
    xml.add_child_from_xml_to_district(district, xml_file_to_copy, 'ActivityType')
    xml.add_child_from_xml_to_district(district, xml_file_to_copy, 'DHWDayProfile')
    xml.add_child_from_xml_to_district(district, xml_file_to_copy, 'DHWYearProfile')
    
    xml.add_child_from_xml_to_district(district, xml_file_to_copy, 'Building')
    xml.add_child_from_xml_to_district(district, xml_file_to_copy, 'DistrictEnergyCenter')
    
    print("Xml source copied")
    
    return root, district 


def Module_1(buildings_df, GEOADMIN_BASE_URL,
             directory_path, xml_name,
             xml_base_file, climate_file, horizon_file,
             create_geometry_3D=False, calculate_volume_3D=False,
             EGID_column='RegBL_EGID'):
    '''
    Parameters
    ----------
    buildings_df : TYPE
        DESCRIPTION.
    GEOADMIN_BASE_URL : TYPE
        DESCRIPTION.
    directory_path : TYPE
        DESCRIPTION.
    xml_file_to_create : TYPE
        DESCRIPTION.
    xml_base_file : TYPE
        DESCRIPTION.
    climate_file : TYPE
        DESCRIPTION.
    horizon_file : TYPE
        DESCRIPTION.
    create_geometry_3D : TYPE, optional
        DESCRIPTION. The default is False.
    calculate_volume_3D : TYPE, optional
        DESCRIPTION. The default is False.
    EGID_column : TYPE, optional
        DESCRIPTION. The default is 'RegBL_EGID'.

    Returns
    -------
    None.
    '''
    
    print("Buildings processing...")
    # try:

    # Ensure that buildings_df columns are GeoSeries
    floor_data = gpd.GeoDataFrame(buildings_df, geometry='floor')
    roof_data = gpd.GeoDataFrame(buildings_df, geometry='roof')
    wall_data = gpd.GeoDataFrame(buildings_df, geometry='wall')
    zone_all = gpd.GeoDataFrame(buildings_df, geometry='geometry').explode(index_parts=True).reset_index()

    # Filter on the zone with 10m buffer around surrounding square box 
    zone_bounds = zone_all.geometry.buffer(10).values.total_bounds
    zone_box = box(zone_bounds[0], zone_bounds[1], zone_bounds[2], zone_bounds[3])
    
    # Cut swissbuildings3D to zone of concern
    floor_data_intersection = floor_data[floor_data.geometry.intersects(zone_box)]
    roof_data_intersection = roof_data[roof_data.geometry.intersects(zone_box)]
    wall_data_intersection = wall_data[wall_data.geometry.intersects(zone_box)]

    # Split Multipolygons into Polygons
    zone_floor = floor_data_intersection.explode(index_parts=True).reset_index()
    zone_roof = roof_data_intersection.explode(index_parts=True).reset_index()
    zone_wall = wall_data_intersection.explode(index_parts=True).reset_index()
    print('Buildings cut to zone of interest \n')
    
    ### Envelope processing ###
    # try:
    #     # Get z coordinates of 1st vertex from 1st surface of 1st building's floor polygon as altitude by default for MO footprints
    #     altitude_default = zone_floor.loc[0].geometry.exterior.coords[0][2]
    # except:
    altitude_default = 0
    
    # Create DataFrames containing all necessary information for each building
    print("Creating Buildings GeoDataFrame...")
    footprints, buildings = generate_buildings(zone_all, GEOADMIN_BASE_URL, altitude_default,
                                               create_geometry_3D, calculate_volume_3D, zone_floor, zone_roof, zone_wall)
    print("Buildings GeoDataFrame created \n") 
    
    # Generate the envelope surfaces
    print("Generating Buildings envelope...")
    envelope, buildings_volume_3D, center_coordinates = generate_envelope(footprints, buildings, calculate_volume_3D)
    print("Envelope created \n")
    
    # Merge "volume_3D" and "n_occupants" to main buildings geodataframe according to 'bid'
    merged_buildings = buildings.merge(buildings_volume_3D, left_on='bid', right_on='bid', how='left')    
    if not merged_buildings.empty:
        columns_to_add = ['volume_3D', 'n_occupants']
        for column in columns_to_add:
            buildings[column] = merged_buildings[column]
        print("Buildings 3D volume calculated and merged \n")
    
    ### Buildings XML processing ###
        
    root, district = create_xml_root(xml_base_file, climate_file, horizon_file)
    
    print("Adding buildings...")
    # Add the buildings
    xml.add_all_buildings(district, buildings, envelope, center_coordinates)
        
    # Write XML file
    xml_path = os.path.join(directory_path, xml_name+".xml")     
    xml.write_xml_file(root, xml_path)
    print(f"{xml_name}.xml file created \n")
    
    return buildings

def simulate_citysim(directory_path, xml_file, citysim_filepath):
    '''
    Parameters
    ----------
    xml_file : TYPE
        DESCRIPTION.

    Returns
    -------
    None.
    '''
    
    import subprocess
    import time
    start = time.time()
    print('Process started')
    print(f'Simulation of {xml_file}.xml...')

    #run CitySim.exe with xml file
    xml_path = os.path.join(directory_path, xml_file+".xml")
    result = subprocess.run([citysim_filepath, '-q', f"{xml_path}"])
    
    end = time.time()
    duration = end - start
    m, s = divmod(duration, 60)
    print('Simulation ended. Time :', "%.0f" %m,'min', "%.0f" %s,'s \n')

##################################################
# 
#         Information to provide
#
##################################################

# Create geometry with swissbuildings3D
create_geometry_3D = True                                  

# Calculate volume from swissbuildings3D
calculate_volume_3D = True                               

# CitySim.exe filepath
citysim_filepath = r"/mnt/c/Users/Missionloyd/Downloads/CitySimPro/CitySimPro/Windows/CitySimPro.exe" #TODO

# XML name to export
directory_path = r"output"                                   

os.makedirs(directory_path, exist_ok=True)
                                      
xml_name = directory_path                                       
xml_DHN = "DHN_"+xml_name

# XML source files
xml_base_file = r"xml_base.xml"                                
climate_file = r"data/cli/UWYO.cli"                                 
horizon_file = r"data/hor/UWYO.hor"                                      

# Scenarios to simulate
scenarios_list = [1]                                  

do_plot = True

def main():
    # Call the function to create the dataframe
    building_df = create_building_dataframe()
    building_df =  assign_building_geometry_osm(building_df)
    building_df = assign_building_type(building_df)
        
    print(building_df[['name', 'building_type']])
        
        
    # Generate individual buildings XML
    # print('***Module 1*** \n')

    Module_1(building_df, GEOADMIN_BASE_URL, 
                        directory_path, xml_name,
                        xml_base_file, climate_file, horizon_file,
                        create_geometry_3D, calculate_volume_3D,
                        EGID_column='asset_id')
	
	# simulate_citysim(directory_path, xml_name, citysim_filepath)

if __name__ == "__main__":
    plt.close("all")
    
    import subprocess
    import time
    start_overall = time.time()
    print('Main code started')
    print('-----------------')
    
    main()    

    print('-----------------')
    print('Main code ended')
    print('-----------------')
    end_overall = time.time()
    duration_overall = end_overall - start_overall
    m, s = divmod(duration_overall, 60)
    print('Overall run time :', "%.0f" %m,'min', "%.0f" %s,'s \n')
