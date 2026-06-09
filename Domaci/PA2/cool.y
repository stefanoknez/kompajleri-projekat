/*
 *  cool.y
 *  Bison gramatika / definicija parsera za jezik Cool (PA2).
 *
 *  Semantičke akcije grade apstraktno sintaksno stablo (AST) preko konstruktora
 *  iz tree paketa deklarisanih u cool-tree.h. Jedini korijen stabla je
 *  `ast_root` (Program), koji driver ispisuje preko dump_with_types.
 */

%{
  #include <iostream>
  #include "cool-tree.h"
  #include "stringtab.h"
  #include "utilities.h"

  extern char *curr_filename;
  extern int   curr_lineno;     /* održava ga lekser  */
  extern int   node_lineno;     /* broj linije koji se upisuje sljedećem čvoru stabla */

  void yyerror(const char *s);  /* bison je zove kad naiđe na grešku u parsiranju */
  extern int yylex();           /* ulazna tačka leksera           */

  /* Lokacije koje lekser pravi su obični brojevi linija (int-ovi).
     Na svakoj redukciji upišemo broj linije konstrukcije u node_lineno
     da bi konstruktori stabla zapamtili razuman broj linije. Uzimamo liniju
     prvog simbola sa desne strane. */
  #define YYLLOC_DEFAULT(Current, Rhs, N)        \
      do {                                       \
          (Current) = (N) ? (Rhs)[1] : (Rhs)[0]; \
          node_lineno = (Current);               \
      } while (0)

  #define SET_NODELOC(Current)  (node_lineno = (Current))

  /************************************************************************/
  /*                NE MIJENJAJ NIŠTA U OVOJ SEKCIJI                     */
  Program ast_root;             /* rezultat parsiranja  */
  Classes parse_results;        /* koristi se u semantičkoj analizi */
  int omerrs = 0;               /* broj grešaka u leksičkoj i sintaksnoj analizi */
%}

/* Ovi include-ovi moraju da se nađu i u generisanom HEADER-u (cool-parse.h),
   da bi tree tipovi iz %union bili deklarisani gdje god se header uključuje
   (npr. u lekseru i u utilities.cc). */
%code requires {
  #include "cool-tree.h"
  #include "stringtab.h"
}

/* Lokacije su obični brojevi linija. */
%define api.location.type {int}
%locations

/* Unija svih tipova koji mogu biti rezultat akcija pri parsiranju. */
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
   Terminali. Eksplicitni brojčani kodovi drže parser i lekser
   (koji uključuje generisani cool-parse.h) usklađene i stabilne.
*/
%token CLASS 258 ELSE 259 FI 260 IF 261 IN 262
%token INHERITS 263 LET 264 LOOP 265 POOL 266 THEN 267 WHILE 268
%token CASE 269 ESAC 270 OF 271 DARROW 272 NEW 273 ISVOID 274
%token <symbol>  STR_CONST 275 INT_CONST 276
%token <boolean> BOOL_CONST 277
%token <symbol>  TYPEID 278 OBJECTID 279
%token ASSIGN 280 NOT 281 LE 282 ERROR 283

/* Tipovi za neterminale. */
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

/* Prioriteti, od najnižeg ka najvišem (Cool Reference Manual, sekcija 11). */
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

/* ---- Program i klase ---------------------------------------------- */

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

/* Klasa bez eksplicitnog roditelja nasljeđuje od Object. */
class
    : CLASS TYPEID '{' feature_list '}' ';'
        { $$ = class_($2, idtable.add_string("Object"), $4,
                      stringtable.add_string(curr_filename)); }
    | CLASS TYPEID INHERITS TYPEID '{' feature_list '}' ';'
        { $$ = class_($2, $4, $6, stringtable.add_string(curr_filename)); }
    | error ';'
        { $$ = NULL; yyerrok; }
    ;

/* ---- Atributi i metode (features) --------------------------------- */

/* Lista feature-a koja može biti i prazna, svaki se završava sa ';'. */
feature_list
    : /* prazno */
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

/* ---- Formalni parametri ------------------------------------------- */

/* Lista formalnih parametara odvojenih zarezom, može biti i prazna. */
formal_list
    : /* prazno */
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

/* ---- Liste argumenata kod poziva (dispatch) ----------------------- */

/* Lista izraza odvojenih zarezom, može biti i prazna. */
actuals
    : /* prazno */
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

/* ---- Tijelo blok izraza ------------------------------------------- */

/* Jedan ili više izraza, svaki se završava sa ';'. */
block_list
    : expression ';'
        { $$ = single_Expressions($1); }
    | block_list expression ';'
        { $$ = append_Expressions($1, single_Expressions($2)); }
    | error ';'
        { $$ = nil_Expressions(); yyerrok; }
    ;

/* ---- Grane case izraza -------------------------------------------- */

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

/* ---- pomoćna pravila za let --------------------------------------- */

/* Opciona inicijalizacija:  <- izraz  | ništa */
opt_init
    : /* prazno */
        { $$ = no_expr(); }
    | ASSIGN expression
        { $$ = $2; }
    ;

/*
   let ima jedno ili više vezivanja. Lanac vezivanja modelujemo desno-rekurzivnim
   pomoćnim pravilom da bi se let protezao što više udesno (LET_PREC je najniži
   prioritet, pa parser radije nastavlja da uvlači u tijelo nego da prerano
   završi let).
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

/* ---- Izrazi ------------------------------------------------------- */

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

/* Ovu funkciju bison automatski zove kad otkrije grešku u parsiranju. */
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
