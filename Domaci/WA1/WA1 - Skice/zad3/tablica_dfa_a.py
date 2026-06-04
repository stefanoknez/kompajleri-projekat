import matplotlib.pyplot as plt

stupci = ['Trenutno stanje', 'Ulaz a', 'Ulaz b', 'Ulaz c']
podaci = [
    ['q0 (Početno)', 'qØ', 'q1', 'q01'],
    ['q1 (Završno)', 'q0', 'qØ', 'q1'],
    ['q01 (Završno)', 'q0', 'q1', 'q01'],
    ['qØ (Mrtvo stanje)', 'qØ', 'qØ', 'qØ']
]

fig, ax = plt.subplots(figsize=(8, 2.5))
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

# POPRAVAK: pad_inches=0.04 reže sve do linije tablice i ostavlja točno ~1mm bjelina
plt.savefig('tablica_dfa_transformacija.png', bbox_inches='tight', pad_inches=0.04, dpi=300)
print("Tablica prijelaza je uspješno spremljena s minimalnim bjelinama!")