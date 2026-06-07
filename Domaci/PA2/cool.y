/*
 *  cool.y
 *  Bison grammar / parser definition for the Cool language (PA2).
 *
 *  Semantic actions build an abstract syntax tree (AST) using the tree
 *  package constructors declared in cool-tree.h.  The single root of the
 *  tree is `ast_root` (a Program), printed by the driver via dump_with_types.
 */

%{
  #include <iostream>
  #include "cool-tree.h"
  #include "stringtab.h"
  #include "utilities.h"

  extern char *curr_filename;
  extern int   curr_lineno;     /* maintained by the lexer  */
  extern int   node_lineno;     /* line number stamped on the next tree node */

  void yyerror(const char *s);  /* called by bison on a parse error */
  extern int yylex();           /* the lexer entry point           */

  /* The locations produced by the lexer are plain line numbers (ints).
     On every reduction, stamp the construct's line number onto node_lineno
     so that the tree constructors record a sensible line.  We use the line
     of the first symbol on the right-hand side. */
  #define YYLLOC_DEFAULT(Current, Rhs, N)        \
      do {                                       \
          (Current) = (N) ? (Rhs)[1] : (Rhs)[0]; \
          node_lineno = (Current);               \
      } while (0)

  #define SET_NODELOC(Current)  (node_lineno = (Current))

  /************************************************************************/
  /*                DON'T CHANGE ANYTHING IN THIS SECTION                */
  Program ast_root;             /* the result of the parse  */
  Classes parse_results;        /* for use in semantic analysis */
  int omerrs = 0;               /* number of errors in lexing and parsing */
%}

/* These includes must appear in the generated HEADER (cool-parse.h) too, so
   that the %union's tree types are declared wherever the header is included
   (e.g. by the lexer and by utilities.cc). */
%code requires {
  #include "cool-tree.h"
  #include "stringtab.h"
}

/* Locations are plain line numbers. */
%define api.location.type {int}
%locations

/* A union of all the types that can be the result of parsing actions. */
%union {
  Boolean boolean;
  Symbol symbol;
  Program program;
  Class_ class_;
  Classes classes;
  Feature feature;
  Features features;
  Formal formal;
  Formals formals;
  Case case_;
  Cases cases;
  Expression expression;
  Expressions expressions;
  char *error_msg;
}

/*
   Terminals.  The explicit numeric codes keep the parser and the lexer
   (which includes the generated cool-parse.h) in agreement and stable.
*/
%token CLASS 258 ELSE 259 FI 260 IF 261 IN 262
%token INHERITS 263 LET 264 LOOP 265 POOL 266 THEN 267 WHILE 268
%token CASE 269 ESAC 270 OF 271 DARROW 272 NEW 273 ISVOID 274
%token <symbol>  STR_CONST 275 INT_CONST 276
%token <boolean> BOOL_CONST 277
%token <symbol>  TYPEID 278 OBJECTID 279
%token ASSIGN 280 NOT 281 LE 282 ERROR 283

/* Types for the non-terminals. */
%type <program>     program
%type <classes>     class_list
%type <class_>      class
%type <features>    feature_list
%type <feature>     feature
%type <formals>     formal_list
%type <formal>      formal
%type <expressions> actuals
%type <expressions> actual_list
%type <expressions> block_list
%type <cases>       case_list
%type <case_>       case_branch
%type <expression>  expression
%type <expression>  let_tail
%type <expression>  opt_init

/* Precedence, lowest to highest (Cool Reference Manual section 11). */
%nonassoc LET_PREC
%right ASSIGN
%right NOT
%nonassoc '<' '=' LE
%left '+' '-'
%left '*' '/'
%left ISVOID
%left '~'
%left '@'
%left '.'

%%

/* ---- Program & classes -------------------------------------------- */

program
    : class_list
        { @$ = @1; ast_root = program($1); }
    ;

class_list
    : class
        { $$ = single_Classes($1); parse_results = $$; }
    | class_list class
        { $$ = append_Classes($1, single_Classes($2)); parse_results = $$; }
    ;

/* A class with no explicit parent inherits from Object. */
class
    : CLASS TYPEID '{' feature_list '}' ';'
        { $$ = class_($2, idtable.add_string("Object"), $4,
                      stringtable.add_string(curr_filename)); }
    | CLASS TYPEID INHERITS TYPEID '{' feature_list '}' ';'
        { $$ = class_($2, $4, $6, stringtable.add_string(curr_filename)); }
    | error ';'
        { $$ = NULL; yyerrok; }
    ;

/* ---- Features ------------------------------------------------------ */

/* Possibly empty list of features, each terminated by ';'. */
feature_list
    : /* empty */
        { $$ = nil_Features(); }
    | feature_list feature
        { $$ = append_Features($1, single_Features($2)); }
    ;

feature
    : OBJECTID '(' formal_list ')' ':' TYPEID '{' expression '}' ';'
        { $$ = method($1, $3, $6, $8); }
    | OBJECTID ':' TYPEID opt_init ';'
        { $$ = attr($1, $3, $4); }
    | error ';'
        { $$ = NULL; yyerrok; }
    ;

