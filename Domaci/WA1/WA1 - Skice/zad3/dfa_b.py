from graphviz import Digraph

dfa = Digraph('NFA_to_DFA_B', format='png')
dfa.attr(rankdir='LR')

dfa.node('start', 'Početno', shape='point')
dfa.node('q0', 'q0')
dfa.node('q01', 'q01')
dfa.node('q012', 'q012', shape='doublecircle')
dfa.node('q02', 'q02', shape='doublecircle')
dfa.node('q_empty', 'qØ', shape='circle')

dfa.edge('start', 'q0')

# Prijelazi iz q0
dfa.edge('q0', 'q_empty', label='a')
dfa.edge('q0', 'q01', label='b')
dfa.edge('q0', 'q0', label='c')

# Prijelazi iz q01
dfa.edge('q01', 'q_empty', label='a')
dfa.edge('q01', 'q01', label='b')
dfa.edge('q01', 'q012', label='c')

# Prijelazi iz q012
dfa.edge('q012', 'q02', label='a')
dfa.edge('q012', 'q01', label='b')
dfa.edge('q012', 'q012', label='c')

# Prijelazi iz q02
dfa.edge('q02', 'q02', label='a')
dfa.edge('q02', 'q01', label='b')
dfa.edge('q02', 'q0', label='c')

# Prelazi iz mrtvoga stanja
dfa.edge('q_empty', 'q_empty', label='a,b,c')

dfa.render('transformirani_dfa_b', cleanup=True)
print("DFA graf pod (b) je uspješno spremljen!")