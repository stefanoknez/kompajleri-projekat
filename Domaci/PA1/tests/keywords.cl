-- Testira case-insensitivnost ključnih riječi Cool jezika
-- Ključne rijeci su case-insensitive (osim true/false koji moraju počinjati malim slovom)

class KeywordTest inherits IO {
    main() : Object {
        let x : Int <- 1 in
        -- if / then / else / fi
        IF x = 1 THEN
            iF x = 1 tHeN
                out_string("ok\n")
            eLsE
                out_string("no\n")
            fI
        ELSE
            out_string("outer else\n")
        FI;

        -- while / loop / pool
        WHILE x < 3 LOOP
            x <- x + 1
        POOL;

        -- case / of / esac
        CASE x OF
            n : Int => out_string("int\n");
        ESAC;

        -- let / in / new / isvoid / not
        LET y : Object <- NEW IO IN
            IF ISVOID y THEN out_string("void\n") ELSE NOT (x = 0) FI
    };
};
