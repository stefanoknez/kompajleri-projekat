#!/bin/bash
# Jedna skripta koja i builduje i pokreće, zove je CodeBlocks PRE-BUILD korak.
# Ide potpuno redom, pa kad se Terminal otvori binarni fajl je već spreman.
cd "$(dirname "$0")"
export PATH="/opt/homebrew/opt/flex/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

# Korak 1: napravi C++ skener od flex gramatike
/opt/homebrew/opt/flex/bin/flex -o lex.yy.cc cool.flex

# Korak 2: iskompajliraj (zadajem FLEX da ga make nađe bez oslanjanja na GUI PATH)
make FLEX=/opt/homebrew/opt/flex/bin/flex

# Korak 3: kopiraj binarni fajl tamo gdje ga CodeBlocks/PA1_run.sh očekuju
mkdir -p bin/Debug
cp lexer bin/Debug/cool_lexer

# Korak 4: otvori Terminal prozor koji pokreće lexer na test.cl.
# Obični 'do script' (NE 'quoted form of') => nema bug-a sa navodnicima u osascript-u.
osascript \
  -e 'tell application "Terminal" to do script "/Users/stefanoknez/PA1_run.sh"' \
  -e 'tell application "Terminal" to activate'
