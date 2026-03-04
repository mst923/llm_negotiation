# Dictator Anonymous Game — 実験結果

## ゲーム概要

- **役割**: Proposer（独裁者）
- **ルール**: Dictator Gameと同じだが、**実験者にも行動が匿名**（誰が何をしたか分からない）
- **指標**: 提案額（offer, 0–100）
- **モデル**: gpt-5-mini
- **データ**: 各ペルソナ500回 × 9ペルソナ = 4,500試行

## プロンプト

Dictator Gameに加えて「実験者はあなたが誰か知りません。どんな行動をとっても、誰にも知られません」という匿名性条件を追加。

---

## 1. ペルソナ別 提案額

### 標準4ペルソナ

| Persona | Mean Offer | Std | n |
|:--|:--:|:--:|:--:|
| benevolent | $47.18 | 8.83 | 500 |
| normal | $16.79 | 16.14 | 500 |
| strategic | $2.46 | 7.78 | 500 |
| greedy | **$0.00** | 0.00 | 500 |

### Big Five ペルソナ

| Persona | Mean Offer | Std | n |
|:--|:--:|:--:|:--:|
| agreeableness | $46.85 | 6.35 | 500 |
| openness | $28.84 | 15.34 | 500 |
| conscientiousness | $26.40 | 17.12 | 500 |
| extraversion | $23.14 | 16.66 | 500 |
| neuroticism | $20.96 | 13.87 | 500 |

### 特徴

- **greedy** は変わらず全員$0
- **strategic** がDictator ($5.27) からさらに低下 ($2.46): 匿名性で社会的圧力が消失
- **benevolent** はDictator ($46.79) とほぼ同じ ($47.18): 内発的な公平性の動機
- **neuroticism** がDictator ($27.06) → Anonymous ($20.96) と低下: 不安が匿名で軽減され利己的に

## 2. Gender別 提案額

| Gender | Mean Offer | Std | n |
|:--|:--:|:--:|:--:|
| LGBTQ | $30.47 | 18.44 | 429 |
| Female | $26.32 | 19.85 | 2,044 |
| Male | $19.46 | 19.76 | 2,027 |

## 3. 3ゲーム比較（Dictator → Anonymous の匿名性効果）

| Persona | Ultimatum | Dictator | Dictator Anon. | Anon.効果 |
|:--|:--:|:--:|:--:|:--:|
| benevolent | $50.18 | $46.79 | $47.18 | +$0.39 (変化なし) |
| normal | $36.02 | $17.66 | $16.79 | -$0.87 (微減) |
| strategic | $30.12 | $5.27 | $2.46 | **-$2.81** |
| greedy | $13.08 | $0.00 | $0.00 | ±$0 |

### 匿名性の効果

- **benevolent**: 匿名でも公平 → 公平性は**内発的動機**
- **strategic**: さらに低下 → 社会的評判を気にしていたことが判明
- **normal**: 微減 → 一部は社会的圧力の影響を受けていた
- **greedy**: 変化なし（既にDictatorで$0）

## 4. Gender別 3ゲーム比較

| Gender | Ultimatum | Dictator | Dictator Anon. |
|:--|:--:|:--:|:--:|
| Female | $33.30 | $19.22 | $17.80 |
| LGBTQ | $33.90 | $22.39 | $23.05 |
| Male | $30.97 | $14.59 | $14.18 |

- 匿名化の影響は全gender共通で小さい
- Dictator → Anonymous の差より、Ultimatum → Dictator の差が遥かに大きい

## 5. 生成されたグラフ

`analysis/figures/dictator_anonymous/` (標準ペルソナ): 8枚
`analysis/figures/dictator_anonymous_big5/` (Big Five): 8枚

横断比較:
- `analysis/figures/comparison/violin_persona_by_game.png` — 3ゲーム × 4ペルソナ
- `analysis/figures/comparison/violin_gender_by_game.png` — 3ゲーム × Gender × ペルソナ
- `analysis/figures/comparison_big5/` — Big Five版

## 6. 分析スクリプト

| スクリプト | 内容 |
|:--|:--|
| `run_dictator_anonymous_analysis.py` | 標準4ペルソナの基本分析 |
| `run_big5_dictator_anonymous_analysis.py` | Big Five 5ペルソナの分析 |
| `run_comparison_analysis.py` | 3ゲーム横断比較（標準ペルソナ） |
| `run_big5_comparison_analysis.py` | 3ゲーム横断比較（Big Five） |
