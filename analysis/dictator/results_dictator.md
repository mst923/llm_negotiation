# Dictator Game — 実験結果

## ゲーム概要

- **役割**: Proposer（独裁者）
- **ルール**: 100ドルの分配を決定。Responderに拒否権なし（提案通りに分配）
- **指標**: 提案額（offer, 0–100）
- **モデル**: gpt-5-mini
- **データ**: 各ペルソナ500回 × 9ペルソナ = 4,500試行

## プロンプト

Proposerとして100ドルの分配を決定。Responderがacceptしてもrejectしても、提案者は提案額通りの金額を得る。Responderには実質的な拒否権がない。

---

## 1. ペルソナ別 提案額

### 標準4ペルソナ

| Persona | Mean Offer | Std | n |
|:--|:--:|:--:|:--:|
| benevolent | $46.79 | 8.65 | 500 |
| normal | $17.66 | 14.85 | 500 |
| strategic | $5.27 | 10.08 | 500 |
| greedy | **$0.00** | 0.00 | 500 |

### Big Five ペルソナ

| Persona | Mean Offer | Std | n |
|:--|:--:|:--:|:--:|
| agreeableness | $47.48 | 6.45 | 500 |
| openness | $29.63 | 13.79 | 500 |
| neuroticism | $27.06 | 13.64 | 500 |
| conscientiousness | $26.62 | 15.68 | 500 |
| extraversion | $25.62 | 13.35 | 500 |

### 特徴

- **greedy** は全員$0（完全な自己利益最大化）
- **strategic** も平均$5.27と非常に低い（拒否権がないため、戦略的に最小限のみ提供）
- **benevolent / agreeableness** は拒否権がなくても公平に近い分配を維持
- Ultimatumと比較して、拒否権の有無が特にstrategic/normalの行動に大きく影響

## 2. Gender別 提案額

| Gender | Mean Offer | Std | n |
|:--|:--:|:--:|:--:|
| LGBTQ | $30.33 | 18.66 | 458 |
| Female | $27.65 | 19.07 | 1,979 |
| Male | $21.55 | 18.78 | 2,063 |

- Ultimatumと同じ傾向（LGBTQ > Female > Male）だが、差がより大きい
- 拒否権がない状況でMaleの利己性がより顕著に表れる

## 3. Ultimatumとの比較

| Persona | Ultimatum | Dictator | 差 |
|:--|:--:|:--:|:--:|
| benevolent | $50.18 | $46.79 | -$3.39 |
| normal | $36.02 | $17.66 | **-$18.36** |
| strategic | $30.12 | $5.27 | **-$24.85** |
| greedy | $13.08 | $0.00 | **-$13.08** |

- 拒否権がなくなると、benevolent以外は大幅に提案額が減少
- strategic で最大の差（-$24.85）: Ultimatumでは拒否回避のため$30提案 → Dictatorでは$5に

## 4. 生成されたグラフ

`analysis/figures/dictator/` (標準ペルソナ): 8枚
`analysis/figures/dictator_big5/` (Big Five): 8枚

同構成:
- offer_distribution_by_persona.png
- offer_boxplot_by_persona.png / offer_violin_by_persona.png
- offer_by_region.png / offer_by_gender.png / offer_violin_by_gender.png
- offer_by_age.png / offer_by_occupation.png

## 5. 分析スクリプト

| スクリプト | 内容 |
|:--|:--|
| `run_dictator_analysis.py` | 標準4ペルソナの基本分析 |
| `run_big5_dictator_analysis.py` | Big Five 5ペルソナの分析 |
| `run_comparison_analysis.py` | 3ゲーム横断比較（標準ペルソナ） |
| `run_big5_comparison_analysis.py` | 3ゲーム横断比較（Big Five） |
