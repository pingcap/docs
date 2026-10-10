---
title: ARRAY_REMOVE_FIRST
summary: 配列から要素の最初の出現を削除します。
---

# ARRAY_REMOVE_FIRST

配列から要素の最初の出現を削除します。

## 構文 {#syntax}

```sql
ARRAY_REMOVE_FIRST(array, element)
```

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| array     | 要素を削除する元の配列です。 |
| element   | 配列から削除する要素です。 |

## 戻り値の型 {#return-type}

指定した要素の最初の出現を削除した配列を返します。

## 注意事項 {#notes}

この関数は、標準の配列型と variant 配列型の両方で使用できます。

## 例 {#examples}

### 例 1: 標準配列からの削除 {#example-1-removing-from-a-standard-array}

```sql
SELECT ARRAY_REMOVE_FIRST([1, 2, 2, 3], 2);
```

結果:

```
[1, 2, 3]
```

### 例 2: variant 配列からの削除 {#example-2-removing-from-a-variant-array}

```sql
SELECT ARRAY_REMOVE_FIRST(PARSE_JSON('["apple", "banana", "apple", "orange"]'), 'apple');
```

結果:

```
["banana", "apple", "orange"]
```

### 例 3: 要素が見つからない場合 {#example-3-element-not-found}

```sql
SELECT ARRAY_REMOVE_FIRST([1, 2, 3], 4);
```

結果:

```
[1, 2, 3]
```