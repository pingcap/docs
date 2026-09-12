---
title: IP Address Functions
summary: 本页提供 {{{ .lake }}} 中与 IP 地址相关的函数参考信息。这些函数可帮助在 IP 地址的字符串表示和数值表示之间进行转换。
---

# IP Address Functions

本页提供 {{{ .lake }}} 中与 IP 地址相关的函数参考信息。这些函数可帮助在 IP 地址的字符串表示和数值表示之间进行转换。

## IP 地址转换函数 {#ip-address-conversion-functions}

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [INET_ATON](/tidb-cloud-lake/sql/inet-aton.md) / [IPV4_STRING_TO_NUM](/tidb-cloud-lake/sql/ipv4-string-to-num.md) | 将 IPv4 地址字符串转换为 32 位整数型 | `INET_ATON('192.168.1.1')` → `3232235777` |
| [INET_NTOA](/tidb-cloud-lake/sql/inet-ntoa.md) / [IPV4_NUM_TO_STRING](/tidb-cloud-lake/sql/ipv4-num-to-string.md) | 将 32 位整数型转换为 IPv4 地址字符串 | `INET_NTOA(3232235777)` → `'192.168.1.1'` |

## 安全的 IP 地址转换函数 {#safe-ip-address-conversion-functions}

这些函数会以优雅的方式处理无效输入，即返回 NULL 而不是报错。

| 函数 | 描述 | 示例 |
|----------|-------------|--------|
| [TRY_INET_ATON](/tidb-cloud-lake/sql/try-inet-aton.md) / [TRY_IPV4_STRING_TO_NUM](/tidb-cloud-lake/sql/try-ipv4-string-to-num.md) | 安全地将 IPv4 地址字符串转换为 32 位整数型 | `TRY_INET_ATON('invalid')` → `NULL` |
| [TRY_INET_NTOA](/tidb-cloud-lake/sql/try-inet-ntoa.md) / [TRY_IPV4_NUM_TO_STRING](/tidb-cloud-lake/sql/try-ipv4-num-to-string.md) | 安全地将 32 位整数型转换为 IPv4 地址字符串 | `TRY_INET_NTOA(-1)` → `NULL` |