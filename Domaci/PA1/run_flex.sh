#!/bin/bash
# Called by the CodeBlocks pre-build step.
# cd to the script's own directory first so flex can find cool.flex,
# regardless of what working directory CodeBlocks happens to use.
cd "$(dirname "$0")"
export PATH="/opt/homebrew/opt/flex/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

# Step 1: generate the C++ scanner from the flex grammar
/opt/homebrew/opt/flex/bin/flex -o lex.yy.cc cool.flex

# Step 2: compile everything (override FLEX so make finds it without relying on PATH)
make FLEX=/opt/homebrew/opt/flex/bin/flex

# Step 3: copy binary to the location CodeBlocks expects
mkdir -p bin/Debug
cp lexer bin/Debug/cool_lexer
