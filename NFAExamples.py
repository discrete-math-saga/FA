import automata

def observe(
    delta: dict[tuple[str, str], str],
    F: set[str],
    q_0: str,
    sample_input: str | None = None,
    latex: bool = False,
    max_length: int= 6
):
    nfa = automata.NFA(delta, F, q_0)
    if sample_input is not None:
        show_sequence=False
    if show_sequence:
        output = nfa.read(sample_input, latex)
        for x, y, z in output:
            print(x,y,z)
    else:
        output_list:list[str] = list()
        inputList = nfa.generateInput(max_length)
        for s in inputList:
            output = nfa.read(s)
            for x,y,z in output:
                if x:
                    if s not in output_list:
                        output_list.append(s)
        for s in output_list:
            print(s)

# NFA Example 1
def example1(latex:bool):
    delta:dict[tuple[str,str],set[str]] = {
    ('q_0','0'):{'q_0'},('q_0','1'):{'q_0','q_1'},
    ('q_1','1'):{'q_2'},('q_2','0'):{'q_2'}
    }
    F = {'q_2'}
    q_0 = 'q_0'
    sample_input = '1010110'
    observe(delta,F,q_0,sample_input=sample_input,latex=latex)

# NFA Example 2
def example2(latex:bool):
    delta:dict[tuple[str,str],set[str]]  = {
    ('q_0','0'):{'q_1','q_2'},('q_0','1'):{'q_0'},
    ('q_1','1'):{'q_1','q_3'},
    ('q_2','0'):{'q_3'},('q_2','1'):{'q_2'},
    }
    F = {'q_3'}
    q_0 = 'q_0'
    sample_input = None
    observe(delta,F,q_0,sample_input=sample_input,latex=latex)

# NFA Example 3
def example3(label:bool):
    delta:dict[tuple[str,str],set[str]]  = {
    ('q_0','a'):{'q_1','q_2'},('q_0','b'):{'q_3'},
    ('q_1','a'):{'q_3'},
    ('q_2','b'):{'q_4'},
    ('q_3','b'):{'q_2','q_3'},
    ('q_4','a'):{'q_4'},('q_4','b'):{'q_4'}
    }
    F = {'q_4'}
    q_0 = 'q_0'
    sample_input = None
    observe(delta,F,q_0,sample_input=sample_input,latex=latex)

if __name__=='__main__':
    example1(latex=False)
    # example2(latex=False)
    # example3(latex=False)
