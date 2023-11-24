---
title: Troubleshoot TiCDC
summary: Learn how to troubleshoot issues you might encounter when you use TiCDC.
---

# TiCDC のトラブルシューティング {#troubleshoot-ticdc}

このドキュメントでは、TiCDC の使用時に発生する可能性のある一般的なエラーと、対応するメンテナンスおよびトラブルシューティングの方法を紹介します。

> **注記：**
>
> このドキュメントでは、 `cdc cli`コマンドで指定するサーバーアドレスは`server=http://127.0.0.1:8300`です。コマンドを使用するときは、アドレスを実際の TiCDC サーバーのアドレスに置き換えてください。

## TiCDC レプリケーションの中断 {#ticdc-replication-interruptions}

### TiCDC レプリケーション タスクが中断されたかどうかを確認するにはどうすればよいですか? {#how-do-i-know-whether-a-ticdc-replication-task-is-interrupted}

-   Grafana ダッシュボードでレプリケーション タスクの`changefeed checkpoint`監視メトリックを確認します (右側の`changefeed id`選択)。メトリック値が変わらない場合、またはメトリック`checkpoint lag`が増加し続ける場合、レプリケーション タスクが中断される可能性があります。
-   `exit error count`監視メトリックを確認します。メトリック値が`0`より大きい場合、レプリケーション タスクでエラーが発生しています。
-   `cdc cli changefeed list`と`cdc cli changefeed query`を実行してレプリケーションタスクの状態を確認します。 `stopped`タスクが停止したことを意味し、 `error`項目は詳細なエラー メッセージを示します。エラーが発生した後、TiCDCサーバーログで`error on running processor`検索して、トラブルシューティングのためにエラー スタックを確認できます。
-   極端な場合には、TiCDC サービスが再起動されることがあります。トラブルシューティングのために、TiCDCサーバーログの`FATAL`レベルのログを検索できます。

### レプリケーションタスクが手動で停止されているかどうかを確認するにはどうすればよいですか? {#how-do-i-know-whether-the-replication-task-is-stopped-manually}

`cdc cli`を実行すると、レプリケーション タスクが手動で停止されているかどうかを確認できます。例えば：

