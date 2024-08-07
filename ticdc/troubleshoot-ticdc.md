---
title: Troubleshoot TiCDC
summary: TiCDC の使用時に発生する可能性のある問題のトラブルシューティング方法を学習します。
---

# TiCDC のトラブルシューティング {#troubleshoot-ticdc}

このドキュメントでは、TiCDC の使用時に発生する可能性のある一般的なエラーと、それに対応するメンテナンスおよびトラブルシューティングの方法について説明します。

> **注記：**
>
> このドキュメントでは、 `cdc cli`コマンドで指定されているサーバーアドレスは`server=http://127.0.0.1:8300`です。コマンドを使用するときは、アドレスを実際の TiCDC サーバー アドレスに置き換えてください。

## TiCDC レプリケーションの中断 {#ticdc-replication-interruptions}

### TiCDC レプリケーション タスクが中断されたかどうかはどうすればわかりますか? {#how-do-i-know-whether-a-ticdc-replication-task-is-interrupted}

-   Grafana ダッシュボードで、レプリケーション タスクの`changefeed checkpoint`監視メトリックを確認します (正しい`changefeed id`を選択)。メトリック値が変更されない場合、または`checkpoint lag`メトリックが増加し続ける場合、レプリケーション タスクが中断されている可能性があります。
-   `exit error count`監視メトリックを確認します。メトリック値が`0`より大きい場合、レプリケーション タスクでエラーが発生しました。
-   `cdc cli changefeed list`と`cdc cli changefeed query`を実行して、レプリケーション タスクのステータスを確認します。5 `stopped`タスクが停止したことを意味し、 `error`項目には詳細なエラー メッセージが表示されます。エラーが発生したら、TiCDCサーバーログで`error on running processor`を検索してエラー スタックを確認し、トラブルシューティングを行うことができます。
-   極端なケースでは、TiCDC サービスが再起動されます。トラブルシューティングのために、TiCDCサーバーログの`FATAL`レベル ログを検索できます。

### レプリケーション タスクが手動で停止されたかどうかを確認するにはどうすればよいですか? {#how-do-i-know-whether-the-replication-task-is-stopped-manually}

`cdc cli`を実行すると、レプリケーション タスクが手動で停止されているかどうかを確認できます。例:

