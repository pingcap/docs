---
title: INET_NTOA
summary: 32 ビット整数を IPv4 アドレスに変換します。
---

# INET_NTOA

32 ビット整数を IPv4 アドレスに変換します。

## 構文 {#syntax}

```sql
INET_NOTA( <int32> )
```

## エイリアス {#aliases}

- [IPV4_NUM_TO_STRING](/tidb-cloud-lake/sql/ipv4-num-to-string.md)

## 戻り値の型 {#return-type}

String。

## 例 {#examples}

```sql
SELECT IPV4_NUM_TO_STRING(16909060), INET_NTOA(16909060);

┌────────────────────────────────────────────────────┐
│ ipv4_num_to_string(16909060) │ inet_ntoa(16909060) │
├──────────────────────────────┼─────────────────────┤
│ 1.2.3.4                      │ 1.2.3.4             │
└────────────────────────────────────────────────────┘
```