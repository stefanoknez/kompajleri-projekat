#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generiše rješenje zadatka 3(b) — eliminacija lijeve rekurzije — kao PNG sliku.
Pokretanje:  python3 zad3b.py
Rezultat:    zadatak_3b.png
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
    ("3. (b)  Eliminacija lijeve rekurzije", False, True),
    ("", False, False),
    ("Polazna gramatika:", False, True),
    (r"$S \rightarrow STS \mid ST \mid T$", True, False),
    (r"$T \rightarrow Ta \mid Tb \mid U$", True, False),
    (r"$U \rightarrow T \mid c$", True, False),
    ("", False, False),
    ("Rezultat (bez lijeve rekurzije):", False, True),
    (r"$S \rightarrow T\,S'$", True, False),
    (r"$S' \rightarrow T\,S\,S' \mid T\,S' \mid \varepsilon$", True, False),
    (r"$T \rightarrow c\,T'$", True, False),
    (r"$T' \rightarrow a\,T' \mid b\,T' \mid \varepsilon$", True, False),
    ("", False, False),
    ("Objašnjenje", False, True),
    (r"1) Ciklus $T \rightarrow U \rightarrow T$: zamijenimo $U$ u pravilu $T \rightarrow U$ sa", False, False),
    (r"   $U \rightarrow T \mid c$, dobijemo $T \rightarrow Ta \mid Tb \mid T \mid c$, pa uklonimo", False, False),
    (r"   trivijalno $T \rightarrow T$ $\Rightarrow$ $T \rightarrow Ta \mid Tb \mid c$. ($U$ postaje nedostižan.)", False, False),
    (r"2) Direktna LR u $T$ ($T \rightarrow Ta \mid Tb \mid c$): $T \rightarrow c\,T'$,", False, False),
    (r"   $T' \rightarrow a\,T' \mid b\,T' \mid \varepsilon$.", False, False),
    (r"3) Direktna LR u $S$ ($S \rightarrow STS \mid ST \mid T$): $S \rightarrow T\,S'$,", False, False),
    (r"   $S' \rightarrow T\,S\,S' \mid T\,S' \mid \varepsilon$.", False, False),
]

fig = plt.figure(figsize=(7.8, 5.6), dpi=300)
fig.patch.set_facecolor("white")
y = 0.97
base = 0.062 * (4.0 / 5.6)
for text, is_rule, bold in LINES:
    if text == "":
        y -= base * 0.55
        continue
    x = 0.10 if is_rule else 0.04
    fig.text(x, y, text, fontsize=12.5, ha="left", va="top",
             fontweight="bold" if bold else "normal")
    y -= base

fig.savefig("zadatak_3b.png", bbox_inches="tight", pad_inches=0.18, facecolor="white")
print("Sačuvano: zadatak_3b.png")
