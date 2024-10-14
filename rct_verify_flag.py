import requests
import json
import argparse
import urllib3
from datetime import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def load_config(config_file):
    """Load the configuration file."""
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def fetch_data_pass_ids(api_base_url, token):
    """Fetches all data passes and returns a dictionary mapping names to IDs."""
    url = f"{api_base_url}/dataPasses?token={token}"
    response = requests.get(url, verify=False)
    if response.status_code != 200:
        print(f"Error fetching data pass IDs: {response.status_code} - {response.text}")
        return {}
    data_passes = response.json().get('data', [])
    return {dp['name']: dp['id'] for dp in data_passes}

def fetch_runs(api_base_url, data_pass_id, token):
    """Fetches a list of runs for a given data pass ID from the API."""
    url = f"{api_base_url}/runs?filter[dataPassIds][]={data_pass_id}&token={token}"
    response = requests.get(url, verify=False)
    if response.status_code != 200:
        print(f"Error fetching runs: {response.status_code} - {response.text}")
        return []
    runs = response.json().get('data', [])
    
    # Extract detectors involved in each run
    for run in runs:
        run['detectors_involved'] = run.get('detectors', '').split(',')
    
    return runs

def fetch_flags(api_base_url, data_pass_id, run_number, detector_id, token):
    """Fetches quality flags for a specific detector and run."""
    url = f"{api_base_url}/perDataPass?dataPassId={data_pass_id}&runNumber={run_number}&dplDetectorId={detector_id}&token={token}"
    response = requests.get(url, verify=False)
    if response.status_code != 200:
        print(f"Error fetching flags: {response.status_code} - {response.text}")
        return []
    data = response.json()
    flags = data.get('data', [])
    
    if not flags:
        return []

    # Sort flags by 'updatedAt' timestamp
    flags.sort(key=lambda x: x['updatedAt'], reverse=True)

    # Keep only the latest flag for each interval
    latest_flags = {}
    for flag in flags:
        key = (flag['from'], flag['to'])
        if key not in latest_flags:
            latest_flags[key] = flag

    return list(latest_flags.values())

def is_run_excluded(run_number, excluded_runs):
    """Check if a run number is in the excluded runs list."""
    return run_number in excluded_runs

# Set up argument parsing
parser = argparse.ArgumentParser(description="Verify quality control flags.")
parser.add_argument('config', type=str, help='Path to the configuration file')
parser.add_argument('--data_pass', type=str, required=True, help='Data pass name to use')
parser.add_argument('--detector', type=str, required=True, help='Detector name to use')
parser.add_argument('--min_run', type=int, help='Minimum run number')
parser.add_argument('--max_run', type=int, help='Maximum run number')
parser.add_argument('--excluded_runs', type=int, nargs='*', default=[], help='List of run numbers to exclude')
parser.add_argument('--comment', type=str, default=None, help='Optional verification comment')
args = parser.parse_args()

# Load configuration from the specified JSON file
config = load_config(args.config)

# Replace with your actual token and URLs from the config
TOKEN = config['token']
API_BASE_URL = config['run_api_url']
FLAG_FETCH_API_URL = config['flag_fetch_api_url']
FLAG_VERIFY_API_URL = config['flag_verify_api_url']

# Fetch data pass IDs
data_pass_ids = fetch_data_pass_ids(API_BASE_URL, TOKEN)

# Get the data pass ID for the specified data pass name
data_pass_id = data_pass_ids.get(args.data_pass)
if not data_pass_id:
    print(f"No data pass ID found for {args.data_pass}. Check if your token is still valid; the token validity is 1 week only.")
    exit(1)


# Fetch runs for the specified data pass ID
runs = fetch_runs(API_BASE_URL, data_pass_id, TOKEN)

# Get the detector ID from the config
detector_id = config['detector_ids'].get(args.detector)
if not detector_id:
    print(f"No detector ID found for {args.detector}")
    exit(1)


# Iterate over the fetched runs, filter them if needed, and make POST requests
for run in runs:
    run_number = run['runNumber']
    
    # Check if the run is excluded
    if is_run_excluded(run_number, args.excluded_runs):
        print(f"Skipping excluded run {run_number}")
        continue

    # Check if filtering by min_run and max_run is required
    if (args.min_run is not None and run_number < args.min_run) or (args.max_run is not None and run_number > args.max_run):
        print(f"Skipping run {run_number} outside the specified range")
        continue
    
    # Check if the detector is involved in the run
    involved_detectors = run['detectors_involved']
    if args.detector not in involved_detectors:
        print(f"Skipping run {run_number} as detector {args.detector} is not involved")
        continue

    # Fetch the flags for the current run and detector
    flags = fetch_flags(FLAG_FETCH_API_URL, data_pass_id, run_number, detector_id, TOKEN)
    
    # Verify each flag
    for flag in flags:
        flag_id = flag['id']
        # URL for the POST request
        url = f"{FLAG_VERIFY_API_URL}/{flag_id}/verify"
        
        # Query parameters
        params = {
            "token": TOKEN
        }

        # Request body
        data = {
            "comment": args.comment  # Optional comment, can be None
        }

        print(f"Verifying flag {flag_id} for run {run_number}")

        # Make the POST request
        response = requests.post(url, params=params, json=data, verify=False)

        # Print the response
        #print(f"Run {run_number}, Flag {flag_id} - Status Code:", response.status_code)
        #print(f"Run {run_number}, Flag {flag_id} - Response Body:", response.json())


