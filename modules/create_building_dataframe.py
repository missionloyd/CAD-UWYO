import pandas as pd
import json

def create_building_dataframe():
    # Load the CSV files
    asset_df = pd.read_csv('./data/asset.csv', sep='|')
    metadata_df = pd.read_csv('./data/metadata.csv', sep='|')

    # Load and parse the JSON file
    with open('./data/geojson_metadata/names.json', 'r') as file:
        names_data = json.load(file)

    # Convert JSON keys to a DataFrame
    names_df = pd.DataFrame(list(names_data.items()), columns=['UW_Building_Name', 'long_name'])

    # Merge the asset and metadata dataframes on the 'id' and 'asset_id' fields
    merged_df = pd.merge(asset_df, metadata_df, left_on='id', right_on='asset_id')

    # Merge with names dataframe on 'name' from asset_df and 'long_name' from names_df
    final_df = pd.merge(merged_df, names_df, left_on='name', right_on='long_name')

    # Order by the 'name' column
    final_df.sort_values('name', inplace=True)    

    # Extract 'category', 'gross_area', 'latitude', and 'longitude' from the 'data' JSON column
    final_df['data'] = final_df['data'].apply(json.loads)  # Convert the JSON strings to dictionaries
    final_df['category'] = final_df['data'].apply(lambda x: x.get('category'))
    final_df['gross_area'] = final_df['data'].apply(lambda x: x.get('gross_area'))
    final_df['latitude'] = final_df['data'].apply(lambda x: x.get('latitude'))
    final_df['longitude'] = final_df['data'].apply(lambda x: x.get('longitude'))
    final_df['construction_year'] = final_df['data'].apply(lambda x: x.get('year_built'))
    final_df['n_floors'] = final_df['data'].apply(lambda x: x.get('floor_count'))

    # Drop unnecessary columns
    final_df.drop(columns=['active', 'tree_id', 'lft', 'rght', 'long_name', 'data'], inplace=True)
    final_df = final_df.reset_index()
    return final_df

