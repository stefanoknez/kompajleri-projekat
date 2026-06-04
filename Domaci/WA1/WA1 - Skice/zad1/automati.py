from graphviz import Digraph

# 1. Generiranje NFA
nfa = Digraph('NFA', comment='NFA za (0|1)*110', format='png')
nfa.attr(rankdir='LR')

# Stanja
nfa.node('q0', 'q0 (Početno)')
nfa.node('q1', 'q1')
nfa.node('q2', 'q2')
nfa.node('q3', 'q3', shape='doublecircle') # Završno stanje

# Prijelazi
nfa.edge('q0', 'q0', label='0,1')
nfa.edge('q0', 'q1', label='1')
nfa.edge('q1', 'q2', label='1')
nfa.edge('q2', 'q3', label='0')

nfa.render('nfa_izlaz', cleanup=True)
print("NFA je uspješno generiran kao 'nfa_izlaz.png'")

# 2. Generiranje DFA
dfa = Digraph('DFA', comment='DFA za (0|1)*110', format='png')
dfa.attr(rankdir='LR')

# Stanja
dfa.node('A', 'A (Početno)')
dfa.node('B', 'B')
dfa.node('C', 'C')
dfa.node('D', 'D', shape='doublecircle') # Završno stanje

# Prijelazi prema tablici
dfa.edge('A', 'A', label='0')
dfa.edge('A', 'B', label='1')

dfa.edge('B', 'A', label='0')
dfa.edge('B', 'C', label='1')

dfa.edge('C', 'D', label='0')
dfa.edge('C', 'C', label='1')

dfa.edge('D', 'A', label='0')
dfa.edge('D', 'B', label='1')

dfa.render('dfa_izlaz', cleanup=True)
print("DFA je uspješno generiran kao 'dfa_izlaz.png'")