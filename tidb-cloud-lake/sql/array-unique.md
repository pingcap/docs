---
title: ARRAY_UNIQUE
summary: 配列内の一意な要素数を返します。
---

# ARRAY_UNIQUE

配列内の一意な要素数を返します。

## 構文 {#syntax}

```sql
ARRAY_UNIQUE(array)
```

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| array     | 一意な要素を分析する対象の配列です。 |

## 戻り値の型 {#return-type}

INTEGER

## 注意事項 {#notes}

この関数は、標準の配列型と variant 配列型の両方で使用できます。

## 例 {#examples}

### 例 1: 標準配列内の一意な要素数を数える {#example-1-counting-unique-elements-in-a-standard-array}

```sql
SELECT ARRAY_UNIQUE([1, 2, 2, 3, 3, 3]);
```

結果:

```
3
```

### 例 2: variant 配列内の一意な要素数を数える {#example-2-counting-unique-elements-in-a-variant-array}

```sql
SELECT ARRAY_UNIQUE(PARSE_JSON('["apple", "banana", "apple", "orange", "banana"]'));
```

結果:

```
3
```

### 例 3: 空の配列 {#example-3-empty-array}

```sql
SELECT ARRAY_UNIQUE([]);
```

結果:

```
0
```