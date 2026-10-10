---
title: TRY_INET_ATON
summary: try_inet_aton 関数は、IPv4 アドレスのドット区切り 4 要素表記を文字列として受け取り、指定された IP アドレスの数値を整数形式で返します。
---

# TRY_INET_ATON

try_inet_aton 関数は、IPv4 アドレスのドット区切り 4 要素表記を文字列として受け取り、指定された IP アドレスの数値を整数形式で返します。

## 構文 {#syntax}

```sql
TRY_INET_ATON( <str> )
```

## エイリアス {#aliases}

- [TRY_IPV4_STRING_TO_NUM](/tidb-cloud-lake/sql/try-ipv4-string-to-num.md)

## 戻り値の型 {#return-type}

Integer。

## 例 {#examples}

```sql
SELECT TRY_INET_ATON('10.0.5.9'), TRY_IPV4_STRING_TO_NUM('10.0.5.9');

┌────────────────────────────────────────────────────────────────┐
│ try_inet_aton('10.0.5.9') │ try_ipv4_string_to_num('10.0.5.9') │
│           UInt32          │               UInt32               │
├───────────────────────────┼────────────────────────────────────┤
│                 167773449 │                          167773449 │
└────────────────────────────────────────────────────────────────┘
```