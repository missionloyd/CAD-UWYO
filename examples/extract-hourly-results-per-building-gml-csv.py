import xml.etree.ElementTree as ET
import pandas as pd
from datetime import datetime, timedelta

# Parse the XML file
tree = ET.parse('output/results.gml')  # Update this with your actual file path
root = tree.getroot()

# Define namespaces
ns = {
    'core': 'http://www.opengis.net/citygml/2.0',
    'bldg': 'http://www.opengis.net/citygml/building/2.0',
    'energy': 'http://www.sig3d.org/citygml/2.0/energy/1.0'
}

# Initialize list for dataframes
dataframes = []
start_ts = datetime(2024, 1, 1)
time_increment = timedelta(hours=1)

# Iterate over each cityObjectMember
for cityObjectMember in root.findall('core:cityObjectMember', ns):
    building = cityObjectMember.find('bldg:Building', ns)
    if building is not None:
        building_id = building.get('{http://www.opengis.net/gml}id')
        usage_zone = cityObjectMember.find('.//energy:UsageZone', ns)
        if usage_zone is not None:
            number_of_occupants = usage_zone.find('.//energy:numberOfOccupants', ns)
            if number_of_occupants is not None:
                number_of_occupants_value = int(number_of_occupants.text)
            else:
                number_of_occupants_value = None
            
            dhw_facilities = usage_zone.find('.//energy:DHWFacilities', ns)
            if dhw_facilities is not None:
                time_series_schedule = dhw_facilities.find('.//energy:TimeSeriesSchedule', ns)
                if time_series_schedule is not None:
                    regular_time_series = time_series_schedule.find('.//energy:RegularTimeSeries', ns)
                    if regular_time_series is not None:
                        values = regular_time_series.find('.//energy:values', ns)
                        if values is not None:
                            value_list = values.text.split()
                            value_list = [float(v) for v in value_list]
                            df = pd.DataFrame(value_list, columns=[building_id])

                                                        # Prepare the dataframe
                            df = pd.DataFrame(value_list, columns=['value'])
                            df['asset_id'] = building_id
                            df['commodity_id'] = 1
                            df['ts'] = [start_ts + i * time_increment for i in range(len(value_list))]
                            df['is_prediction'] = 't'
                            # df['numberOfOccupants'] = number_of_occupants_value

                            # Reorder columns
                            df = df[['asset_id', 'commodity_id', 'ts', 'is_prediction', 'value']]
                            dataframes.append(df)

# Print or save the dataframes as needed
# for df in dataframes:
#   print(df)
all_data = pd.concat(dataframes, ignore_index=True)
print(all_data)
all_data.to_csv('output/measurement.csv', sep='|', index=False)