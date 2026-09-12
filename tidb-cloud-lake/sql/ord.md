---
title: ORD
summary: 如果最左侧字符不是多字节字符，ORD() 返回与 ASCII() 函数相同的值。
---

# ORD

如果最左侧字符不是多字节字符，ORD() 返回与 ASCII() 函数相同的值。

如果字符串 str 的最左侧字符是多字节字符，则返回该字符的编码。该编码根据其组成字节的数值，按以下公式计算：

```sql
  (1st byte code)
+ (2nd byte code * 256)
+ (3rd byte code * 256^2) ...
```

## 语法 {#syntax}

```sql
ORD(<str>)
```

## 参数 {#arguments}

| 参数 | 描述 |
|-----------|-------------|
| `<str>`   | 字符串。 |

## 返回类型 {#return-type}

`BIGINT`

## 示例 {#examples}

```sql
SELECT ORD('2')
+--------+
| ORD(2) |
+--------+
|     50 |
+--------+
```