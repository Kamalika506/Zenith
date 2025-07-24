#CONGESTION RATE FOR EVERY HOUR,HOTSPOT,HIGH CONGESTION LANE
import pandas as pd

# Read the CSV file into a DataFrame
df = pd.read_csv('traffic_data.csv', parse_dates=['DateTime'], dayfirst=True)

# Convert the DateTime column to datetime format
df['Hour'] = pd.to_datetime(df['DateTime'], format='%d-%m-%Y %H:%M')

# Group by hour and lane, and calculate the average congestion rate for each hour
hourly_congestion = df.groupby([df['Hour'].dt.hour, 'Lane']).agg({'Vehicles': 'sum'}).reset_index()

max_capacity = 80

# Add a new column for congestion rate
hourly_congestion['Congestion Rate'] = hourly_congestion['Vehicles'] / max_capacity

# Identify the congestion hotspot time and lane
congestion_hotspot = hourly_congestion.loc[hourly_congestion['Congestion Rate'].idxmax()]

# Write the results to a new CSV file
hourly_congestion.to_csv('congestion_rates.csv', index=False)

print("Congestion rates have been written to congestion_rates.csv")
print(f"Congestion hotspot time: {congestion_hotspot['Hour']}")
print(f"Lane with highest congestion rate: {congestion_hotspot['Lane']}")

# Function to find lane with least congestion rate at a specified hour
def least_congested_lane(hour):
    hour_congestion = hourly_congestion[hourly_congestion['Hour'] == hour]
    least_congested_lane = hour_congestion.loc[hour_congestion['Congestion Rate'].idxmin()]
    return least_congested_lane['Lane']

# Get user input for hour
hour_input = int(input("Enter the railway time (0-23): "))

# Find least congested lane at the specified hour
least_congested_lane = least_congested_lane(hour_input)
print(f"The least congested lane at hour {hour_input} is Lane {least_congested_lane}")
