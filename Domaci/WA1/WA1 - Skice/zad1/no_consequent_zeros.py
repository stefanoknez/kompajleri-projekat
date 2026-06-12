"""
zad1 / no_consequent_zeros.py

Dva automata za jezik "nizovi nula i jedinica BEZ dvije uzastopne nule":
  - DFA  ->  dfa_bez_uzastopnih_nula.png   (ima i mrtvo stanje C kad naletimo na "00")
  - NFA  ->  nfa_bez_uzastopnih_nula.png   (regex (1|01)*(0|ε))

Pokretanje:  python3 no_consequent_zeros.py   (treba graphviz)
"""

from graphviz import Digraph


def nacrtaj(naziv, stanja, prelazi, izlaz):
    """Mala pomocna: napravi graf iz liste stanja i prelaza pa ga snimi."""
    g = Digraph(naziv, format='png')
    g.attr(rankdir='LR')
    for cvor in stanja:
        cid, natpis, oblik = cvor
        g.node(cid, natpis, shape=oblik)
    for iz, u, natpis in prelazi:
        if natpis:
            g.edge(iz, u, label=natpis)
        else:
            g.edge(iz, u)
    g.render(izlaz, cleanup=True)


# --- 1) DFA: A=zadnja bila 1 (ili prazno), B=zadnja bila 0, C=mrtvo ("00") ---
dfa_stanja = [
    ('A', 'A (Zadnja 1 ili prazno)', 'doublecircle'),
    ('B', 'B (Zadnja 0)', 'doublecircle'),
    ('C', 'C (Mrtvo stanje - 00)', 'circle'),
]
dfa_prelazi = [
    ('A', 'A', '1'),
    ('A', 'B', '0'),
    ('B', 'A', '1'),
    ('B', 'C', '0'),     # druga nula zaredom -> upadamo u mrtvo stanje
    ('C', 'C', '0,1'),   # iz mrtvog stanja nema nazad
]
nacrtaj('DFA_BezUzastopnihNula', dfa_stanja, dfa_prelazi, 'dfa_bez_uzastopnih_nula')

# --- 2) NFA za (1|01)*(0|ε) --------------------------------------------
nfa_stanja = [
    ('start', 'Početno', 'point'),
    ('s0', 's0', 'doublecircle'),
    ('s1', 's1', 'circle'),
    ('s2', 's2', 'doublecircle'),
]
nfa_prelazi = [
    ('start', 's0', None),
    ('s0', 's0', '1'),
    ('s0', 's1', '0'),
    ('s1', 's0', '1'),
    ('s0', 's2', '0'),   # zavrsna nula (0|ε)
]
nacrtaj('NFA_BezUzastopnihNula', nfa_stanja, nfa_prelazi, 'nfa_bez_uzastopnih_nula')

print("Novi automati su uspješno generisani!")
