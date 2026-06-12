"""
zad1 / automati.py

Crta dva automata za jezik (0|1)*110 i snimi ih kao PNG:
  - NFA  ->  nfa_izlaz.png
  - DFA  ->  dfa_izlaz.png

Ideja: umjesto da rucno zovem node()/edge() za svaki automat posebno,
stanja i prelaze drzim u listama, pa ih jedna pomocna funkcija samo prosrljka.
Tako je lakse i dodati/izmijeniti neki prelaz.

Pokretanje:  python3 automati.py   (treba ti instaliran graphviz)
"""

from graphviz import Digraph


def napravi_automat(naziv, komentar, stanja, prelazi, izlaz):
    """Sklepa jedan usmjereni graf (automat) i snimi ga kao PNG.

    stanja  -> lista cvorova: (id, natpis) ili (id, natpis, oblik)
    prelazi -> lista grana:   (iz, u) ili (iz, u, natpis_na_grani)
    izlaz   -> ime fajla bez ekstenzije
    """
    g = Digraph(naziv, comment=komentar, format='png')
    g.attr(rankdir='LR')  # crta s lijeva na desno, preglednije za citanje

    # ubaci sva stanja (ako je dat oblik, koristi ga; inace default)
    for cvor in stanja:
        if len(cvor) == 3:
            cid, natpis, oblik = cvor
            g.node(cid, natpis, shape=oblik)
        else:
            cid, natpis = cvor
            g.node(cid, natpis)

    # ubaci sve prelaze (grana moze, ali ne mora, imati natpis)
    for prelaz in prelazi:
        if len(prelaz) == 3:
            iz, u, natpis = prelaz
            g.edge(iz, u, label=natpis)
        else:
            iz, u = prelaz
            g.edge(iz, u)

    g.render(izlaz, cleanup=True)
    print(f"Automat snimljen kao '{izlaz}.png'")


# --- 1) NFA za (0|1)*110 ------------------------------------------------
# q3 je dvostruki krug jer je to jedino zavrsno stanje.
nfa_stanja = [
    ('q0', 'q0 (Početno)'),
    ('q1', 'q1'),
    ('q2', 'q2'),
    ('q3', 'q3', 'doublecircle'),
]
nfa_prelazi = [
    ('q0', 'q0', '0,1'),   # petlja: cita bilo sta dok ne krene "110"
    ('q0', 'q1', '1'),
    ('q1', 'q2', '1'),
    ('q2', 'q3', '0'),     # zatvaramo "110" -> zavrsno
]
napravi_automat('NFA', 'NFA za (0|1)*110', nfa_stanja, nfa_prelazi, 'nfa_izlaz')

# --- 2) DFA za (0|1)*110 ------------------------------------------------
# D je zavrsno (dvostruki krug). Prelazi su prepisani iz tablice prelaza.
dfa_stanja = [
    ('A', 'A (Početno)'),
    ('B', 'B'),
    ('C', 'C'),
    ('D', 'D', 'doublecircle'),
]
dfa_prelazi = [
    ('A', 'A', '0'),
    ('A', 'B', '1'),
    ('B', 'A', '0'),
    ('B', 'C', '1'),
    ('C', 'D', '0'),
    ('C', 'C', '1'),
    ('D', 'A', '0'),
    ('D', 'B', '1'),
]
napravi_automat('DFA', 'DFA za (0|1)*110', dfa_stanja, dfa_prelazi, 'dfa_izlaz')
