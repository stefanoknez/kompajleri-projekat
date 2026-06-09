//
// semant.cc — semantički analizator za Cool (PA3).
//
// Zaduženja (Cool Reference Manual + CS143 handout):
//   1. Izgradi graf nasljeđivanja svih klasa (korisničke + osnovne).
//   2. Provjeri da je graf dobro formiran: nema redefinicija, roditelji postoje,
//      ne nasljeđuje se Int/Bool/String/SELF_TYPE, nema ciklusa, postoji klasa
//      Main sa metodom main().
//   3. Za svaku klasu izgradi okruženje objekata (promjenljivih) i tabelu
//      metoda, pa provjeri tip svakog izraza po Cool pravilima tipova i upiši
//      svakom AST čvoru njegov tip.
//
// Ako se nađe greška, analizator je prijavi i (poslije faze provjere) zaustavi
// kompilaciju, isto kao referentni kompajler.
//

#include <stdlib.h>
#include <stdio.h>
#include <stdarg.h>
#include "semant.h"
#include "utilities.h"

extern char *curr_filename;

//////////////////////////////////////////////////////////////////////
//  Stanje analizatora (lokalno za fajl)
//////////////////////////////////////////////////////////////////////

static ostream &error_stream = cerr;
static int      semant_errors = 0;
static Class_   curr_class = 0;       // klasa koja se trenutno analizira

// Graf nasljeđivanja: ime klase -> Class_ čvor.
typedef std::map<Symbol, Class_> ClassTableMap;
static ClassTableMap classTable;

// Okruženje objekata: ime promjenljive -> njen deklarisani tip.
typedef SymbolTable<Symbol, Symbol> ObjectEnvironment;
static ObjectEnvironment objectEnv;

// Tabela metoda: klasa -> lista njenih (sopstvenih) metoda.
typedef std::vector<method_class *> Methods;
typedef std::map<Class_, Methods> MethodTableMap;
static MethodTableMap methodTable;

//////////////////////////////////////////////////////////////////////
//  Prijavljivanje grešaka
//////////////////////////////////////////////////////////////////////

static ostream &semant_error() {
    semant_errors++;
    return error_stream;
}

// Prijavi grešku na čvoru stabla t, u fajlu trenutne klase.
static ostream &semant_error(tree_node *t) {
    error_stream << curr_class->getFileName() << ":" << t->get_line_number() << ": ";
    return semant_error();
}

static ostream &internal_error(int lineno) {
    error_stream << "FATAL:" << lineno << ": ";
    return error_stream;
}

//////////////////////////////////////////////////////////////////////
//  Predefinisani simboli
//
//  Imenuju osnovne tipove/metode i par naziva rezervisanih za runtime.
//////////////////////////////////////////////////////////////////////

static Symbol
    arg, arg2, Bool, concat, cool_abort, copy, Int, in_int, in_string, IO,
    length, Main, main_meth, No_class, No_type, Object, out_int, out_string,
    prim_slot, self, SELF_TYPE, Str, str_field, substr, type_name, val;

static void initialize_constants(void) {
    arg        = idtable.add_string("arg");
    arg2       = idtable.add_string("arg2");
    Bool       = idtable.add_string("Bool");
    concat     = idtable.add_string("concat");
    cool_abort = idtable.add_string("abort");
    copy       = idtable.add_string("copy");
    Int        = idtable.add_string("Int");
    in_int     = idtable.add_string("in_int");
    in_string  = idtable.add_string("in_string");
    IO         = idtable.add_string("IO");
    length     = idtable.add_string("length");
    Main       = idtable.add_string("Main");
    main_meth  = idtable.add_string("main");
    No_class   = idtable.add_string("_no_class");
    No_type    = idtable.add_string("_no_type");
    Object     = idtable.add_string("Object");
    out_int    = idtable.add_string("out_int");
    out_string = idtable.add_string("out_string");
    prim_slot  = idtable.add_string("_prim_slot");
    self       = idtable.add_string("self");
    SELF_TYPE  = idtable.add_string("SELF_TYPE");
    Str        = idtable.add_string("String");
    str_field  = idtable.add_string("_str_field");
    substr     = idtable.add_string("substr");
    type_name  = idtable.add_string("type_name");
    val        = idtable.add_string("_val");
}