/* ---- Formal parameters -------------------------------------------- */

/* Possibly empty, comma-separated list of formals. */
formal_list
    : /* empty */
        { $$ = nil_Formals(); }
    | formal
        { $$ = single_Formals($1); }
    | formal_list ',' formal
        { $$ = append_Formals($1, single_Formals($3)); }
    ;

formal
    : OBJECTID ':' TYPEID
        { $$ = formal($1, $3); }
    ;

/* ---- Dispatch argument lists -------------------------------------- */

/* Possibly empty, comma-separated list of expressions. */
actuals
    : /* empty */
        { $$ = nil_Expressions(); }
    | actual_list
        { $$ = $1; }
    ;

actual_list
    : expression
        { $$ = single_Expressions($1); }
    | actual_list ',' expression
        { $$ = append_Expressions($1, single_Expressions($3)); }
    ;

/* ---- Block expression body ---------------------------------------- */

/* One-or-more expressions, each terminated by ';'. */
block_list
    : expression ';'
        { $$ = single_Expressions($1); }
    | block_list expression ';'
        { $$ = append_Expressions($1, single_Expressions($2)); }
    | error ';'
        { $$ = nil_Expressions(); yyerrok; }
    ;

/* ---- Case branches ------------------------------------------------- */

case_list
    : case_branch
        { $$ = single_Cases($1); }
    | case_list case_branch
        { $$ = append_Cases($1, single_Cases($2)); }
    ;

case_branch
    : OBJECTID ':' TYPEID DARROW expression ';'
        { $$ = branch($1, $3, $5); }
    ;

/* ---- let helpers --------------------------------------------------- */

/* Optional initializer:  <- expr  | nothing */
opt_init
    : /* empty */
        { $$ = no_expr(); }
    | ASSIGN expression
        { $$ = $2; }
    ;

/*
   A let has one or more bindings.  We model the binding chain with a
   right-recursive helper so that a let extends as far to the right as
   possible (LET_PREC is the lowest precedence, so the parser prefers to
   keep shifting into the body rather than ending the let early).
*/
let_tail
    : OBJECTID ':' TYPEID opt_init IN expression          %prec LET_PREC
        { $$ = let($1, $3, $4, $6); }
    | OBJECTID ':' TYPEID opt_init ',' let_tail
        { $$ = let($1, $3, $4, $6); }
    | error ',' let_tail
        { $$ = $3; yyerrok; }
    | error IN expression                                 %prec LET_PREC
        { $$ = $3; yyerrok; }
    ;

/* ---- Expressions -------------------------------------------------- */

expression
    : OBJECTID ASSIGN expression
        { $$ = assign($1, $3); }
    | expression '.' OBJECTID '(' actuals ')'
        { $$ = dispatch($1, $3, $5); }
    | expression '@' TYPEID '.' OBJECTID '(' actuals ')'
        { $$ = static_dispatch($1, $3, $5, $7); }
    | OBJECTID '(' actuals ')'
        { $$ = dispatch(object(idtable.add_string("self")), $1, $3); }
    | IF expression THEN expression ELSE expression FI
        { $$ = cond($2, $4, $6); }
    | WHILE expression LOOP expression POOL
        { $$ = loop($2, $4); }
    | '{' block_list '}'
        { $$ = block($2); }
    | LET let_tail
        { $$ = $2; }
    | CASE expression OF case_list ESAC
        { $$ = typcase($2, $4); }
    | NEW TYPEID
        { $$ = new_($2); }
    | ISVOID expression
        { $$ = isvoid($2); }
    | expression '+' expression
        { $$ = plus($1, $3); }
    | expression '-' expression
        { $$ = sub($1, $3); }
    | expression '*' expression
        { $$ = mul($1, $3); }
    | expression '/' expression
        { $$ = divide($1, $3); }
    | '~' expression
        { $$ = neg($2); }
    | expression '<' expression
        { $$ = lt($1, $3); }
    | expression LE expression
        { $$ = leq($1, $3); }
    | expression '=' expression
        { $$ = eq($1, $3); }
    | NOT expression
        { $$ = comp($2); }
    | '(' expression ')'
        { $$ = $2; }
    | OBJECTID
        { $$ = object($1); }
    | INT_CONST
        { $$ = int_const($1); }
    | STR_CONST
        { $$ = string_const($1); }
    | BOOL_CONST
        { $$ = bool_const($1); }
    ;

%%

/* This function is called automatically when bison detects a parse error. */
void yyerror(const char *s)
{
    extern int yychar;
    cerr << "\"" << curr_filename << "\", line " << curr_lineno
         << ": " << s << " at or near ";
    print_cool_token(yychar);
    cerr << endl;
    omerrs++;

    if (omerrs > 50) {
        fprintf(stdout, "More than 50 errors\n");
        exit(1);
    }
}
