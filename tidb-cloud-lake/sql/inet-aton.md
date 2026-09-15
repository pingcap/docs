---
title: INET_ATON
summary: 将 IPv4 地址转换为 32 位整数。
---

# INET_ATON

将 IPv4 地址转换为 32 位整数。

## 语法 {#syntax}

```sql
INET_ATON( '<ip>' )
```

## 别名 {#aliases}

- [IPV4_STRING_TO_NUM](/tidb-cloud-lake/sql/ipv4-string-to-num.md)

## 返回类型 {#return-type}

整数型。

## 示例 {#examples}

```sql
SELECT IPV4_STRING_TO_NUM('1.2.3.4'), INET_ATON('1.2.3.4');

┌──────────────────────────────────────────────────────┐
│ ipv4_string_to_num('1.2.3.4') │ inet_aton('1.2.3.4') │
├───────────────────────────────┼──────────────────────┤
│                      16909060 │             16909060 │
└──────────────────────────────────────────────────────┘
```