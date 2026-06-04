from graphviz import Digraph

nfa = Digraph('NFA_a_prije_b', format='png')
nfa.attr(rankdir='LR')

nfa.node('start', 'Početno', shape='point')
nfa.node('q0', 'q0')
nfa.node('q1', 'q1')
nfa.node('q2', 'q2', shape='doublecircle')

nfa.edge('start', 'q0')

# Prijelazi iz q0
nfa.edge('q0', 'q0', label='a,b,c')
nfa.edge('q0', 'q1', label='a')

# Prijelazi iz q1
nfa.edge('q1', 'q1', label='a,c')
nfa.edge('q1', 'q2', label='b')

# Prijelazi iz q2
nfa.edge('q2', 'q2', label='a,b,c')

nfa.render('nfa_a_prije_b', cleanup=True)
print("NFA je uspješno spremljen kao 'nfa_a_prije_b.png'")