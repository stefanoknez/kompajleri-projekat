#!/bin/bash
# Brzi testovi za Cool lekser (PA1).
# Napravi lekser, pa provjeri skup ciljanih ulaza:
#   - strings.cl   — escape sekvence i stringovi
#   - comments.cl  — linijski i ugniježđeni blok komentari
#   - keywords.cl  — case-insensitivnost ključnih riječi
#   - operators.cl — operatori i specijalni znakovi
#   - identifiers.cl — TYPEID vs OBJECTID vs bool konstante
#   - err_string.cl  — mora da prijavi ERROR (nezatvoren string)
#   - err_comment.cl — mora da prijavi ERROR (nezatvoren komentar)
#
# Upotreba:  bash tests/run_tests.sh

cd "$(dirname "$0")/.."

make -s 2>/dev/null || { echo "BUILD FAILED"; exit 1; }

fail=0

# lexer treba da radi bez ERROR tokena
check_ok() {
    out=$(./lexer "$1" 2>&1)
    if echo "$out" | grep -q "^#[0-9]* ERROR"; then
        echo "FAIL  $1 (neočekivana greška)"
        fail=1
    else
        echo "OK    $1"
    fi
}

# lexer mora da ispiše barem jedan ERROR token
check_err() {
    out=$(./lexer "$1" 2>&1)
    if echo "$out" | grep -q "^#[0-9]* ERROR"; then
        echo "OK    $1 (greška ispravno prijavljena)"
    else
        echo "FAIL  $1 (trebalo je da bude ERROR)"
        fail=1
    fi
}

check_ok  tests/strings.cl
check_ok  tests/comments.cl
check_ok  tests/keywords.cl
check_ok  tests/operators.cl
check_ok  tests/identifiers.cl
check_err tests/err_string.cl
check_err tests/err_comment.cl

if [ $fail -eq 0 ]; then echo "=== SVI TESTOVI PROŠLI ==="; else echo "=== NEKI TESTOVI NISU PROŠLI ==="; fi
exit $fail
