import pandas as pd
from datetime import datetime, timedelta

# Define the file path
file_path = 'output/output_TH.tsv'

# Read the TSV file
data = pd.read_csv(file_path, sep='\t')

# Initialize variables
start_ts = datetime(2024, 1, 1)
time_increment = timedelta(hours=1)

# Separate columns for Heating and Cooling
heating_columns = [col for col in data.columns if 'Heating(Wh)' in col]
cooling_columns = [col for col in data.columns if 'Cooling(Wh)' in col]

# Create separate dataframes for Heating and Cooling
heating_data = data[heating_columns].copy()
cooling_data = data[cooling_columns].copy()

# Initialize lists to store results
heating_rows = []
cooling_rows = []

# Process each row in the TSV data
for index, row in data.iterrows():
    current_ts = start_ts + index * time_increment
    
    for col in heating_columns:
        building_id = col.split('(')[0]
        heating_rows.append({
            'asset_id': building_id,
            'commodity_id': 6,
            'ts': current_ts,
            'is_prediction': 't',
            'value': row[col] / 1000  # Convert Wh to kWh
        })
    
    for col in cooling_columns:
        building_id = col.split('(')[0]
        cooling_rows.append({
            'asset_id': building_id,
            'commodity_id': 7,
            'ts': current_ts,
            'is_prediction': 't',
            'value': row[col] / 1000  # Convert Wh to kWh
        })

# Convert lists to dataframes
heating_df = pd.DataFrame(heating_rows)
cooling_df = pd.DataFrame(cooling_rows)

# Combine the dataframes
combined_df = pd.concat([heating_df, cooling_df], ignore_index=True)

# Save the combined dataframe as a CSV file
combined_df.to_csv('output/measurement.csv', sep='|', index=False)

# Print or display the combined dataframe for verification
print(combined_df.head())
