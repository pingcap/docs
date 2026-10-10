---
title: パスワードポリシー
summary: このページでは、{{{ .lake }}} におけるパスワードポリシー操作の包括的な概要を、参照しやすいよう機能別に整理して説明します。
---

# パスワードポリシー

このページでは、{{{ .lake }}} におけるパスワードポリシー操作の包括的な概要を、参照しやすいよう機能別に整理して説明します。

## パスワードポリシー管理 {#password-policy-management}

| コマンド | 説明 |
|---------|-------------|
| [CREATE PASSWORD POLICY](/tidb-cloud-lake/sql/create-password-policy.md) | 特定の要件を持つ新しいパスワードポリシーを作成します |
| [ALTER PASSWORD POLICY](/tidb-cloud-lake/sql/alter-password-policy.md) | 既存のパスワードポリシーを変更します |
| [DROP PASSWORD POLICY](/tidb-cloud-lake/sql/drop-password-policy.md) | パスワードポリシーを削除します |

## パスワードポリシー情報 {#password-policy-information}

| コマンド | 説明 |
|---------|-------------|
| [DESCRIBE PASSWORD POLICY](/tidb-cloud-lake/sql/desc-password-policy.md) | 特定のパスワードポリシーの詳細を表示します |
| [SHOW PASSWORD POLICIES](/tidb-cloud-lake/sql/show-password-policies.md) | すべてのパスワードポリシーを一覧表示します |

## 関連トピック {#related-topics}

- [パスワードポリシー](/tidb-cloud-lake/guides/password-policy.md)

> **Note:**
>
> {{{ .lake }}} のパスワードポリシーを使用すると、最小文字数、複雑さ、有効期限ルールなど、ユーザーパスワードに対するセキュリティ要件を適用できます。