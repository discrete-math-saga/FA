# 有限オートマトンと正規表現

## 基本モデル
- `automata.py`
    - 決定性有限オートマトン: `DFA`
    - 非決定性有限オートマトン: `NFA`
    - 非決定性有限オートマトンから決定性有限オートマトンへ変換: `NFA2DFA`
- `regularGrammar.py`
    - 正規文法: `RG`

## 実行例
- 決定性有限オートマトン
    - `DFAExamples.py`
- 非決定性有限オートマトン
    - `NFAExamples.py`
- 非決定性FAから決定性FAへの変換
    - `NFS2DFAExamples.py`
- 決定性有限オートマトンの最小化
    - `MinimizingDFASample.py`
- 決定性有限オートマトンを正規文法へ変換
    - `DFA2RG.ipynb`
- FAが正規表現で表した文字列を受理する例
    - `RegexAndFA.ipynb`

## 正規表現
pythonの正規表現モジュール`re`を使って、正規表現を扱う。
- `regexExample.ipynb`
