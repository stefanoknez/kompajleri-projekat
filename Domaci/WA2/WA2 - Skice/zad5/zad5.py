#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zadatak 5: LR(0) stanje I0, FOLLOW(A), FOLLOW(B), konflikti i popravka.
Pokretanje:  python3 generisi_zad5.py
Rezultat:    zadatak_5a.png, zadatak_5b.png
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams["mathtext.fontset"]="cm"; rcParams["font.family"]="serif"
rcParams["axes.unicode_minus"]=False

def render(lines, out, fig_h):
    fig=plt.figure(figsize=(8.0,fig_h),dpi=300); fig.patch.set_facecolor("white")
    y=0.97; lh=0.060*(4.0/fig_h)
    for text,ind,bold in lines:
        if text=="": y-=lh*0.5; continue
        x=0.12 if ind==2 else (0.07 if ind==1 else 0.04)
        fig.text(x,y,text,fontsize=12.5,ha="left",va="top",
                 fontweight="bold" if bold else "normal")
        y-=lh
    fig.savefig(out,bbox_inches="tight",pad_inches=0.18,facecolor="white")
    print("Sačuvano:",out)

# box around I0 items: draw as separate axes with border
def render_5a():
    fig=plt.figure(figsize=(8.2,7.6),dpi=300); fig.patch.set_facecolor("white")
    y=0.97; lh=0.038
    def txt(t,x=0.04,bold=False,sz=12.5):
        nonlocal y
        fig.text(x,y,t,fontsize=sz,ha="left",va="top",
                 fontweight="bold" if bold else "normal"); y-=lh

    txt("5. (a)  Prvo LR(0) stanje, FOLLOW skupovi i konflikti",bold=True,sz=13)
    y-=lh*0.3
    txt("Polazna gramatika:",bold=True)
    for s in [r"$S' \rightarrow S$",
              r"$S \rightarrow Aa \mid Bb$",
              r"$A \rightarrow Ac \mid \varepsilon$",
              r"$B \rightarrow Bc \mid \varepsilon$"]:
        txt(s,x=0.09)
    y-=lh*0.4
    txt("Prvo stanje LR(0) automata — zatvaranje skupa $\{S' \\rightarrow {\\bullet}S\}$:",bold=True)

    # draw I0 box
    box_y=y+0.01
    items=[r"$S' \rightarrow {\bullet}\,S$",
           r"$S  \rightarrow {\bullet}\,A\,a$",
           r"$S  \rightarrow {\bullet}\,B\,b$",
           r"$A  \rightarrow {\bullet}\,A\,c$",
           r"$A  \rightarrow \varepsilon\,{\bullet}$",
           r"$B  \rightarrow {\bullet}\,B\,c$",
           r"$B  \rightarrow \varepsilon\,{\bullet}$"]
    item_h=0.036
    box_h=len(items)*item_h+0.02
    ax=fig.add_axes([0.08, box_y-box_h, 0.55, box_h])
    ax.set_xlim(0,1); ax.set_ylim(0,1); ax.axis("off")
    for edge in ['top','bottom','left','right']:
        ax.spines[edge] if False else None
    rect=plt.Rectangle((0,0),1,1,fill=False,edgecolor="#444",lw=1.2)
    ax.add_patch(rect)
    ax.text(0.5,0.97,r"$I_0$",ha="center",va="top",fontsize=13,fontweight="bold",
            transform=ax.transAxes)
    for i,item in enumerate(items):
        yp=0.88-i*0.115
        ax.text(0.06,yp,item,ha="left",va="top",fontsize=12,transform=ax.transAxes)
    y=box_y-box_h-0.01

    y-=lh*0.4
    txt("Napomena: $A \\rightarrow \\varepsilon{\\bullet}$ i $B \\rightarrow \\varepsilon{\\bullet}$ su završene stavke (reduce akcije).",x=0.04,sz=11.5)
    y-=lh*0.5
    txt("FOLLOW skupovi (za SLR analizu):",bold=True)
    txt(r"$\mathrm{FOLLOW}(A) = \{\, a,\ c \,\}$  (iz $S \rightarrow Aa$ i $A \rightarrow Ac$)",x=0.07)
    txt(r"$\mathrm{FOLLOW}(B) = \{\, b,\ c \,\}$  (iz $S \rightarrow Bb$ i $B \rightarrow Bc$)",x=0.07)
    y-=lh*0.4
    txt("Konflikt koji sprečava SLR(1):",bold=True)
    txt(r"U stanju $I_0$ postoje dvije završene stavke: $A \rightarrow \varepsilon{\bullet}$ i $B \rightarrow \varepsilon{\bullet}$.",x=0.04)
    txt(r"Terminal $c$ je u oba FOLLOW skupa: $c \in \mathrm{FOLLOW}(A)$ i $c \in \mathrm{FOLLOW}(B)$.",x=0.04)
    txt(r"Rezultat: reduce/reduce konflikt na terminalu $c$ — parser ne zna da li da",x=0.04)
    txt(r"redukuje $A \rightarrow \varepsilon$ ili $B \rightarrow \varepsilon$, pa gramatika nije SLR(1).",x=0.07)

    fig.savefig("zadatak_5a.png",bbox_inches="tight",pad_inches=0.18,facecolor="white")
    print("Sačuvano: zadatak_5a.png")

