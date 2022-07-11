---
title: Troubleshoot TiCDC
summary: Learn how to troubleshoot issues you might encounter when you use TiCDC.
---

# TiCDCのトラブルシューティング {#troubleshoot-ticdc}

このドキュメントでは、TiCDCを使用するときに発生する可能性のある一般的なエラーと、それに対応するメンテナンスおよびトラブルシューティングの方法を紹介します。

> **ノート：**
>
> このドキュメントでは、 `cdc cli`コマンドで指定されたPDアドレスは`--pd=http://10.0.10.25:2379`です。コマンドを使用するときは、アドレスを実際のPDアドレスに置き換えてください。

## TiCDCレプリケーションの中断 {#ticdc-replication-interruptions}

### TiCDCレプリケーションタスクが中断されているかどうかを確認するにはどうすればよいですか？ {#how-do-i-know-whether-a-ticdc-replication-task-is-interrupted}

-   Grafanaダッシュボードでレプリケーションタスクの`changefeed checkpoint`のモニタリングメトリックを確認します（右の`changefeed id`を選択します）。メトリック値が変更されない場合、または`checkpoint lag`メトリックが増加し続ける場合は、レプリケーションタスクが中断される可能性があります。
-   `exit error count`の監視メトリックを確認します。メトリック値が`0`より大きい場合、レプリケーションタスクでエラーが発生しています。
-   `cdc cli changefeed list`と`cdc cli changefeed query`を実行して、レプリケーションタスクのステータスを確認します。 `stopped`はタスクが停止したことを意味し、 `error`項目は詳細なエラーメッセージを提供します。エラーが発生した後、TiCDCサーバーログで`error on running processor`を検索して、トラブルシューティングのためのエラースタックを確認できます。
-   極端な場合には、TiCDCサービスが再起動されます。トラブルシューティングのために、TiCDCサーバーログで`FATAL`レベルのログを検索できます。

### レプリケーションタスクが手動で停止されているかどうかを確認するにはどうすればよいですか？ {#how-do-i-know-whether-the-replication-task-is-stopped-manually}

`cdc cli`を実行すると、レプリケーションタスクが手動で停止されているかどうかを確認できます。例えば：

{{< copyable "" >}}

```shell
cdc cli changefeed query --pd=http://10.0.10.25:2379 --changefeed-id 28c43ffc-2316-4f4f-a70b-d1a7c59ba79f
```

上記のコマンドの出力で、 `admin-job-type`はこのレプリケーションタスクの状態を示しています。

-   `0` ：進行中です。これは、タスクが手動で停止されていないことを意味します。
-   `1` ：一時停止。タスクが一時停止されると、複製されたすべての`processor`が終了します。タスクの構成と複製ステータスは保持されるため、 `checkpiont-ts`からタスクを再開できます。
-   `2` ：再開しました。レプリケーションタスクは`checkpoint-ts`から再開します。
-   `3` ：削除されました。タスクが削除されると、複製された`processor`がすべて終了し、複製タスクの構成情報がクリアされます。レプリケーションステータスは、後のクエリのためにのみ保持されます。

### レプリケーションの中断を処理するにはどうすればよいですか？ {#how-do-i-handle-replication-interruptions}

次の既知のシナリオでは、レプリケーションタスクが中断される可能性があります。

-   ダウンストリームは引き続き異常であり、TiCDCは何度も再試行した後も失敗します。

    -   このシナリオでは、TiCDCはタスク情報を保存します。 TiCDCはPDにサービスGCセーフポイントを設定しているため、タスクチェックポイント後のデータは有効期間`gc-ttl`以内にTiKVGCによってクリーンアップされません。

    -   処理方法：ダウンストリームが通常に戻った後、HTTPインターフェースを介してレプリケーションタスクを再開できます。

