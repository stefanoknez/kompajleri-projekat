//
// semant-main.cc
//
// Self-contained driver for the Cool semantic analyzer (PA3).
//
// Stanford's original setup pipes three programs (lexer | parser | semant).
// Those rely on Linux reference binaries, so instead this driver runs all
// three phases in one executable:
//
//     lex+parse the .cl file  ->  AST (ast_root)
//     ast_root->semant()      ->  type-check + annotate the AST
//     ast_root->dump_with_types()  ->  print the type-annotated AST
//
//   usage:  semant  <file.cl>
//

#include <cstdio>
#include <cstdlib>
#include "cool-io.h"
#include "cool-tree.h"
#include "utilities.h"

// ---- globals shared with the lexer, parser and analyzer -------------------

extern FILE *yyin;            // flex input
extern int   yyparse();       // bison entry point

int   curr_lineno = 1;        // current source line (maintained by the lexer)
char *curr_filename = (char *) "<stdin>";

int   semant_debug = 0;       // -s debug flag (unused here, but referenced)

extern int     omerrs;        // lex + parse error count (defined in cool.y)
extern Program ast_root;      // AST root (defined in cool.y)

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

    // Phase 1+2: lex & parse into an AST.
    yyparse();
    if (omerrs != 0) {
        cerr << "Compilation halted due to lex and parse errors" << endl;
        fclose(yyin);
        return 1;
    }

    // Phase 3: semantic analysis.  semant() prints errors and calls exit(1)
    // itself if it finds any static-semantic errors.
    ast_root->semant();

    // For a well-formed program, print the type-annotated AST.
    ast_root->dump_with_types(cout, 0);

    fclose(yyin);
    return 0;
}
