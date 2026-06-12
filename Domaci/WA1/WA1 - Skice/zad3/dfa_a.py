"""
zad3 / dfa_a.py

DFA dobijen iz NFA postupkom podskupova (subset construction), varijanta (a)
-> transformirani_dfa.png

Stanja su skupovi NFA-stanja: q0, q1, q01 (={q0,q1}) i mrtvo stanje qØ.
q1 i q01 su zavrsna (dvostruki krug).

Pokretanje:  python3 dfa_a.py   (treba graphviz)
"""

from graphviz import Digraph

dfa = Digraph('NFA_to_DFA', format='png')
dfa.attr(rankdir='LR')

# stanja (id, natpis, oblik)
stanja = [
    ('start', 'Početno', 'point'),
    ('q0', 'q0', None),
    ('q1', 'q1', 'doublecircle'),
    ('q01', 'q01', 'doublecircle'),
    ('q_empty', 'qØ', 'circle'),
]
for cid, natpis, oblik in stanja:
    if oblik:
        dfa.node(cid, natpis, shape=oblik)
    else:
        dfa.node(cid, natpis)

# prelazi (iz, u, slovo) — prepisani iz tablice subset konstrukcije
prelazi = [
    ('start', 'q0', None),
    # iz q0
    ('q0', 'q_empty', 'a'),
    ('q0', 'q1', 'b'),
    ('q0', 'q01', 'c'),
    # iz q1
    ('q1', 'q0', 'a'),
    ('q1', 'q_empty', 'b'),
    ('q1', 'q1', 'c'),
    # iz q01
    ('q01', 'q0', 'a'),
    ('q01', 'q1', 'b'),
    ('q01', 'q01', 'c'),
    # mrtvo stanje ostaje mrtvo
    ('q_empty', 'q_empty', 'a,b,c'),
]
for iz, u, slovo in prelazi:
    if slovo:
        dfa.edge(iz, u, label=slovo)
    else:
        dfa.edge(iz, u)

dfa.render('transformirani_dfa', cleanup=True)
print("DFA graf je uspješno spremljen!")
