---
title: パスワードポリシー
summary: パスワードポリシーは、{{{ .lake }}} のパスワードにどの程度の強度を求めるか（長さ、文字種、履歴、再試行回数の上限など）と、どのくらいの頻度で変更できるかを定義します。これにより、すべての CREATE USER とパスワード変更に対して一貫したガードレールを設けられます。属性の完全な一覧については、Password Policy Attributes を参照してください。
---

# パスワードポリシー

パスワードポリシーは、{{{ .lake }}} のパスワードにどの程度の強度を求めるか（長さ、文字種、履歴、再試行回数の上限など）と、どのくらいの頻度で変更できるかを定義します。これにより、すべての `CREATE USER` とパスワード変更に対して一貫したガードレールを設けられます。属性の完全な一覧については、[パスワードポリシー属性](/tidb-cloud-lake/sql/create-password-policy.md#password-policy-attributes) を参照してください。

## 仕組み {#how-it-works}

- SQL ユーザーは、初期状態ではパスワードポリシーが設定されていません。ユーザー作成時に `CREATE USER ... WITH SET PASSWORD POLICY` で割り当てるか、後から [ALTER USER](/tidb-cloud-lake/sql/alter-user.md) を使って割り当てます。
- 管理対象ユーザーがパスワードを設定または変更するたびに、{{{ .lake }}} は複雑性ルール（長さと文字種の組み合わせ）を検証し、パスワード変更時には最小経過日数とパスワード履歴も適用します。
- ログイン時には、{{{ .lake }}} は `PASSWORD_MAX_RETRIES` / `PASSWORD_LOCKOUT_TIME_MINS` に基づいて失敗試行回数とロックアウトも追跡し、`PASSWORD_MAX_AGE_DAYS` 経過後のパスワードを期限切れとして扱います。期限切れになったユーザーは、パスワードを変更するためにのみログインできます。

> **Note:**
>
> ユーザーは通常、組み込みの `account-admin` ロールを持っていない限り、自分自身のパスワードを変更できません。`account-admin` は `ALTER USER ... IDENTIFIED BY ...` を実行して、任意のユーザーのパスワードをローテーションできます。

## エンドツーエンドの例 {#end-to-end-example}

この手順では、管理者用とアナリスト用の専用ポリシーを作成し、それらをユーザーに関連付け、後で更新または削除する方法を示します。

### 1. ポリシーを作成して確認する {#1-create-policies-and-inspect-them}

```sql
CREATE PASSWORD POLICY dba_policy
    PASSWORD_MIN_LENGTH = 12
    PASSWORD_MAX_LENGTH = 18
    PASSWORD_MIN_UPPER_CASE_CHARS = 2
    PASSWORD_MIN_LOWER_CASE_CHARS = 2
    PASSWORD_MIN_NUMERIC_CHARS = 2
    PASSWORD_MIN_SPECIAL_CHARS = 1
    PASSWORD_MIN_AGE_DAYS = 1
    PASSWORD_MAX_AGE_DAYS = 45
    PASSWORD_MAX_RETRIES = 3
    PASSWORD_LOCKOUT_TIME_MINS = 30
    PASSWORD_HISTORY = 5
    COMMENT='Strict controls for DBAs';

CREATE PASSWORD POLICY analyst_policy
    COMMENT='Defaults for analysts';

SHOW PASSWORD POLICIES;

┌─────────────────┬───────────────────────────────┬─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ name            │ comment                       │ options                                                                                                                             │
├─────────────────┼───────────────────────────────┼─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┤
│ analyst_policy  │ Defaults for analysts         │ MIN_LENGTH=8, MAX_LENGTH=256, MIN_UPPER_CASE_CHARS=1, MIN_LOWER_CASE_CHARS=1, MIN_NUMERIC_CHARS=1, MIN_SPECIAL_CHARS=0, ... HISTORY=0        │
│ dba_policy      │ Strict controls for DBAs      │ MIN_LENGTH=12, MAX_LENGTH=18, MIN_UPPER_CASE_CHARS=2, MIN_LOWER_CASE_CHARS=2, MIN_NUMERIC_CHARS=2, MIN_SPECIAL_CHARS=1, ... HISTORY=5       │
└─────────────────┴───────────────────────────────┴─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

### 2. ユーザーにポリシーを関連付ける {#2-attach-the-policy-to-users}

```sql
CREATE USER dba_jane IDENTIFIED BY 'Str0ngPass123!' WITH SET PASSWORD POLICY='dba_policy';

CREATE USER analyst_mike IDENTIFIED BY 'Abc12345'
    WITH SET PASSWORD POLICY='analyst_policy';

CREATE USER analyst_zoe IDENTIFIED BY 'Byt3Crush!';
ALTER USER analyst_zoe WITH SET PASSWORD POLICY='analyst_policy';
```

### 3. 割り当てを確認する {#3-verify-the-assignments}

```sql
DESC USER dba_jane;

┌──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┐
│  name   │ hostname │       auth_type      │ default_role │ roles │ disabled │ network_policy │ password_policy │ must_change_password │
├─────────┼──────────┼──────────────────────┼──────────────┼───────┼──────────┼────────────────┼─────────────────┼──────────────────────┤
│ dba_jane│ %        │ double_sha1_password │              │       │ false    │                │ dba_policy      │ NULL                 │
└──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────┘

DESC PASSWORD POLICY dba_policy;

Name       |Comment                     |Options
-----------+----------------------------+---------------------------------------------------------------------------------------------------------------------------------+
dba_policy |Strict controls for DBAs    |MIN_LENGTH=12,MAX_LENGTH=18,MIN_UPPER_CASE_CHARS=2,MIN_LOWER_CASE_CHARS=2,MIN_NUMERIC_CHARS=2,MIN_SPECIAL_CHARS=1,...,HISTORY=5   |
```

### 4. ポリシーを一元的に更新する {#4-update-a-policy-centrally}

各ユーザーに個別に手を加えることなくルールを厳格化するには、[ALTER PASSWORD POLICY](/tidb-cloud-lake/sql/alter-password-policy.md) を使用します。

```sql
ALTER PASSWORD POLICY analyst_policy SET
    PASSWORD_MIN_SPECIAL_CHARS = 1
    PASSWORD_MAX_AGE_DAYS = 60
    COMMENT='Analysts need specials now';

DESC PASSWORD POLICY analyst_policy;

Name           |Comment                      |Options
---------------+-----------------------------+------------------------------------------------------------------------------------------------------------------------+
analyst_policy |Analysts need specials now   |MIN_LENGTH=8,MAX_LENGTH=256,MIN_UPPER_CASE_CHARS=1,MIN_LOWER_CASE_CHARS=1,MIN_NUMERIC_CHARS=1,MIN_SPECIAL_CHARS=1,...    |
```

`analyst_policy` を参照しているすべてのユーザーは、より厳格になった文字種要件と有効期限の設定を自動的に継承します。

### 5. 関連付けを解除してクリーンアップする {#5-detach-and-clean-up}

```sql
ALTER USER analyst_zoe WITH UNSET PASSWORD POLICY;
DROP PASSWORD POLICY analyst_policy;
```

{{{ .lake }}} では、まだ使用中のポリシーは削除できません。`DROP PASSWORD POLICY` を実行する前に、すべてのユーザーからそのポリシーを解除してください。

---

完全な構文については、[Password Policy SQL reference](/tidb-cloud-lake/sql/password-policy-sql.md) を参照してください。`CREATE`、`ALTER`、`SHOW`、`DESC`、`DROP` を扱っています。