#!/bin/bash
# Single build+run driver for the PA2 parser, called by the CodeBlocks
# PRE-BUILD step. Runs fully sequentially, so by the time the Terminal opens
# the binary is ready. (Mirrors the PA1 setup.)
cd "$(dirname "$0")"
export PATH="/opt/homebrew/opt/bison/bin:/opt/homebrew/opt/flex/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

# Build: bison -> flex -> compile/link into ./parser
make

# Copy binary to the location CodeBlocks / PA2_run.sh expect
mkdir -p bin/Debug
cp parser bin/Debug/parser

# Open a Terminal window that runs the parser on good.cl.
# Plain 'do script' (NOT 'quoted form of') => no osascript quoting bug.
osascript \
  -e 'tell application "Terminal" to do script "/Users/stefanoknez/PA2_run.sh"' \
  -e 'tell application "Terminal" to activate'
