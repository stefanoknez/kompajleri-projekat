-- Testira parsiranje nasljeđivanja, višestrukih metoda i let-a u tijelu
class Animal {
    sound : String <- "...";
    speak() : String { sound };
};

class Dog inherits Animal {
    init() : SELF_TYPE {
        { sound <- "vau"; self; }
    };
    tricks(n : Int) : Int {
        let i : Int <- 0, result : Int <- 0 in {
            while i < n loop { result <- result + i; i <- i + 1; } pool;
            result;
        }
    };
};

class Main inherits IO {
    main() : Object {
        let d : Dog <- (new Dog).init() in
            out_string(d.speak())
    };
};
