---
title: 配列関数
summary: このセクションでは、{{{ .lake }}} の配列関数に関するリファレンス情報を提供します。配列関数を使用すると、配列データ構造の作成、操作、検索、変換を行えます。
---

# 配列関数

このセクションでは、{{{ .lake }}} の配列関数に関するリファレンス情報を提供します。配列関数を使用すると、配列データ構造の作成、操作、検索、変換を行えます。

## 配列の作成と構築 {#array-creation-construction}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [ARRAY](/tidb-cloud-lake/sql/array.md) | 式から配列を構築します | `ARRAY(1, 2, 3)` → `[1,2,3]` |
| [ARRAY_CONSTRUCT](/tidb-cloud-lake/sql/array-construct.md) | 個々の値から配列を作成します | `ARRAY_CONSTRUCT(1, 2, 3)` → `[1,2,3]` |
| [RANGE](/tidb-cloud-lake/sql/range.md) | 連続した数値の配列を生成します | `RANGE(1, 5)` → `[1,2,3,4]` |
| [ARRAY_GENERATE_RANGE](/tidb-cloud-lake/sql/array-generate-range.md) | オプションのステップを指定してシーケンスを生成します | `ARRAY_GENERATE_RANGE(0, 6, 2)` → `[0,2,4]` |

## 配列へのアクセスと情報取得 {#array-access-information}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [GET](/tidb-cloud-lake/sql/get.md) | インデックスで配列から要素を取得します | `GET([1,2,3], 1)` → `1` |
| [ARRAY_GET](/tidb-cloud-lake/sql/array-get.md) | GET 関数のエイリアスです | `ARRAY_GET([1,2,3], 1)` → `1` |
| [CONTAINS](/tidb-cloud-lake/sql/contains.md) | 配列に特定の値が含まれているかを確認します | `CONTAINS([1,2,3], 2)` → `true` |
| [ARRAY_CONTAINS](/tidb-cloud-lake/sql/array-contains.md) | 配列に特定の値が含まれているかを確認します | `ARRAY_CONTAINS([1,2,3], 2)` → `true` |
| [ARRAY_SIZE](/tidb-cloud-lake/sql/array-size.md) | 配列の長さを返します（エイリアス: `ARRAY_LENGTH`） | `ARRAY_SIZE([1,2,3])` → `3` |
| [ARRAY_COUNT](/tidb-cloud-lake/sql/array-count.md) | `NULL` 以外のエントリ数をカウントします | `ARRAY_COUNT([1,NULL,2])` → `2` |
| [ARRAY_ANY](/tidb-cloud-lake/sql/array-any.md) | 最初の `NULL` 以外の値を返します | `ARRAY_ANY([NULL,'a','b'])` → `'a'` |

## 配列の変更 {#array-modification}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [ARRAY_APPEND](/tidb-cloud-lake/sql/array-append.md) | 配列の末尾に要素を追加します | `ARRAY_APPEND([1,2], 3)` → `[1,2,3]` |
| [ARRAY_PREPEND](/tidb-cloud-lake/sql/array-prepend.md) | 配列の先頭に要素を追加します | `ARRAY_PREPEND(0, [1,2])` → `[0,1,2]` |
| [ARRAY_INSERT](/tidb-cloud-lake/sql/array-insert.md) | 指定した位置に要素を挿入します | `ARRAY_INSERT([1,3], 1, 2)` → `[1,2,3]` |
| [ARRAY_REMOVE](/tidb-cloud-lake/sql/array-remove.md) | 指定した要素のすべての出現を削除します | `ARRAY_REMOVE([1,2,2,3], 2)` → `[1,3]` |
| [ARRAY_REMOVE_FIRST](/tidb-cloud-lake/sql/array-remove-first.md) | 配列の最初の要素を削除します | `ARRAY_REMOVE_FIRST([1,2,3])` → `[2,3]` |
| [ARRAY_REMOVE_LAST](/tidb-cloud-lake/sql/array-remove-last.md) | 配列の最後の要素を削除します | `ARRAY_REMOVE_LAST([1,2,3])` → `[1,2]` |

## 配列の結合と操作 {#array-combination-manipulation}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [ARRAY_CONCAT](/tidb-cloud-lake/sql/array-concat.md) | 複数の配列を連結します | `ARRAY_CONCAT([1,2], [3,4])` → `[1,2,3,4]` |
| [ARRAY_SLICE](/tidb-cloud-lake/sql/array-slice.md) | 配列の一部を抽出します | `ARRAY_SLICE([1,2,3,4], 1, 2)` → `[1,2]` |
| [SLICE](/tidb-cloud-lake/sql/slice.md) | ARRAY_SLICE 関数のエイリアスです | `SLICE([1,2,3,4], 1, 2)` → `[1,2]` |
| [ARRAYS_ZIP](/tidb-cloud-lake/sql/arrays-zip.md) | 複数の配列を要素ごとに結合します | `ARRAYS_ZIP([1,2], ['a','b'])` → `[(1,'a'),(2,'b')]` |
| [ARRAY_SORT](/tidb-cloud-lake/sql/array-sort.md) | 値をソートします。バリアントにより順序や null の扱いを制御できます | `ARRAY_SORT([3,1,2])` → `[1,2,3]` |

