import matplotlib.pyplot as plt

stupci = ['Trenutno stanje', 'Ulaz a', 'Ulaz b', 'Ulaz c']
podaci = [
    ['q0 (Početno)', 'qØ', 'q01', 'q0'],
    ['q01', 'qØ', 'q01', 'q012'],
    ['q012 (Završno)', 'q02', 'q01', 'q012'],
    ['q02 (Završno)', 'q02', 'q01', 'q0'],
    ['qØ (Mrtvo stanje)', 'qØ', 'qØ', 'qØ']
]

# Dimenzije prilagođene za 5 redova podataka
fig, ax = plt.subplots(figsize=(8, 3))
ax.axis('off')

tablica = ax.table(cellText=podaci, colLabels=stupci, loc='center', cellLoc='center')
tablica.auto_set_font_size(False)
tablica.set_fontsize(11)
tablica.auto_set_column_width(col=list(range(len(stupci))))
tablica.scale(1, 1.8)

for (row, col), cell in tablica.get_celld().items():
    if row == 0:
        cell.set_text_props(weight='bold', color='white')
        cell.set_facecolor('#2C3E50')
    elif row > 0 and col == 0:
        cell.set_text_props(weight='bold')

# pad_inches=0.04 ostavlja točno ~1mm bjeline oko tablice
plt.savefig('tablica_dfa_transformacija_b.png', bbox_inches='tight', pad_inches=0.04, dpi=300)
print("Tablica prijelaza pod (b) je uspješno spremljena s minimalnim rubovima!")