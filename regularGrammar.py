import re
# import automata
class RG:
    """
    正規文法のクラス
    """
    
    def __init__(self,alphabet:set[str],P:dict[str,list[list[str]]],S:str):
        """
        Parameters
        ---
        alphabet 終端記号の集合

        P 生成規則

        S 開始記号
        """
        self._alphabet: set[str] = alphabet
        self._P: dict[str, list[list[str]]] = P
        self._S: str = S
        self._N: set[str] = self._getN()

    def _getN(self)->set[str]:
        N = set()
        for n in self._P.keys():
            N.add(n)
            for r in self._P[n]:
                if len(r) == 1:
                    if not (r[0] in self._alphabet):
                        N.add(r[0])
                elif len(r) == 2:
                    N.add(r[1])
        return N
            
    def latexExp(self)->str:
        text:str =''
        text += 'N&=\\set{'
        for n in self._N:
            text += RG._toText(n)+','
        text = text.removesuffix(',')
        text += '}\\\\\n'
        text += '\\Sigma&=\\set{'
        for a in self._alphabet:
            text += f'\\text{{{a}}},'
        text = text.removesuffix(',')
        text += '}\\\\\n'
        text += 'P&=\\set{'
        for k in self._P.keys():
            text += RG._toText(k)+'\\rightarrow'
            for r in self._P[k]:
                if len(r) ==0:
                    text += '\\epsilon'
                else:
                    for j in range(len(r)):
                        text += RG._toText(r[j])
                text += '\\vert '
            text =text.removesuffix('\\vert ')
            text += ','
        text = text.removesuffix(',')
        text += '}\n'
        return text
    
    @staticmethod
    def _toText(s:str) -> str:
        s = f'text{{{s}}}'
        return '\\'+re.sub(r'text{(\S+)_(\S+)}',r'text{\1}_{\2}',s)

    @property
    def alphabet(self) -> set[str]:
        return self._alphabet

    @property
    def N(self) -> set[str]:
        return self._N

    @property
    def P(self) -> dict[str, list[list[str]]]:
        return self._P

    @property
    def S(self) -> str:
        return self._S
