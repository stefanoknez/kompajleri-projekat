#ifndef STRINGTAB_H
#define STRINGTAB_H

#include <deque>
#include <string>

/* Symbol is a pointer into the string table — stable as long as the table lives */
typedef const char* Symbol;

/*
 * StringTable stores unique copies of strings.
 * std::deque guarantees that references to existing elements remain valid
 * after push_back, so the returned const char* pointers are stable.
 */
class StringTable {
    std::deque<std::string> table;
public:
    Symbol add_string(const char* s);
    Symbol add_string(const char* s, int len);
};

/* Three separate tables used by the Cool lexer */
extern StringTable idtable;      /* identifiers */
extern StringTable stringtable;  /* string constants */
extern StringTable inttable;     /* integer constants */

#endif /* STRINGTAB_H */
