---
title: TiDB Data Migration Glossary
summary: TiDB データ移行で使用される用語を学習します。
---

# TiDB データ移行用語集 {#tidb-data-migration-glossary}

このドキュメントでは、TiDB データ移行 (DM) のログ、監視、構成、およびドキュメントで使用される用語を示します。

TiDB 関連の用語と定義については、 [TiDB用語集](/glossary.md)参照してください。

## B {#b}

### Binlog {#binlog}

TiDB DMにおけるbinlogは、TiDBデータベース内で生成されるバイナリログファイルを指します。MySQLやMariaDBにおけるbinlogと同様の意味を持ちます。詳細は[MySQL バイナリログ](https://dev.mysql.com/doc/dev/mysql-server/latest/page_protocol_replication.html)と[MariaDB バイナリログ](https://mariadb.com/docs/server/server-management/server-monitoring-logs/binary-log)参照してください。

### Binlogイベント {#binlog-event}

Binlogイベントは、MySQLまたはMariaDBサーバーインスタンスに対するデータ変更に関する情報です。これらのbinlogイベントはbinlogファイルに保存されます。詳細は[MySQLBinlogイベント](https://dev.mysql.com/doc/dev/mysql-server/latest/page_protocol_replication_binlog_event.html)と[MariaDBBinlogイベント](https://mariadb.com/docs/server/reference/clientserver-protocol/replication-protocol/1-binlog-events)を参照してください。

### Binlogイベントフィルター {#binlog-event-filter}

[Binlogイベントフィルター](/dm/dm-binlog-event-filter.md) 、ブロックリストと許可リストのフィルタリングルールよりもきめ細かなフィルタリング機能です。詳細は[binlogイベントフィルター](/dm/dm-binlog-event-filter.md)を参照してください。

### Binlogの位置 {#binlog-position}

binlog位置は、 binlogファイル内のbinlogイベントのオフセット情報です。詳細は[MySQL `SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/8.0/en/show-binlog-events.html)と[MariaDB `SHOW BINLOG EVENTS`](https://mariadb.com/docs/server/reference/sql-statements/administrative-sql-statements/show/show-binlog-events)参照してください。

### Binlog複製処理ユニット/同期ユニット {#binlog-replication-processing-unit-sync-unit}

Binlogログレプリケーション処理ユニットは、DM-workerにおいて上流のバイナリログまたはローカルリレーログを読み取り、これらのログを下流に移行するために使用される処理ユニットです。各サブタスクは1つのbinlogレプリケーション処理ユニットに対応します。現在のドキュメントでは、binlogログレプリケーション処理ユニットは同期処理ユニットとも呼ばれます。

### ブロックと許可テーブルリスト {#block-x26-allow-table-list}

ブロック・許可テーブルリストは、特定のデータベースまたはテーブルに対するすべての操作をフィルタリングしたり、移行対象のみを選択したりする機能です。詳細は[ブロックと許可のテーブルリスト](/dm/dm-block-allow-table-lists.md)を参照してください。この機能は[MySQL レプリケーション フィルタリング](https://dev.mysql.com/doc/refman/8.0/en/replication-rules.html)および[MariaDB レプリケーションフィルター](https://mariadb.com/docs/server/ha-and-performance/standard-replication/replication-filters)に類似しています。

## C {#c}

### チェックポイント {#checkpoint}

チェックポイントは、完全なデータ インポートまたは増分レプリケーション タスクが一時停止されて再開される位置、または停止されて再起動される位置を示します。

-   フルインポートタスクでは、チェックポイントは、インポート対象のファイル内の正常にインポートされたデータのオフセットなどの情報に対応します。チェックポイントは、データインポートタスクと同期して更新されます。
-   増分レプリケーションでは、チェックポイントは、正常に解析され下流に移行された[binlogイベント](#binlog-event)の[binlogの位置](#binlog-position)とその他の情報に対応します。チェックポイントは、DDL操作が正常に移行された後、または最後の更新から30秒後に更新されます。

さらに、 [リレー処理装置](#relay-processing-unit)に対応する`relay.meta`情報はチェックポイントと同様に機能します。リレー処理ユニットは上流から[binlogイベント](#binlog-event)を取得し、このイベントを[リレーログ](#relay-log)に書き込み、このイベントに対応する[binlogの位置](#binlog-position)またはGTID情報を`relay.meta`に書き込みます。

## D {#d}

### ダンプ処理装置/ダンプユニット {#dump-processing-unit-dump-unit}

ダンプ処理単位は、DM-worker において上流からのすべてのデータをエクスポートするために使用される処理単位です。各サブタスクは 1 つのダンプ処理単位に対応します。

## G {#g}

### GTID {#gtid}

GTIDはMySQLまたはMariaDBのグローバルトランザクションIDです。この機能を有効にすると、GTID情報がbinlogファイルに記録されます。複数のGTIDはGTIDセットを形成します。詳細は[MySQL GTID のフォーマットと保存](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids-concepts.html)と[MariaDB グローバルトランザクションID](https://mariadb.com/docs/server/ha-and-performance/standard-replication/gtid)を参照してください。

## L {#l}

### 負荷処理ユニット/負荷ユニット {#load-processing-unit-load-unit}

ロード処理単位は、DM-workerにおいて、完全にエクスポートされたデータを下流にインポートするために用いられる処理単位です。各サブタスクはロード処理単位に対応します。このドキュメントでは、ロード処理単位はインポート処理単位とも呼ばれます。

## M {#m}

### 移行/移行 {#migrate-migration}

TiDB データ移行ツールを使用して、アップストリーム データベースの**完全なデータを**ダウンストリーム データベースにコピーするプロセス。

「完全」と明記している場合、「完全または増分」とは明記していない場合、「完全 + 増分」と明記している場合は、replicate/replication ではなく migrate/migration を使用します。

## R {#r}

### リレーログ {#relay-log}

リレーログとは、DM-workerが上流のMySQLまたはMariaDBから取得し、ローカルディスクに保存するbinlogファイルを指します。リレーログの形式は標準的なbinlogファイルであり、互換性のあるバージョンの[mysqlbinlog](https://dev.mysql.com/doc/refman/8.0/en/mysqlbinlog.html)などのツールで解析できます。その役割は[MySQLリレーログ](https://dev.mysql.com/doc/refman/8.0/en/replica-logs-relaylog.html)および[MariaDB リレーログ](https://mariadb.com/docs/server/server-management/server-monitoring-logs/binary-log/relay-log)と同様です。

リレー ログのディレクトリ構造、初期移行ルール、TiDB DM のデータ パージなどの詳細については、 [TiDB DMリレーログ](/dm/relay-log.md)参照してください。

### リレー処理ユニット {#relay-processing-unit}

リレー処理ユニットは、DM-worker において上流からbinlogファイルを取得し、リレーログにデータを書き込むために使用される処理ユニットです。各 DM-worker インスタンスには、リレー処理ユニットが 1 つだけ存在します。

### 複製/レプリケーション {#replicate-replication}

TiDB データ移行ツールを使用して、上流データベースの**増分データを**下流データベースにコピーするプロセス。

「増分」を明確に記載する場合は、 migrate/migration ではなく、replicate/replication を使用します。

## S {#s}

### セーフモード {#safe-mode}

セーフモードは、テーブルスキーマに主キーまたは一意のインデックスが存在する場合に、DML文を複数回インポートできるモードです。このモードでは、上流の文の一部は、書き換えられた後にのみ下流に移行されます。1 `INSERT`文は`REPLACE`に書き換えられ、 `UPDATE`文は`DELETE`と`REPLACE`に書き換えられます。

このモードは、次のいずれかの状況で有効になります。

-   タスク構成ファイルの`safe-mode`パラメータが`true`に設定されている場合、セーフ モードは有効なままになります。
-   シャードマージのシナリオでは、すべてのシャードテーブルで DDL ステートメントが複製される前は、セーフ モードが有効なままになります。
-   完全移行タスクのダンプ処理単位に引数`--consistency none`設定されている場合、エクスポート開始時のbinlogの変更がエクスポートされたデータに影響を与えるかどうかを判断できません。そのため、これらのbinlogの変更の増分レプリケーションではセーフモードが有効なままになります。
-   タスクがエラーによって一時停止され、その後再開された場合、一部のデータに対する操作が 2 回実行される可能性があります。

### シャードDDL {#shard-ddl}

シャードDDLは、上流のシャードテーブルに対して実行されるDDL文です。シャードテーブルのマージプロセスにおいて、TiDB DMによって調整および移行される必要があります。現在のドキュメントでは、シャードDDLはシャーディングDDLとも呼ばれています。

### シャードDDLロック {#shard-ddl-lock}

シャードDDLロックは、シャードDDLの移行を調整するロックメカニズムです。詳細は[悲観的モードでのシャードテーブルからのデータのマージと移行の実装原則](/dm/feature-shard-merge-pessimistic.md#principles)を参照してください。現在のドキュメントでは、シャードDDLロックはシャーディングDDLロックとも呼ばれています。

### シャードグループ {#shard-group}

シャードグループとは、下流の同じテーブルにマージおよび移行される上流のシャードテーブルすべてを指します。TiDB DMの実装では、2階層のシャードグループが使用されます。詳細は[悲観的モードでのシャードテーブルからのデータのマージと移行の実装原則](/dm/feature-shard-merge-pessimistic.md#principles)を参照してください。現在のドキュメントでは、シャードグループはシャーディンググループとも呼ばれます。

### サブタスク {#subtask}

サブタスクは、各 DM ワーカーインスタンスで実行されるデータ移行タスクの一部です。タスク構成によっては、1 つのデータ移行タスクに 1 つのサブタスクが含まれる場合もあれば、複数のサブタスクが含まれる場合もあります。

### サブタスクのステータス {#subtask-status}

サブタスクステータスは、データ移行サブタスクのステータスです。現在のステータスオプションには、 `New` 、 `Running` 、 `Paused` 、 `Stopped` 、 `Finished`あります。データ移行タスクまたはサブタスクのステータスの詳細については、 [サブタスクのステータス](/dm/dm-query-status.md#subtask-status)を参照してください。

## T {#t}

### テーブルルーティング {#table-routing}

テーブルルーティング機能により、DMは上流のMySQLまたはMariaDBインスタンスの特定のテーブルを下流の指定されたテーブルに移行できます。この機能は、シャードテーブルのマージと移行に使用できます。詳細は[テーブルルーティング](/dm/dm-table-routing.md)を参照してください。

### タスク {#task}

データ移行タスクは、コマンド`start-task`実行に成功した後に開始されます。タスク構成によっては、単一の移行タスクを単一のDMワーカーインスタンスで実行することも、複数のDMワーカーインスタンスで同時に実行することもできます。

### タスクのステータス {#task-status}

タスクステータスは、データ移行タスクのステータスを指します。タスクステータスは、そのすべてのサブタスクのステータスに依存します。詳細は[サブタスクのステータス](/dm/dm-query-status.md#subtask-status)を参照してください。
