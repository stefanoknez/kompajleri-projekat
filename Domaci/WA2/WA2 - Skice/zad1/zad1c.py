#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generiše rješenje zadatka 1(c) kao PNG sliku.
Jezik: { 0^i 1^j 0^k | j = i + k } nad azbukom {0,1}.
Pokretanje:  python3 zad1c.py
Rezultat:    zadatak_1c.png
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
    (r"$S \rightarrow X\,Y$", True, False),
    (r"$X \rightarrow 0\,X\,1 \mid \varepsilon$", True, False),
    (r"$Y \rightarrow 1\,Y\,0 \mid \varepsilon$", True, False),
    ("", False, False),
    ("Objašnjenje", False, True),
    (r"Jezik je $\{\,0^i\,1^j\,0^k : j = i + k\,\}$ — svih $j$ jedinica je u", False, False),
    (r"sredini, a treba ih tačno $i+k$. Uloge neterminala:", False, False),
    ("", False, False),
    (r"•  $X$ — generiše $0^i\,1^i$: svaka vodeća nula dobija po jednu", False, False),
    (r"   jedinicu ($0\,X\,1$). Pokriva lijevi dio $i$ jedinica.", False, False),
    (r"•  $Y$ — generiše $1^k\,0^k$: svaka prateća nula dobija po jednu", False, False),
    (r"   jedinicu ($1\,Y\,0$). Pokriva desni dio $k$ jedinica.", False, False),
    (r"•  $S \rightarrow XY$ — spaja u $0^i\,1^{\,i}1^{\,k}\,0^k = 0^i\,1^{\,i+k}\,0^k$.", False, False),
]

fig = plt.figure(figsize=(7.6, 4.0), dpi=300)
fig.patch.set_facecolor("white")
y = 0.97
line_h = 0.066
for text, is_rule, bold in LINES:
    if text == "":
        y -= line_h * 0.5
        continue
    x = 0.10 if is_rule else 0.04
    fig.text(x, y, text, fontsize=13, ha="left", va="top",
             fontweight="bold" if bold else "normal")
    y -= line_h

fig.savefig("zadatak_1c.png", bbox_inches="tight", pad_inches=0.18, facecolor="white")
print("Sačuvano: zadatak_1c.png")
