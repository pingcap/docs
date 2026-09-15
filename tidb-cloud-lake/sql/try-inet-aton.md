---
title: TRY_INET_ATON
summary: try_inet_aton 函数用于接收 IPv4 地址的点分十进制字符串表示，并以整数形式返回给定 IP 地址的数值。
---

# TRY_INET_ATON

try_inet_aton 函数用于接收 IPv4 地址的点分十进制字符串表示，并以整数形式返回给定 IP 地址的数值。

## 语法 {#syntax}

```sql
TRY_INET_ATON( <str> )
```

## 别名 {#aliases}

- [TRY_IPV4_STRING_TO_NUM](/tidb-cloud-lake/sql/try-ipv4-string-to-num.md)

## 返回类型 {#return-type}

整数型。

## 示例 {#examples}

```sql
SELECT TRY_INET_ATON('10.0.5.9'), TRY_IPV4_STRING_TO_NUM('10.0.5.9');

┌────────────────────────────────────────────────────────────────┐
│ try_inet_aton('10.0.5.9') │ try_ipv4_string_to_num('10.0.5.9') │
│           UInt32          │               UInt32               │
├───────────────────────────┼────────────────────────────────────┤
│                 167773449 │                          167773449 │
└────────────────────────────────────────────────────────────────┘
```