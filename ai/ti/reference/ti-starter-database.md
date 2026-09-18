---
title: TiDB Cloud Starter CLI コマンドリファレンス
summary: Starter インスタンス、ブランチ、SQL ユーザー、接続文字列、SQL 実行向けの `ti db` コマンドを一覧で示します。
---

# TiDB Cloud Starter CLI コマンドリファレンス

`ti db` を使用して、TiDB Cloud Starter インスタンス、ブランチ、および SQL アクセスを管理します。対象が TiDB Cloud Starter インスタンスではない場合、またはそのサービスプランを検証できない場合、CLI はインスタンススコープの操作を拒否します。

ブランチは、親インスタンスのデータから分岐したコピーを含む、独立した TiDB Cloud Starter インスタンスです。ブランチを使用すると、親に影響を与えることなく、変更を分離してテストできます。詳細は、[TiDB Cloud Branching](/tidb-cloud/branch-overview.md) を参照してください。

## コマンド {#commands}

| コマンド | 説明 |
|---|---|
| [`create-db-cluster`](/ai/ti/reference/ti-db-create-db-cluster.md) | TiDB Cloud Starter インスタンスを作成します。 |
| [`list-db-clusters`](/ai/ti/reference/ti-db-list-db-clusters.md) | 有効なリージョン内の Starter インスタンスを一覧表示します。 |
| [`describe-db-cluster`](/ai/ti/reference/ti-db-describe-db-cluster.md) | TiDB Cloud Starter インスタンスの詳細を表示します。 |
| [`update-db-cluster`](/ai/ti/reference/ti-db-update-db-cluster.md) | TiDB Cloud Starter インスタンスを更新します。 |
| [`delete-db-cluster`](/ai/ti/reference/ti-db-delete-db-cluster.md) | TiDB Cloud Starter インスタンスを削除します。 |
| [`create-db-cluster-branch`](/ai/ti/reference/ti-db-create-db-cluster-branch.md) | TiDB Cloud Starter インスタンスのブランチを作成します。 |
| [`list-db-cluster-branches`](/ai/ti/reference/ti-db-list-db-cluster-branches.md) | TiDB Cloud Starter インスタンスのブランチを一覧表示します。 |
| [`describe-db-cluster-branch`](/ai/ti/reference/ti-db-describe-db-cluster-branch.md) | TiDB Cloud Starter インスタンスのブランチの詳細を表示します。 |
| [`delete-db-cluster-branch`](/ai/ti/reference/ti-db-delete-db-cluster-branch.md) | TiDB Cloud Starter インスタンスからブランチを削除します。 |
| [`create-db-sql-users`](/ai/ti/reference/ti-db-create-db-sql-users.md) | ロールベースの SQL ユーザーを作成または修復します。 |
| [`format-db-connection-string`](/ai/ti/reference/ti-db-format-db-connection-string.md) | 保存済みの SQL 認証情報を接続文字列として整形します。 |
| [`execute-sql-statement`](/ai/ti/reference/ti-db-execute-sql-statement.md) | 1 つの SQL ステートメントを実行します。 |

## 関連情報 {#see-also}

- [TiDB Cloud Starter インスタンスを管理する](/ai/ti/guides/manage-starter-instances.md)
- [明示的な SQL ロールを使用して TiDB Cloud Starter をクエリする](/ai/ti/guides/ti-query-sql-with-roles-example.md)