def render_5b():
    lines=[
        ("5. (b)  Popravka gramatike",0,True),
        ("",0,False),
        ("Modifikacija: zamijeni lijevu rekurziju desnom u produkcijama 4 i 6:",0,True),
        (r"Produkcija 4 (stara):   $A \rightarrow Ac$",1,False),
        (r"Produkcija 4 (nova):    $A \rightarrow cA$",1,False),
        ("",0,False),
        (r"Produkcija 6 (stara):   $B \rightarrow Bc$",1,False),
        (r"Produkcija 6 (nova):    $B \rightarrow cB$",1,False),
        ("",0,False),
        ("Popravljena gramatika (isti jezik):",0,True),
        (r"$S \rightarrow Aa \mid Bb$",1,False),
        (r"$A \rightarrow cA \mid \varepsilon$",1,False),
        (r"$B \rightarrow cB \mid \varepsilon$",1,False),
        ("",0,False),
        ("Novi FOLLOW skupovi:",0,True),
        (r"$\mathrm{FOLLOW}(A) = \{\, a \,\}$   (samo iz $S \rightarrow Aa$; $A \rightarrow cA$ daje $\mathrm{FOLLOW}(A)$ opet, ne širi)",1,False),
        (r"$\mathrm{FOLLOW}(B) = \{\, b \,\}$   (samo iz $S \rightarrow Bb$)",1,False),
        ("",0,False),
        (r"Skupovi su sada disjunktni — nema reduce/reduce konflikta. Gramatika je SLR(1). $\checkmark$",0,False),
        ("",0,False),
        ("Intuicija:",0,True),
        (r"Uz lijevu rekurziju $A \rightarrow Ac$, terminal $c$ se konzumira NAKON što je $A$",0,False),
        (r"već na steku. U početnom stanju parser vidi $c$ u lookahead-u i ne zna",0,False),
        (r"da li gradi $A$ (koje će završiti sa $a$) ili $B$ (koje završava sa $b$).",0,False),
        ("",0,False),
        (r"Uz desnu rekurziju $A \rightarrow cA$, svaki $c$ se odmah POMJERA (shift) na stek",0,False),
        (r"— nema potrebe za odlukom pri viđanju $c$. Razlika između $A$ i $B$",0,False),
        (r"rješava se tek na kraju, kad parser vidi $a$ (jedino u $\mathrm{FOLLOW}(A)$) ili",0,False),
        (r"$b$ (jedino u $\mathrm{FOLLOW}(B)$) — a tada je odluka jednoznačna.",0,False),
    ]
    render(lines,"zadatak_5b.png",fig_h=6.8)

render_5a()
render_5b()
