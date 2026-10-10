---
title: ARRAY_SLICE
summary: start 引数と end 引数の間をスライスして、部分配列を抽出します。
---

# ARRAY_SLICE

start 引数と end 引数の間をスライスして、部分配列を抽出します。

## 構文 {#syntax}

```sql
ARRAY_SLICE(array, start, end)
```

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| array     | スライスを抽出する元の配列です。 |
| start     | スライスの開始位置です（含む）。 |
| end       | スライスの終了位置です（含まない）。 |

## 戻り値の型 {#return-type}

配列（元の配列のスライス）。

## インデックスに関する重要な注意 {#important-note-on-indexing}

- 標準の配列型の場合: インデックスは **1-based** です（最初の要素の位置は 1）。
- variant 配列型の場合: Snowflake との互換性のため、インデックスは **0-based** です（最初の要素の位置は 0）。

## 例 {#examples}

### 例 1: 標準配列のスライス（1-based indexing） {#example-1-slicing-a-standard-array-1-based-indexing}

```sql
SELECT ARRAY_SLICE([10, 20, 30, 40, 50], 2, 4);
```

結果:

```
[20, 30]
```

### 例 2: variant 配列のスライス（0-based indexing） {#example-2-slicing-a-variant-array-0-based-indexing}

```sql
SELECT ARRAY_SLICE(PARSE_JSON('["apple", "banana", "orange", "grape", "kiwi"]'), 1, 3);
```

結果:

```
["banana", "orange"]
```

### 例 3: 範囲外のスライス {#example-3-out-of-bounds-slice}

```sql
SELECT ARRAY_SLICE([1, 2, 3], 4, 6);
```

結果:

```
[]
```