---
title: DROP MASKING POLICY
summary: "{{{ .lake }}} から既存のマスキングポリシーを削除します。マスキングポリシーを削除すると、そのポリシーは {{{ .lake }}} から削除され、関連付けられているマスキングルールは効力を失います。マスキングポリシーを削除する前に、そのポリシーがどのカラムにも関連付けられていないことを確認してください。"
---

# DROP MASKING POLICY

{{{ .lake }}} から既存のマスキングポリシーを削除します。マスキングポリシーを削除すると、そのポリシーは {{{ .lake }}} から削除され、関連付けられているマスキングルールは効力を失います。マスキングポリシーを削除する前に、そのポリシーがどのカラムにも関連付けられていないことを確認してください。

## 構文 {#syntax}

```sql
DROP MASKING POLICY [ IF EXISTS ] <policy_name>
```

## アクセス制御の要件 {#access-control-requirements}

| 権限 | 説明 |
|:----------|:------------|
| APPLY MASKING POLICY | そのポリシーの所有者でない限り、マスキングポリシーを削除するには必要です。 |

グローバルな `APPLY MASKING POLICY` 権限、または対象ポリシーに対する APPLY/OWNERSHIP が必要です。ポリシーが削除されると、{{{ .lake }}} は作成者ロールから OWNERSHIP を自動的に取り消します。

## 例 {#examples}

```sql
CREATE MASKING POLICY email_mask
AS
  (val string)
  RETURNS string ->
  CASE
  WHEN current_role() IN ('MANAGERS') THEN
    val
  ELSE
    '*********'
  END
  COMMENT = 'hide_email';

DROP MASKING POLICY email_mask;
```