-   ダウンストリームに互換性のないSQLステートメントがあるため、レプリケーションを続行できません。

    -   このシナリオでは、TiCDCはタスク情報を保存します。 TiCDCはPDにサービスGCセーフポイントを設定しているため、タスクチェックポイント後のデータは有効期間`gc-ttl`以内にTiKVGCによってクリーンアップされません。
    -   取り扱い手順：
        1.  `cdc cli changefeed query`コマンドを使用してレプリケーションタスクのステータス情報を照会し、値`checkpoint-ts`を記録します。
        2.  新しいタスク構成ファイルを使用し、 `ignore-txn-start-ts`パラメーターを追加して、指定された`start-ts`に対応するトランザクションをスキップします。
        3.  HTTPAPIを介して古いレプリケーションタスクを停止します。 `cdc cli changefeed create`を実行して新しいタスクを作成し、新しいタスク構成ファイルを指定します。手順1で記録した`checkpoint-ts`を`start-ts`として指定し、新しいタスクを開始してレプリケーションを再開します。

-   TiCDC v4.0.13以前のバージョンでは、TiCDCがパーティションテーブルを複製するときに、複製の中断につながるエラーが発生する場合があります。

    -   このシナリオでは、TiCDCはタスク情報を保存します。 TiCDCはPDにサービスGCセーフポイントを設定しているため、タスクチェックポイント後のデータは有効期間`gc-ttl`以内にTiKVGCによってクリーンアップされません。
    -   取り扱い手順：
        1.  `cdc cli changefeed pause -c <changefeed-id>`を実行して、レプリケーションタスクを一時停止します。
        2.  約1つのムナイトを待ってから、 `cdc cli changefeed resume -c <changefeed-id>`を実行してレプリケーションタスクを再開します。

### タスクの中断後にTiCDCが再起動された後に発生するOOMを処理するにはどうすればよいですか？ {#what-should-i-do-to-handle-the-oom-that-occurs-after-ticdc-is-restarted-after-a-task-interruption}

-   TiDBクラスタとTiCDCクラスタを最新バージョンに更新します。 OOMの問題は、 **v4.0.14以降のv4.0バージョン、v5.0.2以降のv5.0バージョン、および最新バージョンで**はすでに解決されています。

## <code>Error 1298: Unknown or incorrect time zone: &#39;UTC&#39;</code>エラーを処理するにはどうすればよいですか？ {#how-do-i-handle-the-code-error-1298-unknown-or-incorrect-time-zone-utc-code-error-when-creating-the-replication-task-or-replicating-data-to-mysql}

