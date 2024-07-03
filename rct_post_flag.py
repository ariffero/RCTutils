import requests
import json
import argparse
import urllib3

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
    data_passes = response.json().get('data', [])
    return {dp['name']: dp['id'] for dp in data_passes}

def fetch_runs(api_base_url, data_pass_id, token):
    """Fetches a list of runs for a given data pass ID from the API."""
    url = f"{api_base_url}/runs?filter[dataPassIds][]={data_pass_id}&token={token}"
    response = requests.get(url, verify=False)
    runs = response.json().get('data', [])
    
    # Extract detectors involved in each run
    for run in runs:
        run['detectors_involved'] = run.get('detectors', '').split(',')
    
    return runs

def is_run_excluded(run_number, excluded_runs):
    """Check if a run number is in the excluded runs list."""
    return run_number in excluded_runs

# Set up argument parsing
parser = argparse.ArgumentParser(description="Post a quality control flag.")
parser.add_argument('config', type=str, help='Path to the configuration file')
parser.add_argument('--data_pass', type=str, required=True, help='Data pass name to use')
parser.add_argument('--detector', type=str, required=True, help='Detector name to use')
parser.add_argument('--flagTypeId', type=int, required=True, help='Flag type ID to use')
parser.add_argument('--min_run', type=int, help='Minimum run number')
parser.add_argument('--max_run', type=int, help='Maximum run number')
parser.add_argument('--excluded_runs', type=int, nargs='*', default=[], help='List of run numbers to exclude')
args = parser.parse_args()

# Load configuration from the specified JSON file
config = load_config(args.config)

# Replace with your actual token and URLs from the config
TOKEN = config['token']
API_BASE_URL = config['run_api_url']
FLAG_API_URL = config['flag_api_url']

# Fetch data pass IDs
data_pass_ids = fetch_data_pass_ids(API_BASE_URL, TOKEN)

# Get the data pass ID for the specified data pass name
data_pass_id = data_pass_ids.get(args.data_pass)
if not data_pass_id:
    print(f"No data pass ID found for {args.data_pass}")
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
        continue

    # Check if filtering by min_run and max_run is required
    if (args.min_run is not None and run_number < args.min_run) or (args.max_run is not None and run_number > args.max_run):
        continue
    
    # Check if the detector is involved in the run
    involved_detectors = run['detectors_involved']
    if args.detector not in involved_detectors:
        continue

    # Request body with optional fields
    data = {
        "from": None,  # Set to None if you want to send null
        "to": None,    # Set to None if you want to send null
        "comment": None,  # Optional comment, can be None
        "flagTypeId": args.flagTypeId,  # Use the provided flagTypeId
        "runNumber": run_number,  # Use the actual runNumber
        "dplDetectorId": detector_id,  # Use the fetched detector ID
        "dataPassId": data_pass_id  # Use the fetched dataPassId
        # "simulationPassId": 4  # Uncomment and use instead of dataPassId if needed
    }

    # Make the POST request
    response = requests.post(FLAG_API_URL, params={"token": TOKEN}, json=data)

    # Print the response
    print(f"Run {run_number} - Status Code:", response.status_code)
    print(f"Run {run_number} - Response Body:", response.json())

