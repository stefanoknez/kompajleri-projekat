#ifndef COOL_PARSE_H
#define COOL_PARSE_H

#include "stringtab.h"

/* Kodovi tokena za Cool ključne riječi i specijalne tokene */
#define CLASS      258
#define ELSE       259
#define FI         260
#define IF         261
#define IN         262
#define INHERITS   263
#define ISVOID     264
#define LET        265
#define LOOP       266
#define POOL       267
#define THEN       268
#define WHILE      269
#define CASE       270
#define ESAC       271
#define NEW        272
#define OF         273
#define NOT        274
#define DARROW     275   /* => */
#define LE         276   /* <= */
#define ASSIGN     277   /* <- */
#define INT_CONST  278
#define STR_CONST  279
#define BOOL_CONST 280
#define TYPEID     281
#define OBJECTID   282
#define ERROR      283
#define LET_STMT   284   /* koristi ga samo parser, lekser ga ignoriše */

typedef int Boolean;

typedef union {
    Symbol   symbol;     /* za INT_CONST, STR_CONST, TYPEID, OBJECTID */
    Boolean  boolean;    /* za BOOL_CONST */
    char    *error_msg;  /* za ERROR */
} YYSTYPE;

extern YYSTYPE cool_yylval;
extern int curr_lineno;

#endif /* COOL_PARSE_H */
