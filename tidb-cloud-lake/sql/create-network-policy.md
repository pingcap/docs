---
title: CREATE NETWORK POLICY
summary: "{{{ .lake }}} で新しいネットワークポリシーを作成します。"
---

# CREATE NETWORK POLICY

{{{ .lake }}} で新しいネットワークポリシーを作成します。

## 構文 {#syntax}

```sql
CREATE [ OR REPLACE ] NETWORK POLICY [ IF NOT EXISTS ] <policy_name>
    ALLOWED_IP_LIST = ( 'allowed_ip1', 'allowed_ip2', ... )
    [ BLOCKED_IP_LIST = ( 'blocked_ip1', 'blocked_ip2', ...) ]
    [ COMMENT = 'comment' ]
```

| パラメータ        | 説明                                                                                                                                                                                       |
|----------------- |-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| policy_name      | 作成するネットワークポリシーの名前を指定します。                                                                                                                                           |
| ALLOWED_IP_LIST  | ポリシーで許可する IP アドレス範囲のカンマ区切りリストを指定します。このポリシーに関連付けられたユーザーは、指定された IP 範囲を使用してネットワークにアクセスできます。                     |
| BLOCKED_IP_LIST  | ポリシーでブロックする IP アドレス範囲のカンマ区切りリストを指定します。このポリシーに関連付けられたユーザーは ALLOWED_IP_LIST から引き続きネットワークにアクセスできますが、BLOCKED_IP_LIST で指定された IP はアクセスが制限されます。  |
| COMMENT          | ネットワークポリシーの説明またはコメントを追加するためのオプションのパラメーターです。                                                                                                                |

## 例 {#examples}

この例では、許可する IP アドレスとブロックする IP アドレスを指定してネットワークポリシーを作成し、その後このポリシーをユーザーに関連付けてネットワークアクセスを制御する方法を示します。このネットワークポリシーでは、192.168.1.0 から 192.168.1.255 までのすべての IP アドレスを許可しますが、特定の IP アドレス 192.168.1.99 は除外されます。

```sql
-- Create a network policy
CREATE NETWORK POLICY sample_policy
    ALLOWED_IP_LIST=('192.168.1.0/24')
    BLOCKED_IP_LIST=('192.168.1.99')
    COMMENT='Sample';

SHOW NETWORK POLICIES;

Name         |Allowed Ip List          |Blocked Ip List|Comment    |
-------------+-------------------------+---------------+-----------+
sample_policy|192.168.1.0/24           |192.168.1.99   |Sample     |

-- Create a user
CREATE USER sample_user IDENTIFIED BY 'datalake';

-- Associate the network policy with the user
ALTER USER sample_user WITH SET NETWORK POLICY='sample_policy';
```