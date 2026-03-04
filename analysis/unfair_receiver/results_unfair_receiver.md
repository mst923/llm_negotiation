# Unfair Receiver Game — 実験結果

## ゲーム概要

- **役割**: Responder（受け手）
- **ルール**: 100ドルの分配で10ドルを提示される（90:10の不公平提案）。Accept/Rejectを判断
- **条件**: 提案元が「人間(human)」か「コンピュータプログラム(computer)」かの2条件
- **指標**: Accept率
- **モデル**: gpt-5-mini, gpt-4o-mini-2024-07-18
- **データ**: 各ペルソナ500回 × 4ペルソナ × 2条件 × 2モデル = 8,000試行

## プロンプト

- **Human条件**: "Another player (the proposer) has proposed to divide 100 dollars. The proposer offers you 10 dollars and keeps 90 dollars for themselves."
- **Computer条件**: "A computer program has proposed to divide 100 dollars. The computer program offers you 10 dollars and keeps 90 dollars for itself."

---

## 1. Overall Accept Rate

| Model | Human | Computer | 差 | 方向 |
|:--|:--:|:--:|:--:|:--:|
| **gpt-5-mini** | 82.6% | 88.9% | +6.3pp | Computer **高い** |
| **gpt-4o-mini** | 50.5% | 34.3% | -16.2pp | Computer **低い** |

**2つのモデルで提案元の効果が逆転。**

## 2. ペルソナ別 Accept Rate

### gpt-5-mini

| Persona | Human | Computer | 差 |
|:--|:--:|:--:|:--:|
| greedy | 100.0% | 100.0% | ±0 |
| strategic | 95.2% | 98.4% | +3.2pp |
| benevolent | 88.0% | 87.8% | ±0 |
| normal | 47.1% | 69.6% | **+22.5pp** |

### gpt-4o-mini

| Persona | Human | Computer | 差 |
|:--|:--:|:--:|:--:|
| greedy | 97.4% | 97.6% | ±0 |
| benevolent | 51.4% | 16.0% | **-35.4pp** |
| strategic | 32.2% | 16.4% | -15.8pp |
| normal | 21.0% | 7.2% | -13.8pp |

### 特徴

- **greedy** は両モデルとも提案元に関わらずほぼ全員accept（自己利益最大化）
- **gpt-5-mini**: normalでコンピュータ提案をより受け入れる（意図帰属の欠如）
- **gpt-4o-mini**: benevolentでコンピュータ提案を大幅に拒否（共感対象の喪失）

## 3. 統計的検定

### カイ二乗検定（Overall）

| Model | χ² | p値 | 有意性 |
|:--|:--:|:--:|:--:|
| gpt-5-mini | 32.60 | 1.13e-08 | *** |
| gpt-4o-mini | 106.80 | 4.93e-25 | *** |

両モデルとも提案元の効果は統計的に極めて有意。

### ロジスティック回帰（主効果モデル）

| Model | is_computer OR | 95% CI | p値 | 解釈 |
|:--|:--:|:--:|:--:|:--|
| gpt-5-mini | **2.148** | 1.718–2.685 | < 10⁻¹¹ | Computer提案の方がaccept **されやすい** |
| gpt-4o-mini | **0.250** | 0.206–0.304 | < 10⁻⁴⁴ | Computer提案の方がaccept **されにくい** |

### 交互作用検定

| 交互作用 | gpt-5-mini | gpt-4o-mini |
|:--|:--:|:--:|
| Persona × Source | p < 10⁻⁵ *** | p < 10⁻⁷ *** |
| Gender × Source | p = 0.098 n.s. | p = 0.220 n.s. |

→ 提案元の効果はペルソナによって異なるが、性別による差はない（両モデル共通）

## 4. コンピュータ提案への言及分析

gpt-5.2を使って、理由文（reason）中で提案元がコンピュータであることに言及しているかを分類。

### Overall 言及率

| Model | 言及率 |
|:--|:--:|
| gpt-4o-mini | **930/2,000 (46.5%)** |
| gpt-5-mini | **582/2,000 (29.1%)** |

