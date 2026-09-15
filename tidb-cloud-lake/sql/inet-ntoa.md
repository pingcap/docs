---
title: INET_NTOA
summary: 将 32 位整数转换为 IPv4 地址。
---

# INET_NTOA

将 32 位整数转换为 IPv4 地址。

## 语法 {#syntax}

```sql
INET_NOTA( <int32> )
```

## 别名 {#aliases}

- [IPV4_NUM_TO_STRING](/tidb-cloud-lake/sql/ipv4-num-to-string.md)

## 返回类型 {#return-type}

字符串。

## 示例 {#examples}

```sql
SELECT IPV4_NUM_TO_STRING(16909060), INET_NTOA(16909060);

┌────────────────────────────────────────────────────┐
│ ipv4_num_to_string(16909060) │ inet_ntoa(16909060) │
├──────────────────────────────┼─────────────────────┤
│ 1.2.3.4                      │ 1.2.3.4             │
└────────────────────────────────────────────────────┘
```