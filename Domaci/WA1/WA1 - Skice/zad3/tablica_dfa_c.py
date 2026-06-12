"""
zad3 / tablica_dfa_c.py

Tablica prelaza za DFA (c) kao slika -> tablica_dfa_transformacija_c.png
Najveca tablica (7 redova), pa je figsize jos malo veci.

Pokretanje:  python3 tablica_dfa_c.py   (treba matplotlib)
"""

import matplotlib.pyplot as plt


def napravi_tablicu(stupci, podaci, izlaz, figsize=(9, 4.5), fontsize=11, pad=0.04):
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
    ['q0 (Početno)', 'q0123', 'q023', 'q03'],
    ['q0123', 'q01234', 'q0234', 'q034'],
    ['q023', 'q0123', 'q0234', 'q034'],
    ['q03', 'q0123', 'q023', 'q034'],
    ['q01234 (Završno)', 'q01234', 'q0234', 'q034'],
    ['q0234 (Završno)', 'q0123', 'q0234', 'q034'],
    ['q034 (Završno)', 'q0123', 'q023', 'q034'],
]

napravi_tablicu(stupci, podaci, 'tablica_dfa_transformacija_c.png')
print("Tablica prelaza pod (c) je uspješno spremljena!")
