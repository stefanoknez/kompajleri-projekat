#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generiše rješenje zadatka 1(d) kao PNG sliku.
Jezik: stringovi koji su SKUPOVI nad azbukom {[,],{,},,}.
Skup = vitičaste zagrade oko liste nizova; niz = uglaste zagrade oko liste skupova.
Pokretanje:  python3 zad1d.py
Rezultat:    zadatak_1d.png
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
    (r"$S \rightarrow \{\,A\,\}$", True, False),
    (r"$A \rightarrow \varepsilon \mid B$", True, False),
    (r"$B \rightarrow R \mid R\,{,}\,B$", True, False),
    (r"$R \rightarrow [\,C\,]$", True, False),
    (r"$C \rightarrow \varepsilon \mid D$", True, False),
    (r"$D \rightarrow S \mid S\,{,}\,D$", True, False),
    ("", False, False),
    ("Objašnjenje", False, True),
    (r"Skup sadrži nizove, a niz sadrži skupove — međusobna rekurzija.", False, False),
    ("Uloge neterminala:", False, False),
    ("", False, False),
    (r"•  $S$ — skup: vitičaste zagrade oko liste nizova, $\{A\}$.", False, False),
    (r"•  $R$ — niz: uglaste zagrade oko liste skupova, $[\,C\,]$.", False, False),
    (r"•  $A,\,C$ — liste ($\varepsilon$ = prazno, ili neprazna lista).", False, False),
    (r"•  $B$ — neprazna lista nizova; $D$ — neprazna lista skupova", False, False),
    (r"   (elementi razdvojeni zarezom).", False, False),
]

fig = plt.figure(figsize=(7.6, 4.6), dpi=300)
fig.patch.set_facecolor("white")
y = 0.97
line_h = 0.066 * (4.0 / 4.6)
for text, is_rule, bold in LINES:
    if text == "":
        y -= line_h * 0.5
        continue
    x = 0.10 if is_rule else 0.04
    fig.text(x, y, text, fontsize=13, ha="left", va="top",
             fontweight="bold" if bold else "normal")
    y -= line_h

fig.savefig("zadatak_1d.png", bbox_inches="tight", pad_inches=0.18, facecolor="white")
print("Sačuvano: zadatak_1d.png")
