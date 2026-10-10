---
title: CREATE PASSWORD POLICY
summary: {{{ .lake }}} に新しいパスワードポリシーを作成します。
---

# CREATE PASSWORD POLICY

{{{ .lake }}} に新しいパスワードポリシーを作成します。

## 構文 {#syntax}

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

### パスワードポリシー属性 {#password-policy-attributes}

この表は、長さ、文字要件、有効期間の制限、再試行回数の上限、ロックアウト時間、およびパスワード履歴など、パスワードポリシーの主要なパラメータをまとめたものです。

| 属性                          | Min | Max | Default | 説明                                                                                 |
|-------------------------------|-----|-----|---------|--------------------------------------------------------------------------------------|
| PASSWORD_MIN_LENGTH           | 8   | 256 | 8       | パスワードの最小長                                                                    |
| PASSWORD_MAX_LENGTH           | 8   | 256 | 256     | パスワードの最大長                                                                    |
| PASSWORD_MIN_UPPER_CASE_CHARS | 0   | 256 | 1       | パスワードに含める大文字の最小数                                                      |
| PASSWORD_MIN_LOWER_CASE_CHARS | 0   | 256 | 1       | パスワードに含める小文字の最小数                                                      |
| PASSWORD_MIN_NUMERIC_CHARS    | 0   | 256 | 1       | パスワードに含める数字の最小数                                                        |
| PASSWORD_MIN_SPECIAL_CHARS    | 0   | 256 | 0       | パスワードに含める特殊文字の最小数                                                    |
| PASSWORD_MIN_AGE_DAYS         | 0   | 999 | 0       | パスワードを変更可能になるまでの最小日数（0 は制限なしを示します）                    |
| PASSWORD_MAX_AGE_DAYS         | 0   | 999 | 90      | パスワードを変更しなければならないまでの最大日数（0 は制限なしを示します）            |
| PASSWORD_MAX_RETRIES          | 1   | 10  | 5       | ロックアウトされるまでのパスワード再試行回数の上限                                    |
| PASSWORD_LOCKOUT_TIME_MINS    | 1   | 999 | 15      | 再試行回数の上限を超えた後のロックアウト時間（分）                                    |
| PASSWORD_HISTORY              | 0   | 24  | 0       | 重複チェック対象とする直近のパスワード数（0 は制限なしを示します）                    |

## 例 {#examples}

次の例では、最小パスワード長を 10 文字に設定した `SecureLogin` という名前のパスワードポリシーを作成します。

```sql
CREATE PASSWORD POLICY SecureLogin
    PASSWORD_MIN_LENGTH = 10;
```