-- Testira sve operatore i specijalne znakove Cool leksera
class Main {
    a : Int <- 1;
    b : Int <- 2;

    main() : Object {
        let x : Int <- 0 in {
            -- aritmetika
            x <- a + b;
            x <- a - b;
            x <- a * b;
            x <- a / b;

            -- poređenje
            if a < b then x <- 1 else x <- 0 fi;
            if a <= b then x <- 1 else x <- 0 fi;
            if a = b  then x <- 1 else x <- 0 fi;

            -- unarni operatori
            x <- ~a;
            if not (a = b) then x <- 1 else x <- 0 fi;

            -- dodjela
            x <- 42;

            -- darrow (u case)
            case x of
                n : Int => x <- n;
            esac;

            -- @ (static dispatch)
            self@Main.main();

            -- interpunkcija: ; : , . ( ) { }
            x
        }
    };
};
