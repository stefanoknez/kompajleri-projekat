#ifndef STRINGTAB_H
#define STRINGTAB_H

#include <deque>
#include <string>

/* Symbol je pokazivač u tabelu stringova — važi dok god tabela postoji */
typedef const char* Symbol;

/*
 * StringTable čuva jedinstvene kopije stringova.
 * std::deque garantuje da pokazivači na postojeće elemente ostaju validni
 * poslije push_back, pa su vraćeni const char* pokazivači stabilni.
 */
class StringTable {
    std::deque<std::string> table;
public:
    Symbol add_string(const char* s);
    Symbol add_string(const char* s, int len);
};

/* Tri odvojene tabele koje koristi Cool lekser */
extern StringTable idtable;      /* identifikatori */
extern StringTable stringtable;  /* string konstante */
extern StringTable inttable;     /* cjelobrojne konstante */

#endif /* STRINGTAB_H */
