import re

class DFA:
    """
    決定性有限オートマトン
    """

    def __init__(self, q_0:str, delta:dict[tuple[str,str],str], F:set[str]) -> None:
        self._q_0: str = q_0 
        self._delta: dict[tuple[str, str], str] = delta
        self._F: set[str] = F
        #状態の集合とアルファベットを作成
        states:list[str] = list()
        alphabet:list[str] = list()
        for f in self._delta:
            (q,a) = f
            if q not in states:
                states.append(q)
            if (a not in alphabet) and (len(a) > 0):
                alphabet.append(a)
        states.sort()
        alphabet.sort()
        self._states:list[str] = states
        self._alphabet:list[str] = alphabet

    def read(self, input:str, latex=False) -> tuple[bool,str,list[str]]:
        """
        入力に対応する動作

        Parameter
        ---
        input 入力文字列

        latex LaTeX出力のオン・オフ

        Returns
        ---
        (result, message, sequence)

        result 受理の有無

        message メッセージ

        sequence 動作の経過
        """
        q: str = self._q_0
        sequence = list()#状態遷移を記録するリスト
        return self._readSub(q, input, sequence, latex)

    def _readSub(self, q:str, input:str, sequence:list[str], latex:bool) -> tuple[bool,str,list[str]]:
        """
        再帰的に入力に対して動作する
        """
        if len(input) == 0:#入力が空になった
            ss: str = DFA._mkStr(q, sequence, input, latex)
            sequence.append(ss)
            message = 'accept'
            result = True
            if q not in self._F:
                message: str = f'stop at {q}'
                result = False
            return result, message, sequence

        s: str = input[0]#入力の先頭の記号
        deltaArg:tuple[str,str] = (q,s)#遷移関数の引数: 状態とアルファベット
        ss = DFA._mkStr(q, sequence, input, latex)
        sequence.append(ss)
        if deltaArg not in self._delta:
            message = f'delta({deltaArg}) is not defined'
            result = False
            return result, message, sequence
        nextState: str = self._delta[deltaArg]#次の状態
        return self._readSub(nextState, input[1:], sequence, latex)
    
    def generateInput(self, length: int) -> list[str]:
        """
        指定した長さ以下の可能な文字列を列挙する
        """
        tmpList=list(self._alphabet)
        returnList = list(self._alphabet)
        for length in range(2, length + 1):
            tmp_list2 = list()
            for s in tmpList:
                for a in self._alphabet:
                    tmp_list2.append(s + a)
            for s in tmp_list2:
                returnList.append(s)
            tmpList=list(tmp_list2)
        return returnList   

    def listOfAcceptedInput(self, length:int) -> list[str]:
        """
        受理文字列を生成
        """
        inputList: list[str] = self.generateInput(length)
        output = list()
        for s in inputList:
            r, _, _ = self.read(s)
            if r:
                output.append(s)
        return output

    def compareWith(self, target:'DFA', length:int)-> tuple[bool,str]:
        """
        targetとなるDFAと同じ文字列を受理するか

        Parameters
        ---
        target 他のDFA

        length 確認する文字列長の上限

        Returns
        ---
        (b, message)

        b 同じならばTrue

        message 失敗した際に、差を表示
        """
        a1 = set(self.listOfAcceptedInput(length))
        a2 = set(target.listOfAcceptedInput(length))
        if a1 == a2:
            return True, 'The same accepted strings'
        d1:set[str] = a1 - a2
        d2:set[str] = a2 - a1
        d3:set[str] = a1.intersection(a2)
        message: str = f'{d1} are only in self\n, {d2} are only in target\n'
        message += f'their intersection is {d3}'
        return False,message

    def checkRegex(self, pattern:str, length:int)-> tuple[bool,list[str]]:
        """
        受理文字列と正規表現を比較

        Parameters
        ---
        pattern 正規表現

        length 確認する文字列長の上限

        Returns
        ---
        (b, message)

        b 同じならばTrue

        message 失敗した際に、一致しない文字列のリスト
        """
        inputList: list[str] = self.listOfAcceptedInput(length)
        p: re.Pattern[str] = re.compile(pattern)
        success = True
        unmatchedStr:list[str] = list()

        for s in inputList:
            m: re.Match[str] | None = p.fullmatch(s)
            if m:
                if s != m.group(0):
                    unmatchedStr.append(s)
                    success = False
        return success,unmatchedStr

    def latexExp(self) -> str:
        text:str = ''
        #States
        text += 'Q &= \\set{' + DFA._list2str(self._states) + '}\\\\\n'
        #Accept states
        text += 'F &= \\set{' + DFA._list2str(list(self._F)) + '}\\\\\n'
        #alphabet
        text += '\\Sigma &= \\set{'+DFA._alphabetList(self._alphabet)+ '}\\\\\n'
        #
        text += '\\begin{tabular}{|c||'
        for k in range(len(self._alphabet)):
            text += 'c|'
        text += '}\\\\\n'
        text += '\t\\hline\n'
        text += '\t\\delta&'
        for s in self._alphabet:
            text += f'\\text{{{s}}}&'
        text = text.removesuffix('&')
        text += '\\\\\\hline\n'
        for p in self._states:
            text += f'\t{p}&'
            for a in self._alphabet:
                q = self._delta[(p,a)]
                text += f'{q}&'
            text = text.removesuffix('&')
            text += '\\\\\n'
        text += '\t\\hline\n'
        text += '\\end{tabular}\n'
        return text

    @staticmethod
    def _mkStr(q:str, sequence:list[str], inputStr:str, latex:bool) -> str:
        ss:str = ''
        if len(sequence) > 0:
            if latex:
                ss = '\\vdash'
            else:
                ss = '|-'
        if latex:
            if len(inputStr) > 0:
                ss += f'\\left({q},\\text{{{inputStr}}}\\right)'
            else:
                ss += f'\\left({q},\\epsilon\\right)'
        else:
            ss += f'({q},{inputStr})'

        return ss
    
    @staticmethod
    def _list2str(inputList:list[str])->str:
        text:str = ''
        for s in inputList:
            text += f'{s},'
        return text.removesuffix(',')

    @staticmethod
    def _alphabetList(inputList:list[str])->str:
        text:str = ''
        for s in inputList:
            text += f'\\text{{{s}}},'
        return text.removesuffix(',')

    def __str__(self) -> str:
        output:str = ''
        output += f'States : {self._states}\n'
        output += f'Initial State : {self._q_0}\n'
        output += f'Accept States : {self._F}\n'
        output += f'Delta : {self._delta}\n'
        output += f'Alphabets : {self._alphabet}'
        return output

    @property
    def states(self) -> list[str]:
        return self._states

    @property
    def alphabet(self) -> list[str]:
        return self._alphabet

    @property
    def F(self) -> set[str]:
        return self._F

    @property
    def delta(self) -> dict[tuple[str,str],str]:
        return self._delta
        
    @property
    def q_0(self) -> str:
        return self._q_0

