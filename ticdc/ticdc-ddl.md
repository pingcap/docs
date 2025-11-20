---
title: Changefeed DDL Replication
summary: TiCDC でサポートされている DDL ステートメントといくつかの特殊なケースについて学習します。
---

# チェンジフィード DDL レプリケーション {#changefeed-ddl-replication}

このドキュメントでは、TiCDC における DDL レプリケーションのルールと特殊なケースについて説明します。

## DDL許可リスト {#ddl-allow-list}

現在、TiCDC は許可リストを使用して DDL ステートメントをレプリケートするかどうかを決定します。許可リストに含まれる DDL ステートメントのみが下流にレプリケートされます。許可リストに含まれない DDL ステートメントはレプリケートされません。

さらに、TiCDCは、テーブルに[有効なインデックス](/ticdc/ticdc-overview.md#valid-index)があるかどうか、および構成項目[`force-replicate`](/ticdc/ticdc-changefeed-config.md#force-replicate)が`true`に設定されているかどうかに基づいて、DDL文をダウンストリームに複製するかどうかを決定します`force-replicate=true`の場合、レプリケーションタスクは強制的に[有効なインデックスのないテーブルを複製する](/ticdc/ticdc-manage-changefeed.md#replicate-tables-without-a-valid-index)試みます。

以下は、TiCDC でサポートされている DDL ステートメントの許可リストです。表内の略語は以下のとおりです。

-   Y: この状態ではダウンストリームへのレプリケーションがサポートされます。
-   N: この状態では、ダウンストリームへのレプリケーションはサポートされません。

> **注記**
>
> -   アップストリームテーブルに有効なインデックスがなく、かつ`force-replicate=true`が設定されていない場合、テーブルはレプリケートされません。ただし、このテーブルに有効なインデックスを作成する後続のDDL文（ `CREATE INDEX` 、 `ADD INDEX` 、 `ADD PRIMARY KEY`を含む）はレプリケートされます。これにより、ダウンストリームテーブルとアップストリームテーブルのスキーマ間に不整合が生じ、その後のデータレプリケーションが失敗する可能性があります。
> -   最後の有効なインデックスを削除する DDL ステートメント ( `DROP INDEX`と`DROP PRIMARY KEY`を含む) は複製されないため、後続のデータ レプリケーションが失敗します。

| DDL                            | 有効なインデックスが存在します | 有効なインデックスが存在せず、 `force-replicate`は`false` (デフォルト) です | 有効なインデックスが存在せず、 `force-replicate` `true`に設定されている |
| ------------------------------ | :-------------: | :--------------------------------------------------: | :----------------------------------------------: |
| `CREATE DATABASE`              |        Y        |                           Y                          |                         Y                        |
| `DROP DATABASE`                |        Y        |                           Y                          |                         Y                        |
| `ALTER DATABASE CHARACTER SET` |        Y        |                           Y                          |                         Y                        |
| `CREATE INDEX`                 |        Y        |                           Y                          |                         Y                        |
| `ADD INDEX`                    |        Y        |                           Y                          |                         Y                        |
| `DROP INDEX`                   |        Y        |                           北                          |                         Y                        |
| `ADD PRIMARY KEY`              |        Y        |                           Y                          |                         Y                        |
| `DROP PRIMARY KEY`             |        Y        |                           北                          |                         Y                        |
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
| `EXCHANGE PARTITION`           |        Y        |                           北                          |                         Y                        |
| `REORGANIZE PARTITION`         |        Y        |                           北                          |                         Y                        |
| `ALTER TABLE TTL`              |        Y        |                           北                          |                         Y                        |
| `ALTER TABLE REMOVE TTL`       |        Y        |                           北                          |                         Y                        |

## DDLレプリケーションの考慮事項 {#ddl-replication-considerations}

### <code>ADD INDEX</code>および<code>CREATE INDEX</code> DDL の非同期実行 {#asynchronous-execution-of-code-add-index-code-and-code-create-index-code-ddls}

ダウンストリームがTiDBの場合、TiCDCは`ADD INDEX`と`CREATE INDEX` DDL操作を非同期的に実行し、変更フィードレプリケーションのレイテンシーへの影響を最小限に抑えます。つまり、 `ADD INDEX`と`CREATE INDEX` DDLをダウンストリームTiDBにレプリケーションして実行した後、TiCDCはDDL実行の完了を待たずに直ちに戻ります。これにより、後続のDML実行がブロックされることを回避できます。

ダウンストリームで`ADD INDEX`または`CREATE INDEX` DDL 操作が実行されている間に、TiCDC が同じテーブルに対して次の DDL 操作を実行すると、この DDL 操作が`queueing`状態で長時間ブロックされる可能性があります。これにより、TiCDC はこの DDL 操作を繰り返し実行することになり、再試行に時間がかかりすぎると、レプリケーションタスクが失敗する可能性があります。v8.4.0 以降では、TiCDC がダウンストリームデータベースに対して`SUPER`権限を持っている場合、定期的に`ADMIN SHOW DDL JOBS`実行して、非同期で実行された DDL タスクのステータスを確認します。TiCDC は、インデックス作成が完了するまで待ってからレプリケーションを続行します。これによりレプリケーションのレイテンシーが増加する可能性がありますが、レプリケーションタスクの失敗を回避できます。

> **注記：**
>
> -   特定のダウンストリーム DML の実行が、レプリケーションが完了していないインデックスに依存している場合、これらの DML の実行速度が遅くなり、TiCDC レプリケーションのレイテンシーに影響する可能性があります。
> -   DDLをダウンストリームに複製する前に、TiCDCノードがクラッシュした場合、またはダウンストリームが他の書き込み操作を実行している場合、DDL複製が失敗する可能性は極めて低くなります。ダウンストリームでそのような状況が発生するかどうかを確認できます。

### テーブル名の変更に関するDDLレプリケーションの考慮事項 {#ddl-replication-considerations-for-renaming-tables}

レプリケーション プロセス中に一部のコンテキストが欠如しているため、TiCDC では`RENAME TABLE` DDL のレプリケーションにいくつかの制約があります。

#### DDL ステートメントで単一のテーブルの名前を変更する {#rename-a-single-table-in-a-ddl-statement}

DDL文で単一のテーブル名を変更する場合、TiCDCは古いテーブル名がフィルタールールに一致する場合にのみ、そのDDL文を複製します。以下に例を示します。

changefeed の構成ファイルが次のようになっていると仮定します。

```toml
[filter]
rules = ['test.t*']
```

TiCDC はこのタイプの DDL を次のように処理します。

| DDL                                   | 複製するかどうか              | 取り扱い理由                                                                                                |
| ------------------------------------- | --------------------- | ----------------------------------------------------------------------------------------------------- |
| `RENAME TABLE test.t1 TO test.t2`     | 複製する                  | `test.t1`フィルタルールに一致します                                                                                |
| `RENAME TABLE test.t1 TO ignore.t1`   | 複製する                  | `test.t1`フィルタルールに一致します                                                                                |
| `RENAME TABLE ignore.t1 TO ignore.t2` | 無視する                  | `ignore.t1`はフィルタルールに一致しません                                                                            |
| `RENAME TABLE test.n1 TO test.t1`     | エラーを報告してレプリケーションを終了する | 古いテーブル名`test.n1`フィルタルールに一致しませんが、新しいテーブル名`test.t1`はフィルタルールに一致します。この操作は無効です。この場合、エラーメッセージを参照して対処してください。 |
| `RENAME TABLE ignore.t1 TO test.t1`   | エラーを報告してレプリケーションを終了する | 上記と同じ理由です。                                                                                            |

#### DDL ステートメントで複数のテーブルの名前を変更する {#rename-multiple-tables-in-a-ddl-statement}

DDL ステートメントで複数のテーブルの名前を変更する場合、TiCDC は、**古いデータベース名**、**古いテーブル名**、および**新しいデータベース名が**すべてフィルター ルールに一致する場合にのみ、DDL ステートメントを複製します。

また、TiCDCはテーブル名を入れ替える`RENAME TABLE` DDLをサポートしていません。以下に例を示します。

changefeed の構成ファイルが次のようになっていると仮定します。

```toml
[filter]
rules = ['test.t*']
```

TiCDC はこのタイプの DDL を次のように処理します。

| DDL                                                                        | 複製するかどうか | 取り扱い理由                                                                                                         |
| -------------------------------------------------------------------------- | -------- | -------------------------------------------------------------------------------------------------------------- |
| `RENAME TABLE test.t1 TO test.t2, test.t3 TO test.t4`                      | 複製する     | すべてのデータベース名とテーブル名はフィルター ルールに一致します。                                                                             |
| `RENAME TABLE test.t1 TO test.ignore1, test.t3 TO test.ignore2`            | 複製する     | 古いデータベース名、古いテーブル名、および新しいデータベース名は、フィルター ルールと一致します。                                                              |
| `RENAME TABLE test.t1 TO ignore.t1, test.t2 TO test.t22;`                  | エラーを報告する | 新しいデータベース名`ignore`フィルター ルールと一致しません。                                                                            |
| `RENAME TABLE test.t1 TO test.t4, test.t3 TO test.t1, test.t4 TO test.t3;` | エラーを報告する | `RENAME TABLE` DDL文は、1つのDDL文内で`test.t1`と`test.t3`の名前を入れ替えているため、TiCDCはこれを正しく処理できません。この場合、エラーメッセージを参照して対処してください。 |

### DDL文の考慮事項 {#ddl-statement-considerations}

アップストリームでクロスデータベースDDL文（例： `CREATE TABLE db1.t1 LIKE t2` ）を実行する場合、関連するすべてのデータベース名をDDL文（例： `CREATE TABLE db1.t1 LIKE db2.t2` ）で明示的に指定することをお勧めします。そうしないと、データベース名情報が不足しているため、ダウンストリームでクロスデータベースDDL文が正しく実行されない可能性があります。

### イベント フィルタ ルールを使用して DDL イベントをフィルタする場合の注意事項 {#notes-on-using-event-filter-rules-to-filter-ddl-events}

フィルタリングされたDDL文がテーブルの作成または削除を伴う場合、TiCDCはDML文のレプリケーション動作に影響を与えることなく、DDL文のみをフィルタリングします。以下に例を示します。

changefeed の構成ファイルが次のようになっていると仮定します。

```toml
[filter]
rules = ['test.t*']

[[filter.event-filters]]
matcher = ["test.t1"] # This filter rule applies only to the t1 table in the test database.
ignore-event = ["create table", "drop table", "truncate table", "rename table"]
```

| DDL                                                    | DDLの動作 | DMLの動作    | 説明                                                                                                                           |
| ------------------------------------------------------ | ------ | --------- | ---------------------------------------------------------------------------------------------------------------------------- |
| `CREATE TABLE test.t1 (id INT, name VARCHAR(50));`     | 無視する   | 複製する      | `test.t1`イベントフィルタルールに一致するため、 `CREATE TABLE`イベントは無視されます。DMLイベントのレプリケーションは影響を受けません。                                            |
| `CREATE TABLE test.t2 (id INT, name VARCHAR(50));`     | 複製する   | 複製する      | `test.t2`はイベント フィルタ ルールと一致しません。                                                                                              |
| `CREATE TABLE test.ignore (id INT, name VARCHAR(50));` | 無視する   | 無視する      | `test.ignore`イベント フィルタ ルールに一致するため、DDL イベントと DML イベントの両方が無視されます。                                                              |
| `DROP TABLE test.t1;`                                  | 無視する   | <li></li> | `test.t1`イベントフィルタルールに一致するため、イベント`DROP TABLE`は無視されます。テーブルが削除されたため、TiCDC は`t1`の DML イベントを複製しなくなります。                            |
| `TRUNCATE TABLE test.t1;`                              | 無視する   | 複製する      | `test.t1`イベントフィルタルールに一致するため、 `TRUNCATE TABLE`イベントは無視されます。DMLイベントのレプリケーションは影響を受けません。                                          |
| `RENAME TABLE test.t1 TO test.t2;`                     | 無視する   | 複製する      | `test.t1`イベントフィルタルールに一致するため、 `RENAME TABLE`イベントは無視されます。DMLイベントのレプリケーションは影響を受けません。                                            |
| `RENAME TABLE test.t1 TO test.ignore;`                 | 無視する   | 無視する      | `test.t1`イベント フィルター ルールに一致するため、 `RENAME TABLE`イベントは無視されます。4 `test.ignore`イベント フィルター ルールに一致するため、DDL イベントと DML イベントの両方が無視されます。 |

> **注記：**
>
> -   データベースにデータをレプリケーションする際は、イベントフィルターを使用してDDLイベントを慎重にフィルタリングしてください。レプリケーション中は、上流と下流のデータベーススキーマの整合性が維持されていることを確認してください。整合性が維持されていない場合、TiCDCはエラーを報告したり、未定義のレプリケーション動作を引き起こしたりする可能性があります。
> -   v6.5.8、v7.1.4、v7.5.1より前のバージョンでは、イベントフィルタを使用してテーブルの作成または削除を含むDDLイベントをフィルタリングすると、DMLレプリケーションに影響します。これらのバージョンでは、この機能の使用は推奨されません。
