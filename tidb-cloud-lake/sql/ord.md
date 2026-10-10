---
title: ORD
summary: 左端の文字がマルチバイト文字でない場合、ORD() は ASCII() 関数と同じ値を返します。
---

# ORD

左端の文字がマルチバイト文字でない場合、ORD() は ASCII() 関数と同じ値を返します。

文字列 str の左端の文字がマルチバイト文字である場合、その文字を構成する各バイトの数値を次の式で計算したコードを返します。

```sql
  (1st byte code)
+ (2nd byte code * 256)
+ (3rd byte code * 256^2) ...
```

## 構文 {#syntax}

```sql
ORD(<str>)
```

## 引数 {#arguments}

| 引数 | 説明 |
|-----------|-------------|
| `<str>`   | 文字列。 |

## 戻り値の型 {#return-type}

`BIGINT`

## 例 {#examples}

```sql
SELECT ORD('2')
+--------+
| ORD(2) |
+--------+
|     50 |
+--------+
```