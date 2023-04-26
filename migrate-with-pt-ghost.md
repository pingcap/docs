---
title: Continuous Replication from Databases that Use gh-ost or pt-osc
summary: Learn how to use DM to replicate incremental data from databases that use online DDL tools gh-ost or pt-osc
---

# gh-ost または pt-osc を使用するデータベースからの連続レプリケーション {#continuous-replication-from-databases-that-use-gh-ost-or-pt-osc}

本番シナリオでは、DDL 実行中にテーブルをロックすると、データベースからの読み取りまたはデータベースへの書き込みがある程度ブロックされる可能性があります。そのため、オンライン DDL ツールを使用して DDL を実行し、読み取りと書き込みへの影響を最小限に抑えることがよくあります。一般的な DDL ツールは[おばけ](https://github.com/github/gh-ost)と[pt-osc](https://www.percona.com/doc/percona-toolkit/3.0/pt-online-schema-change.html)です。

DM を使用して MySQL から TiDB にデータを移行する場合、DM と gh-ost または pt-osc のコラボレーションを許可するために`online-ddl`有効にすることができます。

詳細なレプリケーション手順については、シナリオごとに次のドキュメントを参照してください。

-   [小さなデータセットの MySQL を TiDB に移行する](/migrate-small-mysql-to-tidb.md)
-   [大規模なデータセットの MySQL を TiDB に移行する](/migrate-large-mysql-to-tidb.md)
-   [小さなデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-small-mysql-shards-to-tidb.md)
-   [大規模なデータセットの MySQL シャードを TiDB に移行およびマージする](/migrate-large-mysql-shards-to-tidb.md)

## DM で online-ddl を有効にする {#enable-online-ddl-on-dm}

DM のタスク構成ファイルで、以下に示すように、グローバル パラメーター`online-ddl`から`true`を設定します。

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

DM で online-ddl を有効にすると、DM が gh-ost または pt-osc をレプリケートすることによって生成される DDL ステートメントが変更されます。

gh-ost または pt-osc のワークフロー:

-   DDL実表の表スキーマに従ってゴースト表を作成します。

-   ゴースト テーブルに DDL を適用します。

-   DDL 実表のデータをゴースト表に複製します。

-   2 つのテーブル間でデータの整合性が取れたら、rename ステートメントを使用して実際のテーブルをゴースト テーブルに置き換えます。

DMのワークフロー:

-   ゴースト テーブルのダウンストリームの作成をスキップします。

-   ゴースト テーブルに適用された DDL を記録します。

-   ゴースト テーブルからのみデータをレプリケートします。

-   ダウンストリームで記録された DDL を適用します。

![dm-online-ddl](/media/dm/dm-online-ddl.png)

ワークフローの変更により、次の利点がもたらされます。

-   ダウンストリームの TiDB は、ゴースト テーブルを作成して複製する必要がないため、storageスペースとネットワーク転送のオーバーヘッドが節約されます。

-   シャード テーブルからデータを移行およびマージする場合、レプリケーションの正確性を確保するために、シャード ゴースト テーブルごとに RENAME 操作が無視されます。

## こちらもご覧ください {#see-also}

[オンライン DDL ツールを使用した DM の作業の詳細](/dm/feature-online-ddl.md#working-details-for-dm-with-online-ddl-tools)
