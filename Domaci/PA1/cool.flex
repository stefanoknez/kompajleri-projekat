/*
 * cool.flex  —  Leksički analizator za programski jezik Cool.
 *
 * Pravila Cool leksera (PA1, CS 143 Compilers):
 *   - Ključne riječi neosjetljive na velika/mala slova (osim true/false koje
 *     moraju počinjati malim slovom)
 *   - Ugniježđeni blok komentari  (* ... (* ... *) ... *)
 *   - Linijski komentari  -- ...
 *   - String konstante sa escape sekvencama i ograničenjem od 1024 karaktera
 *   - Sve greške se prosljeđuju kao ERROR tokeni
 */

%{
#include "cool-parse.h"
#include "stringtab.h"
#include <string.h>

#define YY_NO_UNPUT
#define YY_NO_INPUT

extern int curr_lineno;
extern YYSTYPE cool_yylval;

/* Maksimalna dužina string konstante (bez završne nule) */
#define MAX_STR_CONST 1025

static char string_buf[MAX_STR_CONST];  /* radni bafer za string konstante */
static char *string_buf_ptr;            /* pokazivač gdje upisujemo u string_buf */
static int string_has_error;            /* različito od nule ako je već nađena greška u stringu */
static const char *string_error_msg;    /* prva greška u stringu */

static int comment_depth;              /* dubina ugnježđavanja (* *) blok komentara */

static char error_char[2];             /* bafer za poruke o grešci od jednog karaktera */

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

/* ──────────────────────────────────────────────────────────────────
   Definicije ključnih riječi (neosjetljive na velika/mala slova preko klasa
   karaktera). Stavljene su u definicije da bi mogle da se koriste kao {IME}.
   Flex-ovo pravilo najdužeg poklapanja garantuje da npr. "inherits" pobijedi
   "in".
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

/* Boolean literali moraju počinjati malim t/f; ostatak je svejedno */
TRUE_K      t[rR][uU][eE]
FALSE_K     f[aA][lL][sS][eE]

DIGIT       [0-9]
ALPHA       [a-zA-Z_]
ALNUM       [a-zA-Z0-9_]

%%

 /* ════════════════════════════════════════════════════════════════
    Praznine  —  novi red povećava brojač linija, ostalo se preskače
    ════════════════════════════════════════════════════════════════ */
\n                  { curr_lineno++; }
[ \t\r\f\v]+        { /* ignoriši horizontalne/vertikalne praznine */ }


 /* ════════════════════════════════════════════════════════════════
    Linijski komentari:  -- ... <novi red>
    ════════════════════════════════════════════════════════════════ */
"--"                        { BEGIN(LINE_COMMENT); }
<LINE_COMMENT>\n            { curr_lineno++; BEGIN(INITIAL); }
<LINE_COMMENT>.             { /* pojedi ostatak linije */ }
<LINE_COMMENT><<EOF>>       { BEGIN(INITIAL); }


 /* ════════════════════════════════════════════════════════════════
    Blok komentari:  (* ... *)  — podržano proizvoljno ugnježđavanje
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
<COMMENT>.          { /* pojedi sadržaj komentara */ }
<COMMENT><<EOF>>    {
    cool_yylval.error_msg = (char*)"EOF in comment";
    BEGIN(INITIAL);
    return ERROR;
}

 /* Nesparen *) van bilo kakvog komentara */
"*)"    {
    cool_yylval.error_msg = (char*)"Unmatched *)";
    return ERROR;
}


 /* ════════════════════════════════════════════════════════════════
    String konstante
    Escape sekvence:  \n \t \b \f \\ \"  i  \<bilo šta> → <bilo šta>
    Specijalno:  \0 (dva karaktera) → '0' (ASCII 48);  pravi NUL → greška
    Max dužina: 1024 karaktera (bez završne nule)
    ════════════════════════════════════════════════════════════════ */
\"  {
    BEGIN(STRING);
    string_buf_ptr   = string_buf;
    string_has_error = 0;
    string_error_msg = NULL;
}

<STRING>\"  {
    /* Zatvoreni navodnik — vrati STR_CONST ili proslijedi prvu grešku */
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
    /* Neeskejpovan novi red odmah prekida string */
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

 /* Eskejpovan novi red  \<LF>  →  pravi novi red u stringu */
<STRING>\\\n        { curr_lineno++; STR_ADD('\n'); }

 /* Imenovane escape sekvence */
<STRING>\\n         { STR_ADD('\n'); }
<STRING>\\t         { STR_ADD('\t'); }
<STRING>\\b         { STR_ADD('\b'); }
<STRING>\\f         { STR_ADD('\f'); }
<STRING>\\\\        { STR_ADD('\\'); }
<STRING>\\\"        { STR_ADD('"');  }

 /* Bilo koji drugi eskejpovan karakter  \<c>  →  c  (uključuje \0 → '0') */
<STRING>\\.         { STR_ADD(yytext[1]); }

 /* Pravi NUL bajt unutar stringa */
<STRING>\0          {
    if (!string_has_error) {
        string_has_error = 1;
        string_error_msg = "String contains null character";
    }
}

 /* Obični karakteri */
<STRING>.           { STR_ADD(yytext[0]); }


 /* ════════════════════════════════════════════════════════════════
    Ključne riječi  (najduže poklapanje garantuje da npr. "inherits" pobijedi "in")
    Moraju doći PRIJE pravila za identifikatore.
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

 /* Boolean literali (moraju počinjati malim t / f) */
{TRUE_K}    { cool_yylval.boolean = 1; return BOOL_CONST; }
{FALSE_K}   { cool_yylval.boolean = 0; return BOOL_CONST; }


 /* ════════════════════════════════════════════════════════════════
    Identifikatori
    TYPEID  : počinje velikim slovom
    OBJECTID: počinje malim slovom ili donjom crtom
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
    Cjelobrojne konstante
    ════════════════════════════════════════════════════════════════ */
{DIGIT}+    {
    cool_yylval.symbol = inttable.add_string(yytext);
    return INT_CONST;
}


 /* ════════════════════════════════════════════════════════════════
    Operatori od više karaktera  (moraju doći prije pravila od jednog karaktera)
    ════════════════════════════════════════════════════════════════ */
"<-"    { return ASSIGN; }
"=>"    { return DARROW; }
"<="    { return LE;     }


 /* ════════════════════════════════════════════════════════════════
    Tokeni od jednog karaktera  (operatori i interpunkcija)
    ════════════════════════════════════════════════════════════════ */
[+\-*/<=~@.;:,(){}]    { return yytext[0]; }


 /* ════════════════════════════════════════════════════════════════
    Nevažeći / neprepoznat karakter  →  ERROR
    ════════════════════════════════════════════════════════════════ */
.   {
    error_char[0] = yytext[0];
    error_char[1] = '\0';
    cool_yylval.error_msg = error_char;
    return ERROR;
}

%%
