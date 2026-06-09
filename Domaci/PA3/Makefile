# Makefile za Cool semantički analizator (PA3)
# Upotreba:
#   make          — napravi `semant` binarni fajl
#   make test     — napravi, pa analiziraj good.cl
#   make clean    — obriši generisane fajlove
#
# Samostalno: lekser + parser + semantički analizator su povezani u JEDAN
# izvršni fajl (bez referentnih binarnih fajlova / pipe-ova), pa radi na macOS-u.

CXX   = g++
FLEX  = flex
BISON = bison

CPPINCLUDE = -I.
CXXFLAGS   = -std=c++11 -g -Wall -Wno-unused -Wno-write-strings -Wno-deprecated $(CPPINCLUDE)
BISONFLAGS = -d --defines=cool-parse.h -o cool-parse.cc -v

# Dati support fajlovi (nisu generisani)
SUPPORT = tree.cc cool-tree.cc stringtab.cc utilities.cc dumptype.cc \
          semant.cc semant-main.cc

# Generisani fajlovi
GEN = cool-parse.cc lex.yy.cc

OBJS = $(GEN:.cc=.o) $(SUPPORT:.cc=.o)

.PHONY: all test clean

all: semant

cool-parse.cc cool-parse.h: cool.y
	$(BISON) $(BISONFLAGS) cool.y

lex.yy.cc: cool.flex cool-parse.h
	$(FLEX) -o lex.yy.cc cool.flex

semant: $(OBJS)
	$(CXX) $(CXXFLAGS) -o semant $(OBJS)

%.o: %.cc
	$(CXX) $(CXXFLAGS) -c $< -o $@

test: semant
	./semant good.cl

clean:
	rm -f $(GEN) cool-parse.h cool-parse.output cool.output *.o semant
