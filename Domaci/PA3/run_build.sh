#!/bin/bash
# Jedna skripta koja i builduje i pokreće PA3 semantički analizator, zove je
# CodeBlocks PRE-BUILD korak. Ide redom pa je binarni fajl spreman prije nego
# što se Terminal otvori. (Isto kao kod PA1/PA2.)
cd "$(dirname "$0")"
export PATH="/opt/homebrew/opt/bison/bin:/opt/homebrew/opt/flex/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

# Počisti stare .o fajlove (mogu biti kriva arhitektura) pa buildi čisto
make clean
make

# Kopiraj binarni fajl tamo gdje ga CodeBlocks / PA3_run.sh očekuju
mkdir -p bin/Debug
cp semant bin/Debug/semant

# Otvori Terminal prozor koji pokreće analizator na good.cl i bad.cl.
osascript \
  -e 'tell application "Terminal" to do script "/Users/stefanoknez/PA3_run.sh"' \
  -e 'tell application "Terminal" to activate'
