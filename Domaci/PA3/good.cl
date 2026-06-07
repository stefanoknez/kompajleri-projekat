(*
 *  good.cl — a semantically VALID Cool program (PA3).
 *  Exercises inheritance, SELF_TYPE, dispatch, let/case/if/while, arithmetic,
 *  attributes with initializers, method overriding with matching signatures.
 *)

class List inherits IO {
    isNil() : Bool { true };
    cons(hd : Int) : Cons {
        (let new_cell : Cons <- new Cons in new_cell.init(hd, self))
    };
    print_list() : Object { abort() };
};

class Cons inherits List {
    car : Int;
    cdr : List;
    isNil() : Bool { false };
    init(hd : Int, tl : List) : Cons {
        {
            car <- hd;
            cdr <- tl;
            self;
        }
    };
    print_list() : Object {
        {
            out_int(car);
            out_string("\n");
            cdr.print_list();
        }
    };
};

class Main inherits IO {
    mylist : List;

    fib(n : Int) : Int {
        if n < 2 then n else fib(n - 1) + fib(n - 2) fi
    };

    classify(x : Int) : String {
        case x of
            n : Int => "int";
            o : Object => "other";
        esac
    };

    main() : Object {
        {
            mylist <- new List;
            mylist <- mylist.cons(1).cons(2).cons(3);
            mylist.print_list();
            out_int(fib(10));
            out_string(classify(5));
            let i : Int <- 0 in
                while i < 5 loop i <- i + 1 pool;
            out_string(if isvoid mylist then "void" else "ok" fi);
        }
    };
};
