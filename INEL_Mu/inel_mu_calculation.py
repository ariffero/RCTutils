import requests
import json
import pandas as pd
import re
import numpy as np
import subprocess
import datetime
import pytz
import os
import argparse

# Suppress the InsecureRequestWarning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Define timezone objects
utc = pytz.UTC
cet = pytz.timezone('CET')

# Parse command line arguments
parser = argparse.ArgumentParser(description='Process run data and save results to a CSV file.')
parser.add_argument('config_file', help='Path to the configuration JSON file')
args = parser.parse_args()

# Load configuration
with open(args.config_file, 'r') as config_file:
    config = json.load(config_file)

TOKEN = config['token']
MIN_RUN_NUMBER = config['min_run_number']
EXCLUDE_RUNS = config['exclude_runs']
BEAM_ENERGY_MAPPING = config['beam_energy_mapping']  # Load the beam energy mapping

# Define the cache file path
CACHE_FILE = 'run_cache.json'

# Function to load cached run numbers
def load_cache():
    if os.path.exists(CACHE_FILE):
        with open(CACHE_FILE, 'r') as f:
            return json.load(f)
    return []

# Function to save run numbers to cache
def save_cache(run_numbers):
    with open(CACHE_FILE, 'w') as f:
        json.dump(run_numbers, f, indent=4)

# Step 1: Retrieve the JSON data
url = f"https://ali-bookkeeping.cern.ch/api/runs?filter[definitions]=PHYSICS&page[offset]=0&filter[tags][operation]=none-of&filter[tags][values]=Not+for+physics&token={TOKEN}"
response = requests.get(url, verify=False)

if response.status_code == 200:
    runs_data = response.json()
else:
    print(f"Failed to retrieve data: {response.status_code}")
    exit(1)

# Ensure the runs_data contains the necessary information
if 'data' not in runs_data:
    print("JSON response does not contain 'data' key")
    exit(1)

# Load cached run numbers
cached_runs = load_cache()
current_runs = [row['runNumber'] for row in runs_data['data'] if row['runNumber'] >= MIN_RUN_NUMBER and row['runNumber'] not in EXCLUDE_RUNS and row['timeTrgEnd'] is not None]
new_runs = [row for row in runs_data['data'] if row['runNumber'] not in cached_runs and row['runNumber'] >= MIN_RUN_NUMBER and row['runNumber'] not in EXCLUDE_RUNS]

# Filtering and preparing the new run data
filtered_runs = []
for row in new_runs:
    if ("ITS" not in row["detectors"] or 
        row["definition"] != "PHYSICS" or 
        row["runType"]["name"] != "PHYSICS" or 
        row["runQuality"] != "good"):
        continue
    
    # Convert time fields to datetime
    start_time_trigger = datetime.datetime.fromtimestamp(row["timeTrgStart"] // 1000, utc).astimezone(cet)
    end_time_trigger = None
    if row["timeTrgEnd"]:
        end_time_trigger = datetime.datetime.fromtimestamp(row["timeTrgEnd"] // 1000, utc).astimezone(cet)
    filtered_runs.append({
        'run_number': row['runNumber'],
        'time_trg_start': row['timeTrgStart'],
        'filling_scheme_name': row['lhcFill']['fillingSchemeName'],
        'start_time_trigger': start_time_trigger,
        'end_time_trigger': end_time_trigger,
        'beam_type': row['lhcFill']['beamType'],
        'beam_energy': round(row['lhcBeamEnergy'])  # Rounding the beam energy
    })

# Helper functions to mimic Excel formulas
def calculate_ai(ah, end_time, start_time):
    duration = (end_time - start_time).total_seconds()
    return ah / duration

def calculate_am(ai, al):
    return -np.log(1 - ai / 11245 / al)

def calculate_an(am, beam_type, beam_energy):
    # Retrieve the value for AN based on the beam type and energy
    energy_mapping = BEAM_ENERGY_MAPPING.get(beam_type, {})
    an_value = energy_mapping.get(str(beam_energy), 0.757)  # Default to 0.757 if not found
    return am / an_value

def calculate_ao(al, an):
    return al * an * 11245

def regex_extract(value, pattern):
    match = re.search(pattern, value)
    return int(match.group(1)) if match else 0

# Function to extract relevant values according to process.sh logic
def extract_values(run_number, time_trg_start):
    cmd = f"./process.sh {run_number} {time_trg_start}"
    output = subprocess.check_output(cmd, shell=True, text=True)
    
    ft0_vtx, o2_end, o2_start = None, None, None

    for line in output.split("\n"):
        if "TRG=" in line:
            ft0_vtx = float(line.split("TRG=")[1].split()[0].strip())
        if "TSstart=" in line:
            o2_start = float(line.split("TSstart=")[1].split()[0].strip())
        if "TSend=" in line:
            o2_end = float(line.split("TSend=")[1].split()[0].strip())
    
    return ft0_vtx, o2_end, o2_start

# Process the run data
results = []

for run in filtered_runs:
    run_number = run['run_number']
    time_trg_start = run['time_trg_start']
    filling_scheme_name = run['filling_scheme_name']
    start_time_trigger = run['start_time_trigger']
    end_time_trigger = run['end_time_trigger']
    beam_type = run['beam_type']
    beam_energy = run['beam_energy']
    
    # Skip runs with None end_time_trigger2
    if end_time_trigger is None:
        continue
    
    # Extract values using the process logic
    ft0_vtx, o2_end, o2_start = extract_values(run_number, time_trg_start)
    
    # Use start_time_trigger2 and end_time_trigger directly in the calculation
    ai = calculate_ai(ft0_vtx, end_time_trigger, start_time_trigger)
    al = regex_extract(filling_scheme_name, "[A-Za-z0-9]+_[A-Za-z0-9]+_[0-9]+_([0-9]+)_.*")
    am = calculate_am(ai, al)
    an = calculate_an(am, beam_type, beam_energy)
    ao = calculate_ao(al, an)
    results.append({
        'run': run_number,
        'mu': an,  # Assuming 'mu' corresponds to AN
        'inel': ao  # Assuming 'inel' corresponds to AO
    })

# Save the updated list of run numbers to the cache
save_cache(current_runs)

# Get current timestamp
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

# Output the results to a CSV file with timestamp
csv_filename = f'results_{timestamp}.csv'
df = pd.DataFrame(results)
df.to_csv(csv_filename, index=False)

print(f"Results saved to {csv_filename}")

