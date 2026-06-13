#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Zadatak 4: računa FIRST/FOLLOW, LL(1) tabelu i parsiranje '#a?ca?',
pa crta dvije PNG slike. Computer Modern, ijekavica.

Pokretanje:  python3 generisi_zad4.py
Rezultat:    zadatak_4abc.png, zadatak_4d.png
Treba ti:    pip install matplotlib
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import rcParams
rcParams["mathtext.fontset"]="cm"; rcParams["font.family"]="serif"
rcParams["axes.unicode_minus"]=False

# ---------- gramatika i proracun ----------
prods={'S':[['#','U','T'],['T','?']],
       'T':[['a','S'],['b','U','c'],[]],
       'U':[['a','S','c'],['b','T','d']]}
NT=set(prods); terms={'a','b','c','d','#','?'}; EPS='ε'
nullable={A:False for A in NT}; ch=True
while ch:
    ch=False
    for A in NT:
        if not nullable[A] and any(all(s in NT and nullable[s] for s in p) for p in prods[A]):
            nullable[A]=True; ch=True
def first_seq(seq,F):
    out=set()
    for s in seq:
        if s in NT:
            out|=F[s]-{EPS}
            if EPS not in F[s]: return out
        else:
            out.add(s); return out
    out.add(EPS); return out
FIRST={A:set() for A in NT}; ch=True
while ch:
    ch=False
    for A in NT:
        for p in prods[A]:
            add=first_seq(p,FIRST) if p else {EPS}
            if not add<=FIRST[A]: FIRST[A]|=add; ch=True
FOLLOW={A:set() for A in NT}; FOLLOW['S'].add('$'); ch=True
while ch:
    ch=False
    for A in NT:
        for p in prods[A]:
            for i,s in enumerate(p):
                if s in NT:
                    fr=first_seq(p[i+1:],FIRST) if p[i+1:] else {EPS}
                    add=fr-{EPS}
                    if EPS in fr: add|=FOLLOW[A]
                    if not add<=FOLLOW[s]: FOLLOW[s]|=add; ch=True
cols=['a','b','c','d','#','?','$']
tab={A:{t:'' for t in cols} for A in NT}
def ps(A,p): return f"{A}→{''.join(p) if p else 'ε'}"
for A in NT:
    for p in prods[A]:
        fr=first_seq(p,FIRST) if p else {EPS}
        for t in fr-{EPS}: tab[A][t]=ps(A,p)
        if EPS in fr:
            for t in FOLLOW[A]: tab[A][t]=ps(A,p)
def parse(inp):
    st=['S']; inp=list(inp)+['$']; ip=0; rows=[]
    while st:
        top=st[0]; cur=inp[ip]
        if top in terms or top=='$':
            rows.append((''.join(st),''.join(inp[ip:]),f"match {top}")); st.pop(0); ip+=1
        else:
            p=[pp for pp in prods[top] if (lambda fr: cur in fr-{EPS} or (EPS in fr and cur in FOLLOW[top]))(first_seq(pp,FIRST) if pp else {EPS})][0]
            rows.append((''.join(st),''.join(inp[ip:]),ps(top,p))); st.pop(0)
            for s in reversed(p): st.insert(0,s)
    rows.append(('',''.join(inp[ip:]),'accept')); return rows
def fmt(S): return "{ "+", ".join(sorted(S))+" }"

# ---------- slika 1: FIRST, FOLLOW, LL(1) tabela ----------
fig=plt.figure(figsize=(8.4,6.4),dpi=300); fig.patch.set_facecolor("white")
y=0.97; lh=0.045
def line(t,b=False,x=0.04):
    global y
    fig.text(x,y,t,fontsize=12.5,ha="left",va="top",fontweight="bold" if b else "normal"); y-=lh
line("4. (a) FIRST skupovi",True)
for A in ['S','T','U']: line(f"FIRST({A}) = {fmt(FIRST[A])}",x=0.07)
y-=lh*0.3; line("(b) FOLLOW skupovi",True)
for A in ['S','T','U']: line(f"FOLLOW({A}) = {fmt(FOLLOW[A])}",x=0.07)
y-=lh*0.3; line("(c) LL(1) tabela parsiranja",True)
# tabela kao osa
ax=fig.add_axes([0.05,0.04,0.9,y-0.06]); ax.axis("off")
header=['']+cols
data=[[A]+[tab[A][t] if tab[A][t] else '—' for t in cols] for A in ['S','T','U']]
tbl=ax.table(cellText=data,colLabels=header,cellLoc='center',loc='upper center')
tbl.auto_set_font_size(False); tbl.set_fontsize(11); tbl.scale(1,1.6)
for (r,c),cell in tbl.get_celld().items():
    cell.set_edgecolor("#999")
    if r==0 or c==0: cell.set_text_props(fontweight="bold")
fig.savefig("zadatak_4abc.png",bbox_inches="tight",pad_inches=0.18,facecolor="white")
print("Sačuvano: zadatak_4abc.png")

# ---------- slika 2: parsiranje ----------
rows=parse('#a?ca?')
fig=plt.figure(figsize=(6.6,6.2),dpi=300); fig.patch.set_facecolor("white")
fig.text(0.04,0.975,"(d) LL(1) parsiranje stringa  #a?ca?",fontsize=13,ha="left",va="top",fontweight="bold")
fig.text(0.04,0.93,"(vrh steka = lijevo)",fontsize=11,ha="left",va="top")
ax=fig.add_axes([0.05,0.03,0.9,0.86]); ax.axis("off")
tbl=ax.table(cellText=[[s,i,a] for s,i,a in rows],
             colLabels=["Stek","Ulaz","Akcija"],cellLoc='left',loc='center',
             colWidths=[0.30,0.30,0.40])
tbl.auto_set_font_size(False); tbl.set_fontsize(11.5); tbl.scale(1,1.5)
for (r,c),cell in tbl.get_celld().items():
    cell.set_edgecolor("#999")
    if r==0: cell.set_text_props(fontweight="bold")
fig.savefig("zadatak_4d.png",bbox_inches="tight",pad_inches=0.18,facecolor="white")
print("Sačuvano: zadatak_4d.png")
