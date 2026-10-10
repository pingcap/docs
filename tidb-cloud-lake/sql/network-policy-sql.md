---
title: ネットワークポリシー
summary: このページでは、{{{ .lake }}} における Network Policy の操作について、機能別に整理して包括的に説明します。
---

# ネットワークポリシー

このページでは、{{{ .lake }}} における Network Policy の操作について、機能別に整理して包括的に説明します。

## ネットワークポリシー管理 {#network-policy-management}

| コマンド | 説明 |
|---------|-------------|
| [CREATE NETWORK POLICY](/tidb-cloud-lake/sql/create-network-policy.md) | IP アドレスに基づいてアクセスを制御する新しいネットワークポリシーを作成します |
| [ALTER NETWORK POLICY](/tidb-cloud-lake/sql/alter-network-policy.md) | 既存のネットワークポリシーを変更します |
| [DROP NETWORK POLICY](/tidb-cloud-lake/sql/drop-network-policy.md) | ネットワークポリシーを削除します |

## ネットワークポリシー情報 {#network-policy-information}

| コマンド | 説明 |
|---------|-------------|
| [DESCRIBE NETWORK POLICY](/tidb-cloud-lake/sql/desc-network-policy.md) | 特定のネットワークポリシーの詳細を表示します |
| [SHOW NETWORK POLICIES](/tidb-cloud-lake/sql/show-network-policies.md) | すべてのネットワークポリシーを一覧表示します |

## 関連トピック {#related-topics}

- [ネットワークポリシー](/tidb-cloud-lake/guides/network-policy.md)

> **Note:**
>
> {{{ .lake }}} のネットワークポリシーでは、許可またはブロックする IP アドレスやアドレス範囲を指定することで、データベースへのアクセスを制御できます。