//////////////////////////////////////////////////////////////////////
//  Izgradnja grafa nasljeđivanja
//////////////////////////////////////////////////////////////////////

// Ubaci pet ugrađenih klasa (Object, IO, Int, Bool, String).
static void install_basic_classes(void) {
    Symbol filename = stringtable.add_string("<basic class>");

    // Object: abort() : Object, type_name() : String, copy() : SELF_TYPE  (osnovna klasa)
    Class_ Object_class =
        class_(Object, No_class,
            append_Features(
                append_Features(
                    single_Features(method(cool_abort, nil_Formals(), Object, no_expr())),
                    single_Features(method(type_name, nil_Formals(), Str, no_expr()))),
                single_Features(method(copy, nil_Formals(), SELF_TYPE, no_expr()))),
            filename);

    // IO: out_string, out_int : SELF_TYPE; in_string : String; in_int : Int
    Class_ IO_class =
        class_(IO, Object,
            append_Features(
                append_Features(
                    append_Features(
                        single_Features(method(out_string, single_Formals(formal(arg, Str)), SELF_TYPE, no_expr())),
                        single_Features(method(out_int, single_Formals(formal(arg, Int)), SELF_TYPE, no_expr()))),
                    single_Features(method(in_string, nil_Formals(), Str, no_expr()))),
                single_Features(method(in_int, nil_Formals(), Int, no_expr()))),
            filename);

    // Int i Bool: jedan primitivni slot za vrijednost.
    Class_ Int_class  = class_(Int,  Object, single_Features(attr(val, prim_slot, no_expr())), filename);
    Class_ Bool_class = class_(Bool, Object, single_Features(attr(val, prim_slot, no_expr())), filename);

    // String: length, str_field; length() : Int, concat(String) : String,
    //         substr(Int, Int) : String  (osnovna klasa)
    Class_ Str_class =
        class_(Str, Object,
            append_Features(
                append_Features(
                    append_Features(
                        append_Features(
                            single_Features(attr(val, Int, no_expr())),
                            single_Features(attr(str_field, prim_slot, no_expr()))),
                        single_Features(method(length, nil_Formals(), Int, no_expr()))),
                    single_Features(method(concat, single_Formals(formal(arg, Str)), Str, no_expr()))),
                single_Features(method(substr,
                    append_Formals(single_Formals(formal(arg, Int)), single_Formals(formal(arg2, Int))),
                    Str, no_expr()))),
            filename);

    classTable[Object] = Object_class;
    classTable[IO]     = IO_class;
    classTable[Int]    = Int_class;
    classTable[Bool]   = Bool_class;
    classTable[Str]    = Str_class;
}

// Ubaci korisnički definisane klase, uz provjeru najjednostavnijih grešaka.
static void install_classes(Classes classes) {
    for (int i = classes->first(); classes->more(i); i = classes->next(i)) {
        curr_class = classes->nth(i);
        Symbol name   = curr_class->getName();
        Symbol parent = curr_class->getParentName();

        if (name == SELF_TYPE)
            semant_error(curr_class) << "Redefinition of basic class SELF_TYPE.\n";
        else if (classTable.find(name) != classTable.end())
            semant_error(curr_class) << "Class " << name << " was previously defined.\n";
        else if (parent == Int || parent == Str || parent == Bool || parent == SELF_TYPE)
            semant_error(curr_class) << "Class " << name << " cannot inherit class " << parent << ".\n";
        else
            classTable[name] = curr_class;
    }
}

// Zapamti sopstvene metode svake klase, uz provjeru duplih definicija.
static void install_methods() {
    for (ClassTableMap::iterator it = classTable.begin(); it != classTable.end(); ++it) {
        Features features = it->second->getFeatures();
        Methods methods;
        for (int i = features->first(); features->more(i); i = features->next(i)) {
            if (!features->nth(i)->isMethod()) continue;
            method_class *m = static_cast<method_class *>(features->nth(i));

            bool existed = false;
            for (size_t j = 0; j < methods.size(); j++)
                if (methods[j]->getName() == m->getName()) existed = true;

            if (existed) {
                curr_class = it->second;
                semant_error(m) << "Method " << m->getName() << " is multiply defined.\n";
            } else {
                methods.push_back(m);
            }
        }
        methodTable[it->second] = methods;
    }
}

