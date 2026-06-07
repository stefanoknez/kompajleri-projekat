#!/bin/bash
# Smoke tests for the Cool semantic analyzer (PA3).
# Builds, then checks valid programs pass and erroneous programs are rejected.
#
# Usage:  bash tests/run_tests.sh
cd "$(dirname "$0")/.."
export PATH="/opt/homebrew/opt/bison/bin:/opt/homebrew/opt/flex/bin:$PATH"

make >/dev/null || { echo "BUILD FAILED"; exit 1; }

fail=0
ok ()  { if ./semant "$1" >/dev/null 2>&1; then echo "OK    $1 accepted";  else echo "FAIL  $1 should pass";     fail=1; fi; }
err () { if ./semant "$1" >/dev/null 2>&1; then echo "FAIL  $1 should fail"; fail=1; else echo "OK    $1 rejected"; fi; }

# valid programs
ok  good.cl
ok  tests/selftype.cl
# semantic errors
err bad.cl
err tests/cycle.cl
err tests/undef.cl
err tests/inhint.cl
err tests/nomain.cl
err tests/redef.cl
err tests/nomainmeth.cl
err tests/selfbad.cl

if [ $fail -eq 0 ]; then echo "=== ALL TESTS PASSED ==="; else echo "=== SOME TESTS FAILED ==="; fi
exit $fail
