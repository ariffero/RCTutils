# CCDB objects based on RCT flags 

# CCDB Objects Based on RCT Flags

This repository contains utilities to create and manage CCDB objects based on RCT flags. It includes functionality to process CSV files with RCT flags, encode them into bitmasks, upload them to CCDB, and retrieve the stored objects.

---

## Contents

- **process_and_upload.C**: 
  - Processes RCT flag data from a CSV file.
  - Encodes the flags into bitmasks and uploads them to the CCDB.

- **read_encoded_flags.C**: 
  - Reads and decodes the encoded flags from CCDB for a given run number and metadata.

- **dict_ccdb.so**: 
  - A dictionary file for CCDB interactions, required to handle RCT CCDB objects.

- **README.md**: 
  - Documentation for the repository.

---

## Instructions

### Prerequisites

- Ensure you have access to the ALICE CCDB infrastructure (`http://alice-ccdb.cern.ch`).
- The `dict_ccdb.so` file must be in the working directory to enable CCDB object handling.
- ROOT framework should be installed and configured.

---

### 1. Encoding and Uploading RCT Flags to CCDB

#### Input:
- A CSV file containing RCT flags for various detectors.

#### Command:
```bash
root -b -q 'process_and_upload.C("path/to/input.csv", "passName", "periodName", "YourCCDBPath")'

### 2. Reading Encoded Flags from CCDB

#### Input:
- Metadata: Run number, pass name and period name
#### Command: 
``` bash
root -b -q 'read_encoded_flags.C(runNumber, "passName", "periodName", "YourCCDBPath")'


### Error Handling
- Unexpected Flags:

Detected unexpected flags are treated as "Bad" and logged in a file named unexpected_flags_YYYYMMDD_HHMMSS.log.

