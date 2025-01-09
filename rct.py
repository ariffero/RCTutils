import requests
import csv
import json
from datetime import datetime, timezone
import urllib3
import argparse

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
    """
    Fetches and filters detector flags with valid effective periods.
    """
    url = f"{flag_api_url}?dataPassId={data_pass_id}&runNumber={run_number}&dplDetectorId={detector_id}&token={token}"
    response = requests.get(url, verify=False)
    
    flags = response.json().get('data', [])
    if not flags:
        return ["Not Available"]

    return [flag for flag in flags if flag.get("effectivePeriods")]

def format_flags(flags):
    """Formats the flags for CSV output."""
    if flags == ["Not Available"]:
        return "Not Available"
    if len(flags) == 1:
        return flags[0]['flagType']['method']
    formatted_flags = []
    for flag in flags:
        formatted_flags.append(f"{flag['flagType']['method']} (from: {datetime.utcfromtimestamp(flag['from'] / 1000).strftime('%Y-%m-%d %H:%M:%S')}, to: {datetime.utcfromtimestamp(flag['to'] / 1000).strftime('%Y-%m-%d %H:%M:%S')})")
    return " | ".join(formatted_flags)

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
    for data_pass_name, data_pass_info in data_pass_names.items():
        data_pass_id = data_pass_ids.get(data_pass_name)
        if not data_pass_id:
            print(f"No data pass ID found for {data_pass_name}. Check if your token is still valid; the token validity is 1 week only.")
            continue
        runs = fetch_runs(api_base_url, data_pass_id, token)
        
        # Filter runs by range if specified
        run_range = data_pass_info.get("run_range", [None, None])
        if run_range[0] is not None:
            runs = [run for run in runs if run['runNumber'] >= run_range[0]]
        if run_range[1] is not None:
            runs = [run for run in runs if run['runNumber'] <= run_range[1]]
        
        # Define the CSV filename based on the data pass name and run range
        safe_name = data_pass_name.replace(' ', '_').replace('/', '_')
        if run_range[0] is not None and run_range[1] is not None:
            csv_filename = f'Runs_{safe_name}_{run_range[0]}_{run_range[1]}.csv'
        elif run_range[0] is not None:
            csv_filename = f'Runs_{safe_name}_from_{run_range[0]}.csv'
        elif run_range[1] is not None:
            csv_filename = f'Runs_{safe_name}_to_{run_range[1]}.csv'
        else:
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
                        flags = fetch_detector_flags(flag_api_url, data_pass_id, run_number, detector_id, token)
                        row.append(format_flags(flags))
                
                writer.writerow(row)
    
        print(f"Data has been written to {csv_filename}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch run and detector data based on configuration.")
    parser.add_argument("config_file", help="Path to the JSON configuration file")
    args = parser.parse_args()
    main(args.config_file)

