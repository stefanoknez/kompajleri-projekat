#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generiše rješenje zadatka 4(d) — LL(1) parsiranje stringa '#a?ca?' — kao PNG sliku.
Prikazuje korak-po-korak tabelu: stek, ulaz, akcija.
Pokretanje:  python3 zad4d.py
Rezultat:    zadatak_4d.png
Treba ti:    pip install matplotlib
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams["mathtext.fontset"] = "cm"
rcParams["font.family"] = "serif"
rcParams["axes.unicode_minus"] = False

# --- isti proračun gramatike (potreban za parse()) ---
prods = {
    'S': [['#', 'U', 'T'], ['T', '?']],
    'T': [['a', 'S'], ['b', 'U', 'c'], []],
    'U': [['a', 'S', 'c'], ['b', 'T', 'd']],
}
NT = set(prods)
EPS = 'ε'

nullable = {A: False for A in NT}
ch = True
while ch:
    ch = False
    for A in NT:
        if not nullable[A] and any(all(s in NT and nullable[s] for s in p) for p in prods[A]):
            nullable[A] = True; ch = True

def first_seq(seq, F):
    out = set()
    for s in seq:
        if s in NT:
            out |= F[s] - {EPS}
            if EPS not in F[s]: return out
        else:
            out.add(s); return out
    out.add(EPS); return out

FIRST = {A: set() for A in NT}
ch = True
while ch:
    ch = False
    for A in NT:
        for p in prods[A]:
            add = first_seq(p, FIRST) if p else {EPS}
            if not add <= FIRST[A]: FIRST[A] |= add; ch = True

FOLLOW = {A: set() for A in NT}
FOLLOW['S'].add('$')
ch = True
while ch:
    ch = False
    for A in NT:
        for p in prods[A]:
            for i, s in enumerate(p):
                if s in NT:
                    fr = first_seq(p[i+1:], FIRST) if p[i+1:] else {EPS}
                    add = fr - {EPS}
                    if EPS in fr: add |= FOLLOW[A]
                    if not add <= FOLLOW[s]: FOLLOW[s] |= add; ch = True

def ps(A, p): return f"{A}→{''.join(p) if p else 'ε'}"

def parse(inp):
    st = ['S']; inp = list(inp) + ['$']; ip = 0; rows = []
    while st:
        top = st[0]; cur = inp[ip]
        if top in {'a', 'b', 'c', 'd', '#', '?'} or top == '$':
            rows.append((''.join(st), ''.join(inp[ip:]), f"match {top}"))
            st.pop(0); ip += 1
        else:
            p = [pp for pp in prods[top]
                 if (lambda fr: cur in fr - {EPS} or (EPS in fr and cur in FOLLOW[top]))(
                     first_seq(pp, FIRST) if pp else {EPS})][0]
            rows.append((''.join(st), ''.join(inp[ip:]), ps(top, p)))
            st.pop(0)
            for s in reversed(p): st.insert(0, s)
    rows.append(('', ''.join(inp[ip:]), 'accept'))
    return rows

# ---------- slika ----------
rows = parse('#a?ca?')
fig = plt.figure(figsize=(6.6, 6.2), dpi=300)
fig.patch.set_facecolor("white")
fig.text(0.04, 0.975, "(d) LL(1) parsiranje stringa  #a?ca?",
         fontsize=13, ha="left", va="top", fontweight="bold")
fig.text(0.04, 0.93, "(vrh steka = lijevo)", fontsize=11, ha="left", va="top")

ax = fig.add_axes([0.05, 0.03, 0.9, 0.86])
ax.axis("off")
tbl = ax.table(
    cellText=[[s, i, a] for s, i, a in rows],
    colLabels=["Stek", "Ulaz", "Akcija"],
    cellLoc='left', loc='center',
    colWidths=[0.30, 0.30, 0.40],
)
tbl.auto_set_font_size(False)
tbl.set_fontsize(11.5)
tbl.scale(1, 1.5)
for (r, c), cell in tbl.get_celld().items():
    cell.set_edgecolor("#999")
    if r == 0: cell.set_text_props(fontweight="bold")

fig.savefig("zadatak_4d.png", bbox_inches="tight", pad_inches=0.18, facecolor="white")
print("Sačuvano: zadatak_4d.png")
