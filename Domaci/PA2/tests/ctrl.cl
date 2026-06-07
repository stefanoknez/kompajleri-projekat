class Main {
    f(x : Int) : Object {
        case x of
            n : Int => "int";
            s : String => "str";
        esac
    };
    g() : Object { if true then 1 else 2 fi };
    h() : Int { { 1; 2; 3; } };
};
