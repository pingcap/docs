---
title: ARRAY_REVERSE
summary: 配列内の要素の順序を逆にします。
---

# ARRAY_REVERSE

配列内の要素の順序を逆にします。

## 構文 {#syntax}

```sql
ARRAY_REVERSE(array)
```

## パラメータ {#parameters}

| パラメータ | 説明 |
|-----------|-------------|
| array     | 逆順にする配列。 |

## 戻り値の型 {#return-type}

要素が逆順になった配列。

## 注意事項 {#notes}

この関数は、標準の配列型と variant 配列型の両方で使用できます。

## 例 {#examples}

### 例 1: 標準配列を逆順にする {#example-1-reversing-a-standard-array}

```sql
SELECT ARRAY_REVERSE([1, 2, 3, 4, 5]);
```

結果:

```
[5, 4, 3, 2, 1]
```

### 例 2: variant 配列を逆順にする {#example-2-reversing-a-variant-array}

```sql
SELECT ARRAY_REVERSE(PARSE_JSON('["apple", "banana", "orange"]'));
```

結果:

```
["orange", "banana", "apple"]
```

### 例 3: 空の配列を逆順にする {#example-3-reversing-an-empty-array}

```sql
SELECT ARRAY_REVERSE([]);
```

結果:

```
[]
```