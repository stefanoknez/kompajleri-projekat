"""
zad3 / dfa_c.py

DFA iz NFA subset konstrukcijom, varijanta (c) -> transformirani_dfa_c.png
Ovo je najveci od tri (7 stanja), pa zato prelaze drzim u listi i samo ih
provrtim u petlji — mnogo preglednije nego 21 zaseban edge() poziv.

Zavrsna stanja: q01234, q0234, q034 (dvostruki krug).

Pokretanje:  python3 dfa_c.py   (treba graphviz)
"""

from graphviz import Digraph

dfa = Digraph('NFA_to_DFA_C', format='png')
dfa.attr(rankdir='LR')

stanja = [
    ('start', 'Početno', 'point'),
    ('q0', 'q0', None),
    ('q0123', 'q0123', None),
    ('q023', 'q023', None),
    ('q03', 'q03', None),
    ('q01234', 'q01234', 'doublecircle'),
    ('q0234', 'q0234', 'doublecircle'),
    ('q034', 'q034', 'doublecircle'),
]
for cid, natpis, oblik in stanja:
    if oblik:
        dfa.node(cid, natpis, shape=oblik)
    else:
        dfa.node(cid, natpis)

# svaki red = jedno stanje i kuda ide na a / b / c
prelazi = [
    ('start', 'q0', None),
    # iz q0
    ('q0', 'q0123', 'a'), ('q0', 'q023', 'b'), ('q0', 'q03', 'c'),
    # iz q0123
    ('q0123', 'q01234', 'a'), ('q0123', 'q0234', 'b'), ('q0123', 'q034', 'c'),
    # iz q023
    ('q023', 'q0123', 'a'), ('q023', 'q0234', 'b'), ('q023', 'q034', 'c'),
    # iz q03
    ('q03', 'q0123', 'a'), ('q03', 'q023', 'b'), ('q03', 'q034', 'c'),
    # iz q01234
    ('q01234', 'q01234', 'a'), ('q01234', 'q0234', 'b'), ('q01234', 'q034', 'c'),
    # iz q0234
    ('q0234', 'q0123', 'a'), ('q0234', 'q0234', 'b'), ('q0234', 'q034', 'c'),
    # iz q034
    ('q034', 'q0123', 'a'), ('q034', 'q023', 'b'), ('q034', 'q034', 'c'),
]
for iz, u, slovo in prelazi:
    if slovo:
        dfa.edge(iz, u, label=slovo)
    else:
        dfa.edge(iz, u)

dfa.render('transformirani_dfa_c', cleanup=True)
print("DFA graf pod (c) je uspješno spremljen!")
