#include <iostream>
#include <fstream>
#include <sstream>
#include <string>
#include <vector>
#include <map>
#include <regex>
#include <set>
#include <bitset>
#include <algorithm>
#include <stdexcept>
#include <ctime>
#include "TFile.h"
#include "CCDB/CcdbApi.h"

std::string getErrorLogFilename() {
    std::time_t now = std::time(nullptr);
    char buffer[64];
    std::strftime(buffer, sizeof(buffer), "unexpected_flags_%Y%m%d_%H%M%S.log", std::localtime(&now));
    return std::string(buffer);
}

void process_and_upload(const char* csvFilePath,const char* passName, const char* periodName, const char* ccdbPath) {
    // Load the dictionary
    if (gSystem->Load("dict_ccdb.so") < 0) {
        std::cerr << "Error: Failed to load dict_ccdb.so" << std::endl;
        return;
    }
    std::map<std::string, std::map<std::string, int>> detailedBitMapping = {
        {"CPV", { {"Bad", 0}, {"Invalid", 0} }},
        {"EMC", { {"Bad", 1}, {"NoDetectorData", 1}, {"BadEMCalorimetry", 1}, {"LimitedAcceptanceMCReproducible", 2} }},
        {"FDD", { {"Bad", 3}, {"Invalid", 3}, {"NoDetectorData", 3} }},
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

    std::ifstream file(csvFilePath);
    if (!file.is_open()) {
        std::cerr << "Error: Could not open file " << csvFilePath << std::endl;
        return;
    }

    std::string line;
    std::vector<std::string> columns;
    if (!std::getline(file, line)) {
        std::cerr << "Error: Failed to read the header from file " << csvFilePath << std::endl;
        return;
    }

    std::istringstream headerStream(line);
    std::string column;
    while (std::getline(headerStream, column, ',')) {
        column.erase(column.find_last_not_of(" \t\r\n") + 1);
        column.erase(std::remove(column.begin(), column.end(), '\r'), column.end());
        columns.push_back(column);
    }

    if (!columns.empty() && columns.back().empty()) {
        columns.pop_back();
        std::cerr << "Warning: Empty column detected in the header. Removed." << std::endl;
    }

    std::ofstream errorLog(getErrorLogFilename(), std::ios::app);
    if (!errorLog.is_open()) {
        std::cerr << "Error: Could not open error log file for writing." << std::endl;
        return;
    }

    o2::ccdb::CcdbApi ccdb;
    ccdb.init("http://alice-ccdb.cern.ch");

    while (std::getline(file, line)) {
        std::istringstream lineStream(line);
        std::vector<std::string> rowValues;
        std::string value;

        while (std::getline(lineStream, value, ',')) {
            value.erase(value.find_last_not_of(" \t\r\n") + 1);
            value.erase(std::remove(value.begin(), value.end(), '\r'), value.end());
            rowValues.push_back(value);
        }

        if (rowValues.size() != columns.size()) {
            std::cerr << "Error: Mismatch between header and row column count." << std::endl;
            continue;
        }

        std::string runNumber = rowValues[0];
        std::map<std::string, std::vector<std::pair<int64_t, int64_t>>> timeRanges;
        std::map<std::string, std::vector<std::pair<std::string, std::pair<int64_t, int64_t>>>> flagNames;
        std::set<std::string> skippedDetectors;

        for (size_t i = 1; i < rowValues.size(); ++i) {
            std::string detector = columns[i];
            std::string flags = rowValues[i];

            if (flags == "Not present" || flags == "No available") {
                skippedDetectors.insert(detector);
                continue;
            }

            std::regex flagRegex(R"((\w+)\s+\(from:\s+(\d+)\s+to:\s+(\d+)\))");
            std::smatch match;

            auto flagStart = std::sregex_iterator(flags.begin(), flags.end(), flagRegex);
            auto flagEnd = std::sregex_iterator();

            for (auto it = flagStart; it != flagEnd; ++it) {
                match = *it;
                std::string flagName = match[1];
                int64_t from = std::stoll(match[2]);
                int64_t to = std::stoll(match[3]);

                if (!detailedBitMapping[detector].count(flagName) && flagName != "Good") {
                    errorLog << "Run: " << runNumber
                             << ", Detector: " << detector
                             << ", Unexpected Flag: " << flagName
                             << ", From: " << from
                             << ", To: " << to << "\n";
                    flagName = "Bad"; // Treat as "Bad"
                }

                timeRanges[detector].emplace_back(from, to);
                flagNames[detector].emplace_back(flagName, std::make_pair(from, to));
            }
        }

        std::map<int64_t, int32_t> encodedFlags;
        std::set<int64_t> timePoints;

        for (const auto& [detector, ranges] : timeRanges) {
            for (const auto& range : ranges) {
                timePoints.insert(range.first);
                timePoints.insert(range.second);
            }
        }

        std::vector<int64_t> sortedTimePoints(timePoints.begin(), timePoints.end());

        for (size_t i = 0; i < sortedTimePoints.size() - 1; ++i) {
            int64_t fromTimestamp = sortedTimePoints[i];
            int64_t toTimestamp = sortedTimePoints[i + 1];
            int32_t encodedWord = 0;

            for (const auto& [detector, ranges] : flagNames) {
                for (const auto& [flagName, range] : ranges) {
                    if (range.first <= fromTimestamp && range.second >= toTimestamp) {
                        if (detailedBitMapping[detector].count(flagName)) {
                            int bit = detailedBitMapping[detector][flagName];
                            encodedWord |= (1 << bit);
                        }
                    }
                }
            }

            for (const auto& detector : skippedDetectors) {
                if (detailedBitMapping[detector].count("Bad")) {
                    int bit = detailedBitMapping[detector]["Bad"];
                    encodedWord |= (1 << bit);
                }
            }

            encodedFlags[fromTimestamp] = encodedWord;
        }

        std::vector<std::pair<int64_t, int32_t>> encodedVector(encodedFlags.begin(), encodedFlags.end());

        std::cout << "Encoded Vector for Run " << runNumber << ":\n";
        for (const auto& [timestamp, bitmask] : encodedVector) {
            std::cout << "  Timestamp: " << timestamp
                      << ", Bitmask: " << std::bitset<32>(bitmask) << " (" << bitmask << ")\n";
        }

        std::map<std::string, std::string> metadata;
        metadata["run"] = runNumber;
        metadata["passName"] = passName;
        metadata["periodName"] = periodName;

        auto soreor = o2::ccdb::BasicCCDBManager::getRunDuration(ccdb, std::stoi(runNumber));
        auto sor = soreor.first;
        auto eor = soreor.second;

        ccdb.storeAsTFileAny(&encodedVector, ccdbPath, metadata, sor - 10000, eor + 10000);
        std::cout << "Successfully uploaded encoded flags for run " << runNumber << " to CCDB.\n";
    }

    errorLog.close();
}

