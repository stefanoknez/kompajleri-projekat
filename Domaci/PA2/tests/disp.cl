class Main {
    x : Main;
    f() : Object { x.foo().bar(1, 2) };
    g() : Object { x@Main.baz() };
    h() : Object { foo() };
};
