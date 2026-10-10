---
title: Masking Policy
summary: このページでは、{{{ .lake }}} における Masking Policy の操作について、参照しやすいよう機能別に整理して包括的に説明します。
---

# Masking Policy

このページでは、{{{ .lake }}} における Masking Policy の操作について、参照しやすいよう機能別に整理して包括的に説明します。

## Masking Policy の管理 {#masking-policy-management}

| Command | 説明 |
|---------|-------------|
| [CREATE MASKING POLICY](/tidb-cloud-lake/sql/create-masking-policy.md) | データの難読化のための新しい masking policy を作成します |
| [DESCRIBE MASKING POLICY](/tidb-cloud-lake/sql/desc-masking-policy.md) | 特定の masking policy の詳細を表示します |
| [DROP MASKING POLICY](/tidb-cloud-lake/sql/drop-masking-policy.md) | masking policy を削除します |

## 関連トピック {#related-topics}

- [マスキングポリシー](/tidb-cloud-lake/guides/masking-policy.md)

> **Note:**
>
> {{{ .lake }}} の masking policy を使用すると、適切な権限を持たないユーザーがクエリを実行した際に、機密データを動的に変換または難読化して保護できます。