//////////////////////////////////////////////////////////////////////
//  Pomoćne funkcije za nasljeđivanje
//////////////////////////////////////////////////////////////////////

// Lanac od klase c naviše sve do (i uključujući) Object.
static std::vector<Class_> getInheritanceChain(Class_ c) {
    std::vector<Class_> chain;
    while (c->getName() != Object) {
        chain.push_back(c);
        if (classTable.find(c->getParentName()) == classTable.end()) {
            internal_error(__LINE__) << "invalid inheritance chain.\n";
            break;
        }
        c = classTable[c->getParentName()];
    }
    chain.push_back(classTable[Object]);
    return chain;
}

static std::vector<Class_> getInheritanceChain(Symbol name) {
    if (name == SELF_TYPE) name = curr_class->getName();
    if (classTable.find(name) == classTable.end())
        internal_error(__LINE__) << name << " not found in class table.\n";
    return getInheritanceChain(classTable[name]);
}

// Da li tip name1 odgovara (da li je podtip) tipu name2?
static bool conform(Symbol name1, Symbol name2) {
    if (name1 == SELF_TYPE && name2 == SELF_TYPE) return true;
    if (name1 != SELF_TYPE && name2 == SELF_TYPE) return false;
    if (name1 == SELF_TYPE) name1 = curr_class->getName();

    if (classTable.find(name1) == classTable.end())
        internal_error(__LINE__) << name1 << " not found in class table.\n";
    if (classTable.find(name2) == classTable.end())
        internal_error(__LINE__) << name2 << " not found in class table.\n";

    Class_ c2 = classTable[name2];
    std::vector<Class_> chain = getInheritanceChain(classTable[name1]);
    for (size_t i = 0; i < chain.size(); i++)
        if (chain[i] == c2) return true;
    return false;
}

// Najbliži zajednički predak dva tipa u grafu nasljeđivanja (join).
static Class_ LCA(Symbol name1, Symbol name2) {
    std::vector<Class_> chain1 = getInheritanceChain(name1);
    std::vector<Class_> chain2 = getInheritanceChain(name2);
    std::reverse(chain1.begin(), chain1.end());   // sad je korijen (Object) prvi
    std::reverse(chain2.begin(), chain2.end());

    size_t i;
    for (i = 1; i < std::min(chain1.size(), chain2.size()); i++)
        if (chain1[i] != chain2[i]) return chain1[i - 1];
    return chain1[i - 1];
}

// Nađi metodu po imenu u jednoj klasi (samo njene sopstvene metode).
static method_class *getMethod(Class_ c, Symbol method_name) {
    Methods methods = methodTable[c];
    for (size_t i = 0; i < methods.size(); i++)
        if (methods[i]->getName() == method_name) return methods[i];
    return 0;
}

// Nađi metodu po imenu idući uz lanac nasljeđivanja tipa `type`.
static method_class *lookupMethod(Symbol type, Symbol method_name) {
    std::vector<Class_> chain = getInheritanceChain(type);
    for (size_t i = 0; i < chain.size(); i++) {
        method_class *m = getMethod(chain[i], method_name);
        if (m) return m;
    }
    return 0;
}

//////////////////////////////////////////////////////////////////////
//  Provjere ispravnosti grafa nasljeđivanja
//////////////////////////////////////////////////////////////////////

