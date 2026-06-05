#include "stringtab.h"
#include <string>

StringTable idtable;
StringTable stringtable;
StringTable inttable;

Symbol StringTable::add_string(const char* s) {
    for (std::deque<std::string>::iterator it = table.begin(); it != table.end(); ++it)
        if (*it == s) return it->c_str();
    table.push_back(std::string(s));
    return table.back().c_str();
}

Symbol StringTable::add_string(const char* s, int len) {
    std::string str(s, len);
    for (std::deque<std::string>::iterator it = table.begin(); it != table.end(); ++it)
        if (*it == str) return it->c_str();
    table.push_back(str);
    return table.back().c_str();
}
