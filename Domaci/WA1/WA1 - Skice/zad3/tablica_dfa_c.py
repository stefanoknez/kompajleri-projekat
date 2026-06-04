import matplotlib.pyplot as plt

stupci = ['Trenutno stanje', 'Ulaz a', 'Ulaz b', 'Ulaz c']
podaci = [
    ['q0 (Početno)', 'q0123', 'q023', 'q03'],
    ['q0123', 'q01234', 'q0234', 'q034'],
    ['q023', 'q0123', 'q0234', 'q034'],
    ['q03', 'q0123', 'q023', 'q034'],
    ['q01234 (Završno)', 'q01234', 'q0234', 'q034'],
    ['q0234 (Završno)', 'q0123', 'q0234', 'q034'],
    ['q034 (Završno)', 'q0123', 'q023', 'q034']
]

# Dimenzije prilagođene za veći broj redova
fig, ax = plt.subplots(figsize=(9, 4.5))
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

# pad_inches=0.04 ostavlja točno 1mm bjelina oko tablice
plt.savefig('tablica_dfa_transformacija_c.png', bbox_inches='tight', pad_inches=0.04, dpi=300)
print("Tablica prijelaza pod (c) je uspješno spremljena!")