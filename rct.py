import requests
import csv
import json
from datetime import datetime, timezone
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

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

def fetch_detector_flags(flag_api_url, data_pass_id, run_number, detector_id, token):
    """Fetches quality flags for a specific detector and run."""
    url = f"{flag_api_url}?dataPassId={data_pass_id}&runNumber={run_number}&dplDetectorId={detector_id}&token={token}"
    response = requests.get(url, verify=False)
    data = response.json()
    flags = data.get('data', [])
    
    if not flags:
        return "Not Available"
    
    valid_flags = []
    for flag in flags:
        created_at = flag.get('createdAt')
        if isinstance(created_at, int):
            created_at_dt = datetime.fromtimestamp(created_at / 1000, timezone.utc)
            valid_flags.append((created_at_dt, flag))

    if not valid_flags:
        return "Not Available"

    latest_flag = max(valid_flags, key=lambda x: x[0])[1]
    return latest_flag['flagType']['method']

def main(config_file):
    # Load configuration from the specified JSON file
    with open(config_file, 'r') as file:
        config = json.load(file)
    
    api_base_url = config['run_api_url']
    flag_api_url = config['flag_api_url']
    token = config['token']
    data_pass_names = config['dataPassNames']

    # Get mapping of data pass names to IDs
    data_pass_ids = fetch_data_pass_ids(api_base_url, token)

    # Process each data pass name
    for data_pass_name in data_pass_names:
        data_pass_id = data_pass_ids.get(data_pass_name)
        if not data_pass_id:
            print(f"No data pass ID found for {data_pass_name}")
            continue
        runs = fetch_runs(api_base_url, data_pass_id, token)
        
        # Define the CSV filename based on the data pass name
        safe_name = data_pass_name.replace(' ', '_').replace('/', '_')
        csv_filename = f'Runs_{safe_name}.csv'
        
        with open(csv_filename, 'w', newline='') as file:
            writer = csv.writer(file)
            # Write headers with detector names
            headers = ['Run Number'] + [name for name in config['detector_ids'].keys()]
            writer.writerow(headers)

            for run in runs:
                run_number = run['runNumber']
                row = [run_number]
                
                involved_detectors = run['detectors_involved']
                
                for detector_name, detector_id in config['detector_ids'].items():
                    if detector_name not in involved_detectors:
                        row.append("Not present")
                    else:
                        flag = fetch_detector_flags(flag_api_url, data_pass_id, run_number, detector_id, token)
                        row.append(flag)
                
                writer.writerow(row)
    
        print(f"Data has been written to {csv_filename}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Fetch run and detector data based on configuration.")
    parser.add_argument("config_file", help="Path to the JSON configuration file")
    args = parser.parse_args()
    main(args.config_file)

