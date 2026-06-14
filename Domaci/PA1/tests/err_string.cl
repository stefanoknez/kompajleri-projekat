-- Testira da lekser ispravno prijavi grešku za nezatvoren string.
-- String koji prelazi u novi red bez backslash-a je lekserska greška.
class Main {
    main() : Object {
        let s : String <- "ovaj string nije zatvoren
        in s
    };
};
