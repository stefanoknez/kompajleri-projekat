from graphviz import Digraph

# 1. DFA za manje od tri 0
dfa = Digraph('DFA_ManjeOdTriNule', format='png')
dfa.attr(rankdir='LR')

dfa.node('q0', 'q0 (0 nula)', shape='doublecircle')
dfa.node('q1', 'q1 (1 nula)', shape='doublecircle')
dfa.node('q2', 'q2 (2 nule)', shape='doublecircle')
dfa.node('q3', 'q3 (Mrtvo stanje)', shape='circle')

dfa.edge('q0', 'q0', label='1')
dfa.edge('q0', 'q1', label='0')
dfa.edge('q1', 'q1', label='1')
dfa.edge('q1', 'q2', label='0')
dfa.edge('q2', 'q2', label='1')
dfa.edge('q2', 'q3', label='0')
dfa.edge('q3', 'q3', label='0,1')

dfa.render('dfa_manje_od_tri_nule', cleanup=True)

# 2. NFA (Strukturni prikaz unije)
nfa = Digraph('NFA_ManjeOdTriNule', format='png')
nfa.attr(rankdir='LR')

nfa.node('start', 'Početno', shape='point')
nfa.node('s0', 's0', shape='doublecircle')
nfa.node('s1', 's1', shape='doublecircle')
nfa.node('s2', 's2', shape='circle')
nfa.node('s3', 's3', shape='doublecircle')
nfa.node('s4', 's4', shape='circle')
nfa.node('s5', 's5', shape='doublecircle')

nfa.edge('start', 's0')
nfa.edge('s0', 's0', label='1')
nfa.edge('s0', 's1', label='ε')

# Druga grana 1*01*
nfa.edge('s0', 's2', label='0')
nfa.edge('s2', 's2', label='1')
nfa.edge('s2', 's3', label='ε')
nfa.edge('s3', 's3', label='1')

# Treća grana 1*01*01*
nfa.edge('s0', 's4', label='0')
nfa.edge('s4', 's4', label='1')
nfa.edge('s4', 's5', label='0')
nfa.edge('s5', 's5', label='1')

nfa.render('nfa_manje_od_tri_nule', cleanup=True)

print("Automati su uspješno generirani!")