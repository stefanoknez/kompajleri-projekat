"""
zad2 / neparni.py

Pravi dvije stvari za jezik "neparan broj bar jednog od slova a, b ili c":
  1) NFA dijagram        ->  nfa_neparni.png
  2) tablicu prelaza NFA ->  tablica_neparni.png

NFA na pocetku epsilon-granama "pogadja" za koje slovo brojimo parnost
(tri grane: A za 'a', B za 'b', C za 'c'). Svaka grana ima par/nepar stanje
i prebacuje se kad procita "svoje" slovo.

Pokretanje:  python3 neparni.py   (treba graphviz + matplotlib)
"""

from graphviz import Digraph
import matplotlib.pyplot as plt

# =====================================================================
# 1) NFA DIJAGRAM
# =====================================================================
nfa = Digraph('NFA_Neparni_Znakovi', format='png')
nfa.attr(rankdir='LR')

# stanja: *_nep su zavrsna (neparan broj -> dvostruki krug)
stanja = [
    ('start', 'Početno', 'point'),
    ('q0', 'q0', None),
    ('A_par', 'A_par', None),
    ('A_nep', 'A_nep', 'doublecircle'),
    ('B_par', 'B_par', None),
    ('B_nep', 'B_nep', 'doublecircle'),
    ('C_par', 'C_par', None),
    ('C_nep', 'C_nep', 'doublecircle'),
]
for cid, natpis, oblik in stanja:
    if oblik:
        nfa.node(cid, natpis, shape=oblik)
    else:
        nfa.node(cid, natpis)

# prelazi: prvo epsilon "biranje" grane, pa za svaku granu par<->nepar logika
prelazi = [
    ('start', 'q0', None),
    # epsilon skok u sve tri grane (NFA pogadja koju parnost pratimo)
    ('q0', 'A_par', 'ε'),
    ('q0', 'B_par', 'ε'),
    ('q0', 'C_par', 'ε'),
    # grana A: 'a' mijenja parnost, ostala slova ne diraju
    ('A_par', 'A_nep', 'a'),
    ('A_nep', 'A_par', 'a'),
    ('A_par', 'A_par', 'b,c'),
    ('A_nep', 'A_nep', 'b,c'),
    # grana B: 'b' mijenja parnost
    ('B_par', 'B_nep', 'b'),
    ('B_nep', 'B_par', 'b'),
    ('B_par', 'B_par', 'a,c'),
    ('B_nep', 'B_nep', 'a,c'),
    # grana C: 'c' mijenja parnost
    ('C_par', 'C_nep', 'c'),
    ('C_nep', 'C_par', 'c'),
    ('C_par', 'C_par', 'a,b'),
    ('C_nep', 'C_nep', 'a,b'),
]
for iz, u, natpis in prelazi:
    if natpis:
        nfa.edge(iz, u, label=natpis)
    else:
        nfa.edge(iz, u)

nfa.render('nfa_neparni', cleanup=True)
print("NFA graf je uspješno spremljen!")

# =====================================================================
# 2) TABLICA PRELAZA (kao slika)
# =====================================================================
stupci = ['Stanje', 'Ulaz a', 'Ulaz b', 'Ulaz c', 'Ulaz ε']
podaci = [
    ['q0 (Početno)', 'Ø', 'Ø', 'Ø', '{A_par, B_par, C_par}'],
    ['A_par', '{A_nep}', '{A_par}', '{A_par}', 'Ø'],
    ['A_nep (Završno)', '{A_par}', '{A_nep}', '{A_nep}', 'Ø'],
    ['B_par', '{B_par}', '{B_nep}', '{B_par}', 'Ø'],
    ['B_nep (Završno)', '{B_nep}', '{B_par}', '{B_nep}', 'Ø'],
    ['C_par', '{C_par}', '{C_par}', '{C_nep}', 'Ø'],
    ['C_nep (Završno)', '{C_nep}', '{C_nep}', '{C_par}', 'Ø'],
]

fig, ax = plt.subplots(figsize=(9, 4))
ax.axis('off')

tablica = ax.table(cellText=podaci, colLabels=stupci, loc='center', cellLoc='center')
tablica.auto_set_font_size(False)
tablica.set_fontsize(10)
tablica.auto_set_column_width(col=list(range(len(stupci))))
tablica.scale(1, 1.8)

# zaglavlje tamno-plavo, prva kolona bold
for (red, kol), celija in tablica.get_celld().items():
    if red == 0:
        celija.set_text_props(weight='bold', color='white')
        celija.set_facecolor('#2C3E50')
    elif red > 0 and kol == 0:
        celija.set_text_props(weight='bold')

plt.savefig('tablica_neparni.png', bbox_inches='tight', dpi=300)
print("Tablica prelaza je uspješno spremljena!")
