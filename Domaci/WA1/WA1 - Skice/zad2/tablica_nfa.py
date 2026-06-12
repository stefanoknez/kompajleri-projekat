"""
zad2 / tablica_nfa.py

Crta tablicu prelaza NFA-a "a prije b" kao sliku -> tablica_prijelaza_nfa_ab.png

Posto je NFA, celije su skupovi stanja ({q0, q1} itd.). Stil je isti kao kod
ostalih tablica: tamno-plavo zaglavlje, prva kolona bold, sirine se same namjeste.

Pokretanje:  python3 tablica_nfa.py   (treba matplotlib)
"""

import matplotlib.pyplot as plt


def napravi_tablicu(stupci, podaci, izlaz, figsize=(8, 2.5), fontsize=11):
    """Nacrta stilizovanu tabelu i snimi je kao PNG."""
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

    plt.savefig(izlaz, bbox_inches='tight', dpi=300)


# celije su skupovi stanja jer je u pitanju NFA
stupci = ['Trenutno stanje', 'Ulaz a', 'Ulaz b', 'Ulaz c']
podaci = [
    ['q0 (Početno)', '{q0, q1}', '{q0}', '{q0}'],
    ['q1', '{q1}', '{q2}', '{q1}'],
    ['q2 (Završno)', '{q2}', '{q2}', '{q2}'],
]

napravi_tablicu(stupci, podaci, 'tablica_prijelaza_nfa_ab.png')
print("Tablica prelaza za NFA je uspješno spremljena kao 'tablica_prijelaza_nfa_ab.png'")
