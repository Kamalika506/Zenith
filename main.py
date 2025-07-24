from flask import Flask, render_template, request
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

app = Flask(__name__)

# Read the CSV file into a DataFrame
df = pd.read_csv("traffic_data.csv", parse_dates=['DateTime'], dayfirst=True)

# Convert the DateTime column to datetime format
df['Hour'] = pd.to_datetime(df['DateTime'], format='%d-%m-%Y %H:%M')

# Group by hour and lane, and calculate the average congestion rate for each hour
hourly_congestion = df.groupby([df['Hour'].dt.hour, 'Lane']).agg({'Vehicles': 'sum'}).reset_index()

max_capacity = 80

# Add a new column for congestion rate
hourly_congestion['Congestion Rate'] = hourly_congestion['Vehicles'] / max_capacity

# Function to find lane with least congestion rate at a specified hour
def least_congested_lane(hour):
    hour_congestion = hourly_congestion[hourly_congestion['Hour'] == hour]
    least_congested_lane_result = hour_congestion.loc[hour_congestion['Congestion Rate'].idxmin()]
    return least_congested_lane_result['Lane']

# Group the data by lane and hour of the day, and calculate the average number of vehicles
avg_flow = df.groupby([df['Lane'], df['Hour'].dt.hour])['Vehicles'].mean()

# Function to find the peak hours for each lane
def peak_hours():
    # Identify the times of day when traffic is heaviest for each lane
    heaviest_traffic = avg_flow.groupby('Lane').idxmax()
    # Get only the hour (second element of the tuple)
    peak_hours = {lane: hour for lane, (lane_index, hour) in heaviest_traffic.items()}
    return peak_hours


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/cr', methods=['GET', 'POST'])
def congestion_rate():
    if request.method == 'POST':
        hour_input = int(request.form['hour'])
        least_congested_lane_value = least_congested_lane(hour_input)
        return render_template('result1.html', hour=hour_input, lane=least_congested_lane_value)
    return render_template('cr.html')

@app.route('/peak', methods=['GET', 'POST'])
def peak():
    if request.method == 'POST':
        peak_hours_value = peak_hours()
        return render_template('result2.html', peak_hours=peak_hours_value)
    return render_template('peak.html')

@app.route('/traffic_flow', methods=['GET', 'POST'])
def traffic_flow():
    if request.method == 'POST':
        # Convert the traffic_patterns DataFrame to a format that's easier to plot
        df_plot = avg_flow.reset_index()
        df_plot.columns = ['Lane', 'Hour', 'Average Vehicles']
        # Create a bar plot
        plt.figure(figsize=(8, 4))
        sns.barplot(x='Hour', y='Average Vehicles', hue='Lane', data=df_plot)
        plt.title('Average Number of Vehicles for Each Lane at Each Hour of the Day')
        plt.xlabel('Hour of the Day')
        plt.ylabel('Average Number of Vehicles')
        plt.legend(title='Lane')
        plt.savefig('static/plot.png')  # Save the plot as an image
        return render_template('result3.html')
    return render_template('pat.html')


if __name__ == '__main__':
    app.run(debug=True)
