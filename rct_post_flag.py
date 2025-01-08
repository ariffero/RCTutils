import requests
import json
import argparse
import urllib3
import pandas as pd
import os
import math

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

def read_csv_file(csv_file):
    """Read the CSV file and return a list of dictionaries with keys: given by the 1st row. Needed keys: post, run_number, a column with the name of a pass"""
    df = pd.read_csv(csv_file)
    return df.to_dict(orient='records')

# function to produce the minutes for the aQC meeting
def produce_minutes(csv_data, outputFile, flagTypeIdPass):
    # number of runs of each quality
    n_runs = 0 # tot number of runs
    n_good_runs = 0
    n_bad_tracking = 0
    n_lim_acc_runs = 0
    n_lim_acc_no_rep_runs = 0
    n_bad_pid_runs = 0
    n_no_det_data_runs = 0
    n_unknown_runs = 0

    #list with the runs of each quality
    runs = list()
    good_runs = list()
    bad_tracking = list()
    lim_acc_runs = list()
    lim_acc_no_rep_runs = list()
    bad_pid_runs = list()
    no_det_data_runs = list()
    unknown_runs = list()

    # write all the analyzed runs and fill the lists
    f = open(outputFile, "a")
    f.write('\nRuns: ')
    for index, row in enumerate(csv_data):
        if(row['post'] != 'ok'):
            continue
        run_number = row["run_number"]
        runs.append(run_number)
        n_runs = n_runs + 1

        # good
        if(row[flagTypeIdPass]==9):
            n_good_runs = n_good_runs + 1
            good_runs.append(run_number)
        # bad tracking
        if(row[flagTypeIdPass]==7):
            n_bad_tracking = n_bad_tracking + 1
            bad_tracking.append(run_number)
        # lim acc (MC reproducible)
        if(row[flagTypeIdPass]==5):
            n_lim_acc_runs = n_lim_acc_runs + 1
            lim_acc_runs.append(run_number)
        # lim acc (MC Not reproducible)
        if(row[flagTypeIdPass]==4):
            n_lim_acc_no_rep_runs = n_lim_acc_no_rep_runs + 1
            lim_acc_no_rep_runs.append(run_number)
        # bad pid
        if(row[flagTypeIdPass]==6):
            n_bad_pid_runs = n_bad_pid_runs + 1
            bad_pid_runs.append(run_number)
        # no detector data
        if(row[flagTypeIdPass]==3):
            n_no_det_data_runs = n_no_det_data_runs + 1
            no_det_data_runs.append(run_number)
        # unknown
        if(row[flagTypeIdPass]==14):
            n_unknown_runs = n_unknown_runs + 1
            unknown_runs.append(run_number)
        
    for run in range (0, n_runs):  
        if(run != n_runs-1):
            f.write(str(runs[run]).rstrip('.0') + ', ')
        else:
            f.write(str(runs[run]).rstrip('.0') + '.\n')
    
    timeDepenent = ''
    if args.time_dep:
        timeDepenent = ' The quality is time dependent: the first part of the run(s) is GOOD.'

    sameQuality = ''
    if args.no_diff:
        sameQuality = ' The quality was the same in the previous pass.'

    # write the minutes based on the values found in the csv
    if(n_good_runs==n_runs):
        f.write("All the runs are GOOD.\n\n")
        return

    elif(n_bad_tracking==n_runs):
        f.write("All the runs have been flagged as Bad tracking" + timeDepenent + sameQuality + "\n\n")
        return

    elif(n_lim_acc_runs==n_runs):
        f.write("All the runs have been flagged as Limited acceptance (MC reproducible)" + timeDepenent + sameQuality + "\n\n")
        return

    elif(n_lim_acc_no_rep_runs==n_runs):
        f.write("All the runs have been flagged as Limited acceptance (MC Not reproducible)" + timeDepenent + sameQuality + "\n\n")
        return

    elif(n_bad_pid_runs==n_runs):
        f.write("All the runs have been flagged as Bad PID" + timeDepenent + sameQuality + "\n\n")
        return

    elif(n_no_det_data_runs==n_runs):
        f.write("All the runs have been flagged as No Detector Data.\n\n")
        return

    elif(n_unknown_runs==n_runs):
        f.write("All the runs have been flagged as Unknown.\n\n")
        return

    if(n_good_runs != 0):
        f.write('GOOD runs: ')
        for k in range(0, n_good_runs):
            if(k != n_good_runs-1):
                f.write(str(good_runs[k]) + ', ')
            else:
                f.write(str(good_runs[k]) + '.\n')

    if(n_bad_tracking != 0):
        f.write('Runs flagged as Bad tracking: ')
        for k in range(0, n_bad_tracking):
            if(k != n_bad_tracking-1):
                f.write(str(bad_tracking[k]) + ', ')
            else:
                f.write(str(bad_tracking[k]) + '.' + timeDepenent + sameQuality + '\n')

    if(n_lim_acc_runs != 0):
        f.write('Runs flagged as Limited acceptance (MC reproducible): ')
        for k in range(0, n_lim_acc_runs):
            if(k != n_lim_acc_runs-1):
                f.write(str(lim_acc_runs[k]) + ', ')
            else:
                f.write(str(lim_acc_runs[k]) + '.' + timeDepenent + sameQuality + '\n')

    if(n_lim_acc_no_rep_runs != 0):
        f.write('Runs flagged as Limited acceptance (MC Not reproducible): ')
        for k in range(0, n_lim_acc_no_rep_runs):
            if(k != n_lim_acc_no_rep_runs-1):
                f.write(str(lim_acc_no_rep_runs[k]) + ', ')
            else:
                f.write(str(lim_acc_no_rep_runs[k]) + '.' + timeDepenent + sameQuality + '\n')

    if(n_bad_pid_runs != 0):
        f.write('Runs flagged as Bad PID: ')
        for k in range(0, n_bad_pid_runs):
            if(k != n_bad_pid_runs-1):
                f.write(str(bad_pid_runs[k]) + ', ')
            else:
                f.write(str(bad_pid_runs[k]) + '.' + timeDepenent + sameQuality + '\n')

    if(n_unknown_runs != 0):
        f.write('Runs flagged as Unknown: ')
        for k in range(0, n_unknown_runs):
            if(k != n_unknown_runs-1):
                f.write(str(unknown_runs[k]) + ', ')
            else:
                f.write(str(unknown_runs[k]) + '.\n')

    if(n_no_det_data_runs != 0):
        f.write('Runs flagged as No Detector Data: ')
        for k in range(0, n_no_det_data_runs):
            if(k != n_no_det_data_runs-1):
                f.write(str(no_det_data_runs[k]) + ', ')
            else:
                f.write(str(no_det_data_runs[k]) + '.\n')

    f.write('\n')

