# Makefile za Cool lekser (PA1)
# Upotreba:
#   make          — napravi lexer binarni fajl
#   make test     — pokreni lexer na test.cl
#   make clean    — obriši generisane fajlove

# alati koje koristimo (g++ za kompajliranje, flex za lekser)
CXX   = g++
FLEX  = flex

# zastavice: c++11 i upozorenja
CXXFLAGS = -std=c++11 -Wall -Wno-unused-function

# naši izvorni fajlovi
SRCS = stringtab.cc utilities.cc main.cc
GEN  = lex.yy.cc          # izlaz flexa, kompajlira se kao C++

.PHONY: all test clean

# podrazumijevani cilj — samo `make` pravi lexer
all: lexer

# Napravi C++ izvorni kod od flex fajla
$(GEN): cool.flex
	$(FLEX) -o $(GEN) cool.flex

# Iskompajliraj sve sa g++
lexer: $(GEN) $(SRCS)
	$(CXX) $(CXXFLAGS) -o lexer $(GEN) $(SRCS)

test: lexer
	./lexer test.cl

clean:
	rm -f $(GEN) lexer
