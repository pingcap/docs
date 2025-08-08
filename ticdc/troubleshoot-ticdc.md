---
title: Troubleshoot TiCDC
summary: TiCDC の使用時に発生する可能性のある問題のトラブルシューティング方法を学習します。
---

# TiCDC のトラブルシューティング {#troubleshoot-ticdc}

このドキュメントでは、TiCDC の使用時に発生する可能性のある一般的なエラーと、それに対応するメンテナンスおよびトラブルシューティングの方法について説明します。

> **注記：**
>
> このドキュメントでは、 `cdc cli`コマンドで指定されているサーバーアドレスは`server=http://127.0.0.1:8300`です。コマンドを使用する際は、このアドレスを実際の TiCDC サーバアドレスに置き換えてください。

## TiCDC レプリケーションの中断 {#ticdc-replication-interruptions}

### TiCDC レプリケーション タスクが中断されたかどうかはどうすればわかりますか? {#how-do-i-know-whether-a-ticdc-replication-task-is-interrupted}

-   Grafanaダッシュボードで、レプリケーションタスクの監視メトリック`changefeed checkpoint` （適切な`changefeed id`選択）を確認してください。メトリック値が変化しない場合、またはメトリック`checkpoint lag`増加し続ける場合、レプリケーションタスクが中断されている可能性があります。
-   監視メトリック`exit error count`を確認してください。メトリック値が`0`より大きい場合、レプリケーションタスクでエラーが発生しました。
-   `cdc cli changefeed list`と`cdc cli changefeed query`実行して、レプリケーションタスクのステータスを確認します。5 `stopped`タスクが停止したことを意味し、 `error`は詳細なエラーメッセージを示します。エラー発生後、TiCDCサーバーログで`error on running processor`検索してエラースタックを確認し、トラブルシューティングを行うことができます。
-   極端なケースでは、TiCDC サービスが再起動されることがあります。トラブルシューティングのために、TiCDCサーバーログの`FATAL`レベル目のログを検索してください。

### レプリケーション タスクが手動で停止されたかどうかを確認するにはどうすればよいですか? {#how-do-i-know-whether-the-replication-task-is-stopped-manually}

レプリケーションタスクが手動で停止されているかどうかを確認するには、 `cdc cli`実行します。例:

