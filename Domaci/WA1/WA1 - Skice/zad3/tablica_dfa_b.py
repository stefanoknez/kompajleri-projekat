"""
zad3 / tablica_dfa_b.py

Tablica prelaza za DFA (b) kao slika -> tablica_dfa_transformacija_b.png
Ima 5 redova podataka, pa je figsize malo visi nego kod (a).

Pokretanje:  python3 tablica_dfa_b.py   (treba matplotlib)
"""

import matplotlib.pyplot as plt


def napravi_tablicu(stupci, podaci, izlaz, figsize=(8, 3), fontsize=11, pad=0.04):
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
    ['q0 (Početno)', 'qØ', 'q01', 'q0'],
    ['q01', 'qØ', 'q01', 'q012'],
    ['q012 (Završno)', 'q02', 'q01', 'q012'],
    ['q02 (Završno)', 'q02', 'q01', 'q0'],
    ['qØ (Mrtvo stanje)', 'qØ', 'qØ', 'qØ'],
]

napravi_tablicu(stupci, podaci, 'tablica_dfa_transformacija_b.png')
print("Tablica prelaza pod (b) je uspješno spremljena s minimalnim rubovima!")
