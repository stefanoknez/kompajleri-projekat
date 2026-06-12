"""
zad3 / dfa_b.py

DFA iz NFA subset konstrukcijom, varijanta (b) -> transformirani_dfa_b.png

Stanja su skupovi: q0, q01, q012, q02 i mrtvo qØ.
q012 i q02 su zavrsna (dvostruki krug).

Pokretanje:  python3 dfa_b.py   (treba graphviz)
"""

from graphviz import Digraph

dfa = Digraph('NFA_to_DFA_B', format='png')
dfa.attr(rankdir='LR')

stanja = [
    ('start', 'Početno', 'point'),
    ('q0', 'q0', None),
    ('q01', 'q01', None),
    ('q012', 'q012', 'doublecircle'),
    ('q02', 'q02', 'doublecircle'),
    ('q_empty', 'qØ', 'circle'),
]
for cid, natpis, oblik in stanja:
    if oblik:
        dfa.node(cid, natpis, shape=oblik)
    else:
        dfa.node(cid, natpis)

prelazi = [
    ('start', 'q0', None),
    # iz q0
    ('q0', 'q_empty', 'a'),
    ('q0', 'q01', 'b'),
    ('q0', 'q0', 'c'),
    # iz q01
    ('q01', 'q_empty', 'a'),
    ('q01', 'q01', 'b'),
    ('q01', 'q012', 'c'),
    # iz q012
    ('q012', 'q02', 'a'),
    ('q012', 'q01', 'b'),
    ('q012', 'q012', 'c'),
    # iz q02
    ('q02', 'q02', 'a'),
    ('q02', 'q01', 'b'),
    ('q02', 'q0', 'c'),
    # mrtvo stanje
    ('q_empty', 'q_empty', 'a,b,c'),
]
for iz, u, slovo in prelazi:
    if slovo:
        dfa.edge(iz, u, label=slovo)
    else:
        dfa.edge(iz, u)

dfa.render('transformirani_dfa_b', cleanup=True)
print("DFA graf pod (b) je uspješno spremljen!")
