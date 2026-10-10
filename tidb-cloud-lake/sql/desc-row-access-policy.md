---
title: DESC ROW ACCESS POLICY
summary: "{{{ .lake }}} 内の特定の行アクセスポリシーに関する詳細情報を表示します。"
---

# DESC ROW ACCESS POLICY

{{{ .lake }}} 内の特定の行アクセスポリシーに関する詳細情報を表示します。

## 構文 {#syntax}

```sql
DESC ROW ACCESS POLICY <policy_name>
```

`DESCRIBE ROW ACCESS POLICY` もサポートされています。

## アクセス制御の要件 {#access-control-requirements}

| 権限 | 説明 |
|:----------|:------------|
| APPLY ROW ACCESS POLICY | そのポリシーの所有者でない限り、行アクセスポリシーを記述するにはこの権限が必要です。 |

グローバルな `APPLY ROW ACCESS POLICY` 権限、または特定の行アクセスポリシーに対する APPLY/OWNERSHIP のいずれかがあれば、この要件を満たします。

## 例 {#examples}

```sql
SET enable_experimental_row_access_policy = 1;

CREATE ROW ACCESS POLICY rap_engineering
AS (dept STRING)
RETURNS BOOLEAN ->
  CASE
    WHEN current_role() = 'admin' THEN true
    WHEN dept = 'Engineering' THEN true
    ELSE false
  END
  COMMENT = 'show engineering rows';

DESC ROW ACCESS POLICY rap_engineering;

Name            | Created On                  | Signature     | Return Type | Body                                                       | Comment
----------------+-----------------------------+---------------+-------------+------------------------------------------------------------+----------------------
rap_engineering | 2026-05-15 08:42:10.949 UTC | (dept STRING) | BOOLEAN     | CASE WHEN current_role() = 'admin' THEN true WHEN...       | show engineering rows
```