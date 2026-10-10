---
title: Row Access Policy の概要
summary: "参照しやすいように機能別に整理した、{{{ .lake }}} における Row Access Policy 操作の包括的な概要。"
---

# Row Access Policy の概要

このページでは、参照しやすいように機能別に整理した、{{{ .lake }}} における Row Access Policy 操作の包括的な概要を説明します。

## Row Access Policy の管理 {#row-access-policy-management}

| Command | 説明 |
|---------|-------------|
| [CREATE ROW ACCESS POLICY](/tidb-cloud-lake/sql/create-row-access-policy.md) | 行レベルのフィルタポリシーを作成します |
| [DESCRIBE ROW ACCESS POLICY](/tidb-cloud-lake/sql/desc-row-access-policy.md) | Row Access Policy の詳細を表示します |
| [DROP ROW ACCESS POLICY](/tidb-cloud-lake/sql/drop-row-access-policy.md) | Row Access Policy を削除します |

## 関連トピック {#related-topics}

- [行アクセス ポリシー](/tidb-cloud-lake/guides/row-access-policy.md)
- [ALTER TABLE](/tidb-cloud-lake/sql/alter-table.md#row-access-policy-operations)
- [POLICY_REFERENCES](/tidb-cloud-lake/sql/policy-references.md)

> **Note:**
>
> 行アクセスポリシーは、クエリ実行時に行をフィルタリングします。保護されたテーブルでは、ポリシー式が `TRUE` と評価される行のみが返されます。