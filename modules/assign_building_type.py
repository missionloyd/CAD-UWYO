# Define the mapping from the custom categories to ASHRAE standard occupancy density categories
from enerCAD.dictionaries import TYPE

category_mapping = {
    "Mechanical": "Industrial",
    "Well Housing": "Industrial",
    "Shelter": "Other",
    "Athletics Services": "Sports installations",
    "Storage/Parking": "Garage",
    "Food Facility/Merchandising/Meeting Rooms": "Restaurant",
    "Antenna/Equipment": "Industrial",
    "Special Use": "Other",
    "Parking Garage": "Garage",
    "Barn": "Other",
    "Lodging": "Hotel",
    "Storage/Vehicle Storage": "Garage",
    "Research/Classroom/Assembly": "Education",
    "Classroom/Animal Facilities/Assembly": "Education",
    "Office/Storage": "Office",
    "Food Facility": "Restaurant",
    "Residential": "Residential",
    "Shop": "Retail",
    "Stack": "Other",
    "Storage": "Garage",
    "Stack/Study Space/Conference": "Education",
    "Horse Barn": "Other",
    "Animal Facilities": "Other",
    "Garage/Storage": "Garage",
    "Classroom/Office": "Education",
    "Fleet": "Other",
    "Athletics Facilities": "Sports installations",
    "Boat Ramp": "Other",
    "Greenhouse/Office": "Commercial",
    "Laboratory/Office": "Research",
    "Office/Recreation": "Office",
    "Office/Special Use": "Office",
    "Research/Vehicle Storage/Office": "Research",
    "Exhibition/Stacks": "Other",
    "Recreation": "Sports installations",
    "Commercial": "Commercial",
    "Retail": "Retail",
    "Office/Research": "Office",
    "Communications": "Office",
    "Vehicle Storage": "Garage",
    "Greenhouse": "Commercial",
    "Clinic": "Hospital",
    "Restroom": "Other",
    "Office/Communications": "Office",
    "Other": "Other",
    "General Use/Office": "Office",
    "Office/Shop/Storage": "Office",
    "Housing": "Residential",
    "Shed": "Other",
    "Studio Space": "Education",
    "Laboratory": "Research",
    "Classroom": "Education",
    "Physical Plant O&M": "Industrial",
    "Office": "Office",
    "Storage/Special Use": "Garage",
    "Storage/Research": "Research",
    "Classroom/Office/Laboratory": "Education",
    "Communications equipment": "Industrial",
    "Assembly": "Other",
    "Research": "Research",
    "Office/Assembly": "Office",
    "Vehicle Storage/Shop": "Garage",
    "Food Facility/Office": "Restaurant",
    "Telecommunications": "Office",
    "Office/Shop": "Office",
    "Health": "Hospital",
    "Classroom/Day Care": "Education",
    "Vehicle Storage/Storage": "Garage",
    "Classroom/Office/Assembly": "Education",
    "Clinic Space/Support": "Hospital",
    "Office/Parking": "Office",
    "Garage": "Garage",
    "Outreach Classes": "Education",
}

# Function to calculate occupancy
def find_type(building_category):
    """
    Calculate the occupancy for a given space type and area in square feet, using ASHRAE standard categories.
    
    Parameters:
    building_category (str): The type of space according to custom categories.
    
    Returns:
    int: building type
    """
    # Map the custom category to an ASHRAE standard category
    if building_category in category_mapping:
        standard_category = category_mapping[building_category]
    else:
        raise ValueError(f"Category mapping missing for: {building_category}")

    # Calculate the number of occupants based on the density values
    if standard_category in TYPE:
        return TYPE[standard_category]
    else:
        raise ValueError(f"Invalid building category: '{standard_category}' is not recognized.")
 

def assign_building_type(df):
    df['building_type'] = df.apply(lambda row: find_type(row['category']), axis=1)
    return df

