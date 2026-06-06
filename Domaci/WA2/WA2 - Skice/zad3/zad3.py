#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generiše rješenja zadatka 3 (a: lijevo faktorisanje, b: eliminacija lijeve
rekurzije) kao dvije PNG slike. Computer Modern matematika, ijekavica.

Pokretanje:  python3 generisi_zad3.py
Rezultat:    zadatak_3a.png, zadatak_3b.png

Treba ti samo matplotlib:  pip install matplotlib
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams["mathtext.fontset"] = "cm"
rcParams["font.family"] = "serif"
rcParams["axes.unicode_minus"] = False


def render(lines, out, fig_h):
    fig = plt.figure(figsize=(7.8, fig_h), dpi=300)
    fig.patch.set_facecolor("white")
    y = 0.97
    base = 0.062 * (4.0 / fig_h)
    for text, is_rule, bold in lines:
        if text == "":
            y -= base * 0.55
            continue
        x = 0.10 if is_rule else 0.04
        fig.text(x, y, text, fontsize=12.5, ha="left", va="top",
                 fontweight=("bold" if bold else "normal"))
        y -= base
    fig.savefig(out, bbox_inches="tight", pad_inches=0.18, facecolor="white")
    print("Sačuvano:", out)


# ===================== (a) LIJEVO FAKTORISANJE =====================
lines_a = [
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

# ===================== (b) ELIMINACIJA LIJEVE REKURZIJE =====================
lines_b = [
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

render(lines_a, "zadatak_3a.png", fig_h=6.0)
render(lines_b, "zadatak_3b.png", fig_h=5.6)
