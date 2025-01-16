# CCDB Objects Based on RCT Flags

This repository contains utilities to create and manage CCDB objects based on RCT flags. It includes functionality to process CSV files with RCT flags, encode them into bitmasks, upload them to CCDB, and retrieve the stored objects.

## Flag-to-Bit Mapping

The flag-to-bit mapping is defined in the `process_and_upload.C` file. It assigns specific bits in a 32-bit word for each detector, representing its data quality status. Each detector can have one or more flags, including both general and specific ones. The `"Bad"` flag is used as a general indicator for issue, but it may be triggered by different underlying reasons depending on the detector.

### Map Definition Location

The mapping is implemented in the `detailedBitMapping` variable, declared as follows in `process_and_upload.C`:

```cpp
std::map<std::string, std::map<std::string, int>> detailedBitMapping = {
    {"CPV", { {"Bad", 0}, {"Invalid", 0} }},
    {"EMC", { {"Bad", 1}, {"NoDetectorData", 1}, {"BadEMCalorimetry", 1}, {"LimitedAcceptanceMCReproducible", 2} }},
    {"FDD", { {"Bad", 3}, {"NoDetectorData", 3} }},
    {"FT0", { {"Bad", 4}, {"UnknownQuality", 4}, {"Unknown", 4} }},
    {"FV0", { {"Bad", 5} }},
    {"HMP", { {"Bad", 6}, {"NoDetectorData", 6} }},
    {"ITS", { {"Bad", 7}, {"UnknownQuality", 7}, {"BadTracking", 7}, {"LimitedAcceptanceMCReproducible", 8} }},
    {"MCH", { {"Bad", 9}, {"NoDetectorData", 9}, {"Unknown", 9}, {"LimitedAcceptanceMCReproducible", 10} }},
    {"MFT", { {"Bad", 11}, {"BadTracking", 11}, {"LimitedAcceptanceMCReproducible", 12} }},
    {"MID", { {"Bad", 13}, {"BadTracking", 13}, {"LimitedAcceptanceMCReproducible", 14} }},
    {"PHS", { {"Bad", 15}, {"Invalid", 15} }},
    {"TOF", { {"Bad", 16}, {"NoDetectorData", 16}, {"BadPID", 16}, {"LimitedAcceptanceMCReproducible", 17} }},
    {"TPC", { {"Bad", 18}, {"BadTracking", 18}, {"BadPID", 19}, {"LimitedAcceptanceMCNotReproducible", 18}, {"LimitedAcceptanceMCReproducible", 20} }},
    {"TRD", { {"Bad", 21}, {"BadTracking", 21} }},
    {"ZDC", { {"Bad", 22}, {"UnknownQuality", 22}, {"Unknown", 22}, {"NoDetectorData", 22} }}
};
```
### Explanation of the Map

#### **GOOD:**
- The corresponding bit in the encoded-word is not set (remains 0).
#### **"Bad" (General Issue):**
- `"Bad"` is the default flag for general issues and may have different reasons based on the detector.
- For example, in `"EMC"`, it can be due to `"NoDetectorData"` or `"BadEMCalorimetry"`, both of which trigger **bit 1**.

#### **Specific Flags:**
- Certain conditions have unique flags and bits. For example:
  - `"LimitedAcceptanceMCReproducible"` in `"EMC"` triggers **bit 2**.
  - `"BadPID"` in `"TPC"` triggers **bit 19**, separate from the general `"Bad"`.

#### **Detector-Specific Behavior:**
- Each detector may have unique issue modes. For example:
  - `"ITS"` treats `"BadTracking"` and `"UnknownQuality"` as reasons for `"Bad"` (**bit 7**).
  - `"TPC"` handles `"BadTracking"`, `"BadPID"`, and `"LimitedAcceptanceMCNotReproducible"` with distinct bits (**18**, **19**, **20**).

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
- O2/ROOT framework should be installed and configured.

---

### 1. Encoding and Uploading RCT Flags to CCDB

#### Input:
- A CSV file containing RCT flags for various detectors.

#### Command:
```
root -b -q 'process_and_upload.C("path/to/input.csv", "passName", "periodName", "YourCCDBPath")'
```
### 2. Reading Encoded Flags from CCDB

#### Input:
- Metadata: Run number, pass name and period name
#### Command: 
``` 
root -b -q 'read_encoded_flags.C(runNumber, "passName", "periodName", "YourCCDBPath")'
```
#### Example: 
``` 
root -b -q 'read_encoded_flags.C(555651, "apass1", "LHC24am", "Users/j/jian/RCT")'
```
### 3. Error Handling
- Unexpected Flags:

Detected unexpected flags are treated as "Bad" and logged in a file named unexpected_flags_YYYYMMDD_HHMMSS.log.