このエラーは、ダウンストリームのMySQLがタイムゾーンをロードしない場合に返されます。 [`mysql_tzinfo_to_sql`](https://dev.mysql.com/doc/refman/8.0/en/mysql-tzinfo-to-sql.html)を実行すると、タイムゾーンを読み込むことができます。タイムゾーンを読み込んだ後、タスクを作成してデータを通常どおりに複製できます。

{{< copyable "" >}}

```shell
mysql_tzinfo_to_sql /usr/share/zoneinfo | mysql -u root mysql -p
```

上記のコマンドの出力が次のようなものである場合、インポートは成功しています。

```
Enter password:
Warning: Unable to load '/usr/share/zoneinfo/iso3166.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/leap-seconds.list' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone.tab' as time zone. Skipping it.
Warning: Unable to load '/usr/share/zoneinfo/zone1970.tab' as time zone. Skipping it.
```

ダウンストリームが特別なMySQL環境（パブリッククラウドRDSまたは一部のMySQL派生バージョン）であり、上記の方法を使用したタイムゾーンのインポートが失敗した場合、 `sink-uri`の`time-zone`パラメーターを使用してダウンストリームのMySQLタイムゾーンを指定する必要があります。最初に、MySQLで使用されるタイムゾーンをクエリできます。

1.  MySQLで使用されるタイムゾーンをクエリします。

    {{< copyable "" >}}

    ```sql
    show variables like '%time_zone%';
    ```

    ```
    +------------------+--------+
    | Variable_name    | Value  |
    +------------------+--------+
    | system_time_zone | CST    |
    | time_zone        | SYSTEM |
    +------------------+--------+
    ```

2.  レプリケーションタスクを作成してTiCDCサービスを作成するときに、タイムゾーンを指定します。

    {{< copyable "" >}}

    ```shell
    cdc cli changefeed create --sink-uri="mysql://root@127.0.0.1:3306/?time-zone=CST" --pd=http://10.0.10.25:2379
    ```

    > **ノート：**
    >
    > CSTは、次の4つの異なるタイムゾーンの略語である可能性があります。
    >
    > -   中部標準時（米国）UT-6:00
    > -   中部標準時（オーストラリア）UT + 9：30
    > -   中国標準時UT+8：00
    > -   キューバ標準時UT-4:00
    >
    > 中国では、CSTは通常中国標準時の略です。

## TiCDCのアップグレードによって引き起こされる構成ファイルの非互換性の問題をどのように処理しますか？ {#how-do-i-handle-the-incompatibility-issue-of-configuration-files-caused-by-ticdc-upgrade}

[互換性に関する注意](/ticdc/manage-ticdc.md#notes-for-compatibility)を参照してください。

## TiCDCタスクの<code>start-ts</code>タイムスタンプは、現在の時刻とはかなり異なります。このタスクの実行中に、レプリケーションが中断され、エラー<code>[CDC:ErrBufferReachLimit]</code>が発生します {#the-code-start-ts-code-timestamp-of-the-ticdc-task-is-quite-different-from-the-current-time-during-the-execution-of-this-task-replication-is-interrupted-and-an-error-code-cdc-errbufferreachlimit-code-occurs}

v4.0.9以降では、レプリケーションタスクで統合ソーター機能を有効にするか、BRツールを使用して増分バックアップと復元を行い、新しい時間からTiCDCレプリケーションタスクを開始できます。

## チェンジフィードのダウンストリームがMySQLと同様のデータベースであり、TiCDCが時間のかかるDDLステートメントを実行する場合、他のすべてのチェンジフィードはブロックされます。問題をどのように処理する必要がありますか？ {#when-the-downstream-of-a-changefeed-is-a-database-similar-to-mysql-and-ticdc-executes-a-time-consuming-ddl-statement-all-other-changefeeds-are-blocked-how-should-i-handle-the-issue}

1.  時間のかかるDDLステートメントを含むチェンジフィードの実行を一時停止します。次に、他のチェンジフィードがブロックされなくなったことがわかります。
2.  TiCDCログで`apply job`のフィールドを検索し、時間のかかるDDLステートメントの`start-ts`を確認します。
3.  ダウンストリームでDDLステートメントを手動で実行します。実行終了後、以下の操作を行ってください。
4.  チェンジフィード構成を変更し、上記の`start-ts`を`ignore-txn-start-ts`構成項目に追加します。
5.  一時停止したチェンジフィードを再開します。

## TiCDCクラスタをv4.0.8にアップグレードした後、チェンジフィードを実行すると、 <code>[CDC:ErrKafkaInvalidConfig]Canal requires old value to be enabled</code>ますエラーが報告されます {#after-i-upgrade-the-ticdc-cluster-to-v4-0-8-the-code-cdc-errkafkainvalidconfig-canal-requires-old-value-to-be-enabled-code-error-is-reported-when-i-execute-a-changefeed}

v4.0.8以降、チェンジフィードの出力に`canal-json` 、または`canal`プロトコルが使用されている場合、 `maxwell`は古い値の機能を自動的に有効にします。ただし、TiCDCを以前のバージョンから`maxwell` `canal-json` `canal`使用し、古い値の機能が無効になっていると、このエラーが報告されます。

エラーを修正するには、次の手順を実行します。

1.  チェンジフィード構成ファイルの値`enable-old-value`を`true`に設定します。

2.  `cdc cli changefeed pause`を実行して、レプリケーションタスクを一時停止します。

    {{< copyable "" >}}

    ```shell
    cdc cli changefeed pause -c test-cf --pd=http://10.0.10.25:2379
    ```

3.  `cdc cli changefeed update`を実行して、元のチェンジフィード構成を更新します。

    {{< copyable "" >}}

    ```shell
    cdc cli changefeed update -c test-cf --pd=http://10.0.10.25:2379 --sink-uri="mysql://127.0.0.1:3306/?max-txn-row=20&worker-number=8" --config=changefeed.toml
    ```

4.  `cdc cli changfeed resume`を実行して、レプリケーションタスクを再開します。

    {{< copyable "" >}}

    ```shell
    cdc cli changefeed resume -c test-cf --pd=http://10.0.10.25:2379
    ```

## <code>[tikv:9006]GC life time is shorter than transaction duration, transaction starts at xx, GC safe point is yy</code>です。TiCDCを使用してチェンジフィードを作成すると、エラーが報告されます。 {#the-code-tikv-9006-gc-life-time-is-shorter-than-transaction-duration-transaction-starts-at-xx-gc-safe-point-is-yy-code-error-is-reported-when-i-use-ticdc-to-create-a-changefeed}

`pd-ctl service-gc-safepoint --pd <pd-addrs>`コマンドを実行して、現在のGCセーフポイントとサービスGCセーフポイントを照会する必要があります。 GCセーフポイントがTiCDCレプリケーションタスクの`start-ts` （チェンジフィード）よりも小さい場合は、 `cdc cli create changefeed`コマンドに`--disable-gc-check`オプションを直接追加して、チェンジフィードを作成できます。

`pd-ctl service-gc-safepoint --pd <pd-addrs>`の結果に`gc_worker service_id`がない場合：

-   PDのバージョンがv4.0.8以前の場合、詳細については[PDの問題＃3128](https://github.com/tikv/pd/issues/3128)を参照してください。
-   PDがv4.0.8以前のバージョンから新しいバージョンにアップグレードされた場合、詳細については[PDの問題＃3366](https://github.com/tikv/pd/issues/3366)を参照してください。

## TiCDCを使用してメッセージをKafkaに複製すると、Kafkaは<code>Message was too large</code>というエラーを返します {#when-i-use-ticdc-to-replicate-messages-to-kafka-kafka-returns-the-code-message-was-too-large-code-error}

TiCDC v4.0.8以前のバージョンでは、シンクURIでKafkaの`max-message-bytes`設定を構成するだけでは、Kafkaに出力されるメッセージのサイズを効果的に制御することはできません。メッセージサイズを制御するには、Kafkaが受信するメッセージのバイト数の制限も増やす必要があります。このような制限を追加するには、Kafkaサーバー構成に次の構成を追加します。

```
# The maximum byte number of a message that the broker receives
message.max.bytes=2147483648
# The maximum byte number of a message that the broker copies
replica.fetch.max.bytes=2147483648
# The maximum message byte number that the consumer side reads
fetch.message.max.bytes=2147483648
```

## TiCDCレプリケーション中にDDLステートメントがダウンストリームで実行されないかどうかを確認するにはどうすればよいですか？レプリケーションを再開するにはどうすればよいですか？ {#how-can-i-find-out-whether-a-ddl-statement-fails-to-execute-in-downstream-during-ticdc-replication-how-to-resume-the-replication}

DDLステートメントの実行に失敗すると、レプリケーションタスク（changefeed）は自動的に停止します。 checkpoint-tsは、DDLステートメントのfinish-tsから1を引いたものです。 TiCDCがダウンストリームでこのステートメントの実行を再試行する場合は、 `cdc cli changefeed resume`を使用してレプリケーションタスクを再開します。例えば：

{{< copyable "" >}}

```shell
cdc cli changefeed resume -c test-cf --pd=http://10.0.10.25:2379
```

失敗するこのDDLステートメントをスキップする場合は、changefeedのstart-tsをcheckpoint-ts（DDLステートメントが失敗するタイムスタンプ）に1を加えた値に設定します。たとえば、DDLステートメントが失敗するチェックポイント-tsが`415241823337054209`の場合、次のコマンドを実行して、このDDLステートメントをスキップします。

{{< copyable "" >}}

```shell
cdc cli changefeed update -c test-cf --pd=http://10.0.10.25:2379 --start-ts 415241823337054210
cdc cli changefeed resume -c test-cf --pd=http://10.0.10.25:2379
```
