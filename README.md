# How to produce a run list (for Pb-Pb and pp periods in 2023)
- The configuration file: config_pp.json or config_pbpb.json.
  - sheet_name: the name of the google spreadsheets, e.g., `QC_summary_data_2023_pbpb` for 2023 Pb-Pb.
  - tab_name: the name of the tab that you want to take.
  - periods: add which period(s) you want to include in the runlist; if empty, takes all periods in the tab.
  - runlists name: the dumped file name. detectors: add the requested detectors and the flags.
  - pass_shift: select which apass to be checked. For example, "1" refers to the first apass for a detector.
  - pass_name: set the apass name which will be in the dumped file.
- Make sure you have the certificate runlist-5dfcf12a816d.json under the same folder where you run the script. Contact Jian Liu (jian.liu@cern.ch) for the certificate.
- `python3 runlist.py config_pp.json`
