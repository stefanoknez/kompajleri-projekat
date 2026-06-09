#include <cstdio>
#include "cool-parse.h"
#include "utilities.h"

extern int yylex();
extern FILE* yyin;

/* Ovdje ih definišemo, a u cool-parse.h su deklarisani kao extern */
YYSTYPE cool_yylval;
int curr_lineno = 1;

int main(int argc, char* argv[]) {
    if (argc > 1) {
        yyin = fopen(argv[1], "r");
        if (!yyin) {
            fprintf(stderr, "Error: cannot open file '%s'\n", argv[1]);
            return 1;
        }
    }

    int token;
    while ((token = yylex()) != 0) {
        dump_cool_token(token);
    }

    if (argc > 1)
        fclose(yyin);

    return 0;
}