## 配列の集合演算 {#array-set-operations}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [ARRAY_DISTINCT](/tidb-cloud-lake/sql/array-distinct.md) | 配列から一意の要素を返します | `ARRAY_DISTINCT([1,2,2,3])` → `[1,2,3]` |
| [ARRAY_UNIQUE](/tidb-cloud-lake/sql/array-unique.md) | ARRAY_DISTINCT 関数のエイリアスです | `ARRAY_UNIQUE([1,2,2,3])` → `[1,2,3]` |
| [ARRAY_INTERSECTION](/tidb-cloud-lake/sql/array-intersection.md) | 配列間で共通する要素を返します | `ARRAY_INTERSECTION([1,2,3], [2,3,4])` → `[2,3]` |
| [ARRAY_EXCEPT](/tidb-cloud-lake/sql/array-except.md) | 1 つ目の配列にあり、2 つ目の配列にない要素を返します | `ARRAY_EXCEPT([1,2,3], [2,4])` → `[1,3]` |
| [ARRAY_OVERLAP](/tidb-cloud-lake/sql/array-overlap.md) | 配列同士に共通要素があるかを確認します | `ARRAY_OVERLAP([1,2,3], [3,4,5])` → `true` |

## 配列の処理と変換 {#array-processing-transformation}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [ARRAY_TRANSFORM](/tidb-cloud-lake/sql/json-array-transform.md) | 各配列要素に関数を適用します | `ARRAY_TRANSFORM([1,2,3], x -> x * 2)` → `[2,4,6]` |
| [ARRAY_FILTER](/tidb-cloud-lake/sql/array-filter.md) | 条件に基づいて配列要素をフィルタリングします | `ARRAY_FILTER([1,2,3,4], x -> x > 2)` → `[3,4]` |
| [ARRAY_REDUCE](/tidb-cloud-lake/sql/array-reduce.md) | 集計を使用して配列を単一の値に縮約します | `ARRAY_REDUCE([1,2,3], 0, (acc,x) -> acc + x)` → `6` |
| [ARRAY_AGGREGATE](/tidb-cloud-lake/sql/array-aggregate.md) | 関数を使用して配列要素を集計します | `ARRAY_AGGREGATE([1,2,3], 'sum')` → `6` |

## 配列の集計と統計 {#array-aggregations-statistics}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [ARRAY_SUM](/tidb-cloud-lake/sql/array-sum.md) | 数値の合計 | `ARRAY_SUM([1,2,3])` → `6` |
| [ARRAY_AVG](/tidb-cloud-lake/sql/array-avg.md) | 数値の平均 | `ARRAY_AVG([1,2,3])` → `2` |
| [ARRAY_MEDIAN](/tidb-cloud-lake/sql/array-median.md) | 数値の中央値 | `ARRAY_MEDIAN([1,3,2])` → `2` |
| [ARRAY_MIN](/tidb-cloud-lake/sql/array-min.md) | 最小値 | `ARRAY_MIN([3,1,2])` → `1` |
| [ARRAY_MAX](/tidb-cloud-lake/sql/array-max.md) | 最大値 | `ARRAY_MAX([3,1,2])` → `3` |
| [ARRAY_STDDEV_POP](/tidb-cloud-lake/sql/array-stddev-pop.md) | 母標準偏差（エイリアス: `ARRAY_STD`） | `ARRAY_STDDEV_POP([1,2,3])` |
| [ARRAY_STDDEV_SAMP](/tidb-cloud-lake/sql/array-stddev-samp.md) | 標本標準偏差（エイリアス: `ARRAY_STDDEV`） | `ARRAY_STDDEV_SAMP([1,2,3])` |
| [ARRAY_KURTOSIS](/tidb-cloud-lake/sql/array-kurtosis.md) | 値の過剰尖度 | `ARRAY_KURTOSIS([1,2,3,4])` |
| [ARRAY_SKEWNESS](/tidb-cloud-lake/sql/array-skewness.md) | 値の歪度 | `ARRAY_SKEWNESS([1,2,3,4])` |
| [ARRAY_APPROX_COUNT_DISTINCT](/tidb-cloud-lake/sql/array-approx-count-distinct.md) | 近似の重複しない件数 | `ARRAY_APPROX_COUNT_DISTINCT([1,1,2])` → `2` |

## 配列の書式設定 {#array-formatting}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [ARRAY_TO_STRING](/tidb-cloud-lake/sql/array-to-string.md) | 配列要素を結合して文字列にします | `ARRAY_TO_STRING(['a','b'], ',')` → `'a,b'` |

## 配列ユーティリティ関数 {#array-utility-functions}

| 関数 | 説明 | 例 |
|----------|-------------|---------|
| [ARRAY_COMPACT](/tidb-cloud-lake/sql/array-compact.md) | 配列から null 値を削除します | `ARRAY_COMPACT([1,null,2,null,3])` → `[1,2,3]` |
| [ARRAY_FLATTEN](/tidb-cloud-lake/sql/array-flatten.md) | ネストされた配列を 1 つの配列に平坦化します | `ARRAY_FLATTEN([[1,2],[3,4]])` → `[1,2,3,4]` |
| [ARRAY_REVERSE](/tidb-cloud-lake/sql/array-reverse.md) | 配列要素の順序を反転します | `ARRAY_REVERSE([1,2,3])` → `[3,2,1]` |
| [ARRAY_INDEXOF](/tidb-cloud-lake/sql/array-indexof.md) | 要素が最初に出現するインデックスを返します | `ARRAY_INDEXOF([1,2,3,2], 2)` → `1` |
| [UNNEST](/tidb-cloud-lake/sql/unnest.md) | 配列を個別の行に展開します | `UNNEST([1,2,3])` → `1, 2, 3`（それぞれ別の行として） |