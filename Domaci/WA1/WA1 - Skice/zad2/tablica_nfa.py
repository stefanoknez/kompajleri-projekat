import matplotlib.pyplot as plt

# Podaci za tablicu prijelaza NFA (a prije b)
stupci = ['Trenutno stanje', 'Ulaz a', 'Ulaz b', 'Ulaz c']
podaci = [
    ['q0 (Početno)', '{q0, q1}', '{q0}', '{q0}'],
    ['q1', '{q1}', '{q2}', '{q1}'],
    ['q2 (Završno)', '{q2}', '{q2}', '{q2}']
]

# Kreiranje slike s dovoljno širine
fig, ax = plt.subplots(figsize=(8, 2.5))
ax.axis('off')

# Kreiranje tablice
tablica = ax.table(cellText=podaci, colLabels=stupci, loc='center', cellLoc='center')

# Postavljanje fonta
tablica.auto_set_font_size(False)
tablica.set_fontsize(11)

# Automatska širina stupaca prema tekstu
tablica.auto_set_column_width(col=list(range(len(stupci))))

# Vertikalno rastezanje ćelija radi preglednosti
tablica.scale(1, 1.8)

# Bojanje zaglavlja u tamno plavu
for (row, col), cell in tablica.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold', color='white')
        cell.set_facecolor('#2C3E50')
    elif row > 0 and col == 0:
        cell.set_text_props(weight='bold')

# Spremanje slike
plt.savefig('tablica_prijelaza_nfa_ab.png', bbox_inches='tight', dpi=300)
print("Tablica prijelaza za NFA je uspješno spremljena kao 'tablica_prijelaza_nfa_ab.png'")