from graphviz import Digraph

dfa = Digraph('NFA_to_DFA_C', format='png')
dfa.attr(rankdir='LR')

dfa.node('start', 'Početno', shape='point')
dfa.node('q0', 'q0')
dfa.node('q0123', 'q0123')
dfa.node('q023', 'q023')
dfa.node('q03', 'q03')
dfa.node('q01234', 'q01234', shape='doublecircle')
dfa.node('q0234', 'q0234', shape='doublecircle')
dfa.node('q034', 'q034', shape='doublecircle')

dfa.edge('start', 'q0')

# Prijelazi iz q0
dfa.edge('q0', 'q0123', label='a')
dfa.edge('q0', 'q023', label='b')
dfa.edge('q0', 'q03', label='c')

# Prijelazi iz q0123
dfa.edge('q0123', 'q01234', label='a')
dfa.edge('q0123', 'q0234', label='b')
dfa.edge('q0123', 'q034', label='c')

# Prijelazi iz q023
dfa.edge('q023', 'q0123', label='a')
dfa.edge('q023', 'q0234', label='b')
dfa.edge('q023', 'q034', label='c')

# Prijelazi iz q03
dfa.edge('q03', 'q0123', label='a')
dfa.edge('q03', 'q023', label='b')
dfa.edge('q03', 'q034', label='c')

# Prijelazi iz q01234
dfa.edge('q01234', 'q01234', label='a')
dfa.edge('q01234', 'q0234', label='b')
dfa.edge('q01234', 'q034', label='c')

# Prijelazi iz q0234
dfa.edge('q0234', 'q0123', label='a')
dfa.edge('q0234', 'q0234', label='b')
dfa.edge('q0234', 'q034', label='c')

# Prijelazi iz q034
dfa.edge('q034', 'q0123', label='a')
dfa.edge('q034', 'q023', label='b')
dfa.edge('q034', 'q034', label='c')

dfa.render('transformirani_dfa_c', cleanup=True)
print("DFA graf pod (c) je uspješno spremljen!")