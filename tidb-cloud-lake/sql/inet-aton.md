---
title: INET_ATON
summary: IPv4 アドレスを 32 ビット整数に変換します。
---

# INET_ATON

IPv4 アドレスを 32 ビット整数に変換します。

## 構文 {#syntax}

```sql
INET_ATON( '<ip>' )
```

## エイリアス {#aliases}

- [IPV4_STRING_TO_NUM](/tidb-cloud-lake/sql/ipv4-string-to-num.md)

## 戻り値の型 {#return-type}

整数。

## 例 {#examples}

```sql
SELECT IPV4_STRING_TO_NUM('1.2.3.4'), INET_ATON('1.2.3.4');

┌──────────────────────────────────────────────────────┐
│ ipv4_string_to_num('1.2.3.4') │ inet_aton('1.2.3.4') │
├───────────────────────────────┼──────────────────────┤
│                      16909060 │             16909060 │
└──────────────────────────────────────────────────────┘
```