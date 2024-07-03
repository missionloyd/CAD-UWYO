# building type
TYPE = {
    "Residential": 1,
    "Office": 2,
    "Garage": 3,
    "Commercial": 4,
    "Restaurant": 5,
    "Hotel": 6,
    "Hospital": 7,
    "Education": 8,
    "Industrial": 9,
    "Other": 10,
    "Sports installations": 11,
    "Research": 12,
}

# year : (WallType, RoofType, FloorType, Ninf, glazing_Uvalue, glazing_Gvalue, glazing_ratio) (tuple)
THRESHOLDS = {
    1980: (456, 445, 10, 1.4, 2.3, 0.47, 0.25),
    2004: (457, 447, 10, 1.3, 2.3, 0.47, 0.25),
    2007: (458, 446, 10, 1.2, 2.3, 0.47, 0.25),
    2013: (449, 447, 10, 1.1, 2.3, 0.47, 0.25),
    2020: (3004, 447, 10, 1.0, 2.3, 0.47, 0.25),
}

# building type : SIA Surface [m2]/person (int)
SURFACE = {
    "1": 50,   # Residential
    "2": 20,   # Office
    "3": 30,   # Garage (assuming a value since it wasn't provided)
    "4": 10,   # Commercial
    "5": 5,    # Restaurant
    "6": 40,   # Hotel
    "7": 30,   # Hospital
    "8": 10,   # Education
    "9": 20,   # Industrial
    "10": 15,  # Other (assign a default or calculated value)
    "11": 20,  # Sports installations
    "12": 10,  # Research
}

# building type : maximum ambient temperature [°C] (int)
TEMPERATURE = {
    "1": 26,  # Residential - Comfortable living conditions
    "2": 24,  # Office - Standard office comfort
    "3": 30,  # Garage - Less controlled, generally higher
    "4": 25,  # Commercial - Retail spaces
    "5": 24,  # Restaurant - Comfort for dining
    "6": 24,  # Hotel - Guest comfort
    "7": 22,  # Hospital - Stringent for patient care
    "8": 23,  # Education - Suitable for learning environments
    "9": 28,  # Industrial - Can vary widely, set higher due to machinery
    "10": 25,  # Other - Default for miscellaneous buildings
    "11": 26,  # Sports installations - Comfort for physical activity
    "12": 23,  # Research - Controlled environments, similar to education
}

# building type : Occupancy Year Profile IDs with string keys (int)
OCCUPANTS = {
    "1": 0,  # Residential
    "2": 1,  # Office
    "3": 0,  # Garage (assuming minimal occupancy similar to residential off-day profile)
    "4": 0,  # Commercial (generic low occupancy)
    "5": 3,  # Restaurant
    "6": 0,  # Hotel
    "7": 0,  # Hospital
    "8": 2,  # Education
    "9": 0,  # Industrial
    "10": 0, # Other
    "11": 3, # Sports installations
    "12": 4, # Research
}