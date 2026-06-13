#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generiše rješenja zadataka 4(a), 4(b) i 4(c) kao jednu PNG sliku:
  (a) FIRST skupovi,  (b) FOLLOW skupovi,  (c) LL(1) tabela parsiranja.
Pokretanje:  python3 zad4abc.py
Rezultat:    zadatak_4abc.png
Treba ti:    pip install matplotlib
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams["mathtext.fontset"] = "cm"
rcParams["font.family"] = "serif"
rcParams["axes.unicode_minus"] = False

# ---------- gramatika i proračun FIRST/FOLLOW ----------
prods = {
    'S': [['#', 'U', 'T'], ['T', '?']],
    'T': [['a', 'S'], ['b', 'U', 'c'], []],
    'U': [['a', 'S', 'c'], ['b', 'T', 'd']],
}
NT = set(prods)
terms = {'a', 'b', 'c', 'd', '#', '?'}
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

cols = ['a', 'b', 'c', 'd', '#', '?', '$']
tab = {A: {t: '' for t in cols} for A in NT}

def ps(A, p): return f"{A}→{''.join(p) if p else 'ε'}"

for A in NT:
    for p in prods[A]:
        fr = first_seq(p, FIRST) if p else {EPS}
        for t in fr - {EPS}: tab[A][t] = ps(A, p)
        if EPS in fr:
            for t in FOLLOW[A]: tab[A][t] = ps(A, p)

def fmt(S): return "{ " + ", ".join(sorted(S)) + " }"

# ---------- slika: FIRST (a), FOLLOW (b), LL(1) tabela (c) ----------
fig = plt.figure(figsize=(8.4, 6.4), dpi=300)
fig.patch.set_facecolor("white")
y = 0.97; lh = 0.045

def line(t, b=False, x=0.04):
    global y
    fig.text(x, y, t, fontsize=12.5, ha="left", va="top",
             fontweight="bold" if b else "normal")
    y -= lh

line("4. (a) FIRST skupovi", True)
for A in ['S', 'T', 'U']: line(f"FIRST({A}) = {fmt(FIRST[A])}", x=0.07)
y -= lh * 0.3
line("(b) FOLLOW skupovi", True)
for A in ['S', 'T', 'U']: line(f"FOLLOW({A}) = {fmt(FOLLOW[A])}", x=0.07)
y -= lh * 0.3
line("(c) LL(1) tabela parsiranja", True)

ax = fig.add_axes([0.05, 0.04, 0.9, y - 0.06])
ax.axis("off")
header = [''] + cols
data = [[A] + [tab[A][t] if tab[A][t] else '—' for t in cols] for A in ['S', 'T', 'U']]
tbl = ax.table(cellText=data, colLabels=header, cellLoc='center', loc='upper center')
tbl.auto_set_font_size(False)
tbl.set_fontsize(11)
tbl.scale(1, 1.6)
for (r, c), cell in tbl.get_celld().items():
    cell.set_edgecolor("#999")
    if r == 0 or c == 0: cell.set_text_props(fontweight="bold")

fig.savefig("zadatak_4abc.png", bbox_inches="tight", pad_inches=0.18, facecolor="white")
print("Sačuvano: zadatak_4abc.png")
