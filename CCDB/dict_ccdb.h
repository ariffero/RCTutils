#ifndef CCDB_MAP_DICT_H
#define CCDB_MAP_DICT_H

#include <map>
#include <utility>
#include <cstdint> // For uint64_t, uint32_t

// Forward declare the classes for ROOT
#ifdef __CLING__
#pragma link C++ class std::map<uint64_t, uint32_t>+;
#pragma link C++ class std::pair<uint64_t, uint32_t>+;
#endif

#endif // CCDB_MAP_DICT_H

