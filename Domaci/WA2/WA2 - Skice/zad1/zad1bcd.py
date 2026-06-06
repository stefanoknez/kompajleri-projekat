#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Generiše rješenja zadataka 1(b), 1(c) i 1(d) kao PNG slike
(Computer Modern matematika, isti font kao u postavci).

Pokretanje:  python3 generisi_slike_bcd.py
Rezultat:    zadatak_1b.png, zadatak_1c.png, zadatak_1d.png

Treba ti samo matplotlib:  pip install matplotlib
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams

rcParams["mathtext.fontset"] = "cm"      # Computer Modern za formule
rcParams["font.family"] = "serif"         # serif za prozni tekst
rcParams["axes.unicode_minus"] = False


def render(lines, out, fig_h=4.0):
    """lines: lista (tekst, uvuceno?, podebljano?)."""
    fig = plt.figure(figsize=(7.6, fig_h), dpi=300)
    fig.patch.set_facecolor("white")
    y = 0.97
    line_h = 0.066 * (4.0 / fig_h)
    for text, is_rule, bold in lines:
        if text == "":
            y -= line_h * 0.5
            continue
        x = 0.10 if is_rule else 0.04
        w = "bold" if bold else "normal"
        fig.text(x, y, text, fontsize=13, ha="left", va="top", fontweight=w)
        y -= line_h
    fig.savefig(out, bbox_inches="tight", pad_inches=0.18, facecolor="white")
    print("Sačuvano:", out)


# =========================== (b) =========================================
# Jezik: stringovi nad {0,1} sa tačno jednom nulom više nego jedinica (#0 = #1 + 1).
lines_b = [
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

# =========================== (c) =========================================
# Jezik: { 0^i 1^j 0^k : j = i + k }.
lines_c = [
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

# =========================== (d) =========================================
# Skup = { nula ili više zarezom razdvojenih nizova }.
# Niz  = [ nula ili više zarezom razdvojenih skupova ].
# Jezik = svi stringovi koji su SKUPOVI.
lines_d = [
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

render(lines_b, "zadatak_1b.png", fig_h=3.4)
render(lines_c, "zadatak_1c.png", fig_h=4.0)
render(lines_d, "zadatak_1d.png", fig_h=4.6)
