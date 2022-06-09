---
title: Continuous Replication from Databases that Use gh-ost or pt-osc
summary: Learn how to use DM to replicate incremental data from databases that use online DDL tools gh-ost or pt-osc
---

# gh-ostまたはpt-oscを使用するデータベースからの継続的なレプリケーション {#continuous-replication-from-databases-that-use-gh-ost-or-pt-osc}

本番シナリオでは、DDL実行中のテーブルロックにより、データベースからの読み取りまたはデータベースへの書き込みがある程度ブロックされる可能性があります。したがって、オンラインDDLツールは、読み取りと書き込みへの影響を最小限に抑えるためにDDLを実行するためによく使用されます。一般的なDDLツールは[幽霊](https://github.com/github/gh-ost)と[pt-osc](https://www.percona.com/doc/percona-toolkit/3.0/pt-online-schema-change.html)です。

DMを使用してMySQLからTiDBにデータを移行する場合、DMとgh-ostまたはpt-oscのコラボレーションを可能にするために`online-ddl`をエンベールできます。

詳細なレプリケーション手順については、シナリオごとに次のドキュメントを参照してください。

-   [小さなデータセットのMySQLをTiDBに移行する](/migrate-small-mysql-to-tidb.md)
-   [大規模なデータセットのMySQLをTiDBに移行する](/migrate-large-mysql-to-tidb.md)
-   [小さなデータセットのMySQLシャードをTiDBに移行およびマージする](/migrate-small-mysql-shards-to-tidb.md)
-   [大規模なデータセットのMySQLシャードをTiDBに移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)

## DMでonline-ddlを有効にする {#enable-online-ddl-on-dm}

DMのタスク構成ファイルで、以下に示すように、グローバルパラメーター`online-ddl`を`true`に設定します。

```yaml
# ----------- Global configuration -----------
## ********* Basic configuration *********
name: test                      # The name of the task. Should be globally unique.
task-mode: all                  # The task mode. Can be set to `full`, `incremental`, or `all`.
shard-mode: "pessimistic"       # The shard merge mode. Optional modes are `pessimistic` and `optimistic`. The `pessimistic` mode is used by default. After understanding the principles and restrictions of the "optimistic" mode, you can set it to the "optimistic" mode.
meta-schema: "dm_meta"          # The downstream database that stores the `meta` information.
online-ddl: true                # Enable online-ddl support on DM to support automatic processing of "gh-ost" and "pt-osc" for the upstream database.
```

## online-ddlを有効にした後のワークフロー {#workflow-after-enabling-online-ddl}

DMでonline-ddlを有効にすると、DMがgh-ostまたはpt-oscを複製することによって生成されるDDLステートメントが変更されます。

gh-ostまたはpt-oscのワークフロー：

-   DDL実テーブルのテーブルスキーマに従ってゴーストテーブルを作成します。

-   ゴーストテーブルにDDLを適用します。

-   DDL実表のデータをゴースト表に複製します。

-   2つのテーブル間でデータの整合性が取れたら、renameステートメントを使用して、実際のテーブルをゴーストテーブルに置き換えます。

DMのワークフロー：

-   ダウンストリームのゴーストテーブルの作成をスキップします。

-   ゴーストテーブルに適用されたDDLを記録します。

-   ゴーストテーブルからのみデータを複製します。

-   ダウンストリームで記録されたDDLを適用します。

![dm-online-ddl](/media/dm/dm-online-ddl.png)

ワークフローの変更により、次の利点がもたらされます。

-   ダウンストリームTiDBは、ゴーストテーブルを作成して複製する必要がないため、ストレージスペースとネットワーク伝送のオーバーヘッドを節約できます。

-   シャーディングされたテーブルからデータを移行およびマージする場合、レプリケーションの正確性を確保するために、シャーディングされたゴーストテーブルごとにRENAME操作は無視されます。

## も参照してください {#see-also}

[オンラインDDLツールを使用したDMの作業の詳細](/dm/feature-online-ddl.md#working-details-for-dm-with-online-ddl-tools)
