#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generiše rješenje zadatka 5(a) — prvo LR(0) stanje I0, FOLLOW skupovi
i reduce/reduce konflikt — kao PNG sliku.
Pokretanje:  python3 zad5a.py
Rezultat:    zadatak_5a.png
Treba ti:    pip install matplotlib
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams["mathtext.fontset"] = "cm"
rcParams["font.family"] = "serif"
rcParams["axes.unicode_minus"] = False

fig = plt.figure(figsize=(8.2, 7.6), dpi=300)
fig.patch.set_facecolor("white")
y = 0.97; lh = 0.038

def txt(t, x=0.04, bold=False, sz=12.5):
    global y
    fig.text(x, y, t, fontsize=sz, ha="left", va="top",
             fontweight="bold" if bold else "normal")
    y -= lh

txt("5. (a)  Prvo LR(0) stanje, FOLLOW skupovi i konflikti", bold=True, sz=13)
y -= lh * 0.3
txt("Polazna gramatika:", bold=True)
for s in [r"$S' \rightarrow S$",
          r"$S \rightarrow Aa \mid Bb$",
          r"$A \rightarrow Ac \mid \varepsilon$",
          r"$B \rightarrow Bc \mid \varepsilon$"]:
    txt(s, x=0.09)

y -= lh * 0.4
txt("Prvo stanje LR(0) automata — zatvaranje skupa $\\{S' \\rightarrow {\\bullet}S\\}$:", bold=True)

box_y = y + 0.01
items = [r"$S' \rightarrow {\bullet}\,S$",
         r"$S  \rightarrow {\bullet}\,A\,a$",
         r"$S  \rightarrow {\bullet}\,B\,b$",
         r"$A  \rightarrow {\bullet}\,A\,c$",
         r"$A  \rightarrow \varepsilon\,{\bullet}$",
         r"$B  \rightarrow {\bullet}\,B\,c$",
         r"$B  \rightarrow \varepsilon\,{\bullet}$"]
item_h = 0.036
box_h = len(items) * item_h + 0.02
ax = fig.add_axes([0.08, box_y - box_h, 0.55, box_h])
ax.set_xlim(0, 1); ax.set_ylim(0, 1); ax.axis("off")
rect = plt.Rectangle((0, 0), 1, 1, fill=False, edgecolor="#444", lw=1.2)
ax.add_patch(rect)
ax.text(0.5, 0.97, r"$I_0$", ha="center", va="top", fontsize=13,
        fontweight="bold", transform=ax.transAxes)
for i, item in enumerate(items):
    yp = 0.88 - i * 0.115
    ax.text(0.06, yp, item, ha="left", va="top", fontsize=12,
            transform=ax.transAxes)
y = box_y - box_h - 0.01

y -= lh * 0.4
txt(r"Napomena: $A \rightarrow \varepsilon{\bullet}$ i $B \rightarrow \varepsilon{\bullet}$ su završene stavke (reduce akcije).", sz=11.5)
y -= lh * 0.5
txt("FOLLOW skupovi (za SLR analizu):", bold=True)
txt(r"$\mathrm{FOLLOW}(A) = \{\, a,\ c \,\}$  (iz $S \rightarrow Aa$ i $A \rightarrow Ac$)", x=0.07)
txt(r"$\mathrm{FOLLOW}(B) = \{\, b,\ c \,\}$  (iz $S \rightarrow Bb$ i $B \rightarrow Bc$)", x=0.07)
y -= lh * 0.4
txt("Konflikt koji sprečava SLR(1):", bold=True)
txt(r"U stanju $I_0$ postoje dvije završene stavke: $A \rightarrow \varepsilon{\bullet}$ i $B \rightarrow \varepsilon{\bullet}$.")
txt(r"Terminal $c$ je u oba FOLLOW skupa: $c \in \mathrm{FOLLOW}(A)$ i $c \in \mathrm{FOLLOW}(B)$.")
txt(r"Rezultat: reduce/reduce konflikt na terminalu $c$ — parser ne zna da li da")
txt(r"redukuje $A \rightarrow \varepsilon$ ili $B \rightarrow \varepsilon$, pa gramatika nije SLR(1).", x=0.07)

fig.savefig("zadatak_5a.png", bbox_inches="tight", pad_inches=0.18, facecolor="white")
print("Sačuvano: zadatak_5a.png")
