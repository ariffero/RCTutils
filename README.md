# How to produce a run list (for Pb-Pb periods in 2023)
- The configuration file: config.json.
  - name: the name of the tab that you want to take.
  - periods: add which period(s) you want to include in the runlist; if empty, takes all periods in the tab.
  - runlists name: the dumped file name. detectors: add the requested detectors and the flags.
  - pass_shift: select which apass to be checked. For example, "1" refers to the first apass for a detector.
- Make sure you have the certificate runlist-5dfcf12a816d.json under the same folder where you run the script. Contact Jian Liu (jian.liu@cern.ch) for the certificate.
- `python3 runlist_pbpb.py config.json`
