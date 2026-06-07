#!/bin/bash
# Smoke tests for the Cool parser (PA2).
# Builds the parser, then checks a set of focused inputs:
#   - precedence / associativity (prec.cl)
#   - let extends-right + multiple bindings (lets.cl)
#   - dispatch / static dispatch chains (disp.cl)
#   - case / if / block (ctrl.cl)
#   - nonassoc comparison MUST be a syntax error (nonassoc.cl)
#
# Usage:  bash tests/run_tests.sh
cd "$(dirname "$0")/.."
export PATH="/opt/homebrew/opt/bison/bin:/opt/homebrew/opt/flex/bin:$PATH"

make >/dev/null || { echo "BUILD FAILED"; exit 1; }

fail=0
check_ok () {   # file should parse successfully
    if ./parser "$1" >/dev/null 2>&1; then echo "OK    $1 parses"; else echo "FAIL  $1 should parse"; fail=1; fi
}
check_err () {  # file should be rejected
    if ./parser "$1" >/dev/null 2>&1; then echo "FAIL  $1 should be rejected"; fail=1; else echo "OK    $1 correctly rejected"; fi
}

check_ok  tests/prec.cl
check_ok  tests/lets.cl
check_ok  tests/disp.cl
check_ok  tests/ctrl.cl
check_err tests/nonassoc.cl
check_ok  good.cl
check_err bad.cl

if [ $fail -eq 0 ]; then echo "=== ALL TESTS PASSED ==="; else echo "=== SOME TESTS FAILED ==="; fi
exit $fail
