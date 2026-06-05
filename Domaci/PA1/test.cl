-- Test file for the Cool lexer (PA1)
-- This file exercises as many lexer rules as possible.

(* Block comment — single line *)

(*
   Block comment
   spanning multiple lines
*)

(* Nested (* block (* comment *) depth *) test *)

class Main inherits IO {
    -- Keywords: all case variations
    x : Int <- 42;
    y : Bool <- tRuE;       -- BOOL_CONST (mixed case after t)
    z : Bool <- FALSE;      -- false must start lowercase -> TYPEID "FALSE" ... wait, no
                            -- FALSE starts with uppercase -> TYPEID, not BOOL_CONST

    main() : Object {
        let s : String <- "hello\nworld" in {
            -- String with escape sequences
            out_string("tab:\there\n");
            out_string("backslash: \\\n");
            out_string("quote: \"\n");

            -- Integer constants
            out_int(0);
            out_int(9999);

            -- Operators
            if x <= 10 then
                x <- x + 1
            else
                x <- x - 1
            fi;

            -- Comparison / darrow used in case
            case x of
                n : Int => out_int(n);
            esac;

            -- isvoid
            if isvoid s then out_string("void\n") else out_string("not void\n") fi;

            -- while / loop / pool
            while x < 5 loop
                x <- x + 1
            pool;

            -- not
            if not (x = 0) then out_string("nonzero\n") else out_string("zero\n") fi;

            -- new
            new IO;

            -- Type identifiers (start with uppercase)
            self;

            -- Unmatched *) error
            -- *)

            -- String errors (commented out so the file itself lexes cleanly):
            -- "unterminated string constant (unescaped newline follows)"
            -- "string too long ... (would need 1025+ chars)"
        }
    };
};

-- Additional keyword case-insensitivity tests
-- CLASS ELSE FI IF IN INHERITS ISVOID LET LOOP POOL THEN WHILE CASE ESAC NEW OF NOT
-- cLaSs ElSe Fi iF iN iNhErItS iSvOiD lEt LoOp PoOl tHeN wHiLe CaSe eSaC nEw Of NoT

-- Single-char tokens
-- + - * / < = ~ @ . ; : , ( ) { }

-- true / false (must start lowercase)
-- true True TRUE  →  BOOL_CONST, TYPEID, TYPEID
-- false False FALSE → BOOL_CONST, TYPEID, TYPEID
