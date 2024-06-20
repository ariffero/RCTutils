import csv
import json
import pandas as pd
from datetime import datetime
import os

def load_config(config_file):
    """Load the configuration file."""
    with open(config_file, 'r') as file:
        config = json.load(file)
    return config

def read_csv(file_path):
    """Read the CSV file into a pandas DataFrame with error handling."""
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        exit(1)
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_path}' is empty.")
        exit(1)
    except pd.errors.ParserError:
        print(f"Error: The file '{file_path}' could not be parsed.")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading the file '{file_path}': {e}")
        exit(1)

def parse_flags(flags):
    """Parse the flags in a cell."""
    return [flag.strip().split(' ')[0] for flag in flags.split('|')]

def check_flags(flags, required_flags):
    """Check if any of the required flags are present in the flags."""
    if flags == "Not present" or flags == "Not Available":
        return False
    
    parsed_flags = parse_flags(flags)

    for required_flag in required_flags:
        if required_flag in parsed_flags:
            return True
    
    return False

def filter_runs(df, detectors):
    """Filter runs based on the flag criteria for specified detectors."""
    filtered_runs = []

    for _, row in df.iterrows():
        all_criteria_met = True

        for detector, required_flags in detectors.items():
            if detector in row and not check_flags(row[detector], required_flags):
                all_criteria_met = False
                break

        if all_criteria_met:
            filtered_runs.append(row['Run Number'])
    
    return filtered_runs

def generate_runlist_filename(period, data_pass, runlist_name):
    """Generate the runlist filename based on the period, data_pass, and runlist_name."""
    creation_date = datetime.now().strftime('%Y-%m-%d')
    filename = f"Runlist_{period}_{data_pass}_{runlist_name}_{creation_date}.txt"
    return filename

def main(config_file, csv_directory):
    config = load_config(config_file)
    period = config['period']
    data_pass = config['pass']
    csv_file = os.path.join(csv_directory, f"Runs_{period}_{data_pass}.csv")
    
    df = read_csv(csv_file)

    sheets = config['sheets']

    for sheet in sheets:
        runlists = sheet['runlists']
        
        for runlist in runlists:
            runlist_name = runlist['name']
            detectors = runlist['detectors']
            filtered_runs = filter_runs(df, detectors)

            runlist_filename = generate_runlist_filename(period, data_pass, runlist_name)

            with open(runlist_filename, 'w') as file:
                creation_date = datetime.now().strftime('%Y-%m-%d')
                file.write(f"# Creation Date: {creation_date}, Periods: {period}\n")
                file.write(",".join(map(str, filtered_runs)) + "\n")

            print(f"Run list {runlist_filename} has been written with {len(filtered_runs)} runs.")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Generate run lists based on flag criteria for detectors.")
    parser.add_argument("config_file", help="Path to the JSON configuration file")
    parser.add_argument("-d", "--csv_directory", default=".", help="Path to the directory containing the CSV file (default is current directory)")
    args = parser.parse_args()
    main(args.config_file, args.csv_directory)

