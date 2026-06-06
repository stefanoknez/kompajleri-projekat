#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generiše rješenje zadatka 2 (dangling-else / dvosmislenost) kao PNG sliku.
Gornji dio: zaključak + objašnjenje (Computer Modern, ijekavica).
Donji dio:  jedinstveno parse-stablo za 'if x then if x then x else x'.

Pokretanje:  python3 generisi_zad2.py
Rezultat:    zadatak_2.png

Treba ti samo matplotlib:  pip install matplotlib
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams["mathtext.fontset"] = "cm"
rcParams["font.family"] = "serif"
rcParams["axes.unicode_minus"] = False

# ---------------------------------------------------------------- tekst
LINES = [
    ("Zaključak: gramatika NIJE dvosmislena.", True),
    ("", False),
    ("Gramatika dijeli izraze u dvije klase:", False),
    (r"•  $M$ — „upareni“ izraz: svaki $\mathrm{if\,\ldots\,then}$ ima svoj $\mathrm{else}$", False),
    (r"   ($M \rightarrow \mathrm{if\ x\ then}\ M\ \mathrm{else}\ E \mid \mathrm{x}$).", False),
    (r"•  $E$ — opšti izraz, smije imati „otvoreni“ if bez else-a", False),
    (r"   ($E \rightarrow \mathrm{if\ x\ then}\ E \mid M$).", False),
    ("", False),
    (r"Ključ je u pravilu $M \rightarrow \mathrm{if\ x\ then}\ M\ \mathrm{else}\ E$: then-grana mora biti", False),
    (r"$M$ (uparena), pa unutar nje ne može stajati otvoreni if koji bi „preuzeo“", False),
    (r"else. Zato se svaki $\mathrm{else}$ jednoznačno veže za najbliži (unutrašnji) if.", False),
    ("", False),
    (r"Klasičan izraz $\mathrm{if\ x\ then\ if\ x\ then\ x\ else\ x}$ ima samo jedno stablo:", False),
    (r"else pripada unutrašnjem if-u, a spoljašnji if je otvoren ($E \rightarrow \mathrm{if\ x\ then}\ E$).", False),
]

# ---------------------------------------------------------------- stablo
# (labela, [djeca]); listovi su terminali. NT crtamo kao $...$, terminale kao mono.
T = ('E', [
        ('if', []), ('x', []), ('then', []),
        ('E', [
            ('M', [
                ('if', []), ('x', []), ('then', []),
                ('M', [('x', [])]),
                ('else', []),
                ('E', [('M', [('x', [])])]),
            ])
        ])
    ])

# raspored: listovima dodjeljujemo redom x; unutrašnji = prosjek djece; y = -dubina
pos = {}
leafx = [0]
def layout(node, depth, path):
    label, kids = node
    if not kids:
        x = leafx[0]; leafx[0] += 1
    else:
        xs = [layout(k, depth+1, path+(i,)) for i, k in enumerate(kids)]
        x = sum(xs)/len(xs)
    pos[path] = (x, -depth, label, len(kids) == 0)
    return x
layout(T, 0, ())

# crtanje stabla u zasebnoj osi
def draw(ax):
    # grane
    def walk(node, path):
        label, kids = node
        x0, y0, _, _ = pos[path]
        for i, k in enumerate(kids):
            cp = path + (i,)
            x1, y1, _, _ = pos[cp]
            ax.plot([x0, x1], [y0, y1], color="black", lw=1.0, zorder=1)
            walk(k, cp)
    walk(T, ())
    NT = {'E', 'M'}
    for (x, y, label, is_leaf) in pos.values():
        if label in NT:
            txt = f"${label}$"; fw = "normal"; col = "black"
        else:
            txt = label; fw = "normal"; col = "#1a4f8a"  # terminali plavi radi kontrasta
        ax.text(x, y, txt, ha="center", va="center", fontsize=13,
                family=("monospace" if is_leaf else "serif"),
                color=col, fontweight=fw,
                bbox=dict(boxstyle="round,pad=0.18", fc="white", ec="none"), zorder=2)
    ax.set_xlim(min(p[0] for p in pos.values())-0.6,
                max(p[0] for p in pos.values())+0.6)
    ax.set_ylim(min(p[1] for p in pos.values())-0.5, 0.6)
    ax.axis("off")

# ---------------------------------------------------------------- figura
fig = plt.figure(figsize=(8.2, 8.6), dpi=300)
fig.patch.set_facecolor("white")

# tekst (gornji dio)
y = 0.985
line_h = 0.030
for text, bold in LINES:
    if text == "":
        y -= line_h * 0.6; continue
    fig.text(0.04, y, text, fontsize=12.5, ha="left", va="top",
             fontweight=("bold" if bold else "normal"))
    y -= line_h

fig.text(0.04, y - 0.01,
         r"Jedinstveno parse-stablo za $\mathrm{if\ x\ then\ if\ x\ then\ x\ else\ x}$:",
         fontsize=12.5, ha="left", va="top", fontweight="bold")

ax = fig.add_axes([0.05, 0.04, 0.9, y - 0.10])
draw(ax)

fig.savefig("zadatak_2.png", bbox_inches="tight", pad_inches=0.18, facecolor="white")
print("Sačuvano: zadatak_2.png")