# Set up argument parsing
parser = argparse.ArgumentParser(description="Post a quality control flag.")
parser.add_argument('config', type=str, help='Path to the configuration file')
parser.add_argument('--data_pass', type=str, required=True, help='Data pass name to use')
parser.add_argument('--detector', type=str, required=True, help='Detector name to use')
parser.add_argument('--flagTypeId', type=int, help='Flag type ID to use (only in non-batch mode)')
parser.add_argument('--comment', type=str, default=None, help='Optional comment (only in non-batch mode)')
parser.add_argument('--min_run', type=int, help='Minimum run number')
parser.add_argument('--max_run', type=int, help='Maximum run number')
parser.add_argument('--excluded_runs', type=int, nargs='*', default=[], help='List of run numbers to exclude')
parser.add_argument('-b', '--batch', type=str, help='Path to CSV file for batch mode')
parser.add_argument('--minutes', type=str, help='Name of the output file containing the minutes')
parser.add_argument('--no_diff', action="store_true", help='Use this option if the non GOOD runs shows no difference wrt the previous pass')
parser.add_argument('--time_dep', action="store_true", help='Mark the non GOOD runs as time dependent, the quality will need to be posted manually, but the runs are considered in the minutes')
args = parser.parse_args()

# Check for incompatible arguments
if args.batch:
    if args.min_run or args.max_run or args.excluded_runs or args.comment or args.flagTypeId:
        parser.error("--min_run, --max_run, --excluded_runs, --comment, and --flagTypeId cannot be used with -b/--batch")

if not args.batch:
    if args.minutes:
        parser.error('--minutes can be used only in batch mode')
    if args.no_diff:
        parser.error('--no_diff can be used only in batch mode')
    if args.time_dep:
        parser.error('--time_dep can be used only in batch mode')

if not args.minutes:
    if args.no_diff:
        parser.error('--no_diff can be used only if --minutes is used')
    if args.time_dep:
        parser.error('--time_dep can be used only if --minutes is used')

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
    print(f"No data pass ID found for {args.data_pass}. Check if your token is still valid; the token validity is 1 week only.")
    exit(1)

# Fetch runs for the specified data pass ID
runs = fetch_runs(API_BASE_URL, data_pass_id, TOKEN)
run_numbers = {run['runNumber'] for run in runs}

# Get the detector ID from the config
detector_id = config['detector_ids'].get(args.detector)
if not detector_id:
    print(f"No detector ID found for {args.detector}")
    exit(1)

# Function to post a flag
def post_flag(run_number, flagTypeId, comment):
    data = {
        "from": None,  # Set to None if you want to send null
        "to": None,    # Set to None if you want to send null
        "comment": comment,  # Optional comment, can be None
        "flagTypeId": flagTypeId,  # Use the provided flagTypeId
        "runNumber": run_number,  # Use the actual runNumber
        "dplDetectorId": detector_id,  # Use the fetched detector ID
        "dataPassId": data_pass_id  # Use the fetched dataPassId
    }
    # Make the POST request
    response = requests.post(FLAG_API_URL, params={"token": TOKEN}, json=data, verify=False)

    # Print the response
    #print(f"Run {run_number} - Status Code:", response.status_code)
    #print(f"Run {run_number} - Response Body:", response.json())

if args.batch:
    # Batch mode
    csv_data = read_csv_file(args.batch)
    for row in csv_data:
        if(row["post"] != 'ok'):
            continue

        run_number = row["run_number"]
        if run_number not in run_numbers:
            print(f"Error: Run number {run_number} not found.")
            continue

        comment = ""
        if(pd.isna(row['comment'])):
            comment = " "
        else:
            comment = row['comment']

        quality = row[args.data_pass]
        if args.time_dep:
            if quality==9:
                print(run_number)
                post_flag(run_number, quality, comment)
            else:
                print(str(run_number)+' not posted!')
        else:
            print(run_number)
            post_flag(run_number, quality, comment)

    # create the minutes only in batch mode and if requested
    if(args.minutes):
        outputFile = args.minutes
        # use the minutes file if already present or create a new one if missing
        with open(outputFile, "a" if os.path.isfile(outputFile) else "w") as f:
            f.write(args.data_pass)
            f.close()
        # write the minutes
        produce_minutes(csv_data,outputFile,args.data_pass)

else:
    # Non-batch mode
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

        post_flag(run_number, args.flagTypeId, args.comment)

