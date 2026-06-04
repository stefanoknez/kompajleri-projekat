from graphviz import Digraph
import matplotlib.pyplot as plt

# 1. GENERIRANJE DIJAGRAMA AUTOMATA (NFA)
nfa = Digraph('NFA_Neparni_Znakovi', format='png')
nfa.attr(rankdir='LR')

# Stanja
nfa.node('start', 'Početno', shape='point')
nfa.node('q0', 'q0')
nfa.node('A_par', 'A_par')
nfa.node('A_nep', 'A_nep', shape='doublecircle')
nfa.node('B_par', 'B_par')
nfa.node('B_nep', 'B_nep', shape='doublecircle')
nfa.node('C_par', 'C_par')
nfa.node('C_nep', 'C_nep', shape='doublecircle')

# Početni smjer i epsilon prijelazi
nfa.edge('start', 'q0')
nfa.edge('q0', 'A_par', label='ε')
nfa.edge('q0', 'B_par', label='ε')
nfa.edge('q0', 'C_par', label='ε')

# Grana za A
nfa.edge('A_par', 'A_nep', label='a')
nfa.edge('A_nep', 'A_par', label='a')
nfa.edge('A_par', 'A_par', label='b,c')
nfa.edge('A_nep', 'A_nep', label='b,c')

# Grana za B
nfa.edge('B_par', 'B_nep', label='b')
nfa.edge('B_nep', 'B_par', label='b')
nfa.edge('B_par', 'B_par', label='a,c')
nfa.edge('B_nep', 'B_nep', label='a,c')

# Grana za C
nfa.edge('C_par', 'C_nep', label='c')
nfa.edge('C_nep', 'C_par', label='c')
nfa.edge('C_par', 'C_par', label='a,b')
nfa.edge('C_nep', 'C_nep', label='a,b')

nfa.render('nfa_neparni', cleanup=True)
print("NFA graf je uspješno spremljen!")

# 2. GENERIRANJE SLIKE TABLICE PRIJELAZA
stupci = ['Stanje', 'Ulaz a', 'Ulaz b', 'Ulaz c', 'Ulaz ε']
podaci = [
    ['q0 (Početno)', 'Ø', 'Ø', 'Ø', '{A_par, B_par, C_par}'],
    ['A_par', '{A_nep}', '{A_par}', '{A_par}', 'Ø'],
    ['A_nep (Završno)', '{A_par}', '{A_nep}', '{A_nep}', 'Ø'],
    ['B_par', '{B_par}', '{B_nep}', '{B_par}', 'Ø'],
    ['B_nep (Završno)', '{B_nep}', '{B_par}', '{B_nep}', 'Ø'],
    ['C_par', '{C_par}', '{C_par}', '{C_nep}', 'Ø'],
    ['C_nep (Završno)', '{C_nep}', '{C_nep}', '{C_par}', 'Ø']
]

fig, ax = plt.subplots(figsize=(9, 4))
ax.axis('off')

tablica = ax.table(cellText=podaci, colLabels=stupci, loc='center', cellLoc='center')
tablica.auto_set_font_size(False)
tablica.set_fontsize(10)
tablica.auto_set_column_width(col=list(range(len(stupci))))
tablica.scale(1, 1.8)

for (row, col), cell in tablica.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold', color='white')
        cell.set_facecolor('#2C3E50')
    elif row > 0 and col == 0:
        cell.set_text_props(weight='bold')

plt.savefig('tablica_neparni.png', bbox_inches='tight', dpi=300)
print("Tablica prijelaza je uspješno spremljena!")