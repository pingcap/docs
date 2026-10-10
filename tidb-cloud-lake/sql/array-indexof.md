---
title: ARRAY_INDEXOF
summary: 配列内で要素が最初に出現する位置のインデックスを返します。
---

# ARRAY_INDEXOF

配列内で要素が最初に出現する位置のインデックスを返します。

## 構文 {#syntax}

```sql
ARRAY_INDEXOF(array, element)
```

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| array     | 検索対象の配列です。 |
| element   | 検索する要素です。 |

## 戻り値の型 {#return-type}

INTEGER

## インデックスに関する重要な注意事項 {#important-note-on-indexing}

- 標準の配列型の場合: インデックスは **1-based** です（最初の要素の位置は 1）。
- variant 配列型の場合: Snowflake との互換性のため、インデックスは **0-based** です（最初の要素の位置は 0）。

## 例 {#examples}

### 例 1: 標準配列内の要素を検索する（1-based indexing） {#example-1-finding-an-element-in-a-standard-array-1-based-indexing}

```sql
SELECT ARRAY_INDEXOF([10, 20, 30, 20], 20);
```

結果:

```
2
```

### 例 2: variant 配列内の要素を検索する（0-based indexing） {#example-2-finding-an-element-in-a-variant-array-0-based-indexing}

```sql
SELECT ARRAY_INDEXOF(PARSE_JSON('["apple", "banana", "orange"]'), 'banana');
```

結果:

```
1
```

### 例 3: 要素が見つからない場合 {#example-3-element-not-found}

```sql
SELECT ARRAY_INDEXOF([1, 2, 3], 4);
```

結果:

```
0
```