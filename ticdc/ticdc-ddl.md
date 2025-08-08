---
title: Changefeed DDL Replication
summary: TiCDC でサポートされている DDL ステートメントといくつかの特殊なケースについて学習します。
---

# チェンジフィード DDL レプリケーション {#changefeed-ddl-replication}

このドキュメントでは、TiCDC での DDL レプリケーションのルールと特殊なケースについて説明します。

## DDL許可リスト {#ddl-allow-list}

現在、TiCDC は許可リストを使用して DDL ステートメントを複製するかどうかを決定します。許可リストに含まれる DDL ステートメントのみが下流に複製されます。許可リストに含まれない DDL ステートメントは複製されません。

さらに、TiCDCは、テーブルに[valid index](/ticdc/ticdc-overview.md#valid-index)があるかどうか、および構成項目[`force-replicate`](/ticdc/ticdc-changefeed-config.md#force-replicate) `true`に設定されているかどうかに基づいて、DDL文をダウンストリームに複製するかどうかを決定します。7 `force-replicate=true`場合、レプリケーションタスクは強制的に[有効なインデックスのないテーブルを複製する](/ticdc/ticdc-manage-changefeed.md#replicate-tables-without-a-valid-index)試みます。

以下は、TiCDC でサポートされている DDL ステートメントの許可リストです。表内の略語は以下のとおりです。

-   Y: Replication to the downstream is supported in this condition.
-   N: この状態ではダウンストリームへのレプリケーションはサポートされません。

> **注記**
>
> -   アップストリームテーブルに有効なインデックスがなく、かつ`force-replicate=true`設定されていない場合、テーブルはレプリケートされません。ただし、このテーブルに有効なインデックスを作成する後続のDDL文（ `CREATE INDEX` 、 `ADD INDEX` 、 `ADD PRIMARY KEY`を含む）はレプリケートされます。これにより、ダウンストリームテーブルとアップストリームテーブルのスキーマ間に不整合が生じ、その後のデータレプリケーションが失敗する可能性があります。
> -   最後の有効なインデックスを削除する DDL ステートメント ( `DROP INDEX`と`DROP PRIMARY KEY`を含む) は複製されず、後続のデータ レプリケーションが失敗します。

| DDL                            | 有効なインデックスが存在します | 有効なインデックスが存在せず、 `force-replicate`は`false` (デフォルト) です | 有効なインデックスが存在せず、 `force-replicate` `true`に設定されている |
| ------------------------------ | :-------------: | :--------------------------------------------------: | :----------------------------------------------: |
| `CREATE DATABASE`              |        Y        |                           Y                          |                         Y                        |
| `DROP DATABASE`                |        Y        |                           Y                          |                         Y                        |
| `ALTER DATABASE CHARACTER SET` |        Y        |                           Y                          |                         Y                        |
| `CREATE INDEX`                 |        Y        |                           Y                          |                         Y                        |
| `ADD INDEX`                    |        Y        |                           Y                          |                         Y                        |
| `DROP INDEX`                   |        Y        |                           N                          |                         Y                        |
| `ADD PRIMARY KEY`              |        Y        |                           Y                          |                         Y                        |
| `DROP PRIMARY KEY`             |        Y        |                           N                          |                         Y                        |
| `CREATE TABLE`                 |        Y        |                           北                          |                         Y                        |
| `DROP TABLE`                   |        Y        |                           北                          |                         Y                        |
| `ADD COLUMN`                   |        Y        |                           北                          |                         Y                        |
| `DROP COLUMN`                  |        Y        |                           北                          |                         Y                        |
| `TRUNCATE TABLE`               |        Y        |                           北                          |                         Y                        |
| `MODIFY COLUMN`                |        Y        |                           北                          |                         Y                        |
| `RENAME TABLE`                 |        Y        |                           北                          |                         Y                        |
| `ALTER COLUMN DEFAULT VALUE`   |        Y        |                           北                          |                         Y                        |
| `ALTER TABLE COMMENT`          |        Y        |                           北                          |                         Y                        |
| `RENAME INDEX`                 |        Y        |                           北                          |                         Y                        |
| `ADD PARTITION`                |        Y        |                           北                          |                         Y                        |
| `DROP PARTITION`               |        Y        |                           北                          |                         Y                        |
| `TRUNCATE PARTITION`           |        Y        |                           北                          |                         Y                        |
| `CREATE VIEW`                  |        Y        |                           北                          |                         Y                        |
| `DROP VIEW`                    |        Y        |                           北                          |                         Y                        |
| `ALTER TABLE CHARACTER SET`    |        Y        |                           北                          |                         Y                        |
| `RECOVER TABLE`                |        Y        |                           北                          |                         Y                        |
| `REBASE AUTO ID`               |        Y        |                           北                          |                         Y                        |
| `ALTER TABLE INDEX VISIBILITY` |        Y        |                           北                          |                         Y                        |
| `EXCHANGE PARTITION`           |        Y        |                           N                          |                         Y                        |
| `REORGANIZE PARTITION`         |        Y        |                           北                          |                         Y                        |
| `ALTER TABLE TTL`              |        Y        |                           北                          |                         Y                        |
| `ALTER TABLE REMOVE TTL`       |        Y        |                           北                          |                         Y                        |

## DDLレプリケーションの考慮事項 {#ddl-replication-considerations}

### <code>ADD INDEX</code>および<code>CREATE INDEX</code> DDL の非同期実行 {#asynchronous-execution-of-code-add-index-code-and-code-create-index-code-ddls}

下流がTiDBの場合、TiCDCは`ADD INDEX`と`CREATE INDEX` DDL操作を非同期的に実行し、変更フィードレプリケーションのレイテンシーへの影響を最小限に抑えます。つまり、 `ADD INDEX`と`CREATE INDEX` DDLを下流TiDBにレプリケーションして実行した後、TiCDCはDDL実行の完了を待たずに直ちに戻ります。これにより、後続のDML実行がブロックされることを回避できます。

During the execution of the `ADD INDEX` or `CREATE INDEX` DDL operation in the downstream, when TiCDC executes the next DDL operation of the same table, this DDL operation might be blocked in the `queueing` state for a long time. This can cause TiCDC to repeatedly execute this DDL operation, and if retries take too long, it might lead to replication task failure. Starting from v8.4.0, if TiCDC has the `SUPER` permission of the downstream database, it periodically runs `ADMIN SHOW DDL JOBS` to check the status of asynchronously executed DDL tasks. TiCDC will wait for index creation to complete before proceeding with replication. Although this might increase replication latency, it avoids replication task failure.

> **Note:**
>
> -   特定のダウンストリーム DML の実行が、レプリケーションが完了していないインデックスに依存している場合、これらの DML の実行速度が遅くなり、TiCDC レプリケーションのレイテンシーに影響する可能性があります。
> -   DDLを下流に複製する前に、TiCDCノードがクラッシュした場合、または下流で他の書き込み操作が実行されている場合、DDL複製が失敗する可能性は極めて低くなります。下流でそのような状況が発生するかどうかを確認できます。

### DDL replication considerations for renaming tables {#ddl-replication-considerations-for-renaming-tables}

レプリケーション プロセス中に一部のコンテキストが欠如しているため、TiCDC では`RENAME TABLE` DDL のレプリケーションにいくつかの制約があります。

#### DDL ステートメントで単一のテーブルの名前を変更する {#rename-a-single-table-in-a-ddl-statement}

DDL文で単一のテーブル名を変更する場合、TiCDCは古いテーブル名がフィルタールールに一致する場合にのみ、そのDDL文を複製します。以下に例を示します。

changefeed の構成ファイルが次のようになっていると仮定します。

```toml
[filter]
rules = ['test.t*']
```

TiCDC はこのタイプの DDL を次のように処理します。

| DDL                                   | 複製するかどうか              | 取り扱い理由                                                                                               |
| ------------------------------------- | --------------------- | ---------------------------------------------------------------------------------------------------- |
| `RENAME TABLE test.t1 TO test.t2`     | 複製する                  | `test.t1`フィルタルールに一致します                                                                               |
| `RENAME TABLE test.t1 TO ignore.t1`   | 複製する                  | `test.t1`フィルタルールに一致します                                                                               |
| `RENAME TABLE ignore.t1 TO ignore.t2` | Ignore                | `ignore.t1`フィルタルールに一致しません                                                                            |
| `RENAME TABLE test.n1 TO test.t1`     | エラーを報告してレプリケーションを終了する | 古いテーブル名`test.n1`フィルタルールに一致しませんが、新しいテーブル名`test.t1`フィルタルールに一致します。この操作は不正です。この場合、エラーメッセージを参照して対処してください。 |
| `RENAME TABLE ignore.t1 TO test.t1`   | エラーを報告してレプリケーションを終了する | 上記と同じ理由です。                                                                                           |

#### DDL ステートメントで複数のテーブルの名前を変更する {#rename-multiple-tables-in-a-ddl-statement}

If a DDL statement renames multiple tables, TiCDC replicates the DDL statement only when the **old database name**, **old table names**, and **new database name** all match the filter rule.

また、TiCDCはテーブル名を入れ替える`RENAME TABLE` DDLをサポートしていません。以下に例を示します。

changefeed の構成ファイルが次のようになっていると仮定します。

```toml
[filter]
rules = ['test.t*']
```

TiCDC processes this type of DDL as follows:

| DDL                                                                        | 複製するかどうか        | 取り扱い理由                                                                                                           |
| -------------------------------------------------------------------------- | --------------- | ---------------------------------------------------------------------------------------------------------------- |
| `RENAME TABLE test.t1 TO test.t2, test.t3 TO test.t4`                      | 複製する            | すべてのデータベース名とテーブル名はフィルター ルールに一致します。                                                                               |
| `RENAME TABLE test.t1 TO test.ignore1, test.t3 TO test.ignore2`            | 複製する            | 古いデータベース名、古いテーブル名、および新しいデータベース名は、フィルター ルールと一致します。                                                                |
| `RENAME TABLE test.t1 TO ignore.t1, test.t2 TO test.t22;`                  | エラーを報告する        | 新しいデータベース名`ignore`フィルター ルールと一致しません。                                                                              |
| `RENAME TABLE test.t1 TO test.t4, test.t3 TO test.t1, test.t4 TO test.t3;` | Report an error | `RENAME TABLE` DDL文では、 `test.t1`と`test.t3`名前が1つのDDL文内で入れ替わっていますが、TiCDCはこれを正しく処理できません。この場合、エラーメッセージを参照して対処してください。 |

### DDL文の考慮事項 {#ddl-statement-considerations}

アップストリームでクロスデータベースDDL文（例： `CREATE TABLE db1.t1 LIKE t2` ）を実行する場合、関連するすべてのデータベース名をDDL文（例： `CREATE TABLE db1.t1 LIKE db2.t2` ）で明示的に指定することをお勧めします。そうしないと、データベース名情報が不足しているため、ダウンストリームでクロスデータベースDDL文が正しく実行されない可能性があります。

### Notes on using event filter rules to filter DDL events {#notes-on-using-event-filter-rules-to-filter-ddl-events}

フィルタリングされたDDL文がテーブルの作成または削除を伴う場合、TiCDCはDML文のレプリケーション動作に影響を与えることなく、DDL文のみをフィルタリングします。以下に例を示します。

Assume that the configuration file of your changefeed is as follows:

```toml
[filter]
rules = ['test.t*']

[[filter.event-filters]]
matcher = ["test.t1"] # This filter rule applies only to the t1 table in the test database.
ignore-event = ["create table", "drop table", "truncate table", "rename table"]
```

| DDL                                                    | DDL behavior | DMLの動作    | Explanation                                                                                                                        |
| ------------------------------------------------------ | ------------ | --------- | ---------------------------------------------------------------------------------------------------------------------------------- |
| `CREATE TABLE test.t1 (id INT, name VARCHAR(50));`     | 無視する         | 複製する      | `test.t1` matches the event filter rule, so the `CREATE TABLE` event is ignored. The replication of DML events remains unaffected. |
| `CREATE TABLE test.t2 (id INT, name VARCHAR(50));`     | 複製する         | 複製する      | `test.t2` does not match the event filter rule.                                                                                    |
| `CREATE TABLE test.ignore (id INT, name VARCHAR(50));` | Ignore       | 無視する      | `test.ignore`イベント フィルタ ルールに一致するため、DDL イベントと DML イベントの両方が無視されます。                                                                    |
| `DROP TABLE test.t1;`                                  | Ignore       | <li></li> | `test.t1`イベントフィルタルールに一致するため、イベント`DROP TABLE`無視されます。テーブルが削除されたため、TiCDC は`t1`の DML イベントを複製しなくなります。                                   |
| `TRUNCATE TABLE test.t1;`                              | 無視する         | 複製する      | `test.t1`イベントフィルタルールに一致するため、 `TRUNCATE TABLE`イベントは無視されます。DMLイベントのレプリケーションは影響を受けません。                                                |
| `RENAME TABLE test.t1 TO test.t2;`                     | 無視する         | 複製する      | `test.t1`イベントフィルタルールに一致するため、 `RENAME TABLE`イベントは無視されます。DMLイベントのレプリケーションは影響を受けません。                                                  |
| `RENAME TABLE test.t1 TO test.ignore;`                 | 無視する         | 無視する      | `test.t1`イベント フィルター ルールに一致するため、 `RENAME TABLE`イベントは無視されます。4 `test.ignore`イベント フィルター ルールに一致するため、DDL イベントと DML イベントの両方が無視されます。       |

> **注記：**
>
> -   データベースにデータをレプリケーションする際は、イベントフィルターを使用してDDLイベントを慎重にフィルタリングしてください。レプリケーション中は、上流と下流のデータベーススキーマの整合性が維持されていることを確認してください。整合性が維持されていない場合、TiCDCはエラーを報告したり、未定義のレプリケーション動作を引き起こしたりする可能性があります。
> -   v6.5.8、v7.1.4、v7.5.1より前のバージョンでは、イベントフィルタを使用してテーブルの作成または削除を含むDDLイベントをフィルタリングすると、DMLレプリケーションに影響します。これらのバージョンでは、この機能の使用は推奨されません。
