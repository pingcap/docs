---
title: TiDB Data Migration Glossary
summary: Learn the terms used in TiDB Data Migration.
---

# TiDB データ移行用語集 {#tidb-data-migration-glossary}

この文書には、TiDB Data Migration (DM) のログ、モニタリング、構成、およびドキュメントで使用される用語がリストされています。

## B {#b}

### Binlog {#binlog}

TiDB DM では、binlog は TiDB データベースで生成されたバイナリ ログ ファイルを指します。 MySQL や MariaDB と同じ兆候があります。詳細は[MySQLバイナリログ](https://dev.mysql.com/doc/dev/mysql-server/latest/page_protocol_replication.html)と[MariaDB バイナリ ログ](https://mariadb.com/kb/en/library/binary-log/)を参照してください。

### Binlogイベント {#binlog-event}

Binlogイベントは、MySQL または MariaDBサーバーインスタンスに対して行われたデータ変更に関する情報です。これらのbinlogイベントはbinlogファイルに保存されます。詳細は[MySQLBinlogイベント](https://dev.mysql.com/doc/dev/mysql-server/latest/page_protocol_replication_binlog_event.html)と[MariaDBBinlogイベント](https://mariadb.com/kb/en/library/1-binlog-events/)を参照してください。

### Binlogイベントフィルター {#binlog-event-filter}

[Binlogイベントフィルター](/dm/dm-binlog-event-filter.md)は、ブロックおよび許可リストのフィルタリング ルールよりも詳細なフィルタリング機能です。詳細は[binlogイベントフィルター](/dm/dm-binlog-event-filter.md)を参照してください。

### Binlog位置 {#binlog-position}

binlog位置は、 binlogファイル内のbinlogイベントのオフセット情報です。詳細は[MySQL の`SHOW BINLOG EVENTS`](https://dev.mysql.com/doc/refman/8.0/en/show-binlog-events.html)と[MariaDB `SHOW BINLOG EVENTS`](https://mariadb.com/kb/en/library/show-binlog-events/)を参照してください。

### Binlogレプリケーション処理ユニット/同期ユニット {#binlog-replication-processing-unit-sync-unit}

Binlogレプリケーション処理ユニットは、DM ワーカーで上流のビンログまたはローカル リレー ログを読み取り、これらのログを下流に移行するために使用される処理ユニットです。各サブタスクは、binlog複製処理単位に対応します。現在のドキュメントでは、binlog複製処理ユニットは同期処理ユニットとも呼ばれます。

### ブロックおよび許可テーブルのリスト {#block-x26-allow-table-list}

ブロックおよび許可テーブル リストは、一部のデータベースまたは一部のテーブルのすべての操作をフィルタリングするか、移行のみを行う機能です。詳細は[ブロックおよび許可テーブルリスト](/dm/dm-block-allow-table-lists.md)を参照してください。この機能は[MySQL レプリケーション フィルタリング](https://dev.mysql.com/doc/refman/8.0/en/replication-rules.html)および[MariaDB レプリケーション フィルター](https://mariadb.com/kb/en/replication-filters/)に似ています。

## C {#c}

### チェックポイント {#checkpoint}

チェックポイントは、完全データ インポートまたは増分レプリケーション タスクが一時停止して再開される位置、または停止して再開される位置を示します。

-   完全インポート タスクでは、チェックポイントは、インポート中のファイル内の正常にインポートされたデータのオフセットおよびその他の情報に対応します。チェックポイントは、データ インポート タスクと同期して更新されます。
-   インクリメンタル レプリケーションでは、チェックポイントは[binlogの位置](#binlog-position)と、正常に解析されてダウンストリームに移行された[binlogイベント](#binlog-event)のその他の情報に対応します。チェックポイントは、DDL 操作が正常に移行された後、または最後の更新から 30 秒後に更新されます。

さらに、 [中継処理装置](#relay-processing-unit)に対応する`relay.meta`情報はチェックポイントと同様に機能します。中継処理部は上流から[binlogイベント](#binlog-event)プルして[リレーログ](#relay-log)にこのイベントを書き込み、 `relay.meta`に[binlogの位置](#binlog-position)またはこのイベントに対応する GTID 情報を書き込みます。

## D {#d}

### ダンプ処理ユニット/ダンプユニット {#dump-processing-unit-dump-unit}

ダンプ処理単位は、DM-worker で上流からすべてのデータをエクスポートするために使用される処理単位です。各サブタスクはダンプ処理単位に対応します。

## G {#g}

### GTID {#gtid}

GTID は、MySQL または MariaDB のグローバル トランザクション ID です。この機能を有効にすると、GTID 情報がbinlogファイルに記録されます。複数の GTID が GTID セットを形成します。詳細は[MySQL GTID の形式とストレージ](https://dev.mysql.com/doc/refman/8.0/en/replication-gtids-concepts.html)と[MariaDB グローバルトランザクションID](https://mariadb.com/kb/en/library/gtid/)を参照してください。

## L {#l}

### ロードプロセッシングユニット/ロードユニット {#load-processing-unit-load-unit}

ロード処理ユニットは、完全にエクスポートされたデータをダウンストリームにインポートするために DM ワーカーで使用される処理ユニットです。各サブタスクはロード処理単位に対応します。現在のドキュメントでは、ロード処理ユニットはインポート処理ユニットとも呼ばれます。

## M {#m}

### 移行/移行 {#migrate-migration}

TiDB データ移行ツールを使用して、アップストリーム データベースの**完全なデータを**ダウンストリーム データベースにコピーするプロセス。

「フル」と明記されている場合、「フルまたはインクリメンタル」と明示されていない場合、および「フル + インクリメンタル」と明記されている場合は、レプリケート/レプリケーションの代わりに移行/移行を使用してください。

## R {#r}

### リレーログ {#relay-log}

リレー ログは、DM ワーカーが上流の MySQL または MariaDB から取得し、ローカル ディスクに保存するbinlogファイルを指します。リレー ログの形式は標準のbinlogファイルであり、互換性のあるバージョンの[mysqlbinlog](https://dev.mysql.com/doc/refman/8.0/en/mysqlbinlog.html)などのツールで解析できます。その役割は[MySQLリレーログ](https://dev.mysql.com/doc/refman/8.0/en/replica-logs-relaylog.html)および[MariaDB リレーログ](https://mariadb.com/kb/en/library/relay-log/)と似ています。

リレー ログのディレクトリ構造、初期移行ルール、TiDB DM でのデータ パージなどの詳細については、 [TiDB DMリレーログ](/dm/relay-log.md)を参照してください。

### 中継処理装置 {#relay-processing-unit}

リレー処理ユニットは、上流からbinlogファイルを取得し、データをリレー ログに書き込むために DM ワーカーで使用される処理ユニットです。各 DM ワーカー インスタンスにはリレー処理ユニットが 1 つだけあります。

### 複製/レプリケーション {#replicate-replication}

TiDB データ移行ツールを使用して、アップストリーム データベースの**増分データを**ダウンストリーム データベースにコピーするプロセス。

「増分」と明記する場合は、移行/移行ではなく複製/レプリケーションを使用してください。

## S {#s}

### セーフモード {#safe-mode}

セーフ モードは、テーブル スキーマに主キーまたは一意のインデックスが存在する場合に、DML ステートメントを複数回インポートできるモードです。このモードでは、上流からの一部のステートメントは、書き直された後にのみ下流に移行されます。 `INSERT`ステートメントは`REPLACE`として書き直されます。 `UPDATE`ステートメントは`DELETE`および`REPLACE`として書き直されます。

このモードは、次のいずれかの状況で有効になります。

-   タスク構成ファイルの`safe-mode`パラメーターが`true`に設定されている場合、セーフ モードは有効なままになります。
-   シャード マージ シナリオでは、DDL ステートメントがすべてのシャード テーブルにレプリケートされる前に、セーフ モードが有効なままになります。
-   引数`--consistency none`が完全移行タスクのダンプ処理単位に構成されている場合、エクスポート開始時のbinlogの変更がエクスポートされたデータに影響を与えるかどうかを判断できません。したがって、これらのbinlog変更の増分レプリケーションに対してセーフ モードは有効なままになります。
-   タスクがエラーによって一時停止されてから再開されると、一部のデータに対する操作が 2 回実行される可能性があります。

### シャードDDL {#shard-ddl}

シャード DDL は、上流のシャード テーブルで実行される DDL ステートメントです。シャードテーブルを結合するプロセスで、TiDB DM によって調整および移行する必要があります。現在のドキュメントでは、シャード DDL はシャーディング DDL とも呼ばれます。

### シャード DDL ロック {#shard-ddl-lock}

シャード DDL ロックは、シャード DDL の移行を調整するロック メカニズムです。詳細は[悲観的モードでのシャードテーブルからのデータのマージと移行の実装原則](/dm/feature-shard-merge-pessimistic.md#principles)を参照してください。現在のドキュメントでは、シャード DDL ロックはシャーディング DDL ロックとも呼ばれます。

### シャードグループ {#shard-group}

シャード グループは、ダウンストリームの同じテーブルにマージおよび移行されるすべての上流シャード テーブルです。 TiDB DM の実装には 2 レベルのシャード グループが使用されます。詳細は[悲観的モードでのシャードテーブルからのデータのマージと移行の実装原則](/dm/feature-shard-merge-pessimistic.md#principles)を参照してください。現在のドキュメントでは、シャード グループはシャーディング グループとも呼ばれます。

### サブタスク {#subtask}

サブタスクは、各 DM ワーカー インスタンスで実行されるデータ移行タスクの一部です。さまざまなタスク構成では、単一のデータ移行タスクに 1 つのサブタスクまたは複数のサブタスクが含まれる場合があります。

### サブタスクのステータス {#subtask-status}

サブタスクのステータスは、データ移行サブタスクのステータスです。現在のステータスのオプションには、 `New` 、 `Running` 、 `Paused` 、 `Stopped` 、および`Finished`があります。データ移行タスクまたはサブタスクのステータスの詳細については、 [サブタスクのステータス](/dm/dm-query-status.md#subtask-status)を参照してください。

## T {#t}

### テーブルルーティング {#table-routing}

テーブル ルーティング機能を使用すると、DM はアップストリームの MySQL または MariaDB インスタンスの特定のテーブルをダウンストリームの指定されたテーブルに移行でき、これを使用してシャード テーブルをマージおよび移行できます。詳細は[テーブルルーティング](/dm/dm-table-routing.md)を参照してください。

### タスク {#task}

データ移行タスク`start-task`コマンドが正常に実行された後に開始されます。さまざまなタスク構成では、単一の移行タスクを単一の DM ワーカー インスタンス上で実行することも、複数の DM ワーカー インスタンス上で同時に実行することもできます。

### タスクのステータス {#task-status}

タスクのステータスは、データ移行タスクのステータスを指します。タスクのステータスは、そのすべてのサブタスクのステータスに依存します。詳細は[サブタスクのステータス](/dm/dm-query-status.md#subtask-status)を参照してください。
