class Main {
    -- body extends as far right as possible: in x + 1  =>  let(..., plus(x,1))
    a() : Int { let x : Int <- 1 in x + 1 };
    -- multiple bindings nest right: let a, b, c in a
    b() : Int { let p : Int, q : Int <- 5, r : Bool in p };
    -- let as right operand of +
    c() : Int { 1 + let x : Int in x };
    -- nested let inside let body
    d() : Int { let x : Int <- 2 in let y : Int <- 3 in x + y };
};
