---
title: ARRAY_FLATTEN
summary: ネストされた配列を単一の次元の配列にフラット化します。
---

# ARRAY_FLATTEN

ネストされた配列を単一の次元の配列にフラット化します。

## 構文 {#syntax}

```sql
ARRAY_FLATTEN(array)
```

## パラメーター {#parameters}

| パラメーター | 説明 |
|-----------|-------------|
| array     | フラット化するネストされた配列。 |

## 戻り値の型 {#return-type}

配列（フラット化後）。

## 注意事項 {#notes}

この関数は、標準の配列型と variant 配列型の両方で使用できます。

## 例 {#examples}

### 例 1: ネストされた配列のフラット化 {#example-1-flattening-a-nested-array}

```sql
SELECT ARRAY_FLATTEN([[1, 2], [3, 4]]);
```

結果:

```
[1, 2, 3, 4]
```

### 例 2: variant 配列のフラット化 {#example-2-flattening-a-variant-array}

```sql
SELECT ARRAY_FLATTEN(PARSE_JSON('[["a", "b"], ["c", "d"]]'));
```

結果:

```
["a", "b", "c", "d"]
```