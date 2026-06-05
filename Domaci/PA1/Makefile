# Makefile for Cool Lexer (PA1)
# Usage:
#   make          — build the lexer binary
#   make test     — run the lexer on test.cl
#   make clean    — remove generated files

CXX   = g++
FLEX  = flex

CXXFLAGS = -std=c++11 -Wall -Wno-unused-function

SRCS = stringtab.cc utilities.cc main.cc
GEN  = lex.yy.cc          # flex output compiled as C++

.PHONY: all test clean

all: lexer

# Generate C++ source from the flex file
$(GEN): cool.flex
	$(FLEX) -o $(GEN) cool.flex

# Compile everything with g++
lexer: $(GEN) $(SRCS)
	$(CXX) $(CXXFLAGS) -o lexer $(GEN) $(SRCS)

test: lexer
	./lexer test.cl

clean:
	rm -f $(GEN) lexer
