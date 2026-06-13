#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generiše rješenje zadatka 1(b) kao PNG sliku.
Jezik: stringovi nad {0,1} sa tačno jednom nulom više nego jedinica (#0 = #1 + 1).
Pokretanje:  python3 zad1b.py
Rezultat:    zadatak_1b.png
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
    ("Gramatika  (startni simbol $S$):", False, True),
    (r"$S \rightarrow A\,0\,A$", True, False),
    (r"$A \rightarrow 0\,A\,1\,A \mid 1\,A\,0\,A \mid \varepsilon$", True, False),
    ("", False, False),
    ("Objašnjenje", False, True),
    (r"Treba nam $\#0 = \#1 + 1$, tj. tačno jedna nula viška.", False, False),
    ("Uloge neterminala:", False, False),
    ("", False, False),
    (r"•  $A$ — uravnoteženi string ($\#0 = \#1$). Pravila $0A1A$ i", False, False),
    (r"   $1A0A$ uparuju svaku nulu sa po jednom jedinicom; $\varepsilon$ je prazan.", False, False),
    (r"•  $S$ — ubacuje jednu višak-nulu između dva uravnotežena", False, False),
    (r"   dijela ($A\,0\,A$), pa ukupno ostaje tačno jedna nula viška.", False, False),
]

fig = plt.figure(figsize=(7.6, 3.4), dpi=300)
fig.patch.set_facecolor("white")
y = 0.97
line_h = 0.066 * (4.0 / 3.4)
for text, is_rule, bold in LINES:
    if text == "":
        y -= line_h * 0.5
        continue
    x = 0.10 if is_rule else 0.04
    fig.text(x, y, text, fontsize=13, ha="left", va="top",
             fontweight="bold" if bold else "normal")
    y -= line_h

fig.savefig("zadatak_1b.png", bbox_inches="tight", pad_inches=0.18, facecolor="white")
print("Sačuvano: zadatak_1b.png")
