(*
 *  bad.cl — a Cool program with many STATIC SEMANTIC errors (PA3).
 *  Inheritance is well-formed, so the analyzer reaches type checking and
 *  reports the type errors below.  (Inheritance-graph errors are demonstrated
 *  separately in tests/.)
 *)

class Main inherits IO {

    -- attribute initializer does not conform to declared type
    a : Int <- "not an int";

    main() : Object {
        {
            undeclared_var;                 -- undeclared identifier
            1 + "hello";                    -- non-Int argument to '+'
            a <- true;                      -- Bool does not conform to Int
            if 5 then 1 else 2 fi;          -- predicate not Bool
            self.no_such_method();          -- dispatch to undefined method
            out_int("string", 1);           -- wrong number / type of args
            not 5;                          -- 'not' of a non-Bool
            ~ true;                         -- '~' of a non-Int
            let x : Int <- "oops" in x;     -- let init does not conform
        }
    };

    -- redefining an IO method with an incompatible return type
    out_int(x : Int) : String { "wrong return type" };
};
