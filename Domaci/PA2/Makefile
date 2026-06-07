# Makefile for the Cool parser (PA2)
# Usage:
#   make          — build the `parser` binary
#   make test     — build, then parse good.cl
#   make clean    — remove generated files
#
# Self-contained: the flex scanner feeds the bison parser directly, so no
# reference binaries or pipes are needed (works on macOS / Apple Silicon).

CXX   = g++
FLEX  = flex
BISON = bison

CPPINCLUDE = -I.
CXXFLAGS   = -std=c++11 -g -Wall -Wno-unused -Wno-write-strings -Wno-deprecated $(CPPINCLUDE)
BISONFLAGS = -d --defines=cool-parse.h -o cool-parse.cc -v

# Hand-written / provided support sources (NOT generated)
SUPPORT = tree.cc cool-tree.cc stringtab.cc utilities.cc dumptype.cc parser-main.cc

# Generated sources
GEN = cool-parse.cc lex.yy.cc

OBJS = $(GEN:.cc=.o) $(SUPPORT:.cc=.o)

.PHONY: all test clean

all: parser

# 1) bison: grammar -> C++ parser + header
cool-parse.cc cool-parse.h: cool.y
	$(BISON) $(BISONFLAGS) cool.y

# 2) flex: scanner -> C++ lexer (needs the bison header for token codes)
lex.yy.cc: cool.flex cool-parse.h
	$(FLEX) -o lex.yy.cc cool.flex

# 3) compile & link everything into one standalone parser
parser: $(OBJS)
	$(CXX) $(CXXFLAGS) -o parser $(OBJS)

%.o: %.cc
	$(CXX) $(CXXFLAGS) -c $< -o $@

test: parser
	./parser good.cl

clean:
	rm -f $(GEN) cool-parse.h cool.output *.o parser
