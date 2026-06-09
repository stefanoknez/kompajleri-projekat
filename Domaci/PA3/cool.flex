/*
 * cool.flex  —  Leksički analizator za jezik Cool (verzija za PA2).
 *
 * Ovo je isti skener kao za PA1, samo prepravljen da direktno hrani bison parser
 * (postavlja bison `yylval` uniju i prijavljuje broj linije svakog tokena kroz
 * `yylloc`, koji gramatika prepisuje u `node_lineno`).
 */

%{
#include "cool-tree.h"
#include "cool-parse.h"   /* kodovi tokena + YYSTYPE + extern yylval/yylloc */
#include "stringtab.h"
#include "utilities.h"
#include <string.h>

/* cool-tree.handcode.h radi `#define yylineno curr_lineno;` (sa viškom tačke-zareza)
   zbog parsera; taj makro kvari flex-ove sopstvene generisane `yylineno`
   reference, pa ga unutar skenera poništavamo. */
#undef yylineno

#define YY_NO_UNPUT
#define YY_NO_INPUT

extern int curr_lineno;

/* Prije izvršavanja akcije bilo kog pravila, zapamti liniju na kojoj poklopljeni
   tekst počinje. Gramatika to čita kroz @n / YYLLOC_DEFAULT. */
#define YY_USER_ACTION  yylloc = curr_lineno;

/* Maksimalna dužina string konstante (bez završne nule) */
#define MAX_STR_CONST 1025

static char string_buf[MAX_STR_CONST];  /* radni bafer za string konstante */
static char *string_buf_ptr;            /* pokazivač gdje upisujemo u string_buf */
static int string_has_error;            /* različito od nule ako je već nađena greška u stringu */
static const char *string_error_msg;    /* prva greška u stringu */

static int comment_depth;               /* dubina ugnježđavanja (* *) blok komentara */

static char error_char[2];              /* bafer za poruke o grešci od jednog karaktera */

/* Dodaj karakter u string bafer; postavi grešku "predugačak" ako treba. */
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

/* Ekskluzivni start uslovi */
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
[ \t\r\f\v]+        { /* ignoriši horizontalne/vertikalne praznine */ }

"--"                        { BEGIN(LINE_COMMENT); }
<LINE_COMMENT>\n            { curr_lineno++; BEGIN(INITIAL); }
<LINE_COMMENT>.             { /* pojedi ostatak linije */ }
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
<COMMENT>.          { /* pojedi sadržaj komentara */ }
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
