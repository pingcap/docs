---
title: TRY_INET_NTOA
summary: ネットワークバイトオーダーの IPv4 アドレスを受け取り、ドット区切り 4 要素の文字列表現として返します。
---

# TRY_INET_NTOA

ネットワークバイトオーダーの IPv4 アドレスを受け取り、ドット区切り 4 要素の文字列表現として返します。

## 構文 {#syntax}

```sql
TRY_INET_NTOA( <integer> )
```

## エイリアス {#aliases}

- [TRY_IPV4_NUM_TO_STRING](/tidb-cloud-lake/sql/try-ipv4-num-to-string.md)

## 戻り値の型 {#return-type}

String。

## 例 {#examples}

```sql
SELECT TRY_INET_NTOA(167773449), TRY_IPV4_NUM_TO_STRING(167773449);

┌──────────────────────────────────────────────────────────────┐
│ try_inet_ntoa(167773449) │ try_ipv4_num_to_string(167773449) │
├──────────────────────────┼───────────────────────────────────┤
│ 10.0.5.9                 │ 10.0.5.9                          │
└──────────────────────────────────────────────────────────────┘
```