static void check_inheritance() {
    // Svaki roditelj mora da bude definisana klasa.
    for (ClassTableMap::iterator it = classTable.begin(); it != classTable.end(); ++it) {
        if (it->first == Object) continue;
        if (classTable.find(it->second->getParentName()) == classTable.end()) {
            curr_class = it->second;
            semant_error(curr_class) << "Class " << it->second->getName()
                << " inherits from an undefined class " << it->second->getParentName() << ".\n";
        }
    }

    // Nema ciklusa: idi kroz pretke svake klase do Object; ako ponovo naiđemo
    // na samu sebe, to je ciklus.
    for (ClassTableMap::iterator it = classTable.begin(); it != classTable.end(); ++it) {
        if (it->first == Object) continue;
        curr_class = it->second;
        Symbol cname = it->first;
        Symbol pname = it->second->getParentName();
        while (pname != Object) {
            if (pname == cname) {
                semant_error(curr_class) << "Class " << curr_class->getName()
                    << ", or an ancestor of " << curr_class->getName()
                    << ", is involved in an inheritance cycle.\n";
                break;
            }
            if (classTable.find(pname) == classTable.end()) break;
            pname = classTable[pname]->getParentName();
        }
    }
}

static void check_main() {
    if (classTable.find(Main) == classTable.end()) {
        semant_error() << "Class Main is not defined.\n";
        return;
    }
    curr_class = classTable[Main];
    Features features = curr_class->getFeatures();
    bool found = false;
    for (int i = features->first(); features->more(i); i = features->next(i))
        if (features->nth(i)->isMethod() &&
            static_cast<method_class *>(features->nth(i))->getName() == main_meth)
            found = true;
    if (!found)
        semant_error(curr_class) << "No 'main' method in class Main.\n";
}

//////////////////////////////////////////////////////////////////////
//  Provjera tipova atributa i metoda (features)
//////////////////////////////////////////////////////////////////////

static void check_features() {
    for (ClassTableMap::iterator it = classTable.begin(); it != classTable.end(); ++it) {
        // Preskoči osnovne klase (njihova tijela su trivijalna / ugrađena).
        if (it->first == Object || it->first == IO || it->first == Int ||
            it->first == Bool   || it->first == Str)
            continue;

        curr_class = it->second;

        // Lanac nasljeđivanja od trenutne klase do Object.
        std::vector<Class_> chain = getInheritanceChain(curr_class);

        // Ubaci sve atribute (trenutne + naslijeđene) u jedan opseg da bi ih
        // tijela metoda i inicijalizatori atributa mogli vidjeti.
        objectEnv.enterscope();
        for (int k = (int)chain.size() - 1; k >= 0; k--) {   // od korijena ka trenutnoj
            Features fs = chain[k]->getFeatures();
            for (int i = fs->first(); fs->more(i); i = fs->next(i)) {
                if (!fs->nth(i)->isAttr()) continue;
                attr_class *a = static_cast<attr_class *>(fs->nth(i));
                objectEnv.addid(a->getName(), new Symbol(a->getType()));
            }
        }

        // Provjeri tip svakog feature-a trenutne klase.
        Features features = curr_class->getFeatures();
        for (int i = features->first(); features->more(i); i = features->next(i)) {
            if (features->nth(i)->isMethod()) {
                method_class *m = static_cast<method_class *>(features->nth(i));
                m->checkType();

                // Redefinisana (override) metoda mora tačno da se poklapa sa
                // potpisom iz pretka.
                for (size_t k = 1; k < chain.size(); k++) {
                    method_class *anc = getMethod(chain[k], m->getName());
                    if (!anc) continue;

                    if (m->getReturnType() != anc->getReturnType())
                        semant_error(m) << "In redefined method " << m->getName()
                            << ", return type " << m->getReturnType()
                            << " is different from original return type "
                            << anc->getReturnType() << ".\n";

                    Formals fa = m->getFormals();
                    Formals fb = anc->getFormals();
                    int a = fa->first(), b = fb->first();
                    while (fa->more(a) && fb->more(b)) {
                        if (fa->nth(a)->getType() != fb->nth(b)->getType())
                            semant_error(fa->nth(a)) << "In redefined method " << m->getName()
                                << ", parameter type " << fa->nth(a)->getType()
                                << " is different from original type "
                                << fb->nth(b)->getType() << ".\n";
                        a = fa->next(a); b = fb->next(b);
                    }
                    if (fa->more(a) || fb->more(b))
                        semant_error(m) << "Incompatible number of formal parameters in redefined method "
                            << m->getName() << ".\n";
                }
            } else {
                // Atribut: njegov inicijalizator (ako postoji) mora da odgovara
                // deklarisanom tipu.
                attr_class *a = static_cast<attr_class *>(features->nth(i));
                Symbol init_type = a->getInitExpr()->checkType();
                if (a->getType() != SELF_TYPE && classTable.find(a->getType()) == classTable.end())
                    semant_error(a) << "Class " << a->getType() << " of attribute "
                        << a->getName() << " is undefined.\n";
                else if (init_type != No_type && !conform(init_type, a->getType()))
                    semant_error(a) << "Inferred type " << init_type
                        << " of initialization of attribute " << a->getName()
                        << " does not conform to declared type " << a->getType() << ".\n";
            }
        }

        objectEnv.exitscope();
    }
}