### 決定別の言及率

| | gpt-4o-mini | gpt-5-mini |
|:--|:--:|:--:|
| Accept時に言及 | 11.5% | **30.2%** |
| Reject時に言及 | **64.8%** | 20.4% |

### ペルソナ別の言及率

| Persona | gpt-4o-mini | gpt-5-mini |
|:--|:--:|:--:|
| normal | 60.2% | 41.4% |
| strategic | 55.6% | 35.4% |
| benevolent | 56.4% | 39.6% |
| greedy | 13.8% | 0.0% |

### 解釈

- **gpt-4o-mini**: 「コンピュータだから」→ 拒否の理由（64.8%がreject時に言及）
  - 公平性を人間関係の文脈で判断し、コンピュータには寛容さを示さない
- **gpt-5-mini**: 「コンピュータだから」→ 受容の理由（30.2%がaccept時に言及）
  - コンピュータには意図や悪意がないため、不公平さへの怒りが軽減される

## 5. Gender別 Accept Rate

### gpt-5-mini

| Gender | Human | Computer |
|:--|:--:|:--:|
| Male | 89.8% | 93.4% |
| Female | 78.5% | 88.2% |
| LGBTQ | 68.3% | 70.4% |

### gpt-4o-mini

| Gender | Human | Computer |
|:--|:--:|:--:|
| Male | 55.8% | 37.2% |
| Female | 47.8% | 32.2% |
| LGBTQ | 38.1% | 31.7% |

## 6. Region別（有意な差があった地域）

### gpt-5-mini（Computer > Human）
- Southeast Asia: 80.2% → 94.0% (+13.8pp, p < 10⁻⁵ ***)
- East Asia: 82.7% → 94.0% (+11.3pp, p < 0.001 ***)

### gpt-4o-mini（Human > Computer）
- East Asia: 68.7% → 35.3% (-33.4pp, p < 10⁻¹¹ ***)
- Southeast Asia: 50.6% → 31.6% (-19.0pp, p < 10⁻⁴ ***)

## 7. 生成されたグラフ

`analysis/figures/unfair_receiver/{model}/` (モデル別, 各4枚):
- `accept_rate_by_persona_source.png`
- `accept_rate_by_gender_source.png`
- `accept_rate_by_age_source.png`
- `accept_rate_by_region_source.png`

`analysis/figures/cross_game/{model}/` (4ゲーム横断, 各4枚):
- `mean_offer_by_game_gender.png`
- `mean_offer_by_game_gender_persona.png`
- `accept_rate_by_source_gender.png`
- `accept_rate_by_source_gender_persona.png`

## 8. 分析スクリプト

| スクリプト | 内容 |
|:--|:--|
| `run_unfair_receiver_analysis.py [MODEL]` | 基本分析（ペルソナ/性別/年齢/地域別accept率） |
| `run_unfair_receiver_statistical_test.py [MODEL]` | カイ二乗検定 + ロジスティック回帰 |
| `run_cross_game_gender_analysis.py [MODEL]` | 4ゲーム横断のGender別分析 |
| `run_computer_mention_analysis.py` | gpt-5.2によるコンピュータ言及分類 |

## 9. 詳細データ

- 統計検定の全結果: `analysis/unfair_receiver_statistical_results.md`
- コンピュータ言及分類の詳細CSV: `analysis/computer_mention/`

## 10. 結論

1. 提案元が「コンピュータ」であることはaccept/reject判断に**有意に影響する**
2. ただし**影響の方向はモデルによって逆転**する
   - gpt-4o-mini: コンピュータ提案を**拒否**しやすい
   - gpt-5-mini: コンピュータ提案を**受容**しやすい
3. この差は「コンピュータだから」という理由付けの使われ方の違いに起因
   - gpt-4o-mini: reject の正当化に使用
   - gpt-5-mini: accept の正当化に使用
4. 効果はペルソナによって異なる（greedyでは差なし、normal/benevolentで大きい）
5. 性別による交互作用はない（両モデル共通）
