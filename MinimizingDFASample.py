from automata import DFA
class MinimizingDFA:
    """
    DFAを最小化
    """
    def __init__(self, origDFA:DFA):
        self.origDFA = origDFA
        state1:set[str] = set(origDFA.states)
        state2:set[str] = set(origDFA.F)
        for s in state2:
            state1.remove(s)
        self.states:list[set[str]]=list()#独立な状態集合のリストとなる
        #初期では、受理状態の集合と、その他の状態集合
        self.states.append(state1)
        self.states.append(state2)
        
    def exec(self) -> DFA:
        """
        最小化の実行
        """
        end = False
        while not end:
            newList = list(self.states)
            for ss in self.states:#現在の各状態集合
                for a in self.origDFA.alphabet:#アルファベット
                    result = dict()
                    destination = set()
                    for s in ss:#状態集合の各要素
                        if (s, a) in self.origDFA.delta.keys():#遷移関数がある場合
                            q: str|None = self.origDFA.delta[(s, a)]
                            destination.add(q)
                            #遷移先毎に遷移元を分類
                            if q in result.keys():
                                result[q].add(s)
                            else:
                                result[q]=set()
                                result[q].add(s)
                        
                        else:#遷移関数が無い場合
                            q = None
                            destination.add(q)
                            if q in result.keys():
                                result[q].add(s)
                            else:
                                result[q]=set()
                                result[q].add(s)
                        
                    #遷移先が、状態集合の部分集合で無い場合に分割する
                    if not(self._subSetOfMember(destination)):
                        for state in self._newStateSet(destination,result):
                            newList.append(state)
                        newList.remove(ss)
                        break

            if len(newList) > len(self.states):
                self.states:list[set[str]] = newList
            else:
                end = True
        
        return self._createNewDFA()


    def _newStateSet(self,destination,result)->list[set[str]]:
        newDest = list()
        for s in self.states:
            inter:set[str] =s & destination
            if len(inter) > 0:
                newDest.append(inter)
        if None in destination:
            newDest.append(None)
        newSetList=list()
        for nd in newDest:
            state = set()
            if nd is None:
                for p in result[None]:
                    state.add(p)
            else:
                for q in nd:
                    if q in result.keys():
                        for p in result[q]:
                            state.add(p)
            newSetList.append(state)
        return newSetList


    def _subSetOfMember(self,states) -> bool:
        """
        statesを部分集合とする状態集合が状態集合のリストに含まれるか
        """
        for s in self.states:
            if states <= s:
                return True
        return False

    def _findSuperSet(self,states) -> set[str] | None:
        """
        引数で与えられた状態集合を含む集合を返す。無い場合にはNoneを返す
        """
        if len(states) < 1:
            return None
        for ss in self.states:
            if states <= ss:
                return ss
        else:
            return None

    def _createNewDFA(self) -> DFA:
        newDelta = dict()
        for ss in self.states:
            for a in self.origDFA.alphabet:
                destination = set()
                for s in ss:
                    if (s, a) in self.origDFA.delta.keys():
                        q = self.origDFA.delta[(s,a)]
                        destination.add(q)
                d = self._findSuperSet(destination)
                if d is None:
                    if len(destination) > 0:
                        newDelta[(str(ss),a)]=str(destination)
                else:
                    newDelta[(str(ss),a)]=str(d)

        newF = set()
        newQ_0:str = ''
        for s in self.states:
            if len(s- self.origDFA.F) < 1:
                newF.add(str(s))
            if self.origDFA.q_0 in s:
                newQ_0 = str(s)
        return DFA(newQ_0,newDelta,newF)

def example1():
    delta:dict[tuple[str,str],str] = {
        ('q_0','a'):'q_1',('q_0','b'):'q_2',
        ('q_1','a'):'q_1',('q_1','b'):'q_3',
        ('q_2','a'):'q_3',('q_2','b'):'q_4',
        ('q_3','a'):'q_3',('q_3','b'):'q_4',
        ('q_4','a'):'q_2',('q_4','b'):'q_3'
        }
    F = {'q_2','q_3'}
    dfa = DFA('q_0',delta,F)
    minimize = MinimizingDFA(dfa)
    newDFA = minimize.exec()

    n = 10
    b,m=dfa.compareWith(newDFA,n)
    print(b,m)
    print(newDFA)

def example2():
    delta:dict[tuple[str,str],str] = {
        ('q_0','1'):'q_1',
        ('q_1','0'):'q_3', ('q_1','1'):'q_2',
        ('q_2','0'):'q_3', ('q_2','1'):'q_1',
        ('q_3','0'):'q_4', ('q_3','1'):'q_1',
        ('q_4','0'):'q_3', ('q_4','1'):'q_2',
    }
    F = {'q_3','q_4'}
    dfa = DFA('q_0',delta,F)
    minimize = MinimizingDFA(dfa)
    newDFA = minimize.exec()

    n = 10
    b,m=dfa.compareWith(newDFA,n)
    print(b,m)
    print(newDFA)

if __name__ == '__main__':
    example1()
    # example2()

