# Produce a run list from the Temporary RCT (Google spreadsheets)
- The configuration file
  - sheet_name: the name of the google spreadsheets, e.g., `QC_summary_data_2023_pbpb` for 2023 Pb-Pb.
  - tab_name: the name of the tab that you want to take.
  - periods: add which period(s) you want to include in the runlist; if empty, takes all periods in the tab.
  - runlists name: the dumped file name. detectors: add the requested detectors and the flags.
  - pass_shift: select which apass to be checked. For example, "1" refers to the first apass for a detector.
  - pass_name: set the apass name which will be in the dumped file.
  - runlists -> name: indicating which run list it is, e.g., CBT, CBT_hadronPID
  - separate_22o_test: set whether to separate LHC22o_test. Default is "False"
- Make sure you have the certificate runlist-5dfcf12a816d.json under the same folder where you run the script. Contact Jian Liu (jian.liu@cern.ch) for the certificate.
- `python3 runlist.py config_pp.json`
- Take `config_pp_2022.json` as the reference configuration file for 2022 periods, config_pp.json or config_pbpb.json for 2023 periods

# Export runs from RCT (in Bookkeeping)
- The configuration file:
  - "token": add your token to access Bookkeeping
  - "dataPassNames": asynchronous pass name(s), e.g., ["LHC24af_cpass0", "LHC24ag_cpass0"]
- Example file: config_rct.json
- `python3 rct.py config_rct.json`
- Separate .csv files are saved for each period if you have more than one period in the configuration file
 
 
