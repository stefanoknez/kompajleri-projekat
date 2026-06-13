#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generiše rješenje zadatka 5(b) — popravka gramatike eliminacijom
lijeve rekurzije radi uklanjanja reduce/reduce konflikta — kao PNG sliku.
Pokretanje:  python3 zad5b.py
Rezultat:    zadatak_5b.png
Treba ti:    pip install matplotlib
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams["mathtext.fontset"] = "cm"
rcParams["font.family"] = "serif"
rcParams["axes.unicode_minus"] = False

LINES = [
    ("5. (b)  Popravka gramatike", 0, True),
    ("", 0, False),
    ("Modifikacija: zamijeni lijevu rekurziju desnom u produkcijama 4 i 6:", 0, True),
    (r"Produkcija 4 (stara):   $A \rightarrow Ac$", 1, False),
    (r"Produkcija 4 (nova):    $A \rightarrow cA$", 1, False),
    ("", 0, False),
    (r"Produkcija 6 (stara):   $B \rightarrow Bc$", 1, False),
    (r"Produkcija 6 (nova):    $B \rightarrow cB$", 1, False),
    ("", 0, False),
    ("Popravljena gramatika (isti jezik):", 0, True),
    (r"$S \rightarrow Aa \mid Bb$", 1, False),
    (r"$A \rightarrow cA \mid \varepsilon$", 1, False),
    (r"$B \rightarrow cB \mid \varepsilon$", 1, False),
    ("", 0, False),
    ("Novi FOLLOW skupovi:", 0, True),
    (r"$\mathrm{FOLLOW}(A) = \{\, a \,\}$   (samo iz $S \rightarrow Aa$)", 1, False),
    (r"$\mathrm{FOLLOW}(B) = \{\, b \,\}$   (samo iz $S \rightarrow Bb$)", 1, False),
    ("", 0, False),
    (r"Skupovi su sada disjunktni — nema reduce/reduce konflikta. Gramatika je SLR(1). $\checkmark$", 0, False),
    ("", 0, False),
    ("Intuicija:", 0, True),
    (r"Uz lijevu rekurziju $A \rightarrow Ac$, terminal $c$ se konzumira NAKON što je $A$", 0, False),
    (r"već na steku. U početnom stanju parser vidi $c$ u lookahead-u i ne zna", 0, False),
    (r"da li gradi $A$ (koje će završiti sa $a$) ili $B$ (koje završava sa $b$).", 0, False),
    ("", 0, False),
    (r"Uz desnu rekurziju $A \rightarrow cA$, svaki $c$ se odmah POMJERA (shift) na stek", 0, False),
    (r"— nema potrebe za odlukom pri viđanju $c$. Razlika između $A$ i $B$", 0, False),
    (r"rješava se tek na kraju, kad parser vidi $a$ (jedino u $\mathrm{FOLLOW}(A)$) ili", 0, False),
    (r"$b$ (jedino u $\mathrm{FOLLOW}(B)$) — a tada je odluka jednoznačna.", 0, False),
]

fig_h = 6.8
fig = plt.figure(figsize=(8.0, fig_h), dpi=300)
fig.patch.set_facecolor("white")
y = 0.97; lh = 0.060 * (4.0 / fig_h)

for text, ind, bold in LINES:
    if text == "":
        y -= lh * 0.5; continue
    x = 0.12 if ind == 2 else (0.07 if ind == 1 else 0.04)
    fig.text(x, y, text, fontsize=12.5, ha="left", va="top",
             fontweight="bold" if bold else "normal")
    y -= lh

fig.savefig("zadatak_5b.png", bbox_inches="tight", pad_inches=0.18, facecolor="white")
print("Sačuvano: zadatak_5b.png")
