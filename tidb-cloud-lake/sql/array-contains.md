---
title: ARRAY_CONTAINS
summary: 配列に指定した要素が含まれている場合に true を返します。
---

# ARRAY_CONTAINS

配列に指定した要素が含まれている場合に true を返します。

## 構文 {#syntax}

```sql
ARRAY_CONTAINS(array, element)
```

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| array     | 検索対象の配列です。 |
| element   | 検索する要素です。 |

## 戻り値の型 {#return-type}

BOOLEAN

## 注意事項 {#notes}

この関数は、標準の配列型と variant 配列型の両方で使用できます。

## 例 {#examples}

### 例 1: 標準配列の確認 {#example-1-checking-a-standard-array}

```sql
SELECT ARRAY_CONTAINS([1, 2, 3], 2);
```

結果:

```
true
```

### 例 2: variant 配列の確認 {#example-2-checking-a-variant-array}

```sql
SELECT ARRAY_CONTAINS(PARSE_JSON('["apple", "banana", "orange"]'), 'banana');
```

結果:

```
true
```

### 例 3: 要素が見つからない場合 {#example-3-element-not-found}

```sql
SELECT ARRAY_CONTAINS([1, 2, 3], 4);
```

結果:

```
false
```