```shell
cdc cli changefeed query --server=http://127.0.0.1:8300 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

上記のコマンドの出力では、 `admin-job-type`このレプリケーション タスクの状態を示します。各状態とその意味の詳細については、 [フィード状態の変更](/ticdc/ticdc-changefeed-overview.md#changefeed-state-transfer)を参照してください。

### レプリケーションの中断はどのように処理すればよいですか? {#how-do-i-handle-replication-interruptions}

次の既知のシナリオでは、レプリケーション タスクが中断される可能性があります。

-   ダウンストリームは引き続き異常であり、TiCDC は何度も再試行しても失敗します。

    -   このシナリオでは、TiCDC はタスク情報を保存します。 TiCDC は PD にサービス GC セーフポイントを設定しているため、タスク チェックポイント後のデータは、有効期間`gc-ttl`内に TiKV GC によってクリーンアップされません。

    -   対処方法：ダウンストリームが正常に戻った後、 `cdc cli changefeed resume`実行することでレプリケーションタスクを再開できます。

-   ダウンストリームに互換性のない SQL ステートメントがあるため、レプリケーションを続行できません。

    -   このシナリオでは、TiCDC はタスク情報を保存します。 TiCDC は PD にサービス GC セーフポイントを設定しているため、タスク チェックポイント後のデータは、有効期間`gc-ttl`内に TiKV GC によってクリーンアップされません。
    -   取り扱い手順：
        1.  `cdc cli changefeed query`コマンドを使用してレプリケーション タスクのステータス情報をクエリし、 `checkpoint-ts`の値を記録します。
        2.  新しいタスク構成ファイルを使用し、 `ignore-txn-start-ts`パラメーターを追加して、指定された`start-ts`に対応するトランザクションをスキップします。
        3.  `cdc cli changefeed pause -c <changefeed-id>`を実行してレプリケーション タスクを一時停止します。
        4.  `cdc cli changefeed update -c <changefeed-id> --config <config-file-path>`を実行して、新しいタスク構成ファイルを指定します。
        5.  `cdc cli changefeed resume -c <changefeed-id>`を実行してレプリケーション タスクを再開します。

### タスク中断後に TiCDC が再起動された後に発生する OOM を処理するにはどうすればよいですか? {#what-should-i-do-to-handle-the-oom-that-occurs-after-ticdc-is-restarted-after-a-task-interruption}

-   TiDB クラスターと TiCDC クラスターを最新バージョンに更新します。 OOM の問題は**、v4.0.14 以降の v4.0 バージョン、v5.0.2 以降の v5.0 バージョン、および最新バージョンで**すでに解決されています。

## レプリケーション タスクを作成するとき、またはデータを MySQL にレプリケートするときに<code>Error 1298: Unknown or incorrect time zone: &#39;UTC&#39;</code>エラーを処理するにはどうすればよいですか? {#how-do-i-handle-the-code-error-1298-unknown-or-incorrect-time-zone-utc-code-error-when-creating-the-replication-task-or-replicating-data-to-mysql}

このエラーは、ダウンストリーム MySQL がタイムゾーンをロードしない場合に返されます。 [`mysql_tzinfo_to_sql`](https://dev.mysql.com/doc/refman/8.0/en/mysql-tzinfo-to-sql.html)を実行するとタイムゾーンをロードできます。タイムゾーンをロードした後、通常どおりタスクを作成し、データをレプリケートできます。

```shell
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql -p
```

上記のコマンドの出力が次のような場合、インポートは成功しています。

    Enter password:
    Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
    Warning: Unable to load '/usr/share/zoneinfo/leap-seconds.list' as time zone. Skipping it.
    Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
    Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.

ダウンストリームが特別な MySQL 環境 (パブリック クラウド RDS または一部の MySQL 派生バージョン) であり、前述の方法を使用したタイム ゾーンのインポートが失敗した場合は、次のように`time-zone`を空の値に設定することで、ダウンストリームのデフォルトのタイム ゾーンを使用できます。 `time-zone=""` ．

TiCDC でタイム ゾーンを使用する場合は、 `time-zone="Asia/Shanghai"`などのタイム ゾーンを明示的に指定することをお勧めします。また、TiCDCサーバー構成で指定された`tz`とシンク URI で指定された`time-zone` 、ダウンストリーム データベースのタイム ゾーン構成と一致していることを確認してください。これにより、タイムゾーンの不一致によるデータの不整合が防止されます。

## TiCDC のアップグレードによって引き起こされる構成ファイルの非互換性の問題にはどのように対処すればよいですか? {#how-do-i-handle-the-incompatibility-issue-of-configuration-files-caused-by-ticdc-upgrade}

[互換性に関する注意事項](/ticdc/ticdc-compatibility.md)を参照してください。

## TiCDC タスクの<code>start-ts</code>タイムスタンプは、現在時刻とは大きく異なります。このタスクの実行中にレプリケーションが中断され、エラー<code>[CDC:ErrBufferReachLimit]</code>が発生します。どうすればいいですか？ {#the-code-start-ts-code-timestamp-of-the-ticdc-task-is-quite-different-from-the-current-time-during-the-execution-of-this-task-replication-is-interrupted-and-an-error-code-cdc-errbufferreachlimit-code-occurs-what-should-i-do}

v4.0.9 以降、レプリケーション タスクで統合ソーター機能を有効にするか、増分バックアップと復元にBRツールを使用して、TiCDC レプリケーション タスクを新しい時間から開始することができます。

## チェンジフィードのダウンストリームが MySQL に似たデータベースであり、TiCDC が時間のかかる DDL ステートメントを実行する場合、他のすべてのチェンジフィードはブロックされます。どうすればいいですか？ {#when-the-downstream-of-a-changefeed-is-a-database-similar-to-mysql-and-ticdc-executes-a-time-consuming-ddl-statement-all-other-changefeeds-are-blocked-what-should-i-do}

1.  時間のかかる DDL ステートメントを含む変更フィードの実行を一時停止します。その後、他の変更フィードがブロックされていないことがわかります。
2.  TiCDC ログの`apply job`フィールドを検索し、時間のかかる DDL ステートメントの`start-ts`を確認します。
3.  ダウンストリームで DDL ステートメントを手動で実行します。実行が終了したら、引き続き次の操作を実行します。
4.  チェンジフィードの設定を変更し、 `ignore-txn-start-ts`設定項目に上記`start-ts`を追加します。
5.  一時停止した変更フィードを再開します。

## TiCDC クラスターを v4.0.8 にアップグレードした後、変更フィードを実行すると、 <code>[CDC:ErrKafkaInvalidConfig]Canal requires old value to be enabled</code>エラーが報告されます。どうすればいいですか？ {#after-i-upgrade-the-ticdc-cluster-to-v4-0-8-the-code-cdc-errkafkainvalidconfig-canal-requires-old-value-to-be-enabled-code-error-is-reported-when-i-execute-a-changefeed-what-should-i-do}

v4.0.8 以降、変更フィードの出力に`canal-json` 、 `canal` 、または`maxwell`プロトコルが使用されている場合、TiCDC は古い値機能を自動的に有効にします。ただし、TiCDC を以前のバージョンから v4.0.8 以降にアップグレードした場合、変更フィードで`canal-json` 、 `canal`または`maxwell`プロトコルが使用され、古い値機能が無効になっていると、このエラーが報告されます。

エラーを修正するには、次の手順を実行します。

1.  変更フィード構成ファイルの値`enable-old-value`を`true`に設定します。

2.  `cdc cli changefeed pause`を実行してレプリケーション タスクを一時停止します。

    ```shell
    cdc cli changefeed pause -c test-cf --server=http://127.0.0.1:8300
    ```

3.  `cdc cli changefeed update`を実行して、元の変更フィード構成を更新します。

    ```shell
    cdc cli changefeed update -c test-cf --server=http://127.0.0.1:8300 --sink-uri="mysql://127.0.0.1:3306/?max-txn-row=20&worker-number=8" --config=changefeed.toml
    ```

4.  `cdc cli changfeed resume`を実行してレプリケーション タスクを再開します。

    ```shell
    cdc cli changefeed resume -c test-cf --server=http://127.0.0.1:8300
    ```

## TiCDC を使用してチェンジフィード<code>[tikv:9006]GC life time is shorter than transaction duration, transaction starts at xx, GC safe point is yy</code>エラーが報告されます。どうすればいいですか？ {#the-code-tikv-9006-gc-life-time-is-shorter-than-transaction-duration-transaction-starts-at-xx-gc-safe-point-is-yy-code-error-is-reported-when-i-use-ticdc-to-create-a-changefeed-what-should-i-do}

`pd-ctl service-gc-safepoint --pd <pd-addrs>`コマンドを実行して、現在の GC セーフポイントとサービス GC セーフポイントを照会する必要があります。 GC セーフポイントが TiCDC レプリケーション タスク (変更フィード) の`start-ts`より小さい場合は、 `cdc cli create changefeed`コマンドに`--disable-gc-check`オプションを直接追加して変更フィードを作成できます。

`pd-ctl service-gc-safepoint --pd <pd-addrs>`の結果に`gc_worker service_id`がない場合:

-   PD バージョンが v4.0.8 以前の場合、詳細については[PD 問題 #3128](https://github.com/tikv/pd/issues/3128)を参照してください。
-   PD が v4.0.8 以前のバージョンから新しいバージョンにアップグレードされた場合、詳細については[PD 問題 #3366](https://github.com/tikv/pd/issues/3366)を参照してください。

## TiCDC を使用してメッセージを Kafka にレプリケートすると、Kafka は<code>Message was too large</code>エラーを返します。なぜ？ {#when-i-use-ticdc-to-replicate-messages-to-kafka-kafka-returns-the-code-message-was-too-large-code-error-why}

TiCDC v4.0.8 以前のバージョンの場合、シンク URI で Kafka の`max-message-bytes`設定を構成するだけでは、Kafka に出力されるメッセージのサイズを効果的に制御できません。メッセージ サイズを制御するには、Kafka が受信するメッセージのバイト数の制限を増やす必要もあります。このような制限を追加するには、次の構成を Kafkaサーバー構成に追加します。

    # The maximum byte number of a message that the broker receives
    message.max.bytes=2147483648
    # The maximum byte number of a message that the broker copies
    replica.fetch.max.bytes=2147483648
    # The maximum message byte number that the consumer side reads
    fetch.message.max.bytes=2147483648

## TiCDC レプリケーション中にダウンストリームで DDL ステートメントの実行が失敗したかどうかを確認するにはどうすればよいですか?レプリケーションを再開するにはどうすればよいですか? {#how-can-i-find-out-whether-a-ddl-statement-fails-to-execute-in-downstream-during-ticdc-replication-how-to-resume-the-replication}

DDL ステートメントの実行に失敗すると、レプリケーション タスク (変更フィード) が自動的に停止します。チェックポイント ts は、DDL ステートメントの終了 ts から 1 を引いたものです。 TiCDC がダウンストリームでこのステートメントの実行を再試行するようにするには、 `cdc cli changefeed resume`を使用してレプリケーション タスクを再開します。例えば：

```shell
cdc cli changefeed resume -c test-cf --server=http://127.0.0.1:8300
```

問題が発生したこの DDL ステートメントをスキップしたい場合は、変更フィードの start-ts をチェックポイント ts (DDL ステートメントが失敗した時点のタイムスタンプ) に 1 を加えた値に設定し、 `cdc cli changefeed create`コマンドを実行して新しい変更フィードを作成します。タスク。たとえば、DDL ステートメントが失敗する Checkpoint-ts が`415241823337054209`の場合、次のコマンドを実行してこの DDL ステートメントをスキップします。

```shell
cdc cli changefeed remove --server=http://127.0.0.1:8300 --changefeed-id simple-replication-task
cdc cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="mysql://root:123456@127.0.0.1:3306/" --changefeed-id="simple-replication-task" --sort-engine="unified" --start-ts 415241823337054210
```
