#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generiše rješenje zadatka 3(a) — lijevo faktorisanje — kao PNG sliku.
Pokretanje:  python3 zad3a.py
Rezultat:    zadatak_3a.png
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
    ("3. (a)  Lijevo faktorisanje", False, True),
    ("", False, False),
    ("Polazna gramatika:", False, True),
    (r"$S \rightarrow I \mid I-J \mid I+K$", True, False),
    (r"$I \rightarrow (\,J-K\,) \mid (\,J\,)$", True, False),
    (r"$J \rightarrow K1 \mid K2$", True, False),
    (r"$K \rightarrow K3 \mid \varepsilon$", True, False),
    ("", False, False),
    ("Rezultat (izvučeni zajednički prefiksi):", False, True),
    (r"$S \rightarrow I\,S'$", True, False),
    (r"$S' \rightarrow -J \mid +K \mid \varepsilon$", True, False),
    (r"$I \rightarrow (\,J\,I'$", True, False),
    (r"$I' \rightarrow -K\,) \mid )$", True, False),
    (r"$J \rightarrow K\,J'$", True, False),
    (r"$J' \rightarrow 1 \mid 2$", True, False),
    (r"$K \rightarrow K3 \mid \varepsilon$", True, False),
    ("", False, False),
    ("Objašnjenje", False, True),
    (r"Faktorisanje izvlači najduži zajednički prefiks alternativa da", False, False),
    ("predictive (LL) parser ne mora da nagađa koju granu da uzme:", False, False),
    (r"•  $S$: sve tri grane počinju sa $I$ — izvučeno $I$, ostatak ide u $S'$.", False, False),
    (r"•  $I$: obje grane počinju sa $(\,J$ — izvučeno $(\,J$, ostatak u $I'$.", False, False),
    (r"•  $J$: obje počinju sa $K$ — izvučeno $K$, ostatak u $J'$.", False, False),
    (r"•  $K$: $K3$ i $\varepsilon$ nemaju zajednički prefiks, pa ostaje (lijevo", False, False),
    (r"   faktorisanje ne uklanja rekurziju — to je posao iz dijela b).", False, False),
]

fig = plt.figure(figsize=(7.8, 6.0), dpi=300)
fig.patch.set_facecolor("white")
y = 0.97
base = 0.062 * (4.0 / 6.0)
for text, is_rule, bold in LINES:
    if text == "":
        y -= base * 0.55
        continue
    x = 0.10 if is_rule else 0.04
    fig.text(x, y, text, fontsize=12.5, ha="left", va="top",
             fontweight="bold" if bold else "normal")
    y -= base

fig.savefig("zadatak_3a.png", bbox_inches="tight", pad_inches=0.18, facecolor="white")
print("Sačuvano: zadatak_3a.png")
