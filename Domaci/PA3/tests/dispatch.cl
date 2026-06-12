-- Testira semantičku provjeru: tip povratne vrijednosti i static dispatch
class A {
    val() : Int { 0 };
};

class B inherits A {
    val() : Int { 1 };
    extra() : String { "B" };
};

class Main inherits IO {
    helper(x : A) : Int { x.val() };

    main() : Object {
        let b : B <- new B,
            a : A <- b       -- B konformira sa A, ovo je ispravno
        in {
            helper(a);       -- prima A, dobija B (polimorfizam)
            helper(b);       -- B isto konformira
            out_string("dispatch ok\n");
        }
    };
};
