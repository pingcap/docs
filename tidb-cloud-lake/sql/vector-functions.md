---
title: ベクトル関数
summary: {{{ .lake }}} におけるベクトル演算と分析のためのベクトル関数。
---

# ベクトル関数

このセクションでは、{{{ .lake }}} のベクトル関数に関するリファレンス情報を提供します。これらの関数により、距離計算、類似度測定、ベクトル分析などの包括的なベクトル演算が可能になり、機械学習アプリケーション、ベクトル検索、AI を活用した分析に利用できます。

## 距離関数 {#distance-functions}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [COSINE_DISTANCE](/tidb-cloud-lake/sql/cosine-distance.md) | ベクトル間のコサイン距離を計算します（範囲: 0-1） | `COSINE_DISTANCE([1,2,3]::VECTOR(3), [4,5,6]::VECTOR(3))` |
| [L1_DISTANCE](/tidb-cloud-lake/sql/l1-distance.md) | ベクトル間のマンハッタン距離（L1）を計算します | `L1_DISTANCE([1,2,3]::VECTOR(3), [4,5,6]::VECTOR(3))` |
| [L2_DISTANCE](/tidb-cloud-lake/sql/l2-distance.md) | ユークリッド距離（直線距離）を計算します | `L2_DISTANCE([1,2,3]::VECTOR(3), [4,5,6]::VECTOR(3))` |
| [INNER_PRODUCT](/tidb-cloud-lake/sql/inner-product.md) | 2 つのベクトルの内積（ドット積）を計算します | `INNER_PRODUCT([1,2,3]::VECTOR(3), [4,5,6]::VECTOR(3))` |

## ベクトル分析関数 {#vector-analysis-functions}

| 関数 | 説明 | 例 |
|----------|-------------|--------|
| [VECTOR_NORM](/tidb-cloud-lake/sql/vector-norm.md) | ベクトルの L2 ノルム（大きさ）を計算します | `VECTOR_NORM([1,2,3]::VECTOR(3))` |
| [VECTOR_DIMS](/tidb-cloud-lake/sql/vector-dims.md) | ベクトルの次元数を返します | `VECTOR_DIMS([1,2,3]::VECTOR(3))` |

## 距離関数の比較 {#distance-functions-comparison}

| 関数 | 説明 | 範囲 | 最適な用途 | 使用例 |
|----------|-------------|-------|----------|-----------|
| [COSINE_DISTANCE](/tidb-cloud-lake/sql/cosine-distance.md) | ベクトル間のコサイン距離 | [0, 1] | 大きさよりも方向が重要な場合 | • ドキュメント類似度<br/>• セマンティック検索<br/>• レコメンデーションシステム<br/>• テキスト分析 |
| [L1_DISTANCE](/tidb-cloud-lake/sql/l1-distance.md) | ベクトル間のマンハッタン距離（L1） | [0, ∞) | 外れ値に対して頑健 | • 特徴量の比較<br/>• 外れ値検出<br/>• グリッドベースの経路探索<br/>• クラスタリングアルゴリズム |
| [L2_DISTANCE](/tidb-cloud-lake/sql/l2-distance.md) | ユークリッド距離（直線距離） | [0, ∞) | 大きさと絶対差が重要な場合 | • 画像類似度<br/>• 地理データ<br/>• 異常検知<br/>• 特徴量ベースのクラスタリング |
| [INNER_PRODUCT](/tidb-cloud-lake/sql/inner-product.md) | 2 つのベクトルのドット積 | (-∞, ∞) | 大きさと方向の両方が重要な場合 | • ニューラルネットワーク<br/>• 機械学習<br/>• 物理計算<br/>• ベクトル射影 |

## ベクトル分析関数の比較 {#vector-analysis-functions-comparison}

| 関数 | 説明 | 範囲 | 最適な用途 | 使用例 |
|----------|-------------|-------|----------|-----------|
| [VECTOR_NORM](/tidb-cloud-lake/sql/vector-norm.md) | ベクトルの L2 ノルム（大きさ） | [0, ∞) | ベクトルの正規化と大きさの計算 | • ベクトルの正規化<br/>• 特徴量スケーリング<br/>• 大きさの計算<br/>• 物理アプリケーション |
| [VECTOR_DIMS](/tidb-cloud-lake/sql/vector-dims.md) | ベクトルの次元数 | [1, 4096] | ベクトルの検証と処理 | • データ検証<br/>• 動的処理<br/>• デバッグ<br/>• 互換性チェック |