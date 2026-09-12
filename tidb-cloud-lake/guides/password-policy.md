---
title: 密码策略
summary: 密码策略定义了 {{{ .lake }}} 密码必须有多强（长度、字符、历史记录、重试限制等）以及密码可以多久修改一次。它们为每次 `CREATE USER` 和密码修改提供了可预测的约束。有关完整属性列表，请参见 Password Policy Attributes。
---

# 密码策略

密码策略定义了 {{{ .lake }}} 密码必须有多强（长度、字符、历史记录、重试限制等）以及密码可以多久修改一次。它们为每次 `CREATE USER` 和密码修改提供了可预测的约束。有关完整属性列表，请参见[密码策略属性](/tidb-cloud-lake/sql/create-password-policy.md#password-policy-attributes)。

## 工作原理 {#how-it-works}

- SQL 用户默认没有密码策略。你可以在创建用户时通过 `CREATE USER ... WITH SET PASSWORD POLICY` 指定策略，也可以稍后通过 [ALTER USER](/tidb-cloud-lake/sql/alter-user.md) 指定。
- 每当受管理的用户设置或修改密码时，{{{ .lake }}} 都会验证复杂度规则（长度和字符组合）；对于密码修改，还会强制执行最短使用期限和密码历史记录限制。
- 登录时，{{{ .lake }}} 还会根据 `PASSWORD_MAX_RETRIES`/`PASSWORD_LOCKOUT_TIME_MINS` 跟踪失败尝试次数和锁定状态，并在超过 `PASSWORD_MAX_AGE_DAYS` 后将密码标记为过期。密码已过期的用户只能登录来修改自己的密码。

> **Note:**
>
> 用户通常不能修改自己的密码，除非他们具有内置的 `account-admin` 角色。`account-admin` 可以运行 `ALTER USER ... IDENTIFIED BY ...` 为任何用户轮转密码。

## 端到端示例 {#end-to-end-example}

本示例将为管理员和分析师分别创建专用策略，将其绑定到用户，并展示后续如何修改或移除这些策略。

### 1. 创建策略并查看它们 {#1-create-policies-and-inspect-them}

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

### 2. 将策略绑定到用户 {#2-attach-the-policy-to-users}

```sql
CREATE USER dba_jane IDENTIFIED BY 'Str0ngPass123!' WITH SET PASSWORD POLICY='dba_policy';

CREATE USER analyst_mike IDENTIFIED BY 'Abc12345'
    WITH SET PASSWORD POLICY='analyst_policy';

CREATE USER analyst_zoe IDENTIFIED BY 'Byt3Crush!';
ALTER USER analyst_zoe WITH SET PASSWORD POLICY='analyst_policy';
```

### 3. 验证绑定结果 {#3-verify-the-assignments}

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

### 4. 集中修改策略 {#4-update-a-policy-centrally}

使用 [ALTER PASSWORD POLICY](/tidb-cloud-lake/sql/alter-password-policy.md) 可以在不逐个修改用户的情况下收紧规则：

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

现在，所有引用 `analyst_policy` 的用户都会自动继承更严格的密码字符组合要求和过期时间窗口。

### 5. 解绑并清理 {#5-detach-and-clean-up}

```sql
ALTER USER analyst_zoe WITH UNSET PASSWORD POLICY;
DROP PASSWORD POLICY analyst_policy;
```

{{{ .lake }}} 会阻止你删除仍在使用中的策略；在运行 `DROP PASSWORD POLICY` 之前，请先从所有用户上取消该策略。

---

有关完整语法，请参见[密码策略 SQL 参考](/tidb-cloud-lake/sql/password-policy-sql.md)，其中涵盖了 `CREATE`、`ALTER`、`SHOW`、`DESC` 和 `DROP`。