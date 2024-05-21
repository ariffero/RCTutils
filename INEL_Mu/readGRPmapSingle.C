void readGRPmapSingle(int run, long start, long stop=0) {

  std::map<int, uint64_t> runTimesStart;
  runTimesStart[run] = start;

  std::map<int, uint64_t> runTimesEnd;
  runTimesEnd[run] = stop;

  o2::ccdb::CcdbApi c;
  c.init("http://alice-ccdb.cern.ch");
  std::map<std::string, std::string> metadata;

  for (auto& el : runTimesStart) {
    std::string runString = std::to_string(el.first);
    metadata["runNumber"] = runString;
    o2::parameters::GRPECSObject* grp = c.retrieveFromTFileAny<o2::parameters::GRPECSObject>("GLO/Config/GRPECS", metadata, el.second + 20000); // adding 20 seconds
    std::cout << "accessing for time " << el.second + 20000 << ", which should be run " << el.first << ": run = " << grp ->getRun() << ", start time = " << grp ->getTimeStart() << " end time = " << grp->getTimeEnd() << std::endl;
    std::cout << "diff start (logbook - GRP) = " << el.second - grp->getTimeStart() << " ms, end (logbook - GRP) = " << runTimesEnd[el.first] - grp->getTimeEnd() << " ms" << std::endl;
    system(Form("echo %ld >lastTS",grp ->getTimeStart()));
    system(Form("echo %ld >lastTSend",grp ->getTimeEnd()));
  }
}
  
