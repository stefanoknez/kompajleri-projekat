class Main {
    a : Int;  b : Int;  c : Int;
    f() : Int { a + b * c };
    g() : Int { a * b + c };
    h() : Int { a - b - c };
    i() : Int { ~ a * b };
    j() : Int { a + ~ b };
    k() : Bool { not a < b };
    m() : Object { a <- b <- c };
    n() : Bool { isvoid a + b };
};
