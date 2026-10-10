---
title: IP Address Functions
summary: このページでは、{{{ .lake }}} における IP アドレス関連の関数のリファレンス情報を提供します。これらの関数は、IP アドレスの文字列表現と数値表現の相互変換に役立ちます。
---

# IP Address Functions

このページでは、{{{ .lake }}} における IP アドレス関連の関数のリファレンス情報を提供します。これらの関数は、IP アドレスの文字列表現と数値表現の相互変換に役立ちます。

## IP アドレス変換関数 {#ip-address-conversion-functions}

| Function | 説明 | 例 |
|----------|-------------|--------|
| [INET_ATON](/tidb-cloud-lake/sql/inet-aton.md) / [IPV4_STRING_TO_NUM](/tidb-cloud-lake/sql/ipv4-string-to-num.md) | IPv4 アドレス文字列を 32 ビット整数に変換します | `INET_ATON('192.168.1.1')` → `3232235777` |
| [INET_NTOA](/tidb-cloud-lake/sql/inet-ntoa.md) / [IPV4_NUM_TO_STRING](/tidb-cloud-lake/sql/ipv4-num-to-string.md) | 32 ビット整数を IPv4 アドレス文字列に変換します | `INET_NTOA(3232235777)` → `'192.168.1.1'` |

## 安全な IP アドレス変換関数 {#safe-ip-address-conversion-functions}

これらの関数は、不正な入力に対してエラーを発生させる代わりに NULL を返すことで、安全に処理します。

| Function | 説明 | 例 |
|----------|-------------|--------|
| [TRY_INET_ATON](/tidb-cloud-lake/sql/try-inet-aton.md) / [TRY_IPV4_STRING_TO_NUM](/tidb-cloud-lake/sql/try-ipv4-string-to-num.md) | IPv4 アドレス文字列を安全に 32 ビット整数に変換します | `TRY_INET_ATON('invalid')` → `NULL` |
| [TRY_INET_NTOA](/tidb-cloud-lake/sql/try-inet-ntoa.md) / [TRY_IPV4_NUM_TO_STRING](/tidb-cloud-lake/sql/try-ipv4-num-to-string.md) | 32 ビット整数を安全に IPv4 アドレス文字列に変換します | `TRY_INET_NTOA(-1)` → `NULL` |