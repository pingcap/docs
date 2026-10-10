---
title: DROP ROW ACCESS POLICY
summary: "{{{ .lake }}} から既存の行アクセス ポリシーを削除します。ポリシーを削除する前に、そのポリシーを参照しているすべてのテーブルからデタッチしてください。"
---

# DROP ROW ACCESS POLICY

{{{ .lake }}} から既存の行アクセス ポリシーを削除します。ポリシーを削除する前に、そのポリシーを参照しているすべてのテーブルからデタッチしてください。

## 構文 {#syntax}

```sql
DROP ROW ACCESS POLICY [ IF EXISTS ] <policy_name>
```

## アクセス制御の要件 {#access-control-requirements}

| 権限 | 説明 |
|:----------|:------------|
| APPLY ROW ACCESS POLICY | 行アクセス ポリシーを削除するには、このポリシーの所有者でない限り必要です。 |

グローバルな `APPLY ROW ACCESS POLICY` 権限、または対象ポリシーに対する APPLY/OWNERSHIP が必要です。ポリシーが削除されると、{{{ .lake }}} は作成者ロールから OWNERSHIP を自動的に取り消します。

## 例 {#examples}

```sql
SET enable_experimental_row_access_policy = 1;

CREATE ROW ACCESS POLICY rap_engineering
AS (dept STRING)
RETURNS BOOLEAN -> dept = 'Engineering';

CREATE TABLE employees(id INT, department STRING);
ALTER TABLE employees ADD ROW ACCESS POLICY rap_engineering ON (department);

-- Detach the policy before dropping it.
ALTER TABLE employees DROP ROW ACCESS POLICY rap_engineering;

DROP ROW ACCESS POLICY rap_engineering;
```