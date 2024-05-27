---
title: Continuous Replication from Databases that Use gh-ost or pt-osc
summary: DM を使用して、オンライン DDL ツール gh-ost または pt-osc を使用するデータベースから増分データを複製する方法を学びます。
---

# gh-ost または pt-osc を使用するデータベースからの継続的なレプリケーション {#continuous-replication-from-databases-that-use-gh-ost-or-pt-osc}

本番シナリオでは、DDL 実行中のテーブル ロックによって、データベースからの読み取りまたはデータベースへの書き込みがある程度ブロックされる可能性があります。そのため、読み取りと書き込みへの影響を最小限に抑えるために、オンライン DDL ツールを使用して DDL を実行することがよくあります。一般的な DDL ツールは[おばけ](https://github.com/github/gh-ost)と[pt-osc](https://www.percona.com/doc/percona-toolkit/3.0/pt-online-schema-change.html)です。

DM を使用して MySQL から TiDB にデータを移行する場合、 `online-ddl`有効にして DM と gh-ost または pt-osc の連携を許可できます。

詳細なレプリケーション手順については、シナリオごとに次のドキュメントを参照してください。

-   [小規模データセットを MySQL から TiDB に移行する](/migrate-small-mysql-to-tidb.md)
-   [大規模なデータセットをMySQLからTiDBに移行する](/migrate-large-mysql-to-tidb.md)
-   [小さなデータセットの MySQL シャードを TiDB に移行してマージする](/migrate-small-mysql-shards-to-tidb.md)
-   [大規模データセットの MySQL シャードを TiDB に移行してマージする](/migrate-large-mysql-shards-to-tidb.md)

## DM でオンライン DDL を有効にする {#enable-online-ddl-on-dm}

DM のタスク構成ファイルで、以下に示すように、グローバル パラメータ`online-ddl`を`true`に設定します。

```yaml
# ----------- Global configuration -----------
## ********* Basic configuration *********
name: test                      # The name of the task. Should be globally unique.
task-mode: all                  # The task mode. Can be set to `full`, `incremental`, or `all`.
shard-mode: "pessimistic"       # The shard merge mode. Optional modes are `pessimistic` and `optimistic`. The `pessimistic` mode is used by default. After understanding the principles and restrictions of the "optimistic" mode, you can set it to the "optimistic" mode.
meta-schema: "dm_meta"          # The downstream database that stores the `meta` information.
online-ddl: true                # Enable online-ddl support on DM to support automatic processing of "gh-ost" and "pt-osc" for the upstream database.
```

## online-ddl を有効にした後のワークフロー {#workflow-after-enabling-online-ddl}

DM で online-ddl を有効にすると、gh-ost または pt-osc を複製する DM によって生成される DDL ステートメントが変更されます。

gh-ost または pt-osc のワークフロー:

-   DDL 実テーブルのテーブル スキーマに従ってゴースト テーブルを作成します。

-   ゴースト テーブルに DDL を適用します。

-   DDL 実テーブルのデータをゴースト テーブルに複製します。

-   2 つのテーブル間でデータの整合性が取れたら、名前変更ステートメントを使用して実際のテーブルをゴースト テーブルに置き換えます。

DM のワークフロー:

-   下流のゴースト テーブルの作成をスキップします。

-   ゴースト テーブルに適用された DDL を記録します。

-   ゴースト テーブルからのみデータを複製します。

-   下流に記録された DDL を適用します。

![dm-online-ddl](/media/dm/dm-online-ddl.png)

ワークフローの変更により、次の利点がもたらされます。

-   ダウンストリーム TiDB はゴースト テーブルを作成して複製する必要がないため、storageスペースとネットワーク転送のオーバーヘッドが節約されます。

-   シャード化されたテーブルからデータを移行およびマージする場合、レプリケーションの正確性を確保するために、シャード化されたゴースト テーブルごとに RENAME 操作は無視されます。

## 参照 {#see-also}

[オンライン DDL ツールを使用した DM の動作詳細](/dm/feature-online-ddl.md#working-details-for-dm-with-online-ddl-tools)