//////////////////////////////////////////////////////////////////////
//  checkType() — po jedna za svaki AST čvor, vraća zaključeni tip čvora.
//////////////////////////////////////////////////////////////////////

void method_class::checkType() {
    objectEnv.enterscope();
    for (int i = formals->first(); formals->more(i); i = formals->next(i)) {
        Formal f = formals->nth(i);
        if (f->getName() == self)
            semant_error(f) << "'self' cannot be the name of a formal parameter.\n";
        else if (objectEnv.probe(f->getName()))
            semant_error(f) << "Formal parameter " << f->getName() << " is multiply defined.\n";
        else if (f->getType() == SELF_TYPE)
            semant_error(f) << "Formal parameter " << f->getName() << " cannot have type SELF_TYPE.\n";
        else if (classTable.find(f->getType()) == classTable.end())
            semant_error(f) << "Class " << f->getType() << " of formal parameter "
                << f->getName() << " is undefined.\n";
        else
            objectEnv.addid(f->getName(), new Symbol(f->getType()));
    }

    Symbol body_type = expr->checkType();
    if (return_type != SELF_TYPE && classTable.find(return_type) == classTable.end())
        semant_error(this) << "Undefined return type " << return_type
            << " in method " << name << ".\n";
    else if (!conform(body_type, return_type))
        semant_error(this) << "Inferred return type " << body_type << " of method "
            << name << " does not conform to declared return type " << return_type << ".\n";
    objectEnv.exitscope();
}

Symbol assign_class::checkType() {
    Symbol rtype = expr->checkType();
    Symbol *ltype = objectEnv.lookup(name);
    if (ltype == 0) {
        semant_error(this) << "Assignment to undeclared variable " << name << ".\n";
        type = rtype;
    } else if (!conform(rtype, *ltype)) {
        semant_error(this) << "Type " << rtype << " of assigned expression does not conform to declared type "
            << *ltype << " of identifier " << name << ".\n";
        type = *ltype;
    } else {
        type = rtype;
    }
    return type;
}

Symbol static_dispatch_class::checkType() {
    bool error = false;
    Symbol expr_type = expr->checkType();

    if (type_name != SELF_TYPE && classTable.find(type_name) == classTable.end()) {
        semant_error(this) << "Static dispatch to undefined class " << type_name << ".\n";
        type = Object;
        return type;
    }
    if (!conform(expr_type, type_name)) {
        error = true;
        semant_error(this) << "Expression type " << expr_type
            << " does not conform to declared static dispatch type " << type_name << ".\n";
    }

    method_class *method = lookupMethod(type_name, name);
    if (method == 0) {
        error = true;
        semant_error(this) << "Static dispatch to undefined method " << name << ".\n";
    } else {
        Formals formals = method->getFormals();
        int k1 = actual->first(), k2 = formals->first();
        while (actual->more(k1) && formals->more(k2)) {
            Symbol at = actual->nth(k1)->checkType();
            Symbol ft = formals->nth(k2)->getType();
            if (!conform(at, ft)) {
                error = true;
                semant_error(this) << "In call of method " << name << ", type " << at
                    << " of parameter " << formals->nth(k2)->getName()
                    << " does not conform to declared type " << ft << ".\n";
            }
            k1 = actual->next(k1); k2 = formals->next(k2);
        }
        if (actual->more(k1) || formals->more(k2)) {
            error = true;
            semant_error(this) << "Method " << name << " called with wrong number of arguments.\n";
        }
    }

    if (error) {
        type = Object;
    } else {
        type = method->getReturnType();
        if (type == SELF_TYPE) type = expr_type;   // SELF_TYPE se razrješava na primaoca
    }
    return type;
}

