---
title: ALTER NETWORK POLICY
summary: "{{{ .lake }}} 内の既存のネットワークポリシーを変更します。"
---

# ALTER NETWORK POLICY

{{{ .lake }}} 内の既存のネットワークポリシーを変更します。

## 構文 {#syntax}

```sql
ALTER NETWORK POLICY [ IF EXISTS ] <policy_name>
    SET [ ALLOWED_IP_LIST = ('allowed_ip1', 'allowed_ip2', ...) ]
    [ BLOCKED_IP_LIST = ('blocked_ip1', 'blocked_ip2', ...) ]
    [ COMMENT = 'comment' ]
```

| パラメーター     | 説明                                                                                                                                                                                                                                                                    |
|----------------- |----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| policy_name      | 変更するネットワークポリシーの名前を指定します。                                                                                                                                                                                                                         |
| ALLOWED_IP_LIST  | ポリシーに対して更新する、許可された IP アドレス範囲のカンマ区切りリストを指定します。これにより、既存の許可 IP アドレスリストは、指定した新しいリストで上書きされます。                                                                                              |
| BLOCKED_IP_LIST  | ポリシーに対して更新する、ブロックされた IP アドレス範囲のカンマ区切りリストを指定します。これにより、既存のブロック IP アドレスリストは、指定した新しいリストで上書きされます。このパラメーターを空のリスト `()` に設定すると、ブロックされた IP アドレスの制限がすべて削除されます。 |
| COMMENT          | ネットワークポリシーに関連付けられた説明またはコメントを更新するためのオプションのパラメーターです。                                                                                                                                                                   |

> **Note:**
>
> このコマンドでは、許可 IP リストまたはブロック IP リストのいずれか一方を更新し、もう一方のリストは変更せずに維持できます。ALLOWED_IP_LIST と BLOCKED_IP_LIST はどちらもオプションのパラメーターです。

## 例 {#examples}

```sql
-- Modify the network policy test_policy to change the blocked IP address list from ('192.168.1.99') to ('192.168.1.10'):
ALTER NETWORK POLICY test_policy SET BLOCKED_IP_LIST=('192.168.1.10')

-- Update the network policy test_policy to allow IP address ranges ('192.168.10.0', '192.168.20.0') and remove any blocked IP address restrictions. Also, change the comment to 'new comment':

ALTER NETWORK POLICY test_policy SET ALLOWED_IP_LIST=('192.168.10.0', '192.168.20.0') BLOCKED_IP_LIST=() COMMENT='new comment'
```