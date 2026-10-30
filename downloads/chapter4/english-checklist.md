# 第4章：英文校正の確認項目と学術英語表現

2026年10月30日改訂の原稿に対応。
意味と構造、文法、学術的表現、読者の視点の4段階で確認します。
文法の校正と、主張の強さや論理の流れを直す推敲は、分けてAIに依頼してください。

## 文法の基本確認項目

| 項目 | 基本 | 確認例 |
|---|---|---|
| 時制 | 手法の性質は現在、実施した実験は過去 | reduces / evaluated |
| 冠詞 | 単数可算名詞では、初出はa、既出や限定された対象はthe | a method / the method |
| 動詞 | 目的語や前置詞を含めて用法を確認 | submit the paper / search for |

### 時制

`The proposed method reduces computation time.` は、手法の性質を現在形で述べています。
`We evaluated the method on three datasets.` は、実施した実験を過去形で述べています。
日本語の「〜している」を機械的に進行形へ訳すと、一般的な性質が一時的な状態に変わることがあります。

### 冠詞

`We propose a method for failure prediction. The method uses sensor data.` では、最初に方法を紹介する箇所は `a method`、その方法を指す次の文は `the method` としています。
ただし、冠詞は文脈や名詞の可算性によって変わります。
初出なら常にa、と機械的に決めず、読者がどの対象を指すと理解するかを確認してください。

### 動詞と前置詞

論文を投稿するなら `submit the paper`、論文を探すなら `search for papers` のように、目的語や前置詞まで確認します。
使い方に自信がない表現は、辞書や同分野の論文と照合してください。

## 主張の強さを根拠に合わせる

| 表現 | 確認すること |
|---|---|
| will | 将来の予測や比較的強い見通しを、結果が支えているか |
| may | 起きるとは限らない可能性として述べる根拠があるか |
| can | 能力や機能としてできることを確かめたか |
| prove | 結論を厳密に裏づける証拠があるか |
| show / indicate / suggest | 結果が支える主張の強さに合っているか |

たとえば、実験結果が精度の改善を示唆している場合は、次のように書けます。

> The results suggest that the proposed method improves accuracy.

適用範囲を限定するときは、`under the tested operating conditions` のように、確かめた条件を明記します。
`may` や `suggest` と弱めても、調べていない効果の根拠にはなりません。
AIの修正案が新しい成果、数値、因果関係を付け足していないか、元の研究内容と照合してください。
