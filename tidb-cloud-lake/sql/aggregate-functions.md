---
title: 集計関数
summary: このページでは、{{{ .lake }}} の集計関数について、機能別に整理して包括的に紹介します。参照しやすいように構成されています。
---

# 集計関数

このページでは、{{{ .lake }}} の集計関数について、機能別に整理して包括的に紹介します。参照しやすいように構成されています。

## 基本的な集計 {#basic-aggregation}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [COUNT](/tidb-cloud-lake/sql/count.md) | 行数または非 NULL 値の数をカウントします | `COUNT(*)` → `10` |
| [COUNT_DISTINCT](/tidb-cloud-lake/sql/count-distinct.md) | 重複しない値の数をカウントします | `COUNT(DISTINCT city)` → `5` |
| [APPROX_COUNT_DISTINCT](/tidb-cloud-lake/sql/approx-count-distinct.md) | 重複しない値の数を近似的にカウントします | `APPROX_COUNT_DISTINCT(user_id)` → `9955` |
| [SUM](/tidb-cloud-lake/sql/sum.md) | 値の合計を計算します | `SUM(sales)` → `1250.75` |
| [AVG](/tidb-cloud-lake/sql/avg.md) | 値の平均を計算します | `AVG(temperature)` → `72.5` |
| [MIN](/tidb-cloud-lake/sql/min.md) | 最小値を返します | `MIN(price)` → `9.99` |
| [MAX](/tidb-cloud-lake/sql/max.md) | 最大値を返します | `MAX(price)` → `99.99` |
| [ANY_VALUE](/tidb-cloud-lake/sql/any-value.md) | グループ内の任意の値を返します | `ANY_VALUE(status)` → `'active'` |

## 条件付き集計 {#conditional-aggregation}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [COUNT_IF](/tidb-cloud-lake/sql/count-if.md) | 条件に一致する行をカウントします | `COUNT_IF(price > 100)` → `5` |
| [SUM_IF](/tidb-cloud-lake/sql/sum-if.md) | 条件に一致する値を合計します | `SUM_IF(amount, status = 'completed')` → `750.25` |
| [AVG_IF](/tidb-cloud-lake/sql/avg-if.md) | 条件に一致する値の平均を計算します | `AVG_IF(score, passed = true)` → `85.6` |
| [MIN_IF](/tidb-cloud-lake/sql/min-if.md) | 条件が true の場合の最小値を返します | `MIN_IF(temp, location = 'outside')` → `45.2` |
| [MAX_IF](/tidb-cloud-lake/sql/max-if.md) | 条件が true の場合の最大値を返します | `MAX_IF(speed, vehicle = 'car')` → `120.5` |

## 統計関数 {#statistical-functions}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [VAR_POP](/tidb-cloud-lake/sql/var-pop.md) / [VARIANCE_POP](/tidb-cloud-lake/sql/variance-pop.md) | 母分散 | `VAR_POP(height)` → `10.25` |
| [VAR_SAMP](/tidb-cloud-lake/sql/var-samp.md) / [VARIANCE_SAMP](/tidb-cloud-lake/sql/variance-samp.md) | 標本分散 | `VAR_SAMP(height)` → `12.3` |
| [STDDEV_POP](/tidb-cloud-lake/sql/stddev-pop.md) | 母標準偏差 | `STDDEV_POP(height)` → `3.2` |
| [STDDEV_SAMP](/tidb-cloud-lake/sql/stddev-samp.md) | 標本標準偏差 | `STDDEV_SAMP(height)` → `3.5` |
| [COVAR_POP](/tidb-cloud-lake/sql/covar-pop.md) | 母共分散 | `COVAR_POP(x, y)` → `2.5` |
| [COVAR_SAMP](/tidb-cloud-lake/sql/covar-samp.md) | 標本共分散 | `COVAR_SAMP(x, y)` → `2.7` |
| [KURTOSIS](/tidb-cloud-lake/sql/kurtosis.md) | 分布の尖度を測定します | `KURTOSIS(values)` → `2.1` |
| [SKEWNESS](/tidb-cloud-lake/sql/skewness.md) | 分布の非対称性を測定します | `SKEWNESS(values)` → `0.2` |

## パーセンタイルと分布 {#percentile-and-distribution}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [MEDIAN](/tidb-cloud-lake/sql/median.md) | 中央値を計算します | `MEDIAN(response_time)` → `125` |
| [MODE](/tidb-cloud-lake/sql/mode.md) | 最頻値を返します | `MODE(category)` → `'electronics'` |
| [QUANTILE_CONT](/tidb-cloud-lake/sql/quantile-cont.md) | 連続補間による分位点 | `QUANTILE_CONT(0.95)(response_time)` → `350.5` |
| [QUANTILE_DISC](/tidb-cloud-lake/sql/quantile-disc.md) | 離散分位点 | `QUANTILE_DISC(0.5)(age)` → `35` |
| [QUANTILE_TDIGEST](/tidb-cloud-lake/sql/quantile-tdigest.md) | t-digest を使用した近似分位点 | `QUANTILE_TDIGEST(0.9)(values)` → `95.2` |
| [QUANTILE_TDIGEST_WEIGHTED](/tidb-cloud-lake/sql/quantile-tdigest-weighted.md) | 重み付き t-digest 分位点 | `QUANTILE_TDIGEST_WEIGHTED(0.5)(values, weights)` → `50.5` |
| [MEDIAN_TDIGEST](/tidb-cloud-lake/sql/median-tdigest.md) | t-digest を使用した近似中央値 | `MEDIAN_TDIGEST(response_time)` → `124.5` |
| [HISTOGRAM](/tidb-cloud-lake/sql/histogram.md) | ヒストグラムのバケットを作成します | `HISTOGRAM(10)(values)` → `[{...}]` |