```shell
cdc cli changefeed query --server=http://127.0.0.1:8300 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

上記のコマンドの出力で、 `admin-job-type`このレプリケーションタスクの状態を示しています。各状態とその意味の詳細については、 [チェンジフィードの状態](/ticdc/ticdc-changefeed-overview.md#changefeed-state-transfer)参照してください。

### レプリケーションの中断をどのように処理しますか? {#how-do-i-handle-replication-interruptions}

次の既知のシナリオでは、レプリケーション タスクが中断される可能性があります。

-   ダウンストリームは引き続き異常であり、何度も再試行しても TiCDC は失敗します。

    -   このシナリオでは、TiCDCはタスク情報を保存します。TiCDCはPDにサービスGCセーフポイントを設定しているため、タスクチェックポイント以降のデータは有効期間`gc-ttl`内にTiKV GCによってクリーンアップされません。

    -   対処方法：ダウンストリームが正常に戻った後、 `cdc cli changefeed resume`実行することでレプリケーション タスクを再開できます。

-   ダウンストリームに互換性のない SQL ステートメントがあるため、レプリケーションを続行できません。

    -   このシナリオでは、TiCDCはタスク情報を保存します。TiCDCはPDにサービスGCセーフポイントを設定しているため、タスクチェックポイント以降のデータは有効期間`gc-ttl`内にTiKV GCによってクリーンアップされません。
    -   取り扱い手順:
        1.  `cdc cli changefeed query`コマンドを使用してレプリケーション タスクのステータス情報を照会し、 `checkpoint-ts`の値を記録します。
        2.  新しいタスク構成ファイルを使用して`ignore-txn-start-ts`パラメータを追加し、指定された`start-ts`に対応するトランザクションをスキップします。
        3.  `cdc cli changefeed pause -c <changefeed-id>`実行してレプリケーション タスクを一時停止します。
        4.  `cdc cli changefeed update -c <changefeed-id> --config <config-file-path>`実行して新しいタスク構成ファイルを指定します。
        5.  `cdc cli changefeed resume -c <changefeed-id>`実行してレプリケーション タスクを再開します。

### タスク中断後に TiCDC を再起動した後で発生する OOM を処理するにはどうすればよいですか? {#what-should-i-do-to-handle-the-oom-that-occurs-after-ticdc-is-restarted-after-a-task-interruption}

-   TiDBクラスターとTiCDCクラスターを最新バージョンに更新してください。OOM問題は**、v4.0.14以降のv4.0バージョン、v5.0.2以降のv5.0バージョン、および最新バージョン**で既に解決されています。

## レプリケーション タスクを作成するとき、または MySQL にデータをレプリケートするときに発生する<code>Error 1298: Unknown or incorrect time zone: &#39;UTC&#39;</code>エラーを処理するにはどうすればよいですか? {#how-do-i-handle-the-code-error-1298-unknown-or-incorrect-time-zone-utc-code-error-when-creating-the-replication-task-or-replicating-data-to-mysql}

このエラーは、下流のMySQLがタイムゾーンをロードしていない場合に返されます。1 [`mysql_tzinfo_to_sql`](https://dev.mysql.com/doc/refman/8.0/en/mysql-tzinfo-to-sql.html)実行することでタイムゾーンをロードできます。タイムゾーンをロードした後は、タスクを作成してデータを通常どおりにレプリケートできます。

```shell
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql -p
```

上記のコマンドの出力が次のようなものであれば、インポートは成功しています。

    Enter password:
    Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
    Warning: Unable to load '/usr/share/zoneinfo/leap-seconds.list' as time zone. Skipping it.
    Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
    Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.

ダウンストリームが特殊な MySQL 環境 (パブリック クラウド RDS または一部の MySQL 派生バージョン) であり、前述の方法を使用したタイムゾーンのインポートが失敗した場合は、 `time-zone` `time-zone=""`などの空の値に設定することで、ダウンストリームのデフォルトのタイムゾーンを使用できます。

TiCDCでタイムゾーンを使用する場合は、 `time-zone="Asia/Shanghai"`ようにタイムゾーンを明示的に指定することをお勧めします。また、TiCDCサーバー構成で指定する`tz`とシンクURIで指定する`time-zone` 、下流データベースのタイムゾーン設定と一致していることを確認してください。これにより、タイムゾーンの不一致によるデータの不整合を防ぐことができます。

## TiCDC のアップグレードによって発生した構成ファイルの非互換性の問題をどのように処理すればよいですか? {#how-do-i-handle-the-incompatibility-issue-of-configuration-files-caused-by-ticdc-upgrade}

[互換性に関する注意事項](/ticdc/ticdc-compatibility.md)を参照してください。

## TiCDCタスクの<code>start-ts</code>タイムスタンプが現在時刻と大きく異なります。このタスクの実行中にレプリケーションが中断され、エラー<code>[CDC:ErrBufferReachLimit]</code>が発生しました。どうすればよいでしょうか？ {#the-code-start-ts-code-timestamp-of-the-ticdc-task-is-quite-different-from-the-current-time-during-the-execution-of-this-task-replication-is-interrupted-and-an-error-code-cdc-errbufferreachlimit-code-occurs-what-should-i-do}

v4.0.9 以降では、レプリケーション タスクで統合ソーター機能を有効にするか、 BRツールを使用して増分バックアップと復元を実行し、新しい時間から TiCDC レプリケーション タスクを開始することができます。

## 変更フィードの下流にMySQLなどのデータベースがあり、TiCDCが時間のかかるDDL文を実行すると、他のすべての変更フィードがブロックされます。どうすればよいでしょうか？ {#when-the-downstream-of-a-changefeed-is-a-database-similar-to-mysql-and-ticdc-executes-a-time-consuming-ddl-statement-all-other-changefeeds-are-blocked-what-should-i-do}

1.  時間のかかるDDL文を含む変更フィードの実行を一時停止します。すると、他の変更フィードがブロックされなくなったことがわかります。
2.  TiCDC ログで`apply job`フィールドを検索し、時間のかかる DDL ステートメントの`start-ts`確認します。
3.  下流でDDL文を手動で実行します。実行が完了したら、以下の操作を続行します。
4.  changefeed 設定を変更し、上記の`start-ts` `ignore-txn-start-ts`構成項目に追加します。
5.  一時停止された変更フィードを再開します。

## TiCDCを使用してチェンジフィードを作成すると、「 <code>[tikv:9006]GC life time is shorter than transaction duration, transaction starts at xx, GC safe point is yy</code>エラーが報告されます。どうすればよいでしょうか？ {#the-code-tikv-9006-gc-life-time-is-shorter-than-transaction-duration-transaction-starts-at-xx-gc-safe-point-is-yy-code-error-is-reported-when-i-use-ticdc-to-create-a-changefeed-what-should-i-do}

現在のGCセーフポイントとサービスGCセーフポイントを照会するには、コマンド`pd-ctl service-gc-safepoint --pd <pd-addrs>`実行する必要があります。GCセーフポイントがTiCDCレプリケーションタスク（changefeed）の`start-ts`よりも小さい場合は、コマンド`cdc cli create changefeed`にオプション`--disable-gc-check`を直接追加してchangefeedを作成できます。

`pd-ctl service-gc-safepoint --pd <pd-addrs>`の結果に`gc_worker service_id`がない場合:

-   PD バージョンが v4.0.8 以前の場合、詳細については[PD号 #3128](https://github.com/tikv/pd/issues/3128)を参照してください。
-   PD を v4.0.8 以前のバージョンからそれ以降のバージョンにアップグレードする場合は、詳細については[PD号 #3366](https://github.com/tikv/pd/issues/3366)を参照してください。

## TiCDCを使用してメッセージをKafkaに複製すると、Kafkaから<code>Message was too large</code>エラーが返されます。なぜでしょうか？ {#when-i-use-ticdc-to-replicate-messages-to-kafka-kafka-returns-the-code-message-was-too-large-code-error-why}

TiCDC v4.0.8以前のバージョンでは、Sink URIでKafkaに`max-message-bytes`設定するだけでは、Kafkaに出力されるメッセージのサイズを効果的に制御できません。メッセージのサイズを制御するには、Kafkaが受信するメッセージのバイト制限も増やす必要があります。このような制限を追加するには、Kafkaサーバーの設定に以下の設定を追加してください。

    # The maximum byte number of a message that the broker receives
    message.max.bytes=2147483648
    # The maximum byte number of a message that the broker copies
    replica.fetch.max.bytes=2147483648
    # The maximum message byte number that the consumer side reads
    fetch.message.max.bytes=2147483648

## TiCDC レプリケーション中に、ダウンストリームで DDL ステートメントの実行が失敗したかどうかを確認するにはどうすればよいでしょうか? レプリケーションを再開するにはどうすればよいでしょうか? {#how-can-i-find-out-whether-a-ddl-statement-fails-to-execute-in-downstream-during-ticdc-replication-how-to-resume-the-replication}

DDL文の実行に失敗した場合、レプリケーションタスク（changefeed）は自動的に停止します。checkpoint-tsはDDL文のfinish-tsです。TiCDCにこの文の実行を下流で再試行させたい場合は、 `cdc cli changefeed resume`指定してレプリケーションタスクを再開してください。例：

```shell
cdc cli changefeed resume -c test-cf --server=http://127.0.0.1:8300
```

このDDL文のエラーをスキップしたい場合は、changefeedのstart-tsをcheckpoint-ts（DDL文のエラーが発生したタイムスタンプ）に1を加えた値に設定し、 `cdc cli changefeed create`コマンドを実行して新しいchangefeedタスクを作成します。例えば、DDL文のエラーが発生したcheckpoint-tsが`415241823337054209`の場合、以下のコマンドを実行してこのDDL文をスキップします。

この問題のあるDDL文をスキップするには、 `ignore-txn-start-ts`パラメータを設定して、指定した`start-ts`に対応するトランザクションをスキップします。例:

1.  TiCDC ログで`apply job`フィールドを検索し、時間がかかっている`start-ts`の DDL を特定します。
2.  changefeed 設定を変更します。上記の`start-ts` `ignore-txn-start-ts`設定項目に追加します。
3.  中断された変更フィードを再開します。

> **注記：**
>
> changefeed `start-ts`エラー発生時の`checkpoint-ts`に 1 を加えた値に設定してタスクを再作成すると、DDL 文をスキップできますが、TiCDC が`checkpointTs+1`時点での DML データ変更を失う可能性があります。したがって、この操作は実本番環境では厳禁です。

```shell
cdc cli changefeed remove --server=http://127.0.0.1:8300 --changefeed-id simple-replication-task
cdc cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task" --sort-engine="unified" --start-ts 415241823337054210
```

## TiCDC を使用して Kafka にメッセージをレプリケートすると<code>Kafka: client has run out of available brokers to talk to: EOF</code>エラーが報告されます。どうすればよいでしょうか？ {#the-code-kafka-client-has-run-out-of-available-brokers-to-talk-to-eof-code-error-is-reported-when-i-use-ticdc-to-replicate-messages-to-kafka-what-should-i-do}

このエラーは通常、TiCDCとKafkaクラスター間の接続障害によって発生します。トラブルシューティングを行うには、Kafkaのログとネットワークステータスを確認してください。考えられる原因の一つは、レプリケーションタスクの作成時に正しいパラメータ`kafka-version`指定しなかったために、TiCDC内のKafkaクライアントがKafkaサーバーにアクセスする際に間違ったバージョンのKafka APIを使用していることです。この問題を解決するには、 [`--sink-uri`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)で正しいパラメータ`kafka-version`を指定します。例：

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --sink-uri "kafka://127.0.0.1:9092/test?topic=test&protocol=open-protocol&kafka-version=2.4.0" 
```
