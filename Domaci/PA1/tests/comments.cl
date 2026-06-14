-- Linijski komentar
-- Još jedan linijski komentar

(* Blok komentar u jednoj liniji *)

(*
   Blok komentar koji
   se proteže kroz
   više linija
*)

(* Ugniježđeni (* jedan nivo *) komentar *)

(* Dublje (* ugniježđeno (* dva nivoa *) vraćamo se *) na vrh *)

class Main {
    -- komentar unutar klase
    x : Int <- (* inline komentar *) 5;

    main() : Object {
        x  (* komentar na kraju izraza *)
    };
};