```shell
cdc cli changefeed query --server=http://127.0.0.1:8300 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

上記のコマンドの出力では、 `admin-job-type`このレプリケーション タスクの状態を示しています。各状態とその意味の詳細については、 [チェンジフィードの状態](/ticdc/ticdc-changefeed-overview.md#changefeed-state-transfer)を参照してください。

### レプリケーションの中断をどのように処理しますか? {#how-do-i-handle-replication-interruptions}

次の既知のシナリオでは、レプリケーション タスクが中断される可能性があります。

-   ダウンストリームは引き続き異常であり、何度も再試行しても TiCDC は失敗します。

    -   このシナリオでは、TiCDC はタスク情報を保存します。TiCDC は PD にサービス GC セーフポイントを設定しているため、タスク チェックポイント以降のデータは有効期間`gc-ttl`内に TiKV GC によってクリーンアップされません。

    -   処理方法: ダウンストリームが正常に戻った後、 `cdc cli changefeed resume`実行することでレプリケーション タスクを再開できます。

-   ダウンストリームに互換性のない SQL ステートメントがあるため、レプリケーションを続行できません。

    -   このシナリオでは、TiCDC はタスク情報を保存します。TiCDC は PD にサービス GC セーフポイントを設定しているため、タスク チェックポイント以降のデータは有効期間`gc-ttl`内に TiKV GC によってクリーンアップされません。
    -   取り扱い手順:
        1.  `cdc cli changefeed query`コマンドを使用してレプリケーション タスクのステータス情報を照会し、 `checkpoint-ts`の値を記録します。
        2.  新しいタスク構成ファイルを使用して、 `ignore-txn-start-ts`パラメータを追加し、指定された`start-ts`に対応するトランザクションをスキップします。
        3.  `cdc cli changefeed pause -c <changefeed-id>`実行してレプリケーション タスクを一時停止します。
        4.  `cdc cli changefeed update -c <changefeed-id> --config <config-file-path>`を実行して新しいタスク構成ファイルを指定します。
        5.  `cdc cli changefeed resume -c <changefeed-id>`を実行してレプリケーション タスクを再開します。

### タスク中断後に TiCDC を再起動した後に発生する OOM を処理するにはどうすればよいですか? {#what-should-i-do-to-handle-the-oom-that-occurs-after-ticdc-is-restarted-after-a-task-interruption}

-   TiDB クラスターと TiCDC クラスターを最新バージョンに更新します。OOM の問題は**、v4.0.14 以降の v4.0 バージョン、v5.0.2 以降の v5.0 バージョン、および最新バージョンで**はすでに解決されています。

## レプリケーション タスクを作成するとき、またはデータを MySQL にレプリケートするときに発生する<code>Error 1298: Unknown or incorrect time zone: &#39;UTC&#39;</code>エラーをどのように処理すればよいですか? {#how-do-i-handle-the-code-error-1298-unknown-or-incorrect-time-zone-utc-code-error-when-creating-the-replication-task-or-replicating-data-to-mysql}

このエラーは、ダウンストリーム MySQL がタイムゾーンをロードしない場合に返されます。 [`mysql_tzinfo_to_sql`](https://dev.mysql.com/doc/refman/8.0/en/mysql-tzinfo-to-sql.html)実行すると、タイムゾーンをロードできます。タイムゾーンをロードした後は、タスクを作成してデータを正常にレプリケートできます。

```shell
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql -p
```

上記のコマンドの出力が次のようなものであれば、インポートは成功しています。

    Enter password:
    Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
    Warning: Unable to load '/usr/share/zoneinfo/leap-seconds.list' as time zone. Skipping it.
    Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
    Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.

ダウンストリームが特殊な MySQL 環境 (パブリック クラウド RDS または一部の MySQL 派生バージョン) であり、前述の方法を使用したタイム ゾーンのインポートが失敗した場合は、 `time-zone` `time-zone=""`などの空の値に設定することで、ダウンストリームのデフォルトのタイム ゾーンを使用できます。

TiCDC でタイムゾーンを使用する場合は、 `time-zone="Asia/Shanghai"`などのタイムゾーンを明示的に指定することをお勧めします。また、TiCDCサーバー構成で指定された`tz`とシンク URI で指定された`time-zone` 、ダウンストリーム データベースのタイムゾーン構成と一致していることを確認してください。これにより、タイムゾーンの不一致によるデータの不一致を防ぐことができます。

## TiCDC のアップグレードによって発生した構成ファイルの非互換性の問題をどのように処理すればよいですか? {#how-do-i-handle-the-incompatibility-issue-of-configuration-files-caused-by-ticdc-upgrade}

[互換性に関する注意事項](/ticdc/ticdc-compatibility.md)を参照してください。

## TiCDC タスクの<code>start-ts</code>タイムスタンプが現在の時刻と大きく異なります。このタスクの実行中にレプリケーションが中断され、エラー<code>[CDC:ErrBufferReachLimit]</code>が発生します。どうすればよいでしょうか? {#the-code-start-ts-code-timestamp-of-the-ticdc-task-is-quite-different-from-the-current-time-during-the-execution-of-this-task-replication-is-interrupted-and-an-error-code-cdc-errbufferreachlimit-code-occurs-what-should-i-do}

v4.0.9 以降では、レプリケーション タスクで統合ソート機能を有効にするか、 BRツールを使用して増分バックアップと復元を実行し、新しい時間から TiCDC レプリケーション タスクを開始することができます。

## 変更フィードのダウンストリームが MySQL に似たデータベースであり、TiCDC が時間のかかる DDL ステートメントを実行すると、他のすべての変更フィードがブロックされます。どうすればよいでしょうか? {#when-the-downstream-of-a-changefeed-is-a-database-similar-to-mysql-and-ticdc-executes-a-time-consuming-ddl-statement-all-other-changefeeds-are-blocked-what-should-i-do}

1.  時間のかかる DDL ステートメントを含む変更フィードの実行を一時停止します。すると、他の変更フィードがブロックされなくなったことがわかります。
2.  TiCDC ログで`apply job`フィールドを検索し、時間のかかる DDL ステートメントの`start-ts`を確認します。
3.  ダウンストリームで DDL ステートメントを手動で実行します。実行が完了したら、次の操作を実行します。
4.  changefeed 設定を変更し、上記の`start-ts` `ignore-txn-start-ts`構成項目に追加します。
5.  一時停止した変更フィードを再開します。

## TiCDC を使用して変更フィードを作成すると<code>[tikv:9006]GC life time is shorter than transaction duration, transaction starts at xx, GC safe point is yy</code>エラーが報告されます。どうすればよいですか? {#the-code-tikv-9006-gc-life-time-is-shorter-than-transaction-duration-transaction-starts-at-xx-gc-safe-point-is-yy-code-error-is-reported-when-i-use-ticdc-to-create-a-changefeed-what-should-i-do}

現在の GC セーフポイントとサービス GC セーフポイントを照会するには、 `pd-ctl service-gc-safepoint --pd <pd-addrs>`コマンドを実行する必要があります。GC セーフポイントが TiCDC レプリケーション タスク (changefeed) の`start-ts`より小さい場合は、 `cdc cli create changefeed`コマンドに`--disable-gc-check`オプションを直接追加して changefeed を作成できます。

`pd-ctl service-gc-safepoint --pd <pd-addrs>`の結果に`gc_worker service_id`がない場合:

-   PD バージョンが v4.0.8 以前の場合、詳細については[PD 号 #3128](https://github.com/tikv/pd/issues/3128)を参照してください。
-   PD を v4.0.8 以前のバージョンからそれ以降のバージョンにアップグレードする場合は、詳細については[PD 号 #3366](https://github.com/tikv/pd/issues/3366)を参照してください。

## TiCDC を使用してメッセージを Kafka に複製すると、Kafka は<code>Message was too large</code>エラーを返します。なぜでしょうか? {#when-i-use-ticdc-to-replicate-messages-to-kafka-kafka-returns-the-code-message-was-too-large-code-error-why}

TiCDC v4.0.8 以前のバージョンでは、Sink URI で Kafka に`max-message-bytes`設定を構成するだけでは、Kafka に出力されるメッセージのサイズを効果的に制御することはできません。メッセージ サイズを制御するには、Kafka が受信するメッセージのバイト制限も増やす必要があります。このような制限を追加するには、Kafkaサーバー構成に次の構成を追加します。

    # The maximum byte number of a message that the broker receives
    message.max.bytes=2147483648
    # The maximum byte number of a message that the broker copies
    replica.fetch.max.bytes=2147483648
    # The maximum message byte number that the consumer side reads
    fetch.message.max.bytes=2147483648

## TiCDC レプリケーション中に、ダウンストリームで DDL ステートメントの実行が失敗したかどうかを確認するにはどうすればよいでしょうか? レプリケーションを再開するにはどうすればよいでしょうか? {#how-can-i-find-out-whether-a-ddl-statement-fails-to-execute-in-downstream-during-ticdc-replication-how-to-resume-the-replication}

DDL ステートメントの実行に失敗した場合、レプリケーション タスク (changefeed) は自動的に停止します。チェックポイント ts は、DDL ステートメントの終了 ts です。TiCDC にこのステートメントの実行をダウンストリームで再試行させたい場合は、 `cdc cli changefeed resume`使用してレプリケーション タスクを再開します。例:

```shell
cdc cli changefeed resume -c test-cf --server=http://127.0.0.1:8300
```

この間違った DDL ステートメントをスキップする場合は、changefeed の start-ts を checkpoint-ts (DDL ステートメントが間違ったタイムスタンプ) に 1 を加えた値に設定し、 `cdc cli changefeed create`コマンドを実行して新しい changefeed タスクを作成します。たとえば、DDL ステートメントが間違った checkpoint-ts が`415241823337054209`の場合、以下のコマンドを実行してこの DDL ステートメントをスキップします。

この間違った DDL ステートメントをスキップするには、 `ignore-txn-start-ts`パラメータを設定して、指定された`start-ts`に対応するトランザクションをスキップします。例:

1.  TiCDC ログで`apply job`フィールドを検索し、時間がかかっている`start-ts`の DDL を特定します。
2.  changefeed 設定を変更します。上記の`start-ts` `ignore-txn-start-ts`構成項目に追加します。
3.  中断された変更フィードを再開します。

> **注記：**
>
> changefeed `start-ts` `checkpoint-ts` (エラー発生時) に 1 を加えた値に設定してタスクを再作成すると、DDL ステートメントをスキップできますが、TiCDC が`checkpointTs+1`の時点での DML データ変更を失う可能性もあります。したがって、この操作は本番環境では厳重に禁止されています。

```shell
cdc cli changefeed remove --server=http://127.0.0.1:8300 --changefeed-id simple-replication-task
cdc cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task" --sort-engine="unified" --start-ts 415241823337054210
```

## TiCDC を使用してメッセージを Kafka に複製すると<code>Kafka: client has run out of available brokers to talk to: EOF</code>エラーが報告されます。どうすればよいでしょうか? {#the-code-kafka-client-has-run-out-of-available-brokers-to-talk-to-eof-code-error-is-reported-when-i-use-ticdc-to-replicate-messages-to-kafka-what-should-i-do}

このエラーは通常、TiCDC と Kafka クラスター間の接続障害によって発生します。トラブルシューティングするには、Kafka ログとネットワーク ステータスを確認します。考えられる原因の 1 つは、レプリケーション タスクの作成時に正しい`kafka-version`パラメータを指定しなかったため、TiCDC 内の Kafka クライアントが Kafkaサーバーにアクセスするときに間違った Kafka API バージョンを使用していることです。この問題を解決するには、 [`--sink-uri`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)構成で正しい`kafka-version`パラメータを指定します。例:

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --sink-uri "kafka://127.0.0.1:9092/test?topic=test&protocol=open-protocol&kafka-version=2.4.0" 
```
