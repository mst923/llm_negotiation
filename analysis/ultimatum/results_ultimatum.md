# Ultimatum Game — 実験結果

## ゲーム概要

- **役割**: Proposer（提案者）
- **ルール**: 100ドルの分配を提案。Responderがrejectすれば両者0ドル
- **指標**: 提案額（offer, 0–100）
- **モデル**: gpt-5-mini
- **データ**: 各ペルソナ500回 × 9ペルソナ = 4,500試行

## プロンプト

Proposerとして100ドルの分配を提案。Responderがacceptすれば提案通り、rejectすれば両者0ドル。

---

## 1. ペルソナ別 提案額

### 標準4ペルソナ

| Persona | Mean Offer | Std | n |
|:--|:--:|:--:|:--:|
| benevolent | $50.18 | 3.55 | 500 |
| normal | $36.02 | 7.67 | 500 |
| strategic | $30.12 | 3.86 | 500 |
| greedy | $13.08 | 7.23 | 500 |

### Big Five ペルソナ

| Persona | Mean Offer | Std | n |
|:--|:--:|:--:|:--:|
| agreeableness | $49.78 | 1.81 | 500 |
| neuroticism | $46.18 | 5.01 | 500 |
| openness | $40.81 | 7.00 | 500 |
| extraversion | $40.06 | 7.13 | 500 |
| conscientiousness | $37.80 | 7.73 | 500 |

### 特徴

- **benevolent / agreeableness** はほぼ50:50（公平分配）
- **strategic** は拒否されないギリギリのライン（30ドル前後）を狙う
- **greedy** でも13ドル程度は提供（rejectリスクを考慮）
- Big Fiveでは **agreeableness** が最も寛容、**conscientiousness** が最も低い

## 2. Gender別 提案額

| Gender | Mean Offer | Std | n |
|:--|:--:|:--:|:--:|
| LGBTQ | $40.92 | 12.43 | 493 |
| Female | $39.34 | 11.93 | 2,030 |
| Male | $36.41 | 12.56 | 1,977 |

- LGBTQ > Female > Male の順で提案額が高い
- Dictatorゲームほどの差はない（rejectリスクが均等化効果を持つ）

## 3. 生成されたグラフ

`analysis/figures/ultimatum/` (標準ペルソナ):
- `offer_distribution_by_persona.png` — ヒストグラム
- `offer_boxplot_by_persona.png` — 箱ひげ図
- `offer_violin_by_persona.png` — バイオリンプロット
- `offer_by_region.png` — 地域別平均提案額
- `offer_by_gender.png` — 性別別箱ひげ図
- `offer_violin_by_gender.png` — 性別別バイオリンプロット
- `offer_by_age.png` — 年齢 vs 提案額散布図
- `offer_by_occupation.png` — 職業別平均提案額（上位15）

`analysis/figures/ultimatum_big5/` (Big Fiveペルソナ): 同構成8枚

## 4. 分析スクリプト

| スクリプト | 内容 |
|:--|:--|
| `run_analysis.py` | 標準4ペルソナの基本分析 |
| `run_big5_ultimatum_analysis.py` | Big Five 5ペルソナの分析 |
| `run_comparison_analysis.py` | 3ゲーム横断比較（標準ペルソナ） |
| `run_big5_comparison_analysis.py` | 3ゲーム横断比較（Big Five） |
