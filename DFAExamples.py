import automata


def observe(
    delta: dict[tuple[str, str], str],
    F: set[str],
    q_0: str,
    sample_input: str | None = None,
    latex: bool = False,
):
    dfa = automata.DFA(q_0, delta, F)
    if sample_input is None:
        show_sequence = False
    if show_sequence:
        r, m, seq = dfa.read(sample_input, latex)
        for i in range(len(seq)):
            print(seq[i])
    else:
        inputList = dfa.generateInput(10)
        for s in inputList:
            r, m, seq = dfa.read(s)
            if r:
                print(s)


# DFA Example 1
def example1(latex: bool = False):
    delta: dict[tuple[str, str], str] = {
        ("q_0", "a"): "q_2",
        ("q_0", "b"): "q_1",
        ("q_1", "a"): "q_0",
        ("q_1", "b"): "q_0",
        ("q_2", "a"): "q_0",
        ("q_2", "b"): "q_0",
    }
    F = {"q_2"}
    q_0 = "q_0"
    sample_input = None
    observe(delta, F, q_0, sample_input, latex=latex)


# DFA Example 2
def example2(latex: bool = False):
    delta: dict[tuple[str, str], str] = {
        ("q_0", "a"): "q_2",
        ("q_0", "b"): "q_1",
        ("q_1", "a"): "q_0",
        ("q_1", "b"): "q_0",
        ("q_2", "a"): "q_0",
        ("q_2", "b"): "q_0",
    }
    F = {"q_2"}
    q_0 = "q_0"
    sample_input = "ababbaa"
    observe(delta, F, q_0, sample_input, latex=latex)


# DFA Example 3
def example3(latex: bool = False):
    delta: dict[tuple[str, str], str] = {
        ("q_0", "a"): "q_2",
        ("q_0", "b"): "q_1",
        ("q_1", "a"): "q_3",
        ("q_1", "b"): "q_0",
        ("q_2", "a"): "q_0",
        ("q_2", "b"): "q_3",
        ("q_3", "a"): "q_1",
        ("q_3", "b"): "q_2",
    }
    F = {"q_3"}
    q_0 = "q_0"
    sample_input = "abaaa"
    observe(delta, F, q_0, sample_input, latex=latex)


# DFA Example 4
def example4(latex: bool = False):
    delta: dict[tuple[str, str], str] = {
        ("q_0", "0"): "q_2",
        ("q_0", "1"): "q_1",
        ("q_1", "1"): "q_3",
        ("q_2", "1"): "q_4",
        ("q_3", "0"): "q_2",
        ("q_3", "1"): "q_0",
        ("q_4", "0"): "q_4",
        ("q_4", "1"): "q_4",
    }
    F = {"q_4"}
    q_0 = "q_0"
    sample_input = "1101010"
    observe(delta, F, q_0, sample_input, latex=latex)


if __name__ == "__main__":
    example1(latex=True)
    # example2(latex = True)
    # example3(latex = True)
    # example4(latex = True)