Symbol dispatch_class::checkType() {
    bool error = false;
    Symbol expr_type = expr->checkType();

    Symbol lookup_type = expr_type;
    if (lookup_type == SELF_TYPE) lookup_type = curr_class->getName();
    if (classTable.find(lookup_type) == classTable.end()) {
        semant_error(this) << "Dispatch on undefined class " << expr_type << ".\n";
        type = Object;
        return type;
    }

    method_class *method = lookupMethod(lookup_type, name);
    if (method == 0) {
        error = true;
        semant_error(this) << "Dispatch to undefined method " << name << ".\n";
    } else {
        Formals formals = method->getFormals();
        int k1 = actual->first(), k2 = formals->first();
        while (actual->more(k1) && formals->more(k2)) {
            Symbol at = actual->nth(k1)->checkType();
            Symbol ft = formals->nth(k2)->getType();
            if (!conform(at, ft)) {
                error = true;
                semant_error(this) << "In call of method " << name << ", type " << at
                    << " of parameter " << formals->nth(k2)->getName()
                    << " does not conform to declared type " << ft << ".\n";
            }
            k1 = actual->next(k1); k2 = formals->next(k2);
        }
        if (actual->more(k1) || formals->more(k2)) {
            error = true;
            semant_error(this) << "Method " << name << " called with wrong number of arguments.\n";
        }
    }

    if (error) {
        type = Object;
    } else {
        type = method->getReturnType();
        if (type == SELF_TYPE) type = expr_type;   // zadrži SELF_TYPE ako je primalac bio SELF_TYPE
    }
    return type;
}

Symbol cond_class::checkType() {
    if (pred->checkType() != Bool)
        semant_error(this) << "Predicate of 'if' does not have type Bool.\n";
    Symbol then_type = then_exp->checkType();
    Symbol else_type = else_exp->checkType();
    if (then_type == SELF_TYPE && else_type == SELF_TYPE)
        type = SELF_TYPE;
    else
        type = LCA(then_type, else_type)->getName();
    return type;
}

Symbol loop_class::checkType() {
    if (pred->checkType() != Bool)
        semant_error(this) << "Loop condition does not have type Bool.\n";
    body->checkType();
    type = Object;
    return type;
}

Symbol typcase_class::checkType() {
    expr->checkType();
    std::set<Symbol> seen;
    type = NULL;
    for (int i = cases->first(); cases->more(i); i = cases->next(i)) {
        branch_class *b = static_cast<branch_class *>(cases->nth(i));
        if (seen.find(b->get_type_decl()) != seen.end())
            semant_error(b) << "Duplicate branch " << b->get_type_decl() << " in case statement.\n";
        else
            seen.insert(b->get_type_decl());
        Symbol bt = b->checkType();
        if (type == NULL)
            type = bt;
        else if (type != SELF_TYPE || bt != SELF_TYPE)
            type = LCA(type, bt)->getName();
    }
    return type;
}

Symbol branch_class::checkType() {
    objectEnv.enterscope();
    objectEnv.addid(name, new Symbol(type_decl));
    type = expr->checkType();
    objectEnv.exitscope();
    return type;
}

Symbol block_class::checkType() {
    type = Object;
    for (int i = body->first(); body->more(i); i = body->next(i))
        type = body->nth(i)->checkType();
    return type;
}

Symbol let_class::checkType() {
    Symbol init_type = init->checkType();
    if (type_decl != SELF_TYPE && classTable.find(type_decl) == classTable.end())
        semant_error(this) << "Class " << type_decl << " of let-bound identifier "
            << identifier << " is undefined.\n";
    else if (init_type != No_type && !conform(init_type, type_decl))
        semant_error(this) << "Inferred type " << init_type << " of initialization of "
            << identifier << " does not conform to identifier's declared type " << type_decl << ".\n";

    objectEnv.enterscope();
    if (identifier == self)
        semant_error(this) << "'self' cannot be bound in a 'let' expression.\n";
    else
        objectEnv.addid(identifier, new Symbol(type_decl));
    type = body->checkType();
    objectEnv.exitscope();
    return type;
}

