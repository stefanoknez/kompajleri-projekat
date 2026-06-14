-- Testira razliku između TYPEID, OBJECTID i BOOL_CONST
--
-- Pravila Cool leksera:
--   TYPEID    — počinje velikim slovom  (Main, IO, Int, Bool, String, MyClass)
--   OBJECTID  — počinje malim slovom   (x, myVar, self)
--   BOOL_CONST true/false — počinje MALIM slovom; TRUE/FALSE su TYPEID!

class TypeIdTest inherits IO {
    -- TYPEID primjeri (velika početna)
    myObj : MyClass <- new MyClass;
    io    : IO      <- new IO;
    num   : Int     <- 0;
    flag  : Bool    <- true;   -- true je BOOL_CONST
    str   : String  <- "ok";

    main() : Object {
        let t : Bool <- true  in   -- BOOL_CONST
        let f : Bool <- false in   -- BOOL_CONST
        -- True, False, TRUE, FALSE su TYPEID (ne bool konstante!)
        let a : Object <- new Object in
        {
            if t then out_string("true\n")  else out_string("false\n") fi;
            if f then out_string("true\n")  else out_string("false\n") fi;
            -- self je OBJECTID (posebna), SELF_TYPE je TYPEID
            self
        }
    };
};

-- Posebna klasa da se vide TYPEID tokeni
class MyClass { };
