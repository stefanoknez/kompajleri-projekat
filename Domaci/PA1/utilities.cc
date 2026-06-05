#include "utilities.h"
#include <cstdio>

extern int curr_lineno;
extern YYSTYPE cool_yylval;

void dump_cool_token(int token) {
    printf("#%d ", curr_lineno);

    switch (token) {
        case CLASS:    printf("CLASS");    break;
        case ELSE:     printf("ELSE");     break;
        case FI:       printf("FI");       break;
        case IF:       printf("IF");       break;
        case IN:       printf("IN");       break;
        case INHERITS: printf("INHERITS"); break;
        case ISVOID:   printf("ISVOID");   break;
        case LET:      printf("LET");      break;
        case LOOP:     printf("LOOP");     break;
        case POOL:     printf("POOL");     break;
        case THEN:     printf("THEN");     break;
        case WHILE:    printf("WHILE");    break;
        case CASE:     printf("CASE");     break;
        case ESAC:     printf("ESAC");     break;
        case NEW:      printf("NEW");      break;
        case OF:       printf("OF");       break;
        case NOT:      printf("NOT");      break;
        case DARROW:   printf("DARROW");   break;
        case LE:       printf("LE");       break;
        case ASSIGN:   printf("ASSIGN");   break;

        case INT_CONST:
            printf("INT_CONST %s", cool_yylval.symbol);
            break;

        case STR_CONST: {
            printf("STR_CONST \"");
            const char* s = cool_yylval.symbol;
            while (*s) {
                switch (*s) {
                    case '\n': printf("\\n");  break;
                    case '\t': printf("\\t");  break;
                    case '\b': printf("\\b");  break;
                    case '\f': printf("\\f");  break;
                    case '\\': printf("\\\\"); break;
                    case '"':  printf("\\\""); break;
                    default:   printf("%c", *s); break;
                }
                s++;
            }
            printf("\"");
            break;
        }

        case BOOL_CONST:
            printf("BOOL_CONST %s", cool_yylval.boolean ? "true" : "false");
            break;

        case TYPEID:
            printf("TYPEID %s", cool_yylval.symbol);
            break;

        case OBJECTID:
            printf("OBJECTID %s", cool_yylval.symbol);
            break;

        case ERROR:
            printf("ERROR \"%s\"", cool_yylval.error_msg);
            break;

        default:
            /* Single-character tokens: print as 'c' */
            if (token >= 32 && token < 128)
                printf("'%c'", token);
            else
                printf("'\\%03o'", token);
            break;
    }

    printf("\n");
}
