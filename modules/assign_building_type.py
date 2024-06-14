# Define the mapping from the custom categories to ASHRAE standard occupancy density categories
category_mapping = {
    "Mechanical": "Office Space",
    "Well Housing": "General Use/Office",
    "Shelter": "Office Space",
    "Athletics Services": "Athletic Service and Recreation facility",
    "Storage/Parking": "Storage",
    "Food Facility/Merchandising/Meeting Rooms": "Multi-use Cafeteria/Dining",
    "Antenna/Equipment": "Office Space",
    "Special Use": "Assembly Facilities (Conference, dining, gym)",
    "Parking Garage": "Parking",
    "Barn": "Storage",
    "Lodging": "Lounge-Public Assembly Lobbies",
    "Storage/Vehicle Storage": "Storage",
    "Research/Classroom/Assembly": "Laboratories",
    "Classroom/Animal Facilities/Assembly": "Classroom",
    "Office/Storage": "Office Space",
    "Food Facility": "Multi-use Cafeteria/Dining",
    "Residential": "Residential TEDI",
    "Shop": "Shop Facilities",
    "Stack": "Storage",
    "Storage": "Storage",
    "Stack/Study Space/Conference": "Library",
    "Horse Barn": "Storage",
    "Animal Facilities": "Laboratories",
    "Garage/Storage": "Storage",
    "Classroom/Office": "Classroom",
    "Fleet": "Garage",
    "Athletics Facilities": "Athletic Service and Recreation facility",
    "Boat Ramp": "General Use/Office",
    "Greenhouse/Office": "Office Space",
    "Laboratory/Office": "Laboratories",
    "Office/Recreation": "Office Space",
    "Office/Special Use": "Office Space",
    "Research/Vehicle Storage/Office": "Laboratories",
    "Exhibition/Stacks": "Exhibition Facilities (museum)",
    "Recreation": "Athletic Service and Recreation facility",
    "Commercial": "Retail",
    "Retail": "Retail",
    "Office/Research": "Office Space",
    "Communications": "Office Space",
    "Vehicle Storage": "Garage",
    "Greenhouse": "Special Use",
    "Clinic": "Clinic",
    "Restroom": "Public Restroom",
    "Office/Communications": "Office Space",
    "Agricultural Facilities": "Special Use",
    "General Use/Office": "Office Space",
    "Office/Shop/Storage": "Office Space",
    "Housing": "Residential TEDI",
    "Shed": "Storage",
    "Studio Space": "Office Space",
    "Laboratory": "Laboratories",
    "Classroom": "Classroom",
    "Physical Plant O&M": "Office Space",
    "Office": "Office Space",
    "Storage/Special Use": "Storage",
    "Storage/Research": "Storage",
    "Classroom/Office/Laboratory": "Classroom",
    "Communications equipment": "Office Space",
    "Assembly": "Assembly Facilities (Conference, dining, gym)",
    "Research": "Laboratories",
    "Office/Assembly": "Office Space",
    "Vehicle Storage/Shop": "Garage",
    "Food Facility/Office": "Multi-use Cafeteria/Dining",
    "Telecommunications": "Office Space",
    "Office/Shop": "Office Space",
    "Health": "Clinic",
    "Classroom/Day Care": "Daycare",
    "Vehicle Storage/Storage": "Garage",
    "Classroom/Office/Assembly": "Classroom",
    "Clinic Space/Support": "Clinic",
    "Office/Parking": "Office Space",
    "Garage": "Garage",
    "Outreach Classes": "Classroom"
    }

TYPE = {
    "Office Space": 2,  # Originally 5, changed to match 'Office' from first dictionary
    "Conference Room": 6,  # Assuming similar to 'Hotel'
    "Library": 8,  # Assuming similar to 'Education'
    "Study Sleep/Dormitory Bedroom": 8,  # Assuming similar to 'Education'
    "Daycare": 1,  # Assuming similar to 'Residential'
    "Multi-use Cafeteria/Dining": 5,  # Assuming similar to 'Restaurant'
    "Exhibition Facilities": 7,  # Assuming similar to 'Hospital' (public space)
    "Locker room": 1,  # Assuming minimal usage, similar to less frequent residential types
    "Data Processing": 10,  # Assuming similar to 'Other'
    "Nurses Station, Surgery, Healthcare": 7,  # Assuming similar to 'Hospital'
    "Athletic Service and Recreation facility": 11,  # Assuming similar to 'Sports installations'
    "Storage": 10,  # Assuming similar to 'Other'
    "Assembly Facilities (Conference, dining, gym)": 6,  # Assuming similar to 'Hotel'
    "Parking": 10,  # Assuming similar to 'Other'
    "Lounge-Public Assembly Lobbies": 5,  # Assuming similar to 'Restaurant'
    "Laboratories": 8,  # Assuming similar to 'Education'
    "Classroom": 8,  # Assuming similar to 'Education'
    "Shop Facilities": 4,  # Assuming similar to 'Commercial'
    "Residential TEDI": 1,  # Assuming similar to 'Residential'
    "Retail": 4,  # Assuming similar to 'Commercial'
    "Clinic": 7,  # Assuming similar to 'Hospital'
    "Public Restroom": 10,  # Assuming similar to 'Other'
    "Special Use": 10,  # Assuming similar to 'Other'
    "Exhibition Facilities (museum)": 7  # Assuming similar to 'Hospital'
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

