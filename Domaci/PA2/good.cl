(*
 *  good.cl  —  exercises every legal construct of the Cool grammar (PA2).
 *)

class List inherits IO {
    isNil() : Bool { true };

    head()  : Int  { { abort(); 0; } };

    cons(i : Int) : List {
        (new Cons).init(i, self)
    };
};

class Cons inherits List {
    car : Int;
    cdr : List;

    init(i : Int, rest : List) : Cons {
        {
            car <- i;
            cdr <- rest;
            self;
        }
    };

    isNil() : Bool { false };
    head()  : Int  { car };
};

class Main inherits IO {
    mylist : List;

    -- arithmetic, comparison, dispatch, let, if, while, case, new, isvoid, not, neg
    main() : Object {
        {
            mylist <- new List;
            let x : Int <- 1 + 2 * 3 - 4 / 2,
                y : Int,
                z : Bool <- not (x <= 10) in {
                if x < 5 then out_string("small\n") else out_string("big\n") fi;
                while x < 10 loop x <- x + 1 pool;
                case mylist of
                    n : Cons => out_string("cons\n");
                    n : List => out_string("list\n");
                esac;
                out_int(~x);
                isvoid mylist;
                self@IO.out_string("done\n");
            };
        }
    };
};
