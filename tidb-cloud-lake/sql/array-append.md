---
title: ARRAY_APPEND
summary: 配列の末尾に要素を追加します。
---

# ARRAY_APPEND

配列の末尾に要素を追加します。

## 構文 {#syntax}

```sql
ARRAY_APPEND(array, element)
```

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| array     | 要素を追加する対象の元の配列です。 |
| element   | 配列に追加する要素です。 |

## 戻り値の型 {#return-type}

要素が追加された配列。

## 注意事項 {#notes}

この関数は、標準の配列型と variant 配列型の両方で使用できます。

## 例 {#examples}

### 例 1: 標準配列への追加 {#example-1-appending-to-a-standard-array}

```sql
SELECT ARRAY_APPEND([1, 2, 3], 4);
```

結果:

```
[1, 2, 3, 4]
```

### 例 2: variant 配列への追加 {#example-2-appending-to-a-variant-array}

```sql
SELECT ARRAY_APPEND(PARSE_JSON('[1, 2, 3]'), 4);
```

結果:

```
[1, 2, 3, 4]
```

### 例 3: 異なるデータ型の追加 {#example-3-appending-different-data-types}

```sql
SELECT ARRAY_APPEND(['a', 'b'], 'c');
```

結果:

```
["a", "b", "c"]
```

## 関連する関数 {#related-functions}

- [ARRAY_PREPEND](/tidb-cloud-lake/sql/array-prepend.md): 配列の先頭に要素を追加します
- [ARRAY_CONCAT](/tidb-cloud-lake/sql/array-concat.md): 2 つの配列を連結します