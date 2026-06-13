#!/bin/bash
# Provjera sintakse svih Python skripti u WA2 - Skice.
# Radi py_compile na svakom fajlu.
#
# Upotreba: bash provjera.sh (iz foldera WA2 - Skice)

cd "$(dirname "$0")"

fail=0
for fajl in zad1/*.py zad2/*.py zad3/*.py zad4/*.py zad5/*.py; do
    if python3 -m py_compile "$fajl" 2>/dev/null; then
        echo "OK    $fajl"
    else
        echo "FAIL  $fajl"
        fail=1
    fi
done

find . -name "*.pyc" -delete 2>/dev/null
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null

if [ $fail -eq 0 ]; then
    echo "=== SVE SKRIPTE PROŠLE PROVJERU ==="
else
    echo "=== NEKE SKRIPTE IMAJU GREŠKU ==="
fi
exit $fail
