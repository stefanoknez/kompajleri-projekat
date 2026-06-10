# Makefile za Cool parser (PA2)
# Upotreba:
#   make          — napravi `parser` binarni fajl
#   make test     — napravi, pa parsiraj good.cl
#   make clean    — obriši generisane fajlove
#
# Samostalno: flex skener direktno hrani bison parser, pa nisu potrebni
# referentni binarni fajlovi ni pipe-ovi (radi na macOS / Apple Silicon).

# alati koje koristimo (g++ za kompajliranje, flex za lekser, bison za parser)
CXX   = g++
FLEX  = flex
BISON = bison

CPPINCLUDE = -I.
# zastavice: c++11, debug info, upozorenja (par ih gasimo zbog starog support koda)
CXXFLAGS   = -std=c++11 -g -Wall -Wno-unused -Wno-write-strings -Wno-deprecated $(CPPINCLUDE)
BISONFLAGS = -d --defines=cool-parse.h -o cool-parse.cc -v

# Ručno pisani / dati support fajlovi (NISU generisani)
SUPPORT = tree.cc cool-tree.cc stringtab.cc utilities.cc dumptype.cc parser-main.cc

# Generisani fajlovi
GEN = cool-parse.cc lex.yy.cc

# sve pretvaramo u .o pa ih na kraju linkujemo zajedno
OBJS = $(GEN:.cc=.o) $(SUPPORT:.cc=.o)

.PHONY: all test clean

# podrazumijevani cilj — samo `make` pravi parser
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

# svaki .cc fajl u svoj .o
%.o: %.cc
	$(CXX) $(CXXFLAGS) -c $< -o $@

test: parser
	./parser good.cl

clean:
	rm -f $(GEN) cool-parse.h cool.output *.o parser
