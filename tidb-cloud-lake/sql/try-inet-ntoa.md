---
title: TRY_INET_NTOA
summary: 接受一个采用网络字节序的 IPv4 地址，然后返回该地址的点分十进制字符串表示。
---

# TRY_INET_NTOA

接受一个采用网络字节序的 IPv4 地址，然后返回该地址的点分十进制字符串表示。

## 语法 {#syntax}

```sql
TRY_INET_NTOA( <integer> )
```

## 别名 {#aliases}

- [TRY_IPV4_NUM_TO_STRING](/tidb-cloud-lake/sql/try-ipv4-num-to-string.md)

## 返回类型 {#return-type}

字符串。

## 示例 {#examples}

```sql
SELECT TRY_INET_NTOA(167773449), TRY_IPV4_NUM_TO_STRING(167773449);

┌──────────────────────────────────────────────────────────────┐
│ try_inet_ntoa(167773449) │ try_ipv4_num_to_string(167773449) │
├──────────────────────────┼───────────────────────────────────┤
│ 10.0.5.9                 │ 10.0.5.9                          │
└──────────────────────────────────────────────────────────────┘
```