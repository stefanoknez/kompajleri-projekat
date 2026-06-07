(*
 *  bad.cl  —  exercises parser error recovery (PA2).
 *
 *  Each class below contains a deliberate syntax error.  A correct parser
 *  reports the error and then RECOVERS, so that errors in later classes /
 *  features are still found.  The four recovery points are: class, feature,
 *  a let binding, and an expression inside a { ... } block.
 *)

-- 1) Error in a class definition; the next class is well-formed and should
--    still be parsed (recovery at the class level).
class A {
    @#$ bogus garbage here
};

-- 2) Well-formed class to prove class-level recovery worked.
class B {
    x : Int <- 1;
};

-- 3) Error in a feature; later features in the same class should still parse
--    (recovery at the feature level).
class C {
    broken( : Int { 0 };      -- malformed method header
    good() : Int { 42 };      -- this feature should still be parsed
};

-- 4) Error inside a { ... } block expression; later statements recover.
class D {
    f() : Int {
        {
            1 + ;                 -- bad expression, recover at ';'
            2;
        }
    };
};

-- 5) Error in a let binding; the rest of the let recovers.
class E {
    g() : Int {
        let x : Int <- , y : Int <- 5 in y
    };
};