// Pomoćna funkcija za četiri aritmetička operatora.
static Symbol check_arith(tree_node *n, Expression e1, Expression e2, const char *op) {
    Symbol t1 = e1->checkType();
    Symbol t2 = e2->checkType();
    if (t1 != Int || t2 != Int)
        semant_error(n) << "non-Int arguments: " << t1 << " " << op << " " << t2 << "\n";
    return Int;
}

Symbol plus_class::checkType()   { return type = check_arith(this, e1, e2, "+"); }
Symbol sub_class::checkType()    { return type = check_arith(this, e1, e2, "-"); }
Symbol mul_class::checkType()    { return type = check_arith(this, e1, e2, "*"); }
Symbol divide_class::checkType() { return type = check_arith(this, e1, e2, "/"); }

Symbol neg_class::checkType() {
    if (e1->checkType() != Int)
        semant_error(this) << "Argument of '~' has type " << e1->get_type() << " instead of Int.\n";
    type = Int;
    return type;
}

Symbol lt_class::checkType() {
    Symbol t1 = e1->checkType();
    Symbol t2 = e2->checkType();
    if (t1 != Int || t2 != Int)
        semant_error(this) << "non-Int arguments: " << t1 << " < " << t2 << "\n";
    type = Bool;
    return type;
}

Symbol leq_class::checkType() {
    Symbol t1 = e1->checkType();
    Symbol t2 = e2->checkType();
    if (t1 != Int || t2 != Int)
        semant_error(this) << "non-Int arguments: " << t1 << " <= " << t2 << "\n";
    type = Bool;
    return type;
}

Symbol eq_class::checkType() {
    Symbol t1 = e1->checkType();
    Symbol t2 = e2->checkType();
    // Ako je bilo koja strana osnovni tip, obje strane moraju biti ISTI osnovni tip.
    if ((t1 == Int || t1 == Bool || t1 == Str ||
         t2 == Int || t2 == Bool || t2 == Str) && t1 != t2)
        semant_error(this) << "Illegal comparison with a basic type.\n";
    type = Bool;
    return type;
}

Symbol comp_class::checkType() {
    if (e1->checkType() != Bool)
        semant_error(this) << "Argument of 'not' has type " << e1->get_type() << " instead of Bool.\n";
    type = Bool;
    return type;
}

Symbol int_const_class::checkType()    { type = Int;  return type; }
Symbol bool_const_class::checkType()   { type = Bool; return type; }
Symbol string_const_class::checkType() { type = Str;  return type; }

Symbol new__class::checkType() {
    if (type_name != SELF_TYPE && classTable.find(type_name) == classTable.end()) {
        semant_error(this) << "'new' used with undefined class " << type_name << ".\n";
        type = Object;
    } else {
        type = type_name;     // može biti SELF_TYPE, što je dozvoljeno za new
    }
    return type;
}

Symbol isvoid_class::checkType() {
    e1->checkType();
    type = Bool;
    return type;
}

Symbol no_expr_class::checkType() {
    type = No_type;
    return type;
}

Symbol object_class::checkType() {
    if (name == self) {
        type = SELF_TYPE;
    } else if (objectEnv.lookup(name)) {
        type = *objectEnv.lookup(name);
    } else {
        semant_error(this) << "Undeclared identifier " << name << ".\n";
        type = Object;
    }
    return type;
}

//////////////////////////////////////////////////////////////////////
//  Ulazna tačka
//////////////////////////////////////////////////////////////////////

void program_class::semant() {
    initialize_constants();

    install_basic_classes();
    install_classes(classes);
    check_inheritance();

    // Loše formiran graf nasljeđivanja čini sve ostalo besmislenim, pa ovdje
    // prekidamo (kako kaže handout).
    if (semant_errors > 0) {
        cerr << "Compilation halted due to static semantic errors." << endl;
        exit(1);
    }

    check_main();
    install_methods();
    check_features();

    if (semant_errors > 0) {
        cerr << "Compilation halted due to static semantic errors." << endl;
        exit(1);
    }
}
