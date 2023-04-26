---
title: TiDB Data Migration Glossary
summary: Learn the terms used in TiDB Data Migration.
---

# TiDB データ移行用語集 {#tidb-data-migration-glossary}

このドキュメントでは、TiDB Data Migration (DM) のログ、監視、構成、およびドキュメントで使用される用語を一覧表示します。

## B {#b}

### Binlog {#binlog}

TiDB DM では、binlog は TiDB データベースで生成されたバイナリ ログ ファイルを参照します。 MySQL や MariaDB と同様の表示があります。詳細は[MySQL バイナリ ログ](https://dev.mysql.com/doc/internals/en/binary-log.html)と[MariaDB バイナリ ログ](https://mariadb.com/kb/en/library/binary-log/)を参照してください。

### Binlogイベント {#binlog-event}

Binlogイベントは、MySQL または MariaDBサーバーインスタンスに対して行われたデータ変更に関する情報です。これらのbinlogイベントはbinlogファイルに保存されます。詳細は[MySQLBinlogイベント](https://dev.mysql.com/doc/internals/en/binlog-event.html)と[MariaDB Binlogイベント](https://mariadb.com/kb/en/library/1-binlog-events/)を参照してください。

### Binlogイベント フィルター {#binlog-event-filter}

[Binlogイベント フィルター](/dm/dm-binlog-event-filter.md)は、ブロックおよび許可リストのフィルタリング ルールよりもきめ細かいフィルタリング機能です。詳細は[binlogイベント フィルタ](/dm/dm-binlog-event-filter.md)を参照してください。

### Binlogの位置 {#binlog-position}

binlog位置は、 binlogファイル内のbinlogイベントのオフセット情報です。詳細は[MySQL `SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/8.0/en/show-binlog-events.html)と[MariaDB `SHOW BINLOG EVENTS`](https://mariadb.com/kb/en/library/show-binlog-events/)を参照してください。

### Binlogレプリケーション処理ユニット/同期ユニット {#binlog-replication-processing-unit-sync-unit}

Binlogレプリケーション処理ユニットは、上流のバイナリ ログまたはローカル リレー ログを読み取り、これらのログを下流に移行するために DM-worker で使用される処理ユニットです。各サブタスクは、binlogレプリケーション処理ユニットに対応します。現在のドキュメントでは、binlogレプリケーション処理ユニットは同期処理ユニットとも呼ばれます。

### ブロック &amp; 許可テーブル リスト {#block-x26-allow-table-list}

ブロック &amp; 許可テーブル リストは、一部のデータベースまたは一部のテーブルのすべての操作をフィルタリングまたは移行する機能です。詳細は[ブロック &amp; 許可テーブル リスト](/dm/dm-block-allow-table-lists.md)を参照してください。この機能は[MySQL レプリケーション フィルタリング](https://dev.mysql.com/doc/refman/5.6/en/replication-rules.html)および[MariaDB レプリケーション フィルター](https://mariadb.com/kb/en/replication-filters/)に似ています。

## ハ {#c}

### チェックポイント {#checkpoint}

チェックポイントは、完全なデータ インポートまたは増分レプリケーション タスクが一時停止されてから再開されるか、または停止されてから再開される位置を示します。

-   フル インポート タスクでは、チェックポイントは、インポート中のファイル内の正常にインポートされたデータのオフセットおよびその他の情報に対応します。チェックポイントは、データ インポート タスクと同期して更新されます。
-   増分レプリケーションでは、チェックポイントは、正常に解析されてダウンストリームに移行される[binlogイベント](#binlog-event)の[binlog位置](#binlog-position)およびその他の情報に対応します。 DDL 操作が正常に移行された後、または最後の更新から 30 秒後に、チェックポイントが更新されます。

また、 [中継処理ユニット](#relay-processing-unit)に対応する`relay.meta`情報は、チェックポイントと同様に機能します。中継処理部は上流から[binlogイベント](#binlog-event)引っ張ってこのイベントを[中継ログ](#relay-log)に書き込み、 [binlog位置](#binlog-position)またはこのイベントに対応する GTID 情報を`relay.meta`に書き込みます。

## D {#d}

### ダンプ処理単位/ダンプ単位 {#dump-processing-unit-dump-unit}

ダンプ処理単位は、アップストリームからすべてのデータをエクスポートするために DM-worker で使用される処理単位です。各サブタスクは、ダンプ処理単位に対応します。

## G {#g}

### GTID {#gtid}

GTID は、MySQL または MariaDB のグローバル トランザクション ID です。この機能を有効にすると、GTID 情報がbinlogファイルに記録されます。複数の GTID が GTID セットを形成します。詳細は[MySQL GTID のフォーマットとストレージ](https://dev.mysql.com/doc/refman/5.7/en/replication-gtids-concepts.html)と[MariaDB グローバルトランザクションID](https://mariadb.com/kb/en/library/gtid/)を参照してください。

## L {#l}

### 負荷処理装置/負荷装置 {#load-processing-unit-load-unit}

ロード処理単位は、完全にエクスポートされたデータをダウンストリームにインポートするために DM-worker で使用される処理単位です。各サブタスクは、負荷処理ユニットに対応します。現在のドキュメントでは、ロード処理ユニットはインポート処理ユニットとも呼ばれます。

## M {#m}

### 移行/移行 {#migrate-migration}

TiDB データ移行ツールを使用して、アップストリーム データベースの**完全なデータを**ダウンストリーム データベースにコピーするプロセス。

「完全」と明確に言及し、「完全または増分」と明確に言及せず、「完全 + 増分」と明確に言及する場合は、複製/複製の代わりに移行/移行を使用します。

## R {#r}

### 中継ログ {#relay-log}

リレー ログは、DM-worker がアップストリームの MySQL または MariaDB から取得し、ローカル ディスクに保存するbinlogファイルを参照します。リレー ログの形式は標準のbinlogファイルで、互換性のあるバージョンの[mysqlbinlog](https://dev.mysql.com/doc/refman/8.0/en/mysqlbinlog.html)などのツールで解析できます。その役割は[MySQL リレー ログ](https://dev.mysql.com/doc/refman/5.7/en/replica-logs-relaylog.html)および[MariaDB リレー ログ](https://mariadb.com/kb/en/library/relay-log/)に似ています。

リレー ログのディレクトリ構造、初期移行ルール、TiDB DM でのデータ パージなどの詳細については、 [TiDB DMリレーログ](/dm/relay-log.md)を参照してください。

### 中継処理ユニット {#relay-processing-unit}

リレー処理ユニットは、DM-worker でbinlogファイルを上流からプルし、リレー ログにデータを書き込むために使用される処理ユニットです。各 DM-worker インスタンスには、リレー処理ユニットが 1 つだけあります。

### 複製/複製 {#replicate-replication}

TiDB データ移行ツールを使用して、アップストリーム データベースの**増分データを**ダウンストリーム データベースにコピーするプロセス。

「増分」と明示する場合は、migrate/migration ではなく、replicate/replication を使用してください。

## S {#s}

### セーフモード {#safe-mode}

セーフ モードは、主キーまたは一意のインデックスがテーブル スキーマに存在する場合に、DML ステートメントを複数回インポートできるモードです。このモードでは、アップストリームからの一部のステートメントは、書き直された後にのみダウンストリームに移行されます。 `INSERT`ステートメントは`REPLACE`として書き直されます。 `UPDATE`ステートメントは`DELETE`および`REPLACE`として書き直されます。

このモードは、次のいずれかの状況で有効になります。

-   タスク構成ファイルの`safe-mode`パラメーターが`true`に設定されている場合、セーフ モードは有効なままです。
-   シャード マージのシナリオでは、DDL ステートメントがすべてのシャード テーブルで複製される前に、セーフ モードが有効なままになります。
-   引数`--consistency none`がフル マイグレーション タスクのダンプ処理単位に設定されている場合、エクスポートの開始時のbinlog の変更がエクスポートされたデータに影響するかどうかを判断できません。したがって、これらのbinlogの変更の増分レプリケーションでは、セーフ モードが有効なままになります。
-   タスクがエラーによって一時停止され、再開された場合、一部のデータに対する操作が 2 回実行される可能性があります。

### シャード DDL {#shard-ddl}

シャード DDL は、アップストリームのシャード テーブルで実行される DDL ステートメントです。シャードされたテーブルをマージするプロセスで、TiDB DM によって調整および移行される必要があります。現在のドキュメントでは、シャード DDL はシャーディング DDL とも呼ばれます。

### シャード DDL ロック {#shard-ddl-lock}

シャード DDL ロックは、シャード DDL の移行を調整するロック メカニズムです。詳細は[悲観的モードでのシャード テーブルからのデータのマージと移行の実装原則](/dm/feature-shard-merge-pessimistic.md#principles)を参照してください。現在のドキュメントでは、シャード DDL ロックはシャーディング DDL ロックとも呼ばれます。

### シャードグループ {#shard-group}

シャード グループは、マージされてダウンストリームの同じテーブルに移行されるすべてのアップストリーム シャード テーブルです。 TiDB DM の実装には、2 レベルのシャード グループが使用されます。詳細は[悲観的モードでのシャード テーブルからのデータのマージと移行の実装原則](/dm/feature-shard-merge-pessimistic.md#principles)を参照してください。現在のドキュメントでは、シャード グループはシャーディング グループとも呼ばれます。

### サブタスク {#subtask}

サブタスクは、各 DM-worker インスタンスで実行されるデータ移行タスクの一部です。異なるタスク構成では、1 つのデータ移行タスクに 1 つまたは複数のサブタスクが含まれる場合があります。

### サブタスクのステータス {#subtask-status}

サブタスクのステータスは、データ移行サブタスクのステータスです。現在のステータス オプションには、 `New` 、 `Running` 、 `Paused` 、 `Stopped` 、および`Finished`が含まれます。データ移行タスクまたはサブタスクのステータスの詳細については、 [サブタスクのステータス](/dm/dm-query-status.md#subtask-status)を参照してください。

## T {#t}

### テーブル ルーティング {#table-routing}

テーブル ルーティング機能により、DM はアップストリームの MySQL または MariaDB インスタンスの特定のテーブルを、シャード テーブルのマージと移行に使用できるダウンストリームの指定されたテーブルに移行できます。詳細は[テーブル ルーティング](/dm/dm-table-routing.md)を参照してください。

### タスク {#task}

`start-task`コマンドを正常に実行した後に開始されるデータ移行タスク。異なるタスク構成では、1 つの移行タスクを 1 つの DM-worker インスタンスまたは複数の DM-worker インスタンスで同時に実行できます。

### タスクのステータス {#task-status}

タスク ステータスは、データ移行タスクのステータスを示します。タスクのステータスは、そのすべてのサブタスクのステータスによって異なります。詳細は[サブタスクのステータス](/dm/dm-query-status.md#subtask-status)を参照してください。
