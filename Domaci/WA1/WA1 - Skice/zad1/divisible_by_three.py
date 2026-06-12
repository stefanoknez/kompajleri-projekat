"""
zad1 / divisible_by_three.py

Crta DFA koji prepoznaje binarne brojeve djeljive sa 3 -> dfa_djeljivi_s_3.png

Caka: stanja pamte ostatak pri dijeljenju sa 3 (S0=0, S1=1, S2=2).
Kad procitas novi bit b, novi ostatak je (2*stari + b) % 3 — odatle prelazi.
Zavrsno stanje je S0 (ostatak 0 = broj je djeljiv sa 3).

Pokretanje:  python3 divisible_by_three.py   (treba graphviz)
"""

from graphviz import Digraph

dfa = Digraph('DFA_DjeljiviS3', format='png')
dfa.attr(rankdir='LR')  # s lijeva na desno

# stanja: S0 je i pocetno i zavrsno (dvostruki krug)
dfa.node('start', 'Početno', shape='point')   # samo strelica "odakle krece"
dfa.node('S0', 'S0 (Ostatak 0)', shape='doublecircle')
dfa.node('S1', 'S1 (Ostatak 1)', shape='circle')
dfa.node('S2', 'S2 (Ostatak 2)', shape='circle')

# prelazi po formuli novi_ostatak = (2*stari + bit) % 3
prelazi = [
    ('start', 'S0', None),  # ulazimo u pocetno stanje
    ('S0', 'S0', '0'),
    ('S0', 'S1', '1'),
    ('S1', 'S2', '0'),
    ('S1', 'S0', '1'),
    ('S2', 'S1', '0'),
    ('S2', 'S2', '1'),
]
for iz, u, natpis in prelazi:
    if natpis:
        dfa.edge(iz, u, label=natpis)
    else:
        dfa.edge(iz, u)

dfa.render('dfa_djeljivi_s_3', cleanup=True)
print("Automat je uspješno generisan kao 'dfa_djeljivi_s_3.png'")
