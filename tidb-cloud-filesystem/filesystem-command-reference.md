---
title: TiDB Cloud Filesystem コマンドリファレンス
summary: `ti` の設定、TiDB Cloud Filesystem リソース、データ、Git ワークスペース、ジャーナル、Vault シークレットの管理に関する TiDB Cloud CLI のコマンドリファレンスを確認できます。
---

# TiDB Cloud Filesystem コマンドリファレンス

TiDB Cloud CLI (`ti`) は、TiDB Cloud Filesystem を操作するためのコマンドラインインターフェースを提供します。これを使用して、ファイルシステムの作成と管理、ファイルやディレクトリの操作、さらに Git ワークスペース、ジャーナル、Vault シークレットなどのファイルシステム機能を利用できます。

このページは、TiDB Cloud Filesystem に関連する TiDB Cloud CLI リファレンスの索引として利用できます。また、CLI の設定や更新時に必要になる可能性がある、一般的な `ti` コマンドや動作に関するリファレンスも含まれています。

> **Note:**
>
> このページでは、ファイルシステム関連のコマンドリファレンスのみを扱います。`ti db` などの TiDB Cloud Starter データベースコマンドについては、[TiDB Cloud CLI ドキュメント](/ai/ti/ti-overview.md) に別途記載されています。

## 一般的な TiDB Cloud CLI リファレンス {#general-tidb-cloud-cli-references}

以下のリファレンスを使用して、`ti` の設定や更新を行い、その一般的な動作について確認できます。

- [TiDB Cloud CLI リファレンス](/ai/ti/reference/ti-cli-reference.md)
- [`ti configure`](/ai/ti/reference/ti-configure.md)
- [`ti update`](/ai/ti/reference/ti-update.md)

## TiDB Cloud Filesystem コマンドグループ {#tidb-cloud-filesystem-command-groups}

実行したい操作に応じて、コマンドグループを選択してください。

- ファイルシステムの作成と管理、およびファイルシステムデータの操作には [`ti fs` commands](/ai/ti/reference/ti-filesystem.md) を使用します。
- ファイルシステム上の Git リポジトリおよび worktree の操作には [`ti fs-git` commands](/ai/ti/reference/ti-filesystem-git.md) を使用します。
- ファイルシステムジャーナルの管理には [`ti fs-journal` commands](/ai/ti/reference/ti-filesystem-journal.md) を使用します。
- ファイルシステムの Vault シークレットの管理には [`ti fs-vault` commands](/ai/ti/reference/ti-filesystem-vault.md) を使用します。