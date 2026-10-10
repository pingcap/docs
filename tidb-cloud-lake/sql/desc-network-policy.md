---
title: DESC NETWORK POLICY
summary: {{{ .lake }}} 内の特定のネットワークポリシーに関する詳細情報を表示します。ポリシーに関連付けられた許可済みおよびブロック済みの IP アドレスリスト、ならびにポリシーの目的や機能を説明するコメント（存在する場合）を確認できます。
---

# DESC NETWORK POLICY

{{{ .lake }}} 内の特定のネットワークポリシーに関する詳細情報を表示します。ポリシーに関連付けられた許可済みおよびブロック済みの IP アドレスリスト、ならびにポリシーの目的や機能を説明するコメント（存在する場合）を確認できます。

## 構文 {#syntax}

```sql
DESC NETWORK POLICY <policy_name>
```

## 例 {#examples}

```sql
DESC NETWORK POLICY test_policy;

Name       |Allowed Ip List          |Blocked Ip List|Comment    |
-----------+-------------------------+---------------+-----------+
test_policy|192.168.10.0,192.168.20.0|               |new comment|
```