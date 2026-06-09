//
// semant-main.cc
//
// Samostalni driver za Cool semantički analizator (PA3).
//
// Stanfordov originalni setap povezuje tri programa pipe-om (lexer | parser |
// semant). Oni se oslanjaju na Linux referentne binarne fajlove, pa umjesto
// toga ovaj driver pokreće sve tri faze u jednom izvršnom fajlu:
//
//     lex+parse .cl fajla    ->  AST (ast_root)
//     ast_root->semant()     ->  provjeri tipove + anotiraj AST
//     ast_root->dump_with_types()  ->  ispiši AST sa tipovima
//
//   upotreba:  semant  <fajl.cl>
//

#include <cstdio>
#include <cstdlib>
#include "cool-io.h"
#include "cool-tree.h"
#include "utilities.h"

// ---- globalne promjenljive zajedničke za lekser, parser i analizator ------

extern FILE *yyin;            // flex ulaz
extern int   yyparse();       // ulazna tačka bisona

int   curr_lineno = 1;        // trenutna linija u izvoru (održava je lekser)
char *curr_filename = (char *) "<stdin>";

int   semant_debug = 0;       // -s debug flag (ovdje se ne koristi, ali se referencira)

extern int     omerrs;        // broj leksičkih + sintaksnih grešaka (definisan u cool.y)
extern Program ast_root;      // korijen AST-a (definisan u cool.y)

int main(int argc, char *argv[])
{
    if (argc < 2) {
        cerr << "usage: " << argv[0] << " <file.cl>" << endl;
        return 1;
    }

    yyin = fopen(argv[1], "r");
    if (yyin == NULL) {
        cerr << "Error: cannot open file '" << argv[1] << "'" << endl;
        return 1;
    }
    curr_filename = argv[1];

    // Faza 1+2: leksiraj i parsiraj u AST.
    yyparse();
    if (omerrs != 0) {
        cerr << "Compilation halted due to lex and parse errors" << endl;
        fclose(yyin);
        return 1;
    }

    // Faza 3: semantička analiza. semant() sam ispisuje greške i poziva exit(1)
    // ako nađe bilo kakve statičke semantičke greške.
    ast_root->semant();

    // Za ispravan program, ispiši AST sa tipovima.
    ast_root->dump_with_types(cout, 0);

    fclose(yyin);
    return 0;
}
