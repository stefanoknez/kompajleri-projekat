"""
zad1 / three_zeros.py

Dva automata za jezik "stringovi sa MANJE od tri nule" (najvise dvije 0):
  - DFA  ->  dfa_manje_od_tri_nule.png   (q0,q1,q2 broje nule; q3 = mrtvo, treca nula)
  - NFA  ->  nfa_manje_od_tri_nule.png   (strukturni prikaz unije tri grane)

Pokretanje:  python3 three_zeros.py   (treba graphviz)
"""

from graphviz import Digraph


def nacrtaj(naziv, stanja, prelazi, izlaz):
    """Napravi graf iz lista (stanja, prelazi) i snimi ga kao PNG."""
    g = Digraph(naziv, format='png')
    g.attr(rankdir='LR')
    for cid, natpis, oblik in stanja:
        g.node(cid, natpis, shape=oblik)
    for iz, u, natpis in prelazi:
        if natpis:
            g.edge(iz, u, label=natpis)
        else:
            g.edge(iz, u)
    g.render(izlaz, cleanup=True)


# --- 1) DFA: brojimo nule (0,1,2 su ok = zavrsna; treca nula -> mrtvo q3) ---
dfa_stanja = [
    ('q0', 'q0 (0 nula)', 'doublecircle'),
    ('q1', 'q1 (1 nula)', 'doublecircle'),
    ('q2', 'q2 (2 nule)', 'doublecircle'),
    ('q3', 'q3 (Mrtvo stanje)', 'circle'),
]
dfa_prelazi = [
    ('q0', 'q0', '1'),
    ('q0', 'q1', '0'),
    ('q1', 'q1', '1'),
    ('q1', 'q2', '0'),
    ('q2', 'q2', '1'),
    ('q2', 'q3', '0'),     # treca nula = previse, padamo u mrtvo
    ('q3', 'q3', '0,1'),
]
nacrtaj('DFA_ManjeOdTriNule', dfa_stanja, dfa_prelazi, 'dfa_manje_od_tri_nule')

# --- 2) NFA: unija tri grane (0 nula: 1*, 1 nula: 1*01*, 2 nule: 1*01*01*) ---
nfa_stanja = [
    ('start', 'Početno', 'point'),
    ('s0', 's0', 'doublecircle'),
    ('s1', 's1', 'doublecircle'),
    ('s2', 's2', 'circle'),
    ('s3', 's3', 'doublecircle'),
    ('s4', 's4', 'circle'),
    ('s5', 's5', 'doublecircle'),
]
nfa_prelazi = [
    ('start', 's0', None),
    ('s0', 's0', '1'),
    ('s0', 's1', 'ε'),     # grana sa 0 nula
    # grana 1*01* (tacno jedna nula)
    ('s0', 's2', '0'),
    ('s2', 's2', '1'),
    ('s2', 's3', 'ε'),
    ('s3', 's3', '1'),
    # grana 1*01*01* (tacno dvije nule)
    ('s0', 's4', '0'),
    ('s4', 's4', '1'),
    ('s4', 's5', '0'),
    ('s5', 's5', '1'),
]
nacrtaj('NFA_ManjeOdTriNule', nfa_stanja, nfa_prelazi, 'nfa_manje_od_tri_nule')

print("Automati su uspješno generisani!")
