---
title: TiDB Data Migration Glossary
summary: Learn the terms used in TiDB Data Migration.
---

# TiDBデータ移行用語集 {#tidb-data-migration-glossary}

このドキュメントには、TiDBデータ移行（DM）のログ、監視、構成、およびドキュメントで使用される用語がリストされています。

## B {#b}

### ビンログ {#binlog}

TiDB DMでは、binlogsはTiDBデータベースで生成されたバイナリログファイルを参照します。 MySQLまたはMariaDBと同じ表示があります。詳細については、 [MySQLバイナリログ](https://dev.mysql.com/doc/internals/en/binary-log.html)と[MariaDBバイナリログ](https://mariadb.com/kb/en/library/binary-log/)を参照してください。

### Binlogイベント {#binlog-event}

Binlogイベントは、MySQLまたはMariaDBサーバーインスタンスに対して行われたデータ変更に関する情報です。これらのbinlogイベントは、binlogファイルに保存されます。詳細については、 [MySQLBinlogイベント](https://dev.mysql.com/doc/internals/en/binlog-event.html)と[MariaDBBinlogイベント](https://mariadb.com/kb/en/library/1-binlog-events/)を参照してください。

### Binlogイベントフィルター {#binlog-event-filter}

[Binlogイベントフィルター](/dm/dm-key-features.md#binlog-event-filter)は、ブロックおよび許可リストのフィルタリングルールよりもきめ細かいフィルタリング機能です。詳細は[binlogイベントフィルター](/dm/dm-overview.md#binlog-event-filtering)を参照してください。

### ビンログの位置 {#binlog-position}

binlog位置は、binlogファイル内のbinlogイベントのオフセット情報です。詳細については、 [MySQL `SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/8.0/en/show-binlog-events.html)と[MariaDB `SHOW BINLOG EVENTS`](https://mariadb.com/kb/en/library/show-binlog-events/)を参照してください。

### Binlogレプリケーション処理ユニット/同期ユニット {#binlog-replication-processing-unit-sync-unit}

Binlogレプリケーション処理ユニットは、DM-workerでアップストリームbinlogまたはローカルリレーログを読み取り、これらのログをダウンストリームに移行するために使用される処理ユニットです。各サブタスクは、binlogレプリケーション処理ユニットに対応します。現在のドキュメントでは、binlogレプリケーション処理ユニットは同期処理ユニットとも呼ばれます。

### テーブルリストをブロックして許可する {#block-x26-allow-table-list}

テーブルリストのブロックと許可は、一部のデータベースまたは一部のテーブルのすべての操作をフィルタリングまたは移行する機能です。詳細は[テーブルリストをブロックして許可する](/dm/dm-overview.md#block-and-allow-lists-migration-at-the-schema-and-table-levels)を参照してください。この機能は、 [MySQLレプリケーションフィルタリング](https://dev.mysql.com/doc/refman/5.6/en/replication-rules.html)および[MariaDBレプリケーションフィルター](https://mariadb.com/kb/en/replication-filters/)に似ています。

## C {#c}

### チェックポイント {#checkpoint}

チェックポイントは、完全なデータのインポートまたは増分レプリケーションタスクが一時停止して再開する位置、または停止して再開する位置を示します。

-   完全インポートタスクでは、チェックポイントは、インポートされているファイル内の正常にインポートされたデータのオフセットおよびその他の情報に対応します。チェックポイントは、データインポートタスクと同期して更新されます。
-   インクリメンタルレプリケーションでは、チェックポイントは、正常に解析されてダウンストリームに移行された[binlogの位置](#binlog-position)および[binlogイベント](#binlog-event)のその他の情報に対応します。チェックポイントは、DDL操作が正常に移行された後、または最後の更新から30秒後に更新されます。

また、 [リレー処理装置](#relay-processing-unit)に対応する`relay.meta`の情報は、チェックポイントと同様に機能します。リレー処理ユニットは、 [binlogイベント](#binlog-event)をアップストリームからプルしてこのイベントを[リレーログ](#relay-log)に書き込み、 [binlogの位置](#binlog-position)またはこのイベントに対応するGTID情報を`relay.meta`に書き込みます。

## D {#d}

### ダンプ処理装置/ダンプ装置 {#dump-processing-unit-dump-unit}

ダンプ処理装置は、DM-workerでアップストリームからすべてのデータをエクスポートするために使用される処理装置です。各サブタスクは、ダンプ処理ユニットに対応します。

## G {#g}

### GTID {#gtid}

GTIDは、MySQLまたはMariaDBのグローバルトランザクションIDです。この機能を有効にすると、GTID情報がbinlogファイルに記録されます。複数のGTIDがGTIDセットを形成します。詳細については、 [MySQLGTIDフォーマットとストレージ](https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-concepts.html)と[MariaDBグローバルトランザクションID](https://mariadb.com/kb/en/library/gtid/)を参照してください。

## L {#l}

### 負荷処理ユニット/負荷ユニット {#load-processing-unit-load-unit}

負荷処理ユニットは、完全にエクスポートされたデータをダウンストリームにインポートするためにDM-workerで使用される処理ユニットです。各サブタスクは、負荷処理ユニットに対応します。現在のドキュメントでは、ロード処理ユニットはインポート処理ユニットとも呼ばれます。

## M {#m}

### 移行/移行 {#migrate-migration}

TiDBデータ移行ツールを使用して、アップストリームデータベースの**完全なデータ**をダウンストリームデータベースにコピーするプロセス。

「フル」を明示的に言及し、「フルまたはインクリメンタル」を明示的に言及せず、「フル+インクリメンタル」を明確に言及する場合は、レプリケート/レプリケーションの代わりに移行/移行を使用してください。

## R {#r}

### リレーログ {#relay-log}

リレーログは、DM-workerがアップストリームのMySQLまたはMariaDBからプルし、ローカルディスクに保存するbinlogファイルを参照します。リレーログの形式は標準のbinlogファイルであり、互換性のあるバージョンの[mysqlbinlog](https://dev.mysql.com/doc/refman/8.0/en/mysqlbinlog.html)などのツールで解析できます。その役割は[MySQLリレーログ](https://dev.mysql.com/doc/refman/5.7/en/replica-logs-relaylog.html)と[MariaDBリレーログ](https://mariadb.com/kb/en/library/relay-log/)に似ています。

リレーログのディレクトリ構造、初期移行ルール、TiDB DMでのデータパージなどの詳細については、 [TiDBDMリレーログ](/dm/relay-log.md)を参照してください。

### リレー処理装置 {#relay-processing-unit}

リレー処理ユニットは、DM-workerでアップストリームからbinlogファイルをプルし、リレーログにデータを書き込むために使用される処理ユニットです。各DM-workerインスタンスには、リレー処理ユニットが1つだけあります。

### 複製/複製 {#replicate-replication}

TiDBデータ移行ツールを使用して、アップストリームデータベースの**インクリメンタルデータ**をダウンストリームデータベースにコピーするプロセス。

「インクリメンタル」について明確に言及する場合は、移行/移行の代わりにレプリケート/レプリケーションを使用してください。

## S {#s}

### セーフモード {#safe-mode}

セーフモードは、主キーまたは一意のインデックスがテーブルスキーマに存在する場合に、DMLステートメントを複数回インポートできるモードです。このモードでは、アップストリームからの一部のステートメントは、書き直された後にのみダウンストリームに移行されます。 `INSERT`ステートメントは`REPLACE`として書き直されます。 `UPDATE`ステートメントは`DELETE`および`REPLACE`として書き直されます。

このモードは、次のいずれかの状況で有効になります。

-   タスク構成ファイルの`safe-mode`パラメーターが`true`に設定されている場合、セーフモードは有効なままです。
-   シャードマージシナリオでは、すべてのシャードテーブルにDDLステートメントが複製される前に、セーフモードが有効のままになります。
-   引数`--consistency none`が完全マイグレーション・タスクのダンプ処理装置用に構成されている場合、エクスポートの開始時にbinlogの変更がエクスポートされたデータに影響を与えるかどうかを判別できません。したがって、これらのbinlog変更の増分レプリケーションでは、セーフモードが有効のままになります。
-   タスクがエラーによって一時停止されてから再開された場合、一部のデータに対する操作が2回実行される可能性があります。

### シャードDDL {#shard-ddl}

シャードDDLは、アップストリームのシャードテーブルで実行されるDDLステートメントです。シャーディングされたテーブルをマージするプロセスでは、TiDBDMによって調整および移行する必要があります。現在のドキュメントでは、シャードDDLはシャーディングDDLとも呼ばれます。

### シャードDDLロック {#shard-ddl-lock}

シャードDDLロックは、シャードDDLの移行を調整するロックメカニズムです。詳細は[悲観的モードでシャーディングされたテーブルからデータをマージおよび移行する実装原則](/dm/feature-shard-merge-pessimistic.md#principles)を参照してください。現在のドキュメントでは、シャードDDLロックはシャーディングDDLロックとも呼ばれます。

### シャードグループ {#shard-group}

シャードグループは、ダウンストリームの同じテーブルにマージおよび移行されるすべてのアップストリームシャードテーブルです。 TiDB DMの実装には、2レベルのシャードグループが使用されます。詳細は[悲観的モードでシャーディングされたテーブルからデータをマージおよび移行する実装原則](/dm/feature-shard-merge-pessimistic.md#principles)を参照してください。現在のドキュメントでは、シャードグループはシャーディンググループとも呼ばれています。

### サブタスク {#subtask}

サブタスクは、各DM-workerインスタンスで実行されているデータ移行タスクの一部です。異なるタスク構成では、単一のデータ移行タスクに1つのサブタスクまたは複数のサブタスクが含まれる場合があります。

### サブタスクのステータス {#subtask-status}

サブタスクステータスは、データ移行サブタスクのステータスです。現在のステータスオプションには、 `New` 、および`Running`が`Stopped` `Finished` `Paused` 。データ移行タスクまたはサブタスクのステータスの詳細については、 [サブタスクステータス](/dm/dm-query-status.md#subtask-status)を参照してください。

## T {#t}

### テーブルルーティング {#table-routing}

テーブルルーティング機能を使用すると、DMはアップストリームのMySQLまたはMariaDBインスタンスの特定のテーブルをダウンストリームの指定されたテーブルに移行できます。これを使用して、シャーディングされたテーブルをマージおよび移行できます。詳細は[テーブルルーティング](/dm/dm-key-features.md#table-routing)を参照してください。

### 仕事 {#task}

`start-task`コマンドを正常に実行した後に開始されるデータ移行タスク。さまざまなタスク構成では、単一の移行タスクを単一のDM-workerインスタンスまたは複数のDM-workerインスタンスで同時に実行できます。

### タスクステータス {#task-status}

タスクステータスは、データ移行タスクのステータスを指します。タスクのステータスは、そのすべてのサブタスクのステータスによって異なります。詳細は[サブタスクステータス](/dm/dm-query-status.md#subtask-status)を参照してください。
