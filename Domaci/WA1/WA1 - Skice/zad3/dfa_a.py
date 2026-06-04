from graphviz import Digraph

dfa = Digraph('NFA_to_DFA', format='png')
dfa.attr(rankdir='LR')

dfa.node('start', 'Početno', shape='point')
dfa.node('q0', 'q0')
dfa.node('q1', 'q1', shape='doublecircle')
dfa.node('q01', 'q01', shape='doublecircle')
dfa.node('q_empty', 'qØ', shape='circle')

dfa.edge('start', 'q0')

# Prijelazi iz q0
dfa.edge('q0', 'q_empty', label='a')
dfa.edge('q0', 'q1', label='b')
dfa.edge('q0', 'q01', label='c')

# Prijelazi iz q1
dfa.edge('q1', 'q0', label='a')
dfa.edge('q1', 'q_empty', label='b')
dfa.edge('q1', 'q1', label='c')

# Prijelazi iz q01
dfa.edge('q01', 'q0', label='a')
dfa.edge('q01', 'q1', label='b')
dfa.edge('q01', 'q01', label='c')

# Prelazi iz mrtvog stanja
dfa.edge('q_empty', 'q_empty', label='a,b,c')

dfa.render('transformirani_dfa', cleanup=True)
print("DFA graf je uspješno spremljen!")