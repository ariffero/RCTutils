import pandas as pd
import glob

file_name = 'pp2024_ref'

# Get a list of all CSV files in the directory
csv_files = glob.glob(file_name + '/*.csv')

# Read each CSV file and merge them into one DataFrame
df_list = [pd.read_csv(file) for file in csv_files]
merged_df = pd.concat(df_list, ignore_index=True)

# Keep only the "Run Number" and "MID" columns
merged_df = merged_df[['Run Number', 'MID']]

# Filter for rows with "BadTracking"
df_bad = merged_df[merged_df['MID'].str.contains('BadTracking', na=False)]

# Filter for rows with "LimitedAcceptanceMCReproducible"
df_la = merged_df[
    merged_df['MID'].str.contains('LimitedAcceptanceMCReproducible', na=False) &
    ~merged_df['MID'].str.contains('BadTracking', na=False)
]

# Filter for rows with "Good" that are not marked as bad or limited acceptance
df_good = merged_df[
    merged_df['MID'].str.contains('Good', na=False) &
    ~merged_df['MID'].str.contains('BadTracking|LimitedAcceptanceMCReproducible', na=False)
]

# Save the resulting DataFrames to CSV files
df_good.to_csv(file_name + '/' + file_name + '_good.csv', index=False)
df_bad.to_csv(file_name + '/' + file_name + '_bad.csv', index=False)
df_la.to_csv(file_name + '/' + file_name + '_la.csv', index=False)

# Save the merged DataFrame to a new CSV file
merged_df.to_csv(file_name + '/' + file_name + '.csv', index=False)
