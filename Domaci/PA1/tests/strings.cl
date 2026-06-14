-- Testira sve escape sekvence i normalne stringove
class Main inherits IO {
    main() : Object {
        let a : String <- "hello world" in
        let b : String <- "tab:\there" in
        let c : String <- "newline:\nend" in
        let d : String <- "backslash:\\" in
        let e : String <- "quote:\"end" in
        let f : String <- "null:\0end" in
        {
            out_string(a);
            out_string(b);
            out_string(c);
            out_string(d);
            out_string(e);
        }
    };
};
