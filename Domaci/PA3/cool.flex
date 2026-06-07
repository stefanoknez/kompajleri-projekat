/*
 * cool.flex  —  Lexical analyzer for the Cool programming language (PA2 build).
 *
 * This is the same scanner written for PA1, re-wired to feed the bison parser
 * directly (it sets the bison `yylval` union and reports each token's line
 * number through `yylloc`, which the grammar copies into `node_lineno`).
 */

%{
#include "cool-tree.h"
#include "cool-parse.h"   /* token codes + YYSTYPE + extern yylval/yylloc */
#include "stringtab.h"
#include "utilities.h"
#include <string.h>

/* cool-tree.handcode.h does `#define yylineno curr_lineno;` (with a stray
   semicolon) for the parser's benefit; that macro corrupts flex's own
   generated `yylineno` references, so drop it inside the scanner. */
#undef yylineno

#define YY_NO_UNPUT
#define YY_NO_INPUT

extern int curr_lineno;

/* Before running any rule's action, record the line on which the matched
   text begins. The grammar reads this through @n / YYLLOC_DEFAULT. */
#define YY_USER_ACTION  yylloc = curr_lineno;

/* Maximum length of a string constant (excluding null terminator) */
#define MAX_STR_CONST 1025

static char string_buf[MAX_STR_CONST];  /* working buffer for string constants */
static char *string_buf_ptr;            /* write pointer into string_buf */
static int string_has_error;            /* nonzero if a string error was already found */
static const char *string_error_msg;    /* the first error message in the string */

static int comment_depth;               /* nesting depth of (* *) block comments */

static char error_char[2];              /* buffer for single-char error messages */

/* Add a character to the string buffer; set too-long error if needed. */
#define STR_ADD(c) \
    do { \
        if (!string_has_error) { \
            if (string_buf_ptr - string_buf >= MAX_STR_CONST - 1) { \
                string_has_error = 1; \
                string_error_msg = "String constant too long"; \
            } else { \
                *string_buf_ptr++ = (c); \
            } \
        } \
    } while(0)

%}

%option noyywrap

/* Exclusive start conditions */
%x COMMENT
%x LINE_COMMENT
%x STRING

CLASS_K     [cC][lL][aA][sS][sS]
ELSE_K      [eE][lL][sS][eE]
FI_K        [fF][iI]
IF_K        [iI][fF]
IN_K        [iI][nN]
INHERITS_K  [iI][nN][hH][eE][rR][iI][tT][sS]
ISVOID_K    [iI][sS][vV][oO][iI][dD]
LET_K       [lL][eE][tT]
LOOP_K      [lL][oO][oO][pP]
POOL_K      [pP][oO][oO][lL]
THEN_K      [tT][hH][eE][nN]
WHILE_K     [wW][hH][iI][lL][eE]
CASE_K      [cC][aA][sS][eE]
ESAC_K      [eE][sS][aA][cC]
NEW_K       [nN][eE][wW]
OF_K        [oO][fF]
NOT_K       [nN][oO][tT]

TRUE_K      t[rR][uU][eE]
FALSE_K     f[aA][lL][sS][eE]

DIGIT       [0-9]
ALPHA       [a-zA-Z_]
ALNUM       [a-zA-Z0-9_]

%%

\n                  { curr_lineno++; }
[ \t\r\f\v]+        { /* ignore horizontal/vertical whitespace */ }

"--"                        { BEGIN(LINE_COMMENT); }
<LINE_COMMENT>\n            { curr_lineno++; BEGIN(INITIAL); }
<LINE_COMMENT>.             { /* consume rest of line */ }
<LINE_COMMENT><<EOF>>       { BEGIN(INITIAL); }

"(*"                {
    BEGIN(COMMENT);
    comment_depth = 1;
}
<COMMENT>"(*"       { comment_depth++; }
<COMMENT>"*)"       {
    if (--comment_depth == 0)
        BEGIN(INITIAL);
}
<COMMENT>\n         { curr_lineno++; }
<COMMENT>.          { /* consume comment content */ }
<COMMENT><<EOF>>    {
    yylval.error_msg = (char*)"EOF in comment";
    BEGIN(INITIAL);
    return ERROR;
}

"*)"    {
    yylval.error_msg = (char*)"Unmatched *)";
    return ERROR;
}

\"  {
    BEGIN(STRING);
    string_buf_ptr   = string_buf;
    string_has_error = 0;
    string_error_msg = NULL;
}

<STRING>\"  {
    BEGIN(INITIAL);
    if (string_has_error) {
        yylval.error_msg = (char*)string_error_msg;
        return ERROR;
    }
    *string_buf_ptr = '\0';
    yylval.symbol = stringtable.add_string(string_buf);
    return STR_CONST;
}

<STRING>\n  {
    curr_lineno++;
    BEGIN(INITIAL);
    yylval.error_msg = (char*)"Unterminated string constant";
    return ERROR;
}

<STRING><<EOF>>     {
    BEGIN(INITIAL);
    yylval.error_msg = (char*)"EOF in string constant";
    return ERROR;
}

<STRING>\\\n        { curr_lineno++; STR_ADD('\n'); }

<STRING>\\n         { STR_ADD('\n'); }
<STRING>\\t         { STR_ADD('\t'); }
<STRING>\\b         { STR_ADD('\b'); }
<STRING>\\f         { STR_ADD('\f'); }
<STRING>\\\\        { STR_ADD('\\'); }
<STRING>\\\"        { STR_ADD('"');  }

<STRING>\\.         { STR_ADD(yytext[1]); }

<STRING>\0          {
    if (!string_has_error) {
        string_has_error = 1;
        string_error_msg = "String contains null character";
    }
}

<STRING>.           { STR_ADD(yytext[0]); }

{INHERITS_K}        { return INHERITS; }
{ISVOID_K}          { return ISVOID;   }
{CLASS_K}           { return CLASS;    }
{ELSE_K}            { return ELSE;     }
{WHILE_K}           { return WHILE;    }
{THEN_K}            { return THEN;     }
{LOOP_K}            { return LOOP;     }
{POOL_K}            { return POOL;     }
{ESAC_K}            { return ESAC;     }
{CASE_K}            { return CASE;     }
{NOT_K}             { return NOT;      }
{NEW_K}             { return NEW;      }
{LET_K}             { return LET;      }
{IN_K}              { return IN;       }
{IF_K}              { return IF;       }
{FI_K}              { return FI;       }
{OF_K}              { return OF;       }

{TRUE_K}    { yylval.boolean = 1; return BOOL_CONST; }
{FALSE_K}   { yylval.boolean = 0; return BOOL_CONST; }

[A-Z]{ALNUM}*   {
    yylval.symbol = idtable.add_string(yytext);
    return TYPEID;
}

[a-z_]{ALNUM}*  {
    yylval.symbol = idtable.add_string(yytext);
    return OBJECTID;
}

{DIGIT}+    {
    yylval.symbol = inttable.add_string(yytext);
    return INT_CONST;
}

"<-"    { return ASSIGN; }
"=>"    { return DARROW; }
"<="    { return LE;     }

[+\-*/<=~@.;:,(){}]    { return yytext[0]; }

.   {
    error_char[0] = yytext[0];
    error_char[1] = '\0';
    yylval.error_msg = error_char;
    return ERROR;
}

%%
