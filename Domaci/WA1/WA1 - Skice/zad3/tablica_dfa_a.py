"""
zad3 / tablica_dfa_a.py

Tablica prelaza za DFA (a) kao slika -> tablica_dfa_transformacija.png

pad_inches=0.04 -> slika se sasvim tijesno obrezuje oko tablice (oko 1mm bjeline),
da ne ostane gomila praznog prostora kad se ubaci u dokument.

Pokretanje:  python3 tablica_dfa_a.py   (treba matplotlib)
"""

import matplotlib.pyplot as plt


def napravi_tablicu(stupci, podaci, izlaz, figsize=(8, 2.5), fontsize=11, pad=0.04):
    """Nacrta stilizovanu tabelu i snimi je kao PNG sa minimalnim rubom."""
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis('off')

    tablica = ax.table(cellText=podaci, colLabels=stupci, loc='center', cellLoc='center')
    tablica.auto_set_font_size(False)
    tablica.set_fontsize(fontsize)
    tablica.auto_set_column_width(col=list(range(len(stupci))))
    tablica.scale(1, 1.8)

    for (red, kol), celija in tablica.get_celld().items():
        if red == 0:
            celija.set_text_props(weight='bold', color='white')
            celija.set_facecolor('#2C3E50')
        elif red > 0 and kol == 0:
            celija.set_text_props(weight='bold')

    plt.savefig(izlaz, bbox_inches='tight', pad_inches=pad, dpi=300)


stupci = ['Trenutno stanje', 'Ulaz a', 'Ulaz b', 'Ulaz c']
podaci = [
    ['q0 (Početno)', 'qØ', 'q1', 'q01'],
    ['q1 (Završno)', 'q0', 'qØ', 'q1'],
    ['q01 (Završno)', 'q0', 'q1', 'q01'],
    ['qØ (Mrtvo stanje)', 'qØ', 'qØ', 'qØ'],
]

napravi_tablicu(stupci, podaci, 'tablica_dfa_transformacija.png')
print("Tablica prelaza je uspješno spremljena s minimalnim bjelinama!")
