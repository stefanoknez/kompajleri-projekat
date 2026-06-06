#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generiše rješenje zadatka 1(a) kao PNG sliku (Computer Modern matematika).
Pokretanje:  python3 generisi_sliku.py
Rezultat:    zadatak_1a.png

Treba ti samo matplotlib:  pip install matplotlib
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams["mathtext.fontset"] = "cm"      # Computer Modern za formule
rcParams["font.family"] = "serif"         # serif za prozni tekst
rcParams["axes.unicode_minus"] = False

# (tekst, uvučeno?, podebljano?)
# Matematika ide u $...$; naša slova (č, š, ž) idu kao obična Unicode slova.
LINES = [
    ("Gramatika  (startni simbol $S$):", False, True),
    (r"$S \rightarrow 2\,D \mid -2\,U$", True, False),
    (r"$T \rightarrow +2\,T \mid T+2 \mid +2\,T-2\,T \mid -2\,T+2\,T \mid \varepsilon$", True, False),
    (r"$D \rightarrow T \mid T-2\,T$", True, False),
    (r"$U \rightarrow T+2\,T$", True, False),
    ("", False, False),
    ("Objašnjenje", False, True),
    ("Izraz mora biti sintaksno valjan i imati vrijednost $\\geq 0$.", False, False),
    ("Pošto svaki član daje $+2$ ili $-2$, $\\geq 0$ znači da plusa", False, False),
    ("mora biti najmanje koliko i minusa. Uloge neterminala:", False, False),
    ("", False, False),
    ("•  $T$ — niz $+2$/$-2$ sa $\\#(+2)\\geq\\#(-2)$.", False, False),
    ("•  $D$ — ostatak iza $+2$; trpi jedan minus viška.", False, False),
    ("•  $U$ — ostatak iza $-2$; traži bar jedan plus viška.", False, False),
    ("•  $S$ — bira prvi član ($2D$ ili $-2U$); zato vrijednost $\\geq 0$.", False, False),
]

fig = plt.figure(figsize=(7.2, 4.0), dpi=300)
fig.patch.set_facecolor("white")

y = 0.97
line_h = 0.067
for text, is_rule, bold in LINES:
    if text == "":
        y -= line_h * 0.5
        continue
    x = 0.10 if is_rule else 0.04
    weight = "bold" if bold else "normal"
    fig.text(x, y, text, fontsize=13, ha="left", va="top", fontweight=weight)
    y -= line_h

fig.savefig("zadatak_1a.png", bbox_inches="tight", pad_inches=0.18,
            facecolor="white")
print("Sačuvano: zadatak_1a.png")
