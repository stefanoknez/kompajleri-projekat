#!/bin/bash
# Single build+run driver, called by the CodeBlocks PRE-BUILD step.
# Runs fully sequentially, so by the time the Terminal opens the binary is ready.
cd "$(dirname "$0")"
export PATH="/opt/homebrew/opt/flex/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

# Step 1: generate the C++ scanner from the flex grammar
/opt/homebrew/opt/flex/bin/flex -o lex.yy.cc cool.flex

# Step 2: compile (override FLEX so make finds it without relying on GUI PATH)
make FLEX=/opt/homebrew/opt/flex/bin/flex

# Step 3: copy binary to the location CodeBlocks/PA1_run.sh expect
mkdir -p bin/Debug
cp lexer bin/Debug/cool_lexer

# Step 4: open a Terminal window that runs the lexer on test.cl.
# Plain 'do script' (NOT 'quoted form of') => no osascript quoting bug.
osascript \
  -e 'tell application "Terminal" to do script "/Users/stefanoknez/PA1_run.sh"' \
  -e 'tell application "Terminal" to activate'
