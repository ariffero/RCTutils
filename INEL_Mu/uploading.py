import pandas as pd
import requests
import json
import glob
import os
import argparse

# Parse command line arguments
parser = argparse.ArgumentParser(description='Upload inel values from CSV to the bookkeeping system.')
parser.add_argument('config_file', help='Path to the configuration JSON file')
args = parser.parse_args()

# Load configuration
with open(args.config_file, 'r') as config_file:
    config = json.load(config_file)

TOKEN = config['token']
API_URL_TEMPLATE = "https://ali-bookkeeping.cern.ch/api/runs/{}/?token={}"

# Find the latest CSV file
csv_files = sorted(glob.glob('results_*.csv'), key=os.path.getmtime)
latest_csv_file = csv_files[-1] if csv_files else None

if not latest_csv_file:
    print("No CSV files found.")
    exit(1)

# Load the CSV file
data = pd.read_csv(latest_csv_file)

# Function to update inelastic interaction rate
def update_inelastic_interaction_rate(run_number, inel_value):
    url = API_URL_TEMPLATE.format(run_number, TOKEN)
    headers = {"Content-Type": "application/json"}
    payload = {"inelasticInteractionRateAvg": inel_value}
    
    response = requests.put(url, headers=headers, data=json.dumps(payload), verify=False)
    
    if response.status_code == 200:
        print(f"Successfully updated run {run_number} with inelastic interaction rate {inel_value}")
    else:
        print(f"Failed to update run {run_number}: {response.status_code}, {response.text}")

# Iterate over the rows in the CSV and update each run
for index, row in data.iterrows():
    run_number = row['run']
    inel_value = row['inel']
    
    update_inelastic_interaction_rate(run_number, inel_value)

print("All updates completed.")

