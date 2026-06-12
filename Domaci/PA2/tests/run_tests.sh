#!/bin/bash
# Brzi testovi za Cool parser (PA2).
# Napravi parser, pa provjeri skup ciljanih ulaza:
#   - prioritet / asocijativnost (prec.cl)
#   - let se proteže udesno + više vezivanja (lets.cl)
#   - lanci dispatch / static dispatch (disp.cl)
#   - case / if / block (ctrl.cl)
#   - nonassoc poređenje MORA da bude sintaksna greška (nonassoc.cl)
#
# Upotreba:  bash tests/run_tests.sh
cd "$(dirname "$0")/.."
export PATH="/opt/homebrew/opt/bison/bin:/opt/homebrew/opt/flex/bin:$PATH"

make >/dev/null || { echo "BUILD FAILED"; exit 1; }

fail=0
check_ok () {   # fajl treba uspješno da se isparsira
    if ./parser "$1" >/dev/null 2>&1; then echo "OK    $1 parses"; else echo "FAIL  $1 should parse"; fail=1; fi
}
check_err () {  # fajl treba da bude odbijen
    if ./parser "$1" >/dev/null 2>&1; then echo "FAIL  $1 should be rejected"; fail=1; else echo "OK    $1 correctly rejected"; fi
}

check_ok  tests/prec.cl
check_ok  tests/lets.cl
check_ok  tests/disp.cl
check_ok  tests/ctrl.cl
check_ok  tests/inherit.cl
check_err tests/nonassoc.cl
check_ok  good.cl
check_err bad.cl

if [ $fail -eq 0 ]; then echo "=== ALL TESTS PASSED ==="; else echo "=== SOME TESTS FAILED ==="; fi
exit $fail
