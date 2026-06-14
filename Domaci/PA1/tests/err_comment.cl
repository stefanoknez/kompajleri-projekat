-- Testira da lekser ispravno prijavi grešku za nezatvoren blok komentar.
-- EOF unutar (* ... je lekserska greška.
class Main {
    main() : Object {
        0
    };
};

(* Ovaj blok komentar nije zatvoren — EOF slijedi ovdje
