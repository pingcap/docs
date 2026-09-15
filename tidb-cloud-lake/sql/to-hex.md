---
title: TO_HEX
summary: 对于字符串参数 str，TO_HEX() 返回 str 的十六进制字符串表示，其中 str 中每个字符的每个字节都会被转换为两个十六进制数字。此操作的逆操作由 UNHEX() 函数执行。
---

# TO_HEX

对于字符串参数 str，TO_HEX() 返回 str 的十六进制字符串表示，其中 str 中每个字符的每个字节都会被转换为两个十六进制数字。此操作的逆操作由 UNHEX() 函数执行。

对于数值参数 N，TO_HEX() 返回 N 的十六进制字符串表示，其中 N 被视为 longlong (BIGINT) 数值。

## 语法 {#syntax}

```sql
TO_HEX(<expr>)
```

## 别名 {#aliases}

- [HEX](/tidb-cloud-lake/sql/hex.md)

## 示例 {#examples}

```sql
SELECT HEX('abc'), TO_HEX('abc');

┌────────────────────────────┐
│ hex('abc') │ to_hex('abc') │
├────────────┼───────────────┤
│ 616263     │ 616263        │
└────────────────────────────┘

SELECT HEX(255), TO_HEX(255);

┌────────────────────────┐
│ hex(255) │ to_hex(255) │
├──────────┼─────────────┤
│ ff       │ ff          │
└────────────────────────┘
```