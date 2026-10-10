---
title: DESC MASKING POLICY
summary: "{{{ .lake }}} 内の特定のマスキングポリシーの詳細情報を表示します。"
---

# DESC MASKING POLICY

{{{ .lake }}} 内の特定のマスキングポリシーの詳細情報を表示します。

## 構文 {#syntax}

```sql
DESC MASKING POLICY <policy_name>
```

## アクセス制御の要件 {#access-control-requirements}

| Privilege | 説明 |
|:----------|:------------|
| APPLY MASKING POLICY | そのポリシーの所有者でない限り、マスキングポリシーの詳細を表示するには必要です。 |

この要件は、グローバルな `APPLY MASKING POLICY` 権限、または特定のマスキングポリシーに対する APPLY/OWNERSHIP のいずれかで満たされます。

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

DESC MASKING POLICY email_mask;

Name       |Value                                                                |
-----------+---------------------------------------------------------------------+
Name       |email_mask                                                           |
Created On |2023-08-09 02:29:16.177898 UTC                                       |
Signature  |(val STRING)                                                         |
Return Type|STRING                                                               |
Body       |CASE WHEN current_role() IN('MANAGERS') THEN VAL ELSE '*********' END|
Comment    |hide_email                                                           |
```