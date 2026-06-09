//
// parser-main.cc
//
// Samostalni driver za Cool parser (PA2).
//
// Za razliku od Stanfordovog pipe setapa (lexer | parser), ovaj driver pokreće
// flex skener direktno na .cl fajlu, parsira ga bison parserom i ispisuje
// dobijeno apstraktno sintaksno stablo. Tako je parser jedan samostalni
// izvršni fajl koji radi u CodeBlocks / VS Code na macOS-u.
//
//   upotreba:  parser  <fajl.cl>
//

#include <cstdio>
#include <cstdlib>
#include "cool-io.h"
#include "cool-tree.h"
#include "utilities.h"

// ---- globalne promjenljive zajedničke za lekser i generisani parser -------

extern FILE *yyin;            // flex čita odavde
extern int   yyparse();       // ulazna tačka bisona

int   curr_lineno = 1;        // trenutna linija u izvoru (održava je lekser)
char *curr_filename = (char *) "<stdin>";   // fajl koji se parsira

extern int     omerrs;        // broj leksičkih + sintaksnih grešaka (definisan u cool.y)
extern Program ast_root;      // korijen AST-a dobijen parsiranjem (definisan u cool.y)

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

    yyparse();

    if (omerrs != 0) {
        cerr << "Compilation halted due to lex and parse errors" << endl;
        fclose(yyin);
        return 1;
    }

    ast_root->dump_with_types(cout, 0);

    fclose(yyin);
    return 0;
}
