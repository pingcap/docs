---
title: DROP MASKING POLICY
summary: "{{{ .lake }}} から既存の masking policy を削除します。masking policy を削除すると、その policy は {{{ .lake }}} から削除され、関連付けられている masking ルールは効力を失います。masking policy を削除する前に、その policy がどのカラムにも関連付けられていないことを確認してください。"
---

# DROP MASKING POLICY

{{{ .lake }}} から既存の masking policy を削除します。masking policy を削除すると、その policy は {{{ .lake }}} から削除され、関連付けられている masking ルールは効力を失います。masking policy を削除する前に、その policy がどのカラムにも関連付けられていないことを確認してください。

## 構文 {#syntax}

```sql
DROP MASKING POLICY [ IF EXISTS ] <policy_name>
```

## アクセス制御の要件 {#access-control-requirements}

| Privilege | 説明 |
|:----------|:------------|
| APPLY MASKING POLICY | その policy の所有者でない限り、masking policy を削除するには必要です。 |

グローバルな `APPLY MASKING POLICY` 権限、または対象 policy に対する APPLY/OWNERSHIP が必要です。policy が削除されると、{{{ .lake }}} は作成者ロールから OWNERSHIP を自動的に取り消します。

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