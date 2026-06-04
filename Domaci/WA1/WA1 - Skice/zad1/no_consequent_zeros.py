from graphviz import Digraph

# 1. DFA za nizove bez uzastopnih nula
dfa = Digraph('DFA_BezUzastopnihNula', format='png')
dfa.attr(rankdir='LR')

dfa.node('A', 'A (Zadnja 1 ili prazno)', shape='doublecircle')
dfa.node('B', 'B (Zadnja 0)', shape='doublecircle')
dfa.node('C', 'C (Mrtvo stanje - 00)', shape='circle')

dfa.edge('A', 'A', label='1')
dfa.edge('A', 'B', label='0')
dfa.edge('B', 'A', label='1')
dfa.edge('B', 'C', label='0')
dfa.edge('C', 'C', label='0,1')

dfa.render('dfa_bez_uzastopnih_nula', cleanup=True)

# 2. NFA za (1|01)*(0|ε)
nfa = Digraph('NFA_BezUzastopnihNula', format='png')
nfa.attr(rankdir='LR')

nfa.node('start', 'Početno', shape='point')
nfa.node('s0', 's0', shape='doublecircle')
nfa.node('s1', 's1', shape='circle')
nfa.node('s2', 's2', shape='doublecircle')

nfa.edge('start', 's0')
nfa.edge('s0', 's0', label='1')
nfa.edge('s0', 's1', label='0')
nfa.edge('s1', 's0', label='1')
nfa.edge('s0', 's2', label='0')

nfa.render('nfa_bez_uzastopnih_nula', cleanup=True)

print("Novi automati su uspješno generirani!")