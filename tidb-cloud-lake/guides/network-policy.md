---
title: ネットワークポリシー
summary: ネットワークポリシーは、クライアント IP に基づいて {{{ .lake }}} にログインできるユーザーを制御します。認証情報が正しくても、IP がポリシーを満たさない場合は接続要求が拒否されるため、ユーザー名とパスワードに加えて追加のセキュリティレイヤーを提供します。
---

# ネットワークポリシー

ネットワークポリシーは、クライアント IP に基づいて {{{ .lake }}} にログインできるユーザーを制御します。認証情報が正しくても、IP がポリシーを満たさない場合は接続要求が拒否されるため、ユーザー名とパスワードに加えて追加のセキュリティレイヤーを提供します。

## 仕組み {#how-it-works}

- `ALLOWED_IP_LIST` には、単一の IPv4 アドレスまたは `10.0.0.0/24` のような CIDR ブロックを指定できます。リスト内のアドレスのみがログインを許可されます。
- `BLOCKED_IP_LIST`（任意）を使用すると、許可された範囲の中から明示的な拒否ルールを切り出して定義できます。{{{ .lake }}} は最初に blocked list を確認するため、両方のリストに存在する IP は拒否されます。
- 1 人のユーザーが同時に参照できるネットワークポリシーは最大 1 つですが、同じポリシーを複数のユーザーで共有できるため、管理が容易になります。
- サーバーがクライアント IP を判定できない場合、または IP が allowed list に一致しない場合、{{{ .lake }}} は直ちに `AuthenticateFailure` を返します。

## エンドツーエンドの例 {#end-to-end-example}

以下の手順では、一般的なライフサイクルを説明します。ポリシーを作成し、ユーザーに関連付け、状態を確認し、一元的に更新し、最後に関連付けを解除して削除します。

### 1. ポリシーを作成して確認する {#1-create-and-inspect-a-policy}

```sql
CREATE NETWORK POLICY corp_vpn_policy
    ALLOWED_IP_LIST=('10.1.0.0/16', '172.16.8.12/32')
    BLOCKED_IP_LIST=('10.1.10.25')
    COMMENT='Only VPN ranges';

SHOW NETWORK POLICIES;

Name            |Allowed Ip List           |Blocked Ip List|Comment          |
----------------+--------------------------+---------------+-----------------+
corp_vpn_policy |10.1.0.0/16,172.16.8.12/32|10.1.10.25     |Only VPN ranges  |
```

### 2. ユーザーにポリシーを関連付ける {#2-attach-the-policy-to-users}

```sql
CREATE USER alice IDENTIFIED BY 'Str0ngPass!' WITH SET NETWORK POLICY='corp_vpn_policy';
CREATE USER bob IDENTIFIED BY 'An0therPass!';

-- Apply the policy to an existing user
ALTER USER bob WITH SET NETWORK POLICY='corp_vpn_policy';
```

### 3. 適用を確認する {#3-verify-enforcement}

```sql
DESC USER alice;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  name  │ hostname │       auth_type      │ default_role │ roles │ disabled │   network_policy  │ password_policy │ must_change_password │
├────────┼──────────┼──────────────────────┼──────────────┼───────┼──────────┼───────────────────┼─────────────────┼──────────────────────┤
│ alice  │ %        │ double_sha1_password │              │       │ false    │ corp_vpn_policy   │                 │ NULL                 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

DESC NETWORK POLICY corp_vpn_policy;

Name            |Allowed Ip List           |Blocked Ip List|Comment         |
----------------+--------------------------+---------------+----------------+
corp_vpn_policy |10.1.0.0/16,172.16.8.12/32|10.1.10.25     |Only VPN ranges |
```

### 4. ポリシーを更新して再利用する {#4-update-and-reuse-the-policy}

各ユーザーに手を加えることなく、許可または拒否する IP を調整するには、[ALTER NETWORK POLICY](/tidb-cloud-lake/sql/network-policy-sql.md) を使用します。

```sql
ALTER NETWORK POLICY corp_vpn_policy
    SET ALLOWED_IP_LIST=('10.1.0.0/16', '10.2.0.0/16')
        BLOCKED_IP_LIST=('10.1.10.25', '10.2.5.5')
        COMMENT='VPN + DR site';

DESC NETWORK POLICY corp_vpn_policy;

Name            |Allowed Ip List             |Blocked Ip List          |Comment          |
----------------+----------------------------+-------------------------+-----------------+
corp_vpn_policy |10.1.0.0/16,10.2.0.0/16     |10.1.10.25,10.2.5.5      |VPN + DR site    |
```

このポリシーを参照しているすべてのユーザーに、新しい IP 範囲が自動的に適用されます。

### 5. 関連付けを解除してクリーンアップする {#5-detach-and-clean-up}

```sql
ALTER USER bob WITH UNSET NETWORK POLICY;
DROP NETWORK POLICY corp_vpn_policy;
```

ポリシーを削除する前に、そのポリシーに依存しているユーザーがいないことを確認してください。そうしないと、それらのユーザーはログインに失敗します。

---

完全な構文の詳細については、[Network Policy SQL reference](/tidb-cloud-lake/sql/network-policy-sql.md) を参照してください。`CREATE`、`ALTER`、`SHOW`、`DESC`、`DROP` を扱っています。