class NFA(DFA):
    """
    非決定性有限オートマトン
    """
    def __init__(self, q_0:str, delta:dict[tuple[str,str],set[str]], F:set[str]):
        self._q_0: str = q_0 
        self._delta: dict[tuple[str, str], set[str]] = delta
        self._F: set[str] = F
        #状態の集合とアルファベットを作成
        states:list[str] = list()
        alphabet:list[str] = list()
        for f in self._delta:
            (q,a) = f
            if q not in states:
                states.append(q)
            if (a not in alphabet) and (len(a) > 0):
                alphabet.append(a)
        states.sort()
        alphabet.sort()
        self._states:list[str] = states
        self._alphabet:list[str] = alphabet

    def read(self,input:str, latex=False) -> list[tuple[bool,str,list[str]]]:
        """
        入力に対応する動作

        Parameter
        ---
        input 入力文字列

        latex LaTeX出力のオン・オフ

        Returns
        ---
        List of (result, message, sequence)

        result 受理の有無

        message メッセージ

        sequence 動作の経過
        """
        sequence = list()
        sequenceList = list()
        q: str = self._q_0
        self._readSub(q,input,sequence,sequenceList,latex)
        return sequenceList

    def _readSub(self, q:str, input:str, sequence:list[str], sequenceList:list[tuple[bool,str,list[str]]], latex:bool) -> None:
        if len(input) == 0:
            ss = DFA._mkStr(q,sequence,input,latex)
            sequence.append(ss)
            message = 'accept'
            result = True
            if q not in self._F:
                message = f'stop at {q}'
                result = False
            sequenceList.append((result,message,sequence))
            return
        s :str= input[0]
        deltaArg:tuple[str,str] = (q,s)
        ss:str = DFA._mkStr(q,sequence,input,latex)
        sequence.append(ss)
        if deltaArg not in self._delta:
            message: str = f'delta({deltaArg}) in not defined'
            result = False
            sequenceList.append((result,message,sequence))
            return
        newInput:str = input[1:]
        for nextState in self._delta[deltaArg]:
            newSequence = list(sequence)
            self._readSub(nextState,newInput,newSequence,sequenceList,latex)
    
    def listOfAcceptedInput(self,length:int) -> list[str]:
        """
        受理文字列を生成
        """
        inputList: list[str] = self.generateInput(length)
        output = list()
        for s in inputList:
            seqList:list[tuple[bool,str,list[str]]] = self.read(s)
            for r,_,_ in seqList:
                if r:
                    output.append(s)
        return output

