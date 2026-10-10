---
title: TYPEOF
summary: TYPEOF 関数は、データ型の名前を返すために使用されます。
---

# TYPEOF

TYPEOF 関数は、データ型の名前を返すために使用されます。

## 構文 {#syntax}

```sql
TYPEOF( <expr> )
```

## 引数 {#arguments}

| 引数   | 説明 |
| ----------- | ----------- |
| `<expr>` | 任意の式。<br />カラム名、別の関数の結果、または数値演算を指定できます。 |

## 戻り値の型 {#return-type}

String

## 例 {#examples}

```sql
SELECT typeof(1::INT);
+------------------+
| typeof(1::Int32) |
+------------------+
| INT              |
+------------------+
```