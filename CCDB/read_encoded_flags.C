#include <map>
#include <string>
#include <vector>
#include <utility>
#include <iostream>
#if !defined(__CLING__) || defined(__ROOTCLING__)
#include "CCDB/BasicCCDBManager.h"
#endif

void read_encoded_flags(int run, const char* passName, const char* periodName, const char* ccdbPath = "Users/j/jian/RCT") {
    // Get the CCDB manager instance
    auto& ccdb = o2::ccdb::BasicCCDBManager::instance();

    // Get start-of-run and end-of-run timestamps
    auto soreor = ccdb.getRunDuration(run);
    uint64_t ts = (soreor.first + soreor.second) / 2; // Use timestamp in the middle of the run for safety

    // Metadata (optional but good practice)
    std::map<std::string, std::string> metadata;
    metadata["run"] = std::to_string(run);
    metadata["passName"] = passName;
    metadata["periodName"] = periodName;

    // Retrieve the encoded flags
    try {
        auto encodedFlags = ccdb.getSpecific<std::vector<std::pair<int64_t, int32_t>>>(ccdbPath, ts, metadata);

        // Check if the object was successfully retrieved
        if (!encodedFlags) {
            std::cerr << "Error: Unable to retrieve encoded flags for run " << run << " from CCDB.\n";
            return;
        }

        // Print the retrieved encoded flags
        std::cout << "Encoded Flags for Run " << run << ":\n";
        for (const auto& [timestamp, bitmask] : *encodedFlags) {
            std::cout << "  Timestamp: " << timestamp
                      << ", Bitmask: " << std::bitset<32>(bitmask) << " (" << bitmask << ")\n";
        }
    } catch (const std::exception& ex) {
        std::cerr << "Error: Exception occurred while retrieving CCDB object: " << ex.what() << "\n";
    }
}

