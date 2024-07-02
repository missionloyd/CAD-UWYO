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
}

# building type : minimum ambient temperature [°C] (int)
TEMPERATURE = {
    "1": 20,  # Residential
    "2": 20,  # Office
    "3": 15,  # Garage (assuming a value since it wasn't provided)
    "4": 20,  # Commercial
    "5": 20,  # Restaurant
    "6": 20,  # Hotel
    "7": 22,  # Hospital
    "8": 20,  # Education
    "9": 18,  # Industrial
    "10": 18,  # Other (assign a reasonable default)
    "11": 18,  # Sports installations
}