## 配列およびコレクションの集計 {#array-and-collection-aggregation}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [ARRAY_AGG](/tidb-cloud-lake/sql/array-agg.md) | 値を配列に収集します | `ARRAY_AGG(product)` → `['A', 'B', 'C']` |
| [GROUP_ARRAY_MOVING_AVG](/tidb-cloud-lake/sql/group-array-moving-avg.md) | 配列に対する移動平均 | `GROUP_ARRAY_MOVING_AVG(3)(values)` → `[null, null, 3.0, 6.0, 9.0]` |
| [GROUP_ARRAY_MOVING_SUM](/tidb-cloud-lake/sql/group-array-moving-sum.md) | 配列に対する移動合計 | `GROUP_ARRAY_MOVING_SUM(2)(values)` → `[null, 3, 7, 11, 15]` |

## 地理空間集計 {#geospatial-aggregation}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [ST_UNION_AGG](/tidb-cloud-lake/sql/st-union-agg.md) | グループ内の GEOMETRY 値を結合します | `ST_UNION_AGG(geom)` → `MULTIPOINT(...)` |
| [ST_INTERSECTION_AGG](/tidb-cloud-lake/sql/st-intersection-agg.md) | グループ内の GEOMETRY 値の共通部分を求めます | `ST_INTERSECTION_AGG(geom)` → `POLYGON(...)` |
| [ST_ENVELOPE_AGG](/tidb-cloud-lake/sql/st-envelope-agg.md) | グループ内の GEOMETRY 値の外接矩形を返します | `ST_ENVELOPE_AGG(geom)` → `POLYGON(...)` |
| [ST_COLLECT](/tidb-cloud-lake/sql/st-collect.md) | GEOMETRY 値を 1 つの GEOMETRY 結果に収集します | `ST_COLLECT(geom)` → `GEOMETRYCOLLECTION(...)` |

## 文字列集計 {#string-aggregation}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [GROUP_CONCAT](/tidb-cloud-lake/sql/group-concat.md) | 区切り文字を使って値を連結します | `GROUP_CONCAT(city, ', ')` → `'New York, London, Tokyo'` |
| [STRING_AGG](/tidb-cloud-lake/sql/string-agg.md) | 区切り文字を使って文字列を連結します | `STRING_AGG(tag, ',')` → `'red,green,blue'` |
| [LISTAGG](/tidb-cloud-lake/sql/listagg.md) | 区切り文字を使って値を連結します | `LISTAGG(name, ', ')` → `'Alice, Bob, Charlie'` |

## JSON 集計 {#json-aggregation}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [JSON_ARRAY_AGG](/tidb-cloud-lake/sql/json-array-agg.md) | 値を JSON 配列として集計します | `JSON_ARRAY_AGG(name)` → `'["Alice", "Bob", "Charlie"]'` |
| [JSON_OBJECT_AGG](/tidb-cloud-lake/sql/json-object-agg.md) | キーと値のペアから JSON オブジェクトを作成します | `JSON_OBJECT_AGG(name, score)` → `'{"Alice": 95, "Bob": 87}'` |

## 引数選択 {#argument-selection}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [ARG_MAX](/tidb-cloud-lake/sql/arg-max.md) | expr2 が最大のときの expr1 の値を返します | `ARG_MAX(name, score)` → `'Alice'` |
| [ARG_MIN](/tidb-cloud-lake/sql/arg-min.md) | expr2 が最小のときの expr1 の値を返します | `ARG_MIN(name, score)` → `'Charlie'` |

## ファネル分析 {#funnel-analysis}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [RETENTION](/tidb-cloud-lake/sql/retention.md) | リテンション率を計算します | `RETENTION(action = 'signup', action = 'purchase')` → `[100, 40]` |
| [WINDOWFUNNEL](/tidb-cloud-lake/sql/window-funnel.md) | 時間ウィンドウ内のイベントシーケンスを検索します | `WINDOWFUNNEL(1800)(timestamp, event='view', event='click', event='purchase')` → `2` |

## 匿名化 {#anonymization}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [MARKOV_TRAIN](/tidb-cloud-lake/sql/markov-train.md) | マルコフモデルを学習します | `MARKOV_TRAIN(address)` |