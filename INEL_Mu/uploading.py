import pandas as pd
import requests
import json
import argparse
import glob
import os

# Parse command line arguments
parser = argparse.ArgumentParser(description='Upload INEL values based on run data from a CSV file.')
parser.add_argument('config_file', help='Path to the configuration JSON file')
args = parser.parse_args()

# Load configuration
with open(args.config_file, 'r') as config_file:
    config = json.load(config_file)

TOKEN = config['token']
API_URL_TEMPLATE = "https://ali-bookkeeping.cern.ch/api/runs/{}/?token={}"

# Find the latest CSV file
csv_files = sorted(glob.glob(f'results_*.csv'), key=os.path.getmtime)
latest_csv_file = csv_files[-1] if csv_files else None

if not latest_csv_file or os.path.getsize(latest_csv_file) == 0:
    print("No valid CSV file found.")
    exit(1)

# Load CSV data
try:
    data = pd.read_csv(latest_csv_file)
except pd.errors.EmptyDataError:
    print(f"The CSV file '{latest_csv_file}' contains no data to parse.")
    exit(1)

# Upload function for both pp and PbPb data
def update_inelastic_interaction_rates(run_number, beam_type, values):
    url = API_URL_TEMPLATE.format(run_number, TOKEN)
    headers = {"Content-Type": "application/json"}
    
    # Construct payload based on beam type
    if beam_type == "PB82 - PB82" and {'zdcir', 'zdcir_start', 'zdcir_mid', 'zdcir_end'}.issubset(values):
        payload = {
            "inelasticInteractionRateAvg": values['zdcir'],
            "inelasticInteractionRateAtStart": values['zdcir_start'],
            "inelasticInteractionRateAtMid": values['zdcir_mid'],
            "inelasticInteractionRateAtEnd": values['zdcir_end']
        }
    elif beam_type == "PROTON - PROTON" and {'mu', 'inel'}.issubset(values):
        payload = {"inelasticInteractionRateAvg": values['inel']}
    
    response = requests.put(url, headers=headers, data=json.dumps(payload), verify=False)
    
    if response.status_code == 200:
        print(f"Successfully updated run {run_number} for beam type '{beam_type}'.")
    else:
        print(f"Failed to update run {run_number}: {response.status_code}, {response.text}")

# Process each row in the CSV file
for _, row in data.iterrows():
    run_number = row['run']
    beam_type = row['beam_type']
    
    # Prepare values based on beam type columns
    if beam_type == "PB82 - PB82":
        values = {
            'zdcir': row.get('zdcir'),
            'zdcir_start': row.get('zdcir_start'),
            'zdcir_mid': row.get('zdcir_mid'),
            'zdcir_end': row.get('zdcir_end')
        }
    elif beam_type == "PROTON - PROTON":
        values = {'mu': row.get('mu'), 'inel': row.get('inel')}
    
    # Update database with respective payload
    update_inelastic_interaction_rates(run_number, beam_type, values)

