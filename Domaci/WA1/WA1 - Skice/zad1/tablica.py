import matplotlib.pyplot as plt

# Podaci za tablicu prijelaza
stupci = ['Trenutno stanje', 'Ulaz 0', 'Ulaz 1', 'Ostatak / Značenje']
podaci = [
    ['S0 (Početno/Završno)', 'S0', 'S1', 'Ostatak 0 (Djeljivo s 3)'],
    ['S1', 'S2', 'S0', 'Ostatak 1'],
    ['S2', 'S1', 'S2', 'Ostatak 2']
]

# Povećana širina slike (figsize) sa 7 na 10 da sve stane komotno
fig, ax = plt.subplots(figsize=(10, 2.5))
ax.axis('off')

# Kreiranje tablice
tablica = ax.table(cellText=podaci, colLabels=stupci, loc='center', cellLoc='center')

# Isključujemo automatsku veličinu fonta i fiksiramo je
tablica.auto_set_font_size(False)
tablica.set_fontsize(11)

# KLJUČNI POPRAVAK: Automatski prilagodi širinu stupaca na temelju teksta
tablica.auto_set_column_width(col=list(range(len(stupci))))

# Malo povećavamo vertikalni razmak u ćelijama radi preglednosti
tablica.scale(1, 1.8)

# Bojanje zaglavlja
for (row, col), cell in tablica.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold', color='white')
        cell.set_facecolor('#2C3E50') # Tamno plava/siva za zaglavlje
    elif row > 0 and col == 0:
        cell.set_text_props(weight='bold')

# Spremanje tablice kao slike
plt.savefig('tablica_prijelaza_dfa.png', bbox_inches='tight', dpi=300)
print("Ispravljena tablica je uspješno spremljena!")