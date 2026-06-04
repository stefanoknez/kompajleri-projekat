from graphviz import Digraph

# DFA / NFA za binarni broj djeljiv s 3
dfa = Digraph('DFA_DjeljiviS3', format='png')
dfa.attr(rankdir='LR')

dfa.node('start', 'Početno', shape='point')
dfa.node('S0', 'S0 (Ostatak 0)', shape='doublecircle')
dfa.node('S1', 'S1 (Ostatak 1)', shape='circle')
dfa.node('S2', 'S2 (Ostatak 2)', shape='circle')

dfa.edge('start', 'S0')
dfa.edge('S0', 'S0', label='0')
dfa.edge('S0', 'S1', label='1')

dfa.edge('S1', 'S2', label='0')
dfa.edge('S1', 'S0', label='1')

dfa.edge('S2', 'S1', label='0')
dfa.edge('S2', 'S2', label='1')

dfa.render('dfa_djeljivi_s_3', cleanup=True)
print("Automat je uspješno generiran kao 'dfa_djeljivi_s_3.png'")