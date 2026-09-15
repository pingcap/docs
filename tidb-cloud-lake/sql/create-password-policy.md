---
title: CREATE PASSWORD POLICY
summary: 在 {{{ .lake }}} 中创建新的密码策略。
---

# CREATE PASSWORD POLICY

在 {{{ .lake }}} 中创建新的密码策略。

## 语法 {#syntax}

```sql
CREATE [ OR REPLACE ] PASSWORD POLICY [ IF NOT EXISTS ] <policy_name>
    [ PASSWORD_MIN_LENGTH = <number> ]
    [ PASSWORD_MAX_LENGTH = <number> ]
    [ PASSWORD_MIN_UPPER_CASE_CHARS = <number> ]
    [ PASSWORD_MIN_LOWER_CASE_CHARS = <number> ]
    [ PASSWORD_MIN_NUMERIC_CHARS = <number> ]
    [ PASSWORD_MIN_SPECIAL_CHARS = <number> ]
    [ PASSWORD_MIN_AGE_DAYS = <number> ]
    [ PASSWORD_MAX_AGE_DAYS = <number> ]
    [ PASSWORD_MAX_RETRIES = <number> ]
    [ PASSWORD_LOCKOUT_TIME_MINS = <number> ]
    [ PASSWORD_HISTORY = <number> ]
    [ COMMENT = '<comment>' ]
```

### 密码策略属性 {#password-policy-attributes}

下表汇总了密码策略的关键参数，涵盖长度、字符要求、有效期限制、重试次数限制、锁定时长以及密码历史等方面：

| 属性                          | 最小值 | 最大值 | 默认值 | 描述                                                                                 |
|-------------------------------|-----|-----|---------|--------------------------------------------------------------------------------------|
| PASSWORD_MIN_LENGTH           | 8   | 256 | 8       | 密码的最小长度                                                                       |
| PASSWORD_MAX_LENGTH           | 8   | 256 | 256     | 密码的最大长度                                                                       |
| PASSWORD_MIN_UPPER_CASE_CHARS | 0   | 256 | 1       | 密码中大写字符的最小数量                                                             |
| PASSWORD_MIN_LOWER_CASE_CHARS | 0   | 256 | 1       | 密码中小写字符的最小数量                                                             |
| PASSWORD_MIN_NUMERIC_CHARS    | 0   | 256 | 1       | 密码中数字字符的最小数量                                                             |
| PASSWORD_MIN_SPECIAL_CHARS    | 0   | 256 | 0       | 密码中特殊字符的最小数量                                                             |
| PASSWORD_MIN_AGE_DAYS         | 0   | 999 | 0       | 密码可被修改前所需的最少天数（0 表示无限制）                                         |
| PASSWORD_MAX_AGE_DAYS         | 0   | 999 | 90      | 密码必须修改前允许的最长天数（0 表示无限制）                                         |
| PASSWORD_MAX_RETRIES          | 1   | 10  | 5       | 触发锁定前允许的最大密码重试次数                                                     |
| PASSWORD_LOCKOUT_TIME_MINS    | 1   | 999 | 15      | 超过重试次数后锁定的持续时间，单位为分钟                                             |
| PASSWORD_HISTORY              | 0   | 24  | 0       | 用于检查是否重复的最近密码数量（0 表示无限制）                                       |

## 示例 {#examples}

以下示例创建了一个名为 `SecureLogin` 的密码策略，并将密码最小长度要求设置为 10 个字符：

```sql
CREATE PASSWORD POLICY SecureLogin
    PASSWORD_MIN_LENGTH = 10;
```