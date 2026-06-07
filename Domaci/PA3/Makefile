# Makefile for the Cool semantic analyzer (PA3)
# Usage:
#   make          — build the `semant` binary
#   make test     — build, then analyze good.cl
#   make clean    — remove generated files
#
# Self-contained: lexer + parser + semantic analyzer are linked into ONE
# executable (no reference binaries / pipes), so it runs on macOS.

CXX   = g++
FLEX  = flex
BISON = bison

CPPINCLUDE = -I.
CXXFLAGS   = -std=c++11 -g -Wall -Wno-unused -Wno-write-strings -Wno-deprecated $(CPPINCLUDE)
BISONFLAGS = -d --defines=cool-parse.h -o cool-parse.cc -v

# Provided support sources (not generated)
SUPPORT = tree.cc cool-tree.cc stringtab.cc utilities.cc dumptype.cc \
          semant.cc semant-main.cc

# Generated sources
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
