# Makefile za Cool parser (PA2)
# Upotreba:
#   make          — napravi `parser` binarni fajl
#   make test     — napravi, pa parsiraj good.cl
#   make clean    — obriši generisane fajlove
#
# Samostalno: flex skener direktno hrani bison parser, pa nisu potrebni
# referentni binarni fajlovi ni pipe-ovi (radi na macOS / Apple Silicon).

CXX   = g++
FLEX  = flex
BISON = bison

CPPINCLUDE = -I.
CXXFLAGS   = -std=c++11 -g -Wall -Wno-unused -Wno-write-strings -Wno-deprecated $(CPPINCLUDE)
BISONFLAGS = -d --defines=cool-parse.h -o cool-parse.cc -v

# Ručno pisani / dati support fajlovi (NISU generisani)
SUPPORT = tree.cc cool-tree.cc stringtab.cc utilities.cc dumptype.cc parser-main.cc

# Generisani fajlovi
GEN = cool-parse.cc lex.yy.cc

OBJS = $(GEN:.cc=.o) $(SUPPORT:.cc=.o)

.PHONY: all test clean

all: parser

# 1) bison: gramatika -> C++ parser + header
cool-parse.cc cool-parse.h: cool.y
	$(BISON) $(BISONFLAGS) cool.y

# 2) flex: skener -> C++ lekser (treba mu bison header zbog kodova tokena)
lex.yy.cc: cool.flex cool-parse.h
	$(FLEX) -o lex.yy.cc cool.flex

# 3) iskompajliraj i poveži sve u jedan samostalni parser
parser: $(OBJS)
	$(CXX) $(CXXFLAGS) -o parser $(OBJS)

%.o: %.cc
	$(CXX) $(CXXFLAGS) -c $< -o $@

test: parser
	./parser good.cl

clean:
	rm -f $(GEN) cool-parse.h cool.output *.o parser
