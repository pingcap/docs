---
title: SHOW NETWORK POLICIES
summary: "{{{ .lake }}} に存在するすべてのネットワークポリシーの一覧を表示します。利用可能なネットワークポリシーについて、名前や、許可またはブロックされた IP アドレスリストが設定されているかどうかなどの情報を提供します。"
---

# SHOW NETWORK POLICIES

{{{ .lake }}} に存在するすべてのネットワークポリシーの一覧を表示します。利用可能なネットワークポリシーについて、名前や、許可またはブロックされた IP アドレスリストが設定されているかどうかなどの情報を提供します。

## 構文 {#syntax}

```sql
SHOW NETWORK POLICIES
```

## 例 {#examples}

```sql
SHOW NETWORK POLICIES;

Name        |Allowed Ip List |Blocked Ip List|Comment     |
------------+----------------+---------------+------------+
test_policy |192.168.1.0/24  |192.168.1.99   |test comment|
test_policy1|192.168.100.0/24|               |            |
```