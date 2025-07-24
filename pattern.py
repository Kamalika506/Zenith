import pandas as pd

# Read the CSV data
df = pd.read_csv('Templates/traffic_data.csv')

# Convert the 'DateTime' column to datetime format
df['Hour'] = pd.to_datetime(df['DateTime'], format="%d-%m-%Y %H:%M")

# Group the data by lane and hour of the day, and calculate the average number of vehicles
traffic_patterns = df.groupby([df['Lane'], df['Hour'].dt.hour])['Vehicles'].mean()

# Identify the times of day when traffic is heaviest for each lane
heaviest_traffic = traffic_patterns.groupby('Lane').idxmax()

# Write the traffic patterns to a new CSV file
traffic_patterns.reset_index().to_csv('pattern.csv', index=False)

#print("Traffic avg: ", traffic_patterns)
print("Peak hours: ", heaviest_traffic)
print("Traffic avg have been written to pattern.csv")




import matplotlib.pyplot as plt
import seaborn as sns

# Convert the traffic_patterns DataFrame to a format that's easier to plot
df_plot = traffic_patterns.reset_index()
df_plot.columns = ['Lane', 'Hour', 'Average Vehicles']

# Create a bar plot
plt.figure(figsize=(8, 4))
sns.barplot(x='Hour', y='Average Vehicles', hue='Lane', data=df_plot)

plt.title('Average Number of Vehicles for Each Lane at Each Hour of the Day')
plt.xlabel('Hour of the Day')
plt.ylabel('Average Number of Vehicles')
plt.legend(title='Lane')

plt.show()

plt.savefig('static/plot.png')  # Save the plot as an image
