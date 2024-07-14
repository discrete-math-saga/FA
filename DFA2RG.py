from automata import DFA, NFA
from regularGrammar import RG

def dfa2rg(dfa:DFA) -> RG:
    """
    Construct a regular grammar accepted by the given DFA
    """
    P:dict[str,list[list[str]]] = dict()
    alphabet:set[str] = set()
    for k in dfa.delta.keys():
        (q, a) = k
        qq: str = dfa.delta[k]
        alphabet.add(a)
        if not (q in P.keys()):
            P[q] = list()
        P[q].append([a,qq])
        if qq in dfa.F:
            P[q].append([a])
    if (dfa.q_0 in dfa.F):
        if not (dfa.q_0 in P.keys()):
            P[dfa.q_0] = list()
        P[dfa.q_0].append([])
    print(type(alphabet))
    rg = RG(alphabet,P,dfa.q_0)
    return rg

def rg2nfa(rg:RG) -> NFA:
    """
    Construct an NFA that accepts the same language as the given regular grammar
    """
    Q:set[str] = set(rg.N)
    Q.add('q_f')
    F = {'q_f'}
    delta = dict()
    for k in rg.P.keys():
        rList: list[list[str]] = rg.P[k]
        for s in rList:
            if len(s) == 1:
                if not ((k,s[0]) in delta.keys()):
                    delta[(k,s[0])]=set()
                delta[(k,s[0])].add('q_f')
            elif len(s) == 2:
                if not ((k,s[0]) in delta.keys()):
                    delta[(k,s[0])]=set()
                delta[(k,s[0])].add(s[1])
    k = rg.S
    """
    for rList in rg.P[k]:
        for s in rList:
            print(s)
            if len(s) == 0:
                if not ((k,s[0]) in delta.keys()):
                    delta[(k,s[0])]=set()
                delta[(k,s[0])].add('')
    """
    return NFA(k,delta,F)

# Example: DFA to Regular Grammar
def example_dfa2rg():
    delta:dict[tuple[str,str],str] = {
        ('q_0','a'):'q_2',('q_0','b'):'q_1',
        ('q_1','a'):'q_0',('q_1','b'):'q_0',
        ('q_2','a'):'q_0',('q_2','b'):'q_0'
        }
    F = {'q_2'}
    dfa = DFA('q_0',delta,F)
    rg = dfa2rg(dfa)
    print(rg.latexExp())

# Example: Regular Grammar to NFA
def example_rg2nfa():
    delta:dict[tuple[str,str],str] = {
        ('q_0','a'):'q_2',('q_0','b'):'q_1',
        ('q_1','a'):'q_0',('q_1','b'):'q_0',
        ('q_2','a'):'q_0',('q_2','b'):'q_0'
        }
    F = {'q_2'}
    dfa = DFA('q_0',delta,F)
    rg = dfa2rg(dfa)
    print(rg.latexExp())
    nfa = rg2nfa(rg)
    print(nfa.latexExp())

if __name__ == '__main__':
    example_dfa2rg()
    example_rg2nfa()