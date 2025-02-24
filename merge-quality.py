import csv

def load_run_numbers(filename):
  runs = set()
  with open(filename, 'r') as f:
    for line in f:
      # Split the line into columns using tab as separator
      parts = line.strip().split('\t')
      if parts:
        runs.add(parts[0])
  return runs

# insert period 
period = 'PbPb2023_pass4'

# luca 
good_runs_luca = load_run_numbers(period + '/data-MC-quality/goodRuns.txt')
bad_runs_luca = load_run_numbers(period + '/data-MC-quality/badRuns.txt')
# chi 2
good_runs_chi2 = load_run_numbers(period + '/data-MC-quality/goodRuns_chi2.txt')
bad_runs_chi2 = load_run_numbers(period + '/data-MC-quality/badRuns_chi2.txt')
# 2sigmas
good_runs_2sigmas = load_run_numbers(period + '/data-MC-quality/goodRuns_2sigmas.txt')
bad_runs_2sigmas = load_run_numbers(period + '/data-MC-quality/badRuns_2sigmas.txt')

input_csv = period + '/' + period + '.csv'
output_csv = period + '/data-mc-quality-' + period + '.csv'

with open(input_csv, 'r', newline='') as infile, open(output_csv, 'w', newline='') as outfile:
  reader = csv.DictReader(infile)
  # Rename the "MID" column to "aQC" in the header if present
  original_fieldnames = reader.fieldnames
  modified_fieldnames = [('aQC MID' if field == 'MID' else field) for field in original_fieldnames]
  # Add new columns
  fieldnames = reader.fieldnames + ['data/MC thresholds', 'data/MC chi2', 'data/MC 2 sigmas']
  writer = csv.DictWriter(outfile, fieldnames=fieldnames)
    
  writer.writeheader()
    
  for row in reader:
    run_number = row.get('Run Number', '').strip()
        
    # Determine Luca column value
    if run_number in good_runs_luca:
      row['data/MC thresholds'] = 'Good'
    elif run_number in bad_runs_luca:
      row['data/MC thresholds'] = 'Bad'
    else:
      row['data/MC thresholds'] = 'Missing'
    
    # Determine chi2 column value
    if run_number in good_runs_chi2:
      row['data/MC chi2'] = 'Good'
    elif run_number in bad_runs_chi2:
      row['data/MC chi2'] = 'Bad'
    else:
      row['data/MC chi2'] = 'Missing'
    
    # Determine sigma column value
    if run_number in good_runs_2sigmas:
      row['data/MC 2 sigmas'] = 'Good'
    elif run_number in bad_runs_2sigmas:
      row['data/MC 2 sigmas'] = 'Bad'
    else:
      row['data/MC 2 sigmas'] = 'Missing'
    
    writer.writerow(row)
