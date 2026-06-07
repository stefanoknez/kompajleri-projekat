//
// parser-main.cc
//
// Self-contained driver for the Cool parser (PA2).
//
// Unlike Stanford's piped setup (lexer | parser), this driver runs the flex
// scanner directly on a .cl source file, parses it with the bison parser, and
// prints the resulting abstract syntax tree.  This makes the parser a single
// standalone executable that works in CodeBlocks / VS Code on macOS.
//
//   usage:  parser  <file.cl>
//

#include <cstdio>
#include <cstdlib>
#include "cool-io.h"
#include "cool-tree.h"
#include "utilities.h"

// ---- globals shared with the lexer and the generated parser ---------------

extern FILE *yyin;            // flex reads from this
extern int   yyparse();       // bison entry point

int   curr_lineno = 1;        // current source line (maintained by the lexer)
char *curr_filename = (char *) "<stdin>";   // file being parsed

extern int     omerrs;        // lex + parse error count (defined in cool.y)
extern Program ast_root;      // AST root produced by the parse (defined in cool.y)

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