class NFA2DFA:
    """
    非決定性有限オートマトンから決定性有限オートマトンへ変換
    """
    def __init__(self,nfa:NFA) -> None:
        self._nfa: NFA = nfa
        self._new_q0:str = ''

    def exec(self) -> DFA:
        states,delta0 = self._createStates()
        F = self._createF(states)
        delta:dict[tuple[str,str],str] = dict(delta0)
        for f in delta0.keys():
            (q,a) = f
            if len(a) == 0:
                delta.pop((q,a))
        return DFA(self._new_q0,delta,F)

    def _createF(self,states)->set[str]:
        F:set[str] = set()
        for s in states:
            r = False
            for q in s:
                if q in self._nfa.F:
                    r = True
                    break
            if r:
                F.add(str(s))
        return F

    def _createStates(self)-> tuple[list[list[str]], dict[tuple[str,str],str] ]:
        delta:dict[tuple[str,str],str] = dict()
        iState: list[str] = self._createEClosure([self._nfa._q_0])
        self._new_q0 = str(iState)
        states:list[list[str]]  = list()
        states.append(iState)
        numState = len(states)
        running = True
        while running:
            statesTmp = list(states)
            for fromState in statesTmp:
                for a in self._nfa._alphabet:
                    nextState = self._createEClosure(self._createNextState(fromState,a))
                    if len(nextState) >= 1:
                        if nextState not in states:
                            states.append(nextState)
                        f:tuple[str,str] = (str(fromState),a)
                        delta[f]=str(nextState)
            if len(states) > numState:
                numState: int = len(states)
            else:
                running = False
        return states,delta
            

    def _createNextState(self, states:list[str], a:str)->list[str]:
        nextState=list()
        for q in states:
            f:tuple[str,str] = (q,a)
            if f in self._nfa._delta:
                ps: set[str] = self._nfa._delta[f]
                for p in ps:
                    if p not in nextState:
                        nextState.append(p)
        nextState.sort()
        return nextState

    def _createEClosure(self, states:list[str]) -> list[str]:
        closure = list(states)
        for q in states:
            self._createEClosureSub(q,closure)
        closure.sort()
        return closure

    def _createEClosureSub(self, q, closure) -> None:
        f:tuple[str,str] = (q, '')
        if f in self._nfa._delta:
            nextStates: set[str] = self._nfa._delta[f]
            for p in nextStates:
                if p not in closure:
                    closure.append(p)
                    self._createEClosureSub(p,closure)
