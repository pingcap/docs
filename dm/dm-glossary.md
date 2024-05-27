---
title: TiDB Data Migration Glossary
summary: TiDB データ移行で使用される用語を学習します。
---

# TiDB データ移行用語集 {#tidb-data-migration-glossary}

このドキュメントでは、TiDB データ移行 (DM) のログ、監視、構成、およびドキュメントで使用される用語を示します。

## B {#b}

### Binlog {#binlog}

TiDB DM では、バイナリログは TiDB データベースで生成されるバイナリログファイルを指します。MySQL や MariaDB と同じ意味を持ちます。詳細は[MySQL バイナリログ](https://dev.mysql.com/doc/dev/mysql-server/latest/page_protocol_replication.html)と[MariaDB バイナリ ログ](https://mariadb.com/kb/en/library/binary-log/)を参照してください。

### Binlogイベント {#binlog-event}

Binlogイベントは、MySQL または MariaDBサーバーインスタンスに対して行われたデータ変更に関する情報です。これらのbinlogイベントは、binlogファイルに保存されます。詳細については、 [MySQLBinlogイベント](https://dev.mysql.com/doc/dev/mysql-server/latest/page_protocol_replication_binlog_event.html)と[MariaDBBinlogイベント](https://mariadb.com/kb/en/library/1-binlog-events/)を参照してください。

### Binlogイベント フィルター {#binlog-event-filter}

[Binlogイベント フィルター](/dm/dm-binlog-event-filter.md) 、ブロック リストと許可リストのフィルタリング ルールよりもきめ細かいフィルタリング機能です。詳細については、 [binlogイベント フィルター](/dm/dm-binlog-event-filter.md)を参照してください。

### Binlogの位置 {#binlog-position}

binlog位置は、 binlogファイル内のbinlogイベントのオフセット情報です。詳細については、 [MySQL `SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/8.0/en/show-binlog-events.html)と[MariaDB `SHOW BINLOG EVENTS`](https://mariadb.com/kb/en/library/show-binlog-events/)を参照してください。

### Binlogレプリケーション処理ユニット/同期ユニット {#binlog-replication-processing-unit-sync-unit}

Binlogログ レプリケーション処理ユニットは、DM-worker でアップストリーム バイナリログまたはローカル リレー ログを読み取り、これらのログをダウンストリームに移行するために使用する処理ユニットです。各サブタスクは、binlogレプリケーション処理ユニットに対応します。現在のドキュメントでは、binlogレプリケーション処理ユニットは同期処理ユニットとも呼ばれます。

### ブロックと許可テーブルリスト {#block-x26-allow-table-list}

ブロックおよび許可テーブルリストは、一部のデータベースまたは一部のテーブルのすべての操作をフィルタリングしたり、移行のみを行う機能です。詳細については[ブロックと許可のテーブルリスト](/dm/dm-block-allow-table-lists.md)を参照してください。この機能は[MySQL レプリケーション フィルタリング](https://dev.mysql.com/doc/refman/8.0/en/replication-rules.html)および[MariaDB レプリケーション フィルター](https://mariadb.com/kb/en/replication-filters/)に似ています。

## Ｃ {#c}

### チェックポイント {#checkpoint}

チェックポイントは、完全なデータ インポートまたは増分レプリケーション タスクが一時停止されて再開される位置、または停止されて再起動される位置を示します。

-   完全インポート タスクでは、チェックポイントは、インポート中のファイル内の正常にインポートされたデータのオフセットおよびその他の情報に対応します。チェックポイントは、データ インポート タスクと同期して更新されます。
-   増分レプリケーションでは、チェックポイントは、正常に解析され、ダウンストリームに移行された[binlogイベント](#binlog-event)の[binlogの位置](#binlog-position)およびその他の情報に対応します。チェックポイントは、DDL 操作が正常に移行された後、または最後の更新から 30 秒後に更新されます。

また、 [リレー処理装置](#relay-processing-unit)に対応する`relay.meta`情報は、チェックポイントと同様に機能します。リレー処理ユニットは、上流から[binlogイベント](#binlog-event)をプルしてこのイベントを[リレーログ](#relay-log)に書き込み、このイベントに対応する[binlogの位置](#binlog-position)または GTID 情報を`relay.meta`に書き込みます。

## だ {#d}

### ダンプ処理装置/ダンプユニット {#dump-processing-unit-dump-unit}

ダンプ処理単位は、DM-worker でアップストリームからすべてのデータをエクスポートするために使用される処理単位です。各サブタスクはダンプ処理単位に対応します。

## グ {#g}

### GTID {#gtid}

GTID は、MySQL または MariaDB のグローバル トランザクション ID です。この機能を有効にすると、GTID 情報がbinlogファイルに記録されます。複数の GTID が GTID セットを形成します。詳細については、 [MySQL GTID のフォーマットと保存](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids-concepts.html)と[MariaDB グローバルトランザクションID](https://mariadb.com/kb/en/library/gtid/)を参照してください。

## ら {#l}

### 負荷処理装置/負荷ユニット {#load-processing-unit-load-unit}

ロード処理ユニットは、完全にエクスポートされたデータをダウンストリームにインポートするために DM-worker で使用される処理ユニットです。各サブタスクはロード処理ユニットに対応します。現在のドキュメントでは、ロード処理ユニットはインポート処理ユニットとも呼ばれます。

## ま {#m}

### 移行/移行 {#migrate-migration}

TiDB データ移行ツールを使用して、上流データベースの**全データ**を下流データベースにコピーするプロセス。

「完全」と明記し、「完全または増分」とは明記せず、「完全 + 増分」と明記する場合は、replicate/replication ではなく migrate/migration を使用します。

## R {#r}

### リレーログ {#relay-log}

リレーログとは、DM-worker がアップストリームの MySQL または MariaDB から取得し、ローカルディスクに保存するbinlogファイルを指します。リレーログの形式は標準のbinlogファイルであり、互換バージョンの[mysqlbinlog](https://dev.mysql.com/doc/refman/8.0/en/mysqlbinlog.html)などのツールで解析できます。その役割は[MySQL リレーログ](https://dev.mysql.com/doc/refman/8.0/en/replica-logs-relaylog.html)や[MariaDB リレーログ](https://mariadb.com/kb/en/library/relay-log/)と同様です。

リレー ログのディレクトリ構造、初期移行ルール、TiDB DM のデータ消去などの詳細については、 [TiDB DMリレーログ](/dm/relay-log.md)を参照してください。

### リレー処理ユニット {#relay-processing-unit}

リレー処理ユニットは、DM-worker でアップストリームからbinlogファイルを取得し、リレー ログにデータを書き込むために使用される処理ユニットです。各 DM-worker インスタンスには、リレー処理ユニットが 1 つだけあります。

### 複製/レプリケーション {#replicate-replication}

TiDB データ移行ツールを使用して、上流データベースの**増分データ**を下流データベースにコピーするプロセス。

「増分」を明記する場合は、migrate/migration ではなく replicate/replication を使用します。

## S {#s}

### セーフモード {#safe-mode}

セーフ モードは、テーブル スキーマに主キーまたは一意のインデックスが存在する場合に、DML ステートメントを複数回インポートできるモードです。このモードでは、上流の一部のステートメントは、書き換えられた後にのみ下流に移行されます`INSERT`ステートメントは`REPLACE`に書き換えられ、 `UPDATE`ステートメントは`DELETE`と`REPLACE`に書き換えられます。

このモードは、次のいずれかの状況で有効になります。

-   タスク構成ファイルの`safe-mode`パラメータが`true`に設定されている場合、セーフ モードは有効のままになります。
-   シャード マージ シナリオでは、すべてのシャード テーブルで DDL ステートメントが複製される前は、セーフ モードが有効なままになります。
-   完全移行タスクのダンプ処理単位に引数`--consistency none`が設定されている場合、エクスポート開始時のbinlog の変更がエクスポートされたデータに影響するかどうかを判断できません。そのため、これらのbinlogの変更の増分レプリケーションではセーフ モードが有効なままになります。
-   タスクがエラーによって一時停止され、その後再開された場合、一部のデータに対する操作が 2 回実行される可能性があります。

### シャードDDL {#shard-ddl}

シャード DDL は、上流のシャード テーブルで実行される DDL ステートメントです。シャード テーブルをマージするプロセスで、TiDB DM によって調整および移行される必要があります。現在のドキュメントでは、シャード DDL はシャーディング DDL とも呼ばれます。

### シャードDDLロック {#shard-ddl-lock}

シャード DDL ロックは、シャード DDL の移行を調整するロック メカニズムです。詳細については、 [悲観的モードでのシャードテーブルからのデータのマージと移行の実装原則](/dm/feature-shard-merge-pessimistic.md#principles)を参照してください。現在のドキュメントでは、シャード DDL ロックはシャーディング DDL ロックとも呼ばれます。

### シャードグループ {#shard-group}

シャード グループとは、下流の同じテーブルにマージおよび移行される上流のシャード テーブルすべてです。2 レベルのシャード グループは、TiDB DM の実装に使用されます。詳細については、 [悲観的モードでのシャードテーブルからのデータのマージと移行の実装原則](/dm/feature-shard-merge-pessimistic.md#principles)を参照してください。現在のドキュメントでは、シャード グループはシャーディング グループとも呼ばれます。

### サブタスク {#subtask}

サブタスクは、各 DM ワーカー インスタンスで実行されているデータ移行タスクの一部です。さまざまなタスク構成では、単一のデータ移行タスクに 1 つのサブタスクまたは複数のサブタスクが含まれる場合があります。

### サブタスクのステータス {#subtask-status}

サブタスク ステータスは、データ移行サブタスクのステータスです。現在のステータス オプションには、 `New` 、 `Running` 、 `Paused` 、 `Stopped` 、および`Finished`があります。データ移行タスクまたはサブタスクのステータスの詳細については、 [サブタスクのステータス](/dm/dm-query-status.md#subtask-status)を参照してください。

## T {#t}

### テーブルルーティング {#table-routing}

テーブル ルーティング機能により、DM は上流の MySQL または MariaDB インスタンスの特定のテーブルを下流の指定されたテーブルに移行することができ、シャードされたテーブルをマージして移行するために使用できます。詳細については[テーブルルーティング](/dm/dm-table-routing.md)を参照してください。

### タスク {#task}

データ移行タスクは、 `start-task`コマンドを正常に実行した後に開始されます。さまざまなタスク構成では、単一の移行タスクを単一の DM ワーカー インスタンスで実行することも、複数の DM ワーカー インスタンスで同時に実行することもできます。

### タスクのステータス {#task-status}

タスク ステータスは、データ移行タスクのステータスを指します。タスク ステータスは、そのすべてのサブタスクのステータスに依存します。詳細については、 [サブタスクのステータス](/dm/dm-query-status.md#subtask-status)を参照してください。
