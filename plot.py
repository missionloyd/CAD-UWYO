import os
import pandas as pd
from datetime import datetime, timedelta
import matplotlib.pyplot as plt

app_path = './app'

if os.path.exists(app_path) and os.path.isdir(app_path):
  os.chdir(app_path)

path = os.getcwd()

measurement_type_ids = {
  'Consumption': 1,
  'Heating': 6,
  'Cooling': 7
}

inv_measurement_type_ids = {v: k for k, v in measurement_type_ids.items()}

# Read in the files
assets = pd.read_csv(f'{path}/input_data/asset.csv', sep='|')
data = pd.read_csv(f'{path}/output_data/data_TH.out', sep='\t')

# Create output plot directory if it doesn't exist
plot_dir = f'{path}/output_data/plots'
if not os.path.exists(plot_dir):
  os.makedirs(plot_dir)

# Initialize variables
start_ts = datetime(2022, 1, 1)
time_increment = timedelta(hours=1)

# Separate columns for Heating and Cooling
consumption_columns = [col for col in data.columns if 'ElectricConsumption(kWh)' in col]
heating_columns = [col for col in data.columns if 'Heating(Wh)' in col]
cooling_columns = [col for col in data.columns if 'Cooling(Wh)' in col]

# Create separate dataframes for Heating and Cooling
consumption_data = data[consumption_columns].copy()
heating_data = data[heating_columns].copy()
cooling_data = data[cooling_columns].copy()

# Initialize lists to store results
consumption_rows = []
heating_rows = []
cooling_rows = []

# Process each row in the TSV data
for index, row in data.iterrows():
  current_ts = start_ts + index * time_increment
  
  for col in consumption_columns:
    building_id = col.split('(')[0]
    consumption_rows.append({
      'asset_id': building_id,
      'measurement_type_id': measurement_type_ids['Consumption'],
      'measurement_prediction_type_id': 1,
      'ts': current_ts,
      'value': row[col] # Already in kWh
    })

  for col in heating_columns:
    building_id = col.split('(')[0]
    heating_rows.append({
      'asset_id': building_id,
      'measurement_type_id': measurement_type_ids['Heating'],
      'measurement_prediction_type_id': 1,
      'ts': current_ts,
      'value': row[col] / 1000  # Convert Wh to kWh
    })
  
  for col in cooling_columns:
    building_id = col.split('(')[0]
    cooling_rows.append({
      'asset_id': building_id,
      'measurement_type_id': measurement_type_ids['Cooling'],
      'measurement_prediction_type_id': 1,
      'ts': current_ts,
      'value': row[col] / 1000  # Convert Wh to kWh
    })


# Convert lists to dataframes
consumption_df = pd.DataFrame(consumption_rows)
heating_df = pd.DataFrame(heating_rows)
cooling_df = pd.DataFrame(cooling_rows)

# Combine the dataframes
combined_df = pd.concat([consumption_df, heating_df, cooling_df], ignore_index=True)
combinded_df_month = combined_df.copy()

# Truncate dates to month and sum values
combinded_df_month['month'] = combinded_df_month['ts'].dt.to_period('M')
monthly_sum_df = combinded_df_month.groupby(['asset_id', 'measurement_type_id', 'month']).agg({'value': 'sum'}).reset_index()

# Plot each asset and save the plots
for asset_id, asset_group in monthly_sum_df.groupby('asset_id'):
  asset_name = assets.loc[assets['id'] == int(asset_id), 'name'].values[0]
  asset_name_fixed = asset_name.replace(' ', '_')
  plt.figure()
  for measurement_type_id, commodity_group in asset_group.groupby('measurement_type_id'):
    color = 'red' if measurement_type_id == 6 else 'blue' if measurement_type_id == 7 else 'gold' if measurement_type_id == 1 else 'gray'
    label = 'Heating' if measurement_type_id == 6 else 'Cooling' if measurement_type_id == 7 else 'Consumption' if measurement_type_id == 1 else 'Unknown'
    plt.plot(commodity_group['month'].astype(str), commodity_group['value'], marker='o', color=color, label=f'{label} Sum')
    
    # Calculate and plot the average value
    average_value = commodity_group['value'].mean()
    plt.axhline(y=average_value, color=color, linestyle='--', label=f'{label} Average')
  
  plt.title(f'{asset_name}')
  plt.xlabel('Month')
  plt.ylabel('Value (kWh)')
  plt.xticks(rotation=45)
  plt.legend()
  plt.tight_layout()
  plt.savefig(f'{path}/output_data/plots/{asset_name_fixed}.png')
  plt.close()

# Save the combined dataframe as a CSV file
combined_df.to_csv(f'{path}/output_data/citysim_prediction_measurement.csv', sep='|', index=False)

print('\nPlots saved to output_data/plots...')
print('\nSuccess...')