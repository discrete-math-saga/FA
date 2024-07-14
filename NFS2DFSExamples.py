import automata

def convert(delta:dict[tuple[str,str],set[str]],    F:set[str],q_0:str):
    nfa:automata.NFA = automata.NFA(q_0,delta,F)
    dfa:automata.DFA = automata.NFA2DFA(nfa).exec()
    for f in dfa.delta:
        print(str(f)+" -> "+dfa.delta[f])
    print()
    print(dfa.F)

# Example 1
def example1():
    delta:dict[tuple[str,str],set[str]]  = {('q_0','0'):{'q_0'},('q_0','1'):{'q_0','q_1'},
    ('q_1','1'):{'q_2'},('q_2','0'):{'q_2'},('q_2','1'):{'q_2'}
    }
    F = {'q_2'}    
    q_0 = 'q_0'
    convert(delta,F,q_0)

# Example 2
def example2():
    delta:dict[tuple[str,str],set[str]] = {('q_0','0'):{'q_0'},('q_0','1'):{'q_0','q_1'},
    ('q_1','0'):{'q_1','q_2'},('q_2','0'):{'q_2'},('q_2','1'):{'q_1','q_2'}
    }
    F = {'q_1'}
    q_0 = 'q_0'
    convert(delta,F,q_0)

# Example 3
def example3():
    delta:dict[tuple[str,str],set[str]] = {('q_0','0'):{'q_0'},('q_0',''):{'q_1'},
    ('q_1','0'):{'q_1'},('q_1','1'):{'q_1'},('q_1',''):{'q_2'},
    ('q_2','1'):{'q_2'}
    }
    F = {'q_2'}
    q_0 = 'q_0'
    convert(delta,F,q_0)

# Example 4
def example4():
    delta:dict[tuple[str,str],set[str]] = {
        ('q_0','0'):{'q_0'},('q_0','1'):{'q_0',},('q_0',''):{'q_1',},
        ('q_1','0'):{'q_1','q_2'},
        ('q_2','0'):{'q_2'},('q_2','1'):{'q_2'},('q_2',''):{'q_1'}
    }
    F = {'q_2'}
    q_0 = 'q_0'
    convert(delta,F,q_0)

# Example 5
def example5():
    delta:dict[tuple[str,str],set[str]] = {
        ('q_0',''):{'q_1','q_4'},('q_1','0'):{'q_2'},('q_2',''):{'q_3'},
        ('q_4','1'):{'q_5'},('q_5',''):{'q_6'},
        ('q_6',''):{'q_7','q_9'},('q_7','0'):{'q_8'},('q_8',''):{'q_11'},('q_11',''):{'q_6'},
        ('q_9','1'):{'q_10'},('q_10',''):{'q_11'}
    }
    F={'q_3','q_11'}    
    q_0 = 'q_0'
    convert(delta,F,q_0)

if __name__=="__main__":
    example1()
    # example2()
    # example3()
    # example4()
    # example5()