---
title: ARRAY_PREPEND
summary: 配列の先頭に要素を追加します。
---

# ARRAY_PREPEND

配列の先頭に要素を追加します。

## 構文 {#syntax}

```sql
ARRAY_PREPEND(element, array)
```

## パラメーター {#parameters}

| パラメーター | 説明 |
|-----------|-------------|
| element   | 配列の先頭に追加する要素です。 |
| array     | 要素が先頭に追加される元の配列です。 |

## 戻り値の型 {#return-type}

要素が先頭に追加された配列。

## 注意事項 {#notes}

この関数は、標準の配列型と variant 配列型の両方で使用できます。

## 例 {#examples}

### 例 1: 標準配列の先頭に追加する {#example-1-prepending-to-a-standard-array}

```sql
SELECT ARRAY_PREPEND(0, [1, 2, 3]);
```

結果:

```
[0, 1, 2, 3]
```

### 例 2: variant 配列の先頭に追加する {#example-2-prepending-to-a-variant-array}

```sql
SELECT ARRAY_PREPEND('apple', PARSE_JSON('["banana", "orange"]'));
```

結果:

```
["apple", "banana", "orange"]
```

### 例 3: 複雑な要素を先頭に追加する {#example-3-prepending-a-complex-element}

```sql
SELECT ARRAY_PREPEND(PARSE_JSON('{"value": 0}'), [1, 2, 3]);
```

結果:

```
[{"value": 0}, 1, 2, 3]
```