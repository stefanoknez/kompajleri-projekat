#!/bin/bash
# Single build+run driver for the PA3 semantic analyzer, called by the
# CodeBlocks PRE-BUILD step. Runs sequentially so the binary is ready before
# the Terminal opens. (Same pattern as PA1/PA2.)
cd "$(dirname "$0")"
export PATH="/opt/homebrew/opt/bison/bin:/opt/homebrew/opt/flex/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin"

# Build: bison -> flex -> compile/link into ./semant
make

# Copy binary where CodeBlocks / PA3_run.sh expect it
mkdir -p bin/Debug
cp semant bin/Debug/semant

# Open a Terminal window that runs the analyzer on good.cl and bad.cl.
osascript \
  -e 'tell application "Terminal" to do script "/Users/stefanoknez/PA3_run.sh"' \
  -e 'tell application "Terminal" to activate'
