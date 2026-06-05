/*
 * cool.flex  —  Lexical analyzer for the Cool programming language.
 *
 * Cool lexer rules (PA1, CS 143 Compilers):
 *   - Case-insensitive keywords (except true/false which must start lowercase)
 *   - Nested block comments  (* ... (* ... *) ... *)
 *   - Line comments  -- ...
 *   - String constants with escape sequences and 1024-char limit
 *   - All error conditions forwarded as ERROR tokens
 */

%{
#include "cool-parse.h"
#include "stringtab.h"
#include <string.h>

#define YY_NO_UNPUT
#define YY_NO_INPUT

extern int curr_lineno;
extern YYSTYPE cool_yylval;

/* Maximum length of a string constant (excluding null terminator) */
#define MAX_STR_CONST 1025

static char string_buf[MAX_STR_CONST];  /* working buffer for string constants */
static char *string_buf_ptr;            /* write pointer into string_buf */
static int string_has_error;            /* nonzero if a string error was already found */
static const char *string_error_msg;    /* the first error message in the string */

static int comment_depth;              /* nesting depth of (* *) block comments */

static char error_char[2];             /* buffer for single-char error messages */

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

/* ──────────────────────────────────────────────────────────────────
   Keyword definitions (case-insensitive via character classes)
   Placed in definitions so they can be referenced as {NAME_K}.
   Flex's longest-match rule ensures e.g. "inherits" beats "in".
   ────────────────────────────────────────────────────────────────── */
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

/* Boolean literals must start with lowercase t/f; rest is case-insensitive */
TRUE_K      t[rR][uU][eE]
FALSE_K     f[aA][lL][sS][eE]

DIGIT       [0-9]
ALPHA       [a-zA-Z_]
ALNUM       [a-zA-Z0-9_]

%%

 /* ════════════════════════════════════════════════════════════════
    Whitespace  —  newlines update line counter, rest is skipped
    ════════════════════════════════════════════════════════════════ */
\n                  { curr_lineno++; }
[ \t\r\f\v]+        { /* ignore horizontal/vertical whitespace */ }


 /* ════════════════════════════════════════════════════════════════
    Line comments:  -- ... <newline>
    ════════════════════════════════════════════════════════════════ */
"--"                        { BEGIN(LINE_COMMENT); }
<LINE_COMMENT>\n            { curr_lineno++; BEGIN(INITIAL); }
<LINE_COMMENT>.             { /* consume rest of line */ }
<LINE_COMMENT><<EOF>>       { BEGIN(INITIAL); }


 /* ════════════════════════════════════════════════════════════════
    Block comments:  (* ... *)  — support arbitrary nesting
    ════════════════════════════════════════════════════════════════ */
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
    cool_yylval.error_msg = (char*)"EOF in comment";
    BEGIN(INITIAL);
    return ERROR;
}

 /* Unmatched *) outside any comment */
"*)"    {
    cool_yylval.error_msg = (char*)"Unmatched *)";
    return ERROR;
}


 /* ════════════════════════════════════════════════════════════════
    String constants
    Escape sequences:  \n \t \b \f \\ \"  and  \<any> → <any>
    Special:  \0 (two chars) → '0' (ASCII 48);  literal NUL → error
    Max length: 1024 characters (excluding null terminator)
    ════════════════════════════════════════════════════════════════ */
\"  {
    BEGIN(STRING);
    string_buf_ptr   = string_buf;
    string_has_error = 0;
    string_error_msg = NULL;
}

<STRING>\"  {
    /* Closing quote — emit STR_CONST or propagate first error */
    BEGIN(INITIAL);
    if (string_has_error) {
        cool_yylval.error_msg = (char*)string_error_msg;
        return ERROR;
    }
    *string_buf_ptr = '\0';
    cool_yylval.symbol = stringtable.add_string(string_buf);
    return STR_CONST;
}

<STRING>\n  {
    /* Unescaped newline terminates the string immediately */
    curr_lineno++;
    BEGIN(INITIAL);
    cool_yylval.error_msg = (char*)"Unterminated string constant";
    return ERROR;
}

<STRING><<EOF>>     {
    BEGIN(INITIAL);
    cool_yylval.error_msg = (char*)"EOF in string constant";
    return ERROR;
}

 /* Escaped newline  \<LF>  →  actual newline character in string */
<STRING>\\\n        { curr_lineno++; STR_ADD('\n'); }

 /* Named escape sequences */
<STRING>\\n         { STR_ADD('\n'); }
<STRING>\\t         { STR_ADD('\t'); }
<STRING>\\b         { STR_ADD('\b'); }
<STRING>\\f         { STR_ADD('\f'); }
<STRING>\\\\        { STR_ADD('\\'); }
<STRING>\\\"        { STR_ADD('"');  }

 /* Any other escaped character  \<c>  →  c  (includes \0 → '0') */
<STRING>\\.         { STR_ADD(yytext[1]); }

 /* Literal NUL byte inside string */
<STRING>\0          {
    if (!string_has_error) {
        string_has_error = 1;
        string_error_msg = "String contains null character";
    }
}

 /* Ordinary characters */
<STRING>.           { STR_ADD(yytext[0]); }


 /* ════════════════════════════════════════════════════════════════
    Keywords  (longest-match guarantees e.g. "inherits" beats "in")
    Must come BEFORE the identifier rules.
    ════════════════════════════════════════════════════════════════ */
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

 /* Boolean literals (must start with lowercase t / f) */
{TRUE_K}    { cool_yylval.boolean = 1; return BOOL_CONST; }
{FALSE_K}   { cool_yylval.boolean = 0; return BOOL_CONST; }


 /* ════════════════════════════════════════════════════════════════
    Identifiers
    TYPEID  : starts with uppercase letter
    OBJECTID: starts with lowercase letter or underscore
    ════════════════════════════════════════════════════════════════ */
[A-Z]{ALNUM}*   {
    cool_yylval.symbol = idtable.add_string(yytext);
    return TYPEID;
}

[a-z_]{ALNUM}*  {
    cool_yylval.symbol = idtable.add_string(yytext);
    return OBJECTID;
}


 /* ════════════════════════════════════════════════════════════════
    Integer constants
    ════════════════════════════════════════════════════════════════ */
{DIGIT}+    {
    cool_yylval.symbol = inttable.add_string(yytext);
    return INT_CONST;
}


 /* ════════════════════════════════════════════════════════════════
    Multi-character operators  (must appear before single-char rules)
    ════════════════════════════════════════════════════════════════ */
"<-"    { return ASSIGN; }
"=>"    { return DARROW; }
"<="    { return LE;     }


 /* ════════════════════════════════════════════════════════════════
    Single-character tokens  (operators and punctuation)
    ════════════════════════════════════════════════════════════════ */
[+\-*/<=~@.;:,(){}]    { return yytext[0]; }


 /* ════════════════════════════════════════════════════════════════
    Invalid / unrecognised character  →  ERROR
    ════════════════════════════════════════════════════════════════ */
.   {
    error_char[0] = yytext[0];
    error_char[1] = '\0';
    cool_yylval.error_msg = error_char;
    return ERROR;
}

%%
