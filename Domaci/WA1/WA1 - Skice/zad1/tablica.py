"""
zad1 / tablica.py

Crta tablicu prelaza DFA-a za "djeljivo sa 3" kao sliku -> tablica_prijelaza_dfa.png

Nista pametno, samo lijepo iscrtana matplotlib tabela: zaglavlje tamno-plavo,
prva kolona boldirana, sirine kolona se same namjeste prema tekstu.

Pokretanje:  python3 tablica.py   (treba matplotlib)
"""

import matplotlib.pyplot as plt


def napravi_tablicu(stupci, podaci, izlaz, figsize=(10, 2.5), fontsize=11, pad=None):
    """Nacrta stilizovanu tabelu i snimi je kao PNG.

    stupci  -> nazivi kolona (zaglavlje)
    podaci  -> redovi tabele (lista listi)
    izlaz   -> ime fajla slike
    """
    fig, ax = plt.subplots(figsize=figsize)
    ax.axis('off')  # bez osa, hocemo samo tabelu

    tablica = ax.table(cellText=podaci, colLabels=stupci, loc='center', cellLoc='center')

    # fiksiramo font (da ga matplotlib ne smanjuje sam)
    tablica.auto_set_font_size(False)
    tablica.set_fontsize(fontsize)
    # sirine kolona po duzini teksta + malo vertikalnog vazduha
    tablica.auto_set_column_width(col=list(range(len(stupci))))
    tablica.scale(1, 1.8)

    # bojenje: zaglavlje tamno-plavo/bijelo, prva kolona bold
    for (red, kol), celija in tablica.get_celld().items():
        if red == 0:
            celija.set_text_props(weight='bold', color='white')
            celija.set_facecolor('#2C3E50')
        elif red > 0 and kol == 0:
            celija.set_text_props(weight='bold')

    if pad is not None:
        plt.savefig(izlaz, bbox_inches='tight', pad_inches=pad, dpi=300)
    else:
        plt.savefig(izlaz, bbox_inches='tight', dpi=300)


# podaci: stanje pamti ostatak pri dijeljenju sa 3
stupci = ['Trenutno stanje', 'Ulaz 0', 'Ulaz 1', 'Ostatak / Značenje']
podaci = [
    ['S0 (Početno/Završno)', 'S0', 'S1', 'Ostatak 0 (Djeljivo s 3)'],
    ['S1', 'S2', 'S0', 'Ostatak 1'],
    ['S2', 'S1', 'S2', 'Ostatak 2'],
]

napravi_tablicu(stupci, podaci, 'tablica_prijelaza_dfa.png')
print("Tablica je uspješno spremljena!")
