#!/bin/bash
# Jedna skripta koja i builduje i pokreće PA2 parser, zove je CodeBlocks
# PRE-BUILD korak. Ide potpuno redom, pa kad se Terminal otvori binarni fajl
# je već spreman. (Isto kao kod PA1.)
cd "$(dirname "$0")"
export PATH="/opt/homebrew/opt/bison/bin:/opt/homebrew/opt/flex/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

# Build: bison -> flex -> kompajliranje/povezivanje u ./parser
make

# Kopiraj binarni fajl tamo gdje ga CodeBlocks / PA2_run.sh očekuju
mkdir -p bin/Debug
cp parser bin/Debug/parser

# Otvori Terminal prozor koji pokreće parser na good.cl.
# Obični 'do script' (NE 'quoted form of') => nema bug-a sa navodnicima u osascript-u.
osascript \
  -e 'tell application "Terminal" to do script "/Users/stefanoknez/PA2_run.sh"' \
  -e 'tell application "Terminal" to activate'
