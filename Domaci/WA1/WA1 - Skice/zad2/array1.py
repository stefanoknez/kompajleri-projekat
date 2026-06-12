"""
zad2 / array1.py

Crta NFA za jezik "negdje se pojavi 'a' pa kasnije 'b'" (a prije b)
-> nfa_a_prije_b.png

q0 vrti u mjestu dok ne vidi 'a', pa skoci u q1; iz q1 na 'b' ide u q2 (zavrsno),
a q2 onda prima bilo sta.

Pokretanje:  python3 array1.py   (treba graphviz)
"""

from graphviz import Digraph

nfa = Digraph('NFA_a_prije_b', format='png')
nfa.attr(rankdir='LR')

# stanja (q2 je zavrsno -> dvostruki krug)
stanja = [
    ('start', 'Početno', 'point'),
    ('q0', 'q0', None),
    ('q1', 'q1', None),
    ('q2', 'q2', 'doublecircle'),
]
for cid, natpis, oblik in stanja:
    if oblik:
        nfa.node(cid, natpis, shape=oblik)
    else:
        nfa.node(cid, natpis)

# prelazi
prelazi = [
    ('start', 'q0', None),
    ('q0', 'q0', 'a,b,c'),   # cekamo prvo 'a'
    ('q0', 'q1', 'a'),
    ('q1', 'q1', 'a,c'),     # cekamo 'b'
    ('q1', 'q2', 'b'),
    ('q2', 'q2', 'a,b,c'),   # poslije toga sve prolazi
]
for iz, u, natpis in prelazi:
    if natpis:
        nfa.edge(iz, u, label=natpis)
    else:
        nfa.edge(iz, u)

nfa.render('nfa_a_prije_b', cleanup=True)
print("NFA je uspješno spremljen kao 'nfa_a_prije_b.png'")
