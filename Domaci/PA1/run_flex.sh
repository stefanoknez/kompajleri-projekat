#!/bin/bash
# Called by the CodeBlocks pre-build step.
# cd to the script's own directory first so flex can find cool.flex,
# regardless of what working directory CodeBlocks happens to use.
cd "$(dirname "$0")"
/opt/homebrew/opt/flex/bin/flex -o lex.yy.cc cool.flex
