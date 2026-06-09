# Makefile za Cool lekser (PA1)
# Upotreba:
#   make          — napravi lexer binarni fajl
#   make test     — pokreni lexer na test.cl
#   make clean    — obriši generisane fajlove

CXX   = g++
FLEX  = flex

CXXFLAGS = -std=c++11 -Wall -Wno-unused-function

SRCS = stringtab.cc utilities.cc main.cc
GEN  = lex.yy.cc          # izlaz flexa, kompajlira se kao C++

.PHONY: all test clean

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
