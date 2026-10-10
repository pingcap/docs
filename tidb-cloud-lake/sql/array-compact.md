---
title: ARRAY_COMPACT
summary: 配列からすべての NULL 値を削除します。
---

# ARRAY_COMPACT

配列からすべての NULL 値を削除します。

## 構文 {#syntax}

```sql
ARRAY_COMPACT(array)
```

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| array     | NULL 値を削除する対象の配列です。 |

## 戻り値の型 {#return-type}

NULL 値を含まない配列。

## 注意事項 {#notes}

この関数は、標準の配列型と variant 配列型の両方で使用できます。

## 例 {#examples}

### 例 1: 標準配列から NULL を削除する {#example-1-removing-nulls-from-a-standard-array}

```sql
SELECT ARRAY_COMPACT([1, NULL, 2, NULL, 3]);
```

結果:

```
[1, 2, 3]
```

### 例 2: variant 配列から NULL を削除する {#example-2-removing-nulls-from-a-variant-array}

```sql
SELECT ARRAY_COMPACT(PARSE_JSON('["apple", null, "banana", null, "orange"]'));
```

結果:

```
["apple", "banana", "orange"]
```

### 例 3: NULL を含まない配列 {#example-3-array-with-no-nulls}

```sql
SELECT ARRAY_COMPACT([1, 2, 3]);
```

結果:

```
[1, 2, 3]
```