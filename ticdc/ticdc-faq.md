---
title: TiCDC FAQs
summary: Learn the FAQs you might encounter when you use TiCDC.
---

# TiCDCのFAQ {#ticdc-faqs}

このドキュメントでは、TiCDCを使用するときに遭遇する可能性のある一般的な質問を紹介します。

> **ノート：**
>
> このドキュメントでは、 `cdc cli`コマンドで指定されたPDアドレスは`--pd=http://10.0.10.25:2379`です。コマンドを使用するときは、アドレスを実際のPDアドレスに置き換えてください。

## TiCDCでタスクを作成するときに<code>start-ts</code>を選択するにはどうすればよいですか？ {#how-do-i-choose-code-start-ts-code-when-creating-a-task-in-ticdc}

レプリケーションタスクの`start-ts`は、アップストリームTiDBクラスタのタイムスタンプOracle（TSO）に対応します。 TiCDCは、レプリケーションタスクでこのTSOにデータを要求します。したがって、レプリケーションタスクの`start-ts`は、次の要件を満たす必要があります。

-   `start-ts`の値は、現在のTiDBクラスタの`tikv_gc_safe_point`の値よりも大きくなります。そうしないと、タスクの作成時にエラーが発生します。
-   タスクを開始する前に、ダウンストリームに`start-ts`より前のすべてのデータがあることを確認してください。メッセージキューへのデータの複製などのシナリオで、アップストリームとダウンストリーム間のデータの整合性が必要ない場合は、アプリケーションのニーズに応じてこの要件を緩和できます。

`start-ts`を指定しない場合、または`start-ts`を`0`として指定する場合、レプリケーションタスクの開始時に、TiCDCは現在のTSOを取得し、このTSOからタスクを開始します。

## TiCDCでタスクを作成すると、一部のテーブルを複製できないのはなぜですか？ {#why-can-t-some-tables-be-replicated-when-i-create-a-task-in-ticdc}

`cdc cli changefeed create`を実行してレプリケーションタスクを作成すると、TiCDCはアップストリームテーブルが[レプリケーションの制限](/ticdc/ticdc-overview.md#restrictions)を満たしているかどうかを確認します。一部のテーブルが制限を満たしていない場合は、不適格なテーブルのリストとともに`some tables are not eligible to replicate`が返されます。 `Y`または`y`を選択してタスクの作成を続行でき、これらのテーブルのすべての更新はレプリケーション中に自動的に無視されます。 `Y`または`y`以外の入力を選択した場合、レプリケーションタスクは作成されません。

## TiCDCレプリケーションタスクの状態を表示するにはどうすればよいですか？ {#how-do-i-view-the-state-of-ticdc-replication-tasks}

TiCDCレプリケーションタスクのステータスを表示するには、 `cdc cli`を使用します。例えば：

{{< copyable "" >}}

```shell
cdc cli changefeed list --pd=http://10.0.10.25:2379
```

期待される出力は次のとおりです。

```json
[{
    "id": "4e24dde6-53c1-40b6-badf-63620e4940dc",
    "summary": {
      "state": "normal",
      "tso": 417886179132964865,
      "checkpoint": "2020-07-07 16:07:44.881",
      "error": null
    }
}]
```

-   `checkpoint` ：TiCDCは、このタイムスタンプより前のすべてのデータをダウンストリームに複製しました。
-   `state` ：このレプリケーションタスクの状態：
    -   `normal` ：タスクは正常に実行されます。
    -   `stopped` ：タスクが手動で停止されたか、エラーが発生しました。
    -   `removed` ：タスクは削除されます。

> **ノート：**
>
> この機能はTiCDC4.0.3で導入されました。

## TiCDC <code>gc-ttl</code>とは何ですか？ {#what-is-code-gc-ttl-code-in-ticdc}

v4.0.0-rc.1以降、PDはサービスレベルのGCセーフポイントを設定する際に外部サービスをサポートします。どのサービスでも、GCセーフポイントを登録および更新できます。 PDは、このGCセーフポイントより後のKey-ValueデータがGCによってクリーンアップされないようにします。

レプリケーションタスクが使用できないか中断されている場合、この機能により、TiCDCによって消費されるデータがGCによってクリーンアップされることなくTiKVに保持されます。

TiCDCサーバーを起動するときに、 `gc-ttl`を構成することにより、GCセーフポイントの存続時間（TTL）期間を指定できます。 `gc-ttl`もでき[TiUPを使用して変更する](/ticdc/manage-ticdc.md#modify-ticdc-configuration-using-tiup) 。デフォルト値は24時間です。 TiCDCでは、この値は次のことを意味します。

-   TiCDCサービスが停止した後、GCセーフポイントがPDに保持される最大時間。
-   タスクが中断または手動で停止された後、レプリケーションタスクを一時停止できる最大時間。中断されたレプリケーションタスクの時間が`gc-ttl`で設定された値より長い場合、レプリケーションタスクは`failed`ステータスになり、再開できず、GCセーフポイントの進行に影響を与え続けることができません。

上記の2番目の動作は、TiCDCv4.0.13以降のバージョンで導入されています。目的は、TiCDCのレプリケーションタスクが長時間中断され、アップストリームTiKVクラスタのGCセーフポイントが長時間継続せず、古いデータバージョンが多すぎて、アップストリームクラスタのパフォーマンスに影響を与えるのを防ぐことです。

> **ノート：**
>
> 一部のシナリオでは、たとえば、 Dumpling/ BRを使用した完全レプリケーションの後に増分レプリケーションにTiCDCを使用する場合、デフォルトの24時間の`gc-ttl`では不十分な場合があります。 TiCDCサーバーを起動するときは、 `gc-ttl`に適切な値を指定する必要があります。

## TiCDCガベージコレクション（GC）セーフポイントの完全な動作は何ですか？ {#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint}

TiCDCサービスの開始後にレプリケーションタスクが開始された場合、TiCDC所有者は、すべてのレプリケーションタスクの中で最小値の`checkpoint-ts`でPDサービスGCセーフポイントを更新します。サービスGCセーフポイントは、TiCDCがその時点およびそれ以降に生成されたデータを削除しないことを保証します。レプリケーションタスクが中断された場合、または手動で停止された場合、このタスクの`checkpoint-ts`は変更されません。一方、PDの対応するサービスGCセーフポイントも更新されません。

レプリケーションタスクが`gc-ttl`で指定された時間より長く中断された場合、レプリケーションタスクは`failed`ステータスになり、再開できません。 PDに対応するサービスGCセーフポイントは続行されます。

TiCDCがサービスGCセーフポイントに設定するTime-To-Live（TTL）は24時間です。つまり、TiCDCサービスが中断されてから24時間以内に回復できる場合、GCメカニズムはデータを削除しません。

## TiCDCタイムゾーンとアップストリーム/ダウンストリームデータベースのタイムゾーンの関係を理解するにはどうすればよいですか？ {#how-to-understand-the-relationship-between-the-ticdc-time-zone-and-the-time-zones-of-the-upstream-downstream-databases}

|                              |                              上流のタイムゾーン                             |                                  TiCDCタイムゾーン                                 |                            下流のタイムゾーン                           |
| :--------------------------: | :----------------------------------------------------------------: | :--------------------------------------------------------------------------: | :------------------------------------------------------------: |
| Configuration / コンフィグレーション方法 |              [タイムゾーンのサポート](/configure-time-zone.md)を参照             |                       TiCDCサーバーの起動時に`--tz`パラメーターを使用して構成                      |               `sink-uri`の`time-zone`パラメータを使用して構成               |
|              説明              | アップストリームTiDBのタイムゾーン。タイムスタンプタイプのDML操作とタイムスタンプタイプの列に関連するDDL操作に影響します。 | TiCDCは、アップストリームTiDBのタイムゾーンがTiCDCタイムゾーン構成と同じであると想定し、タイムスタンプ列に対して関連する操作を実行します。 | ダウンストリームMySQLは、ダウンストリームタイムゾーン設定に従って、DMLおよびDDL操作のタイムスタンプを処理します。 |

> **ノート：**
>
> TiCDCサーバーのタイムゾーンを設定するときは注意してください。このタイムゾーンはタイムタイプの変換に使用されるためです。アップストリームタイムゾーン、TiCDCタイムゾーン、およびダウンストリームタイムゾーンの一貫性を保ちます。 TiCDCサーバーは、次の優先順位でタイムゾーンを選択します。
>
> -   TiCDCは、最初に`--tz`を使用して指定されたタイムゾーンを使用します。
> -   `--tz`が使用できない場合、TiCDCは`TZ`環境変数を使用して設定されたタイムゾーンを読み取ろうとします。
> -   `TZ`の環境変数が使用できない場合、TiCDCはマシンのデフォルトのタイムゾーンを使用します。

## <code>--config</code>で構成ファイルを指定せずにレプリケーションタスクを作成した場合のTiCDCのデフォルトの動作は何ですか？ {#what-is-the-default-behavior-of-ticdc-if-i-create-a-replication-task-without-specifying-the-configuration-file-in-code-config-code}

`-config`パラメータを指定せずに`cdc cli changefeed create`コマンドを使用すると、TiCDCは次のデフォルトの動作でレプリケーションタスクを作成します。

-   システムテーブルを除くすべてのテーブルを複製します
-   古い値機能を有効にします
-   [有効なインデックス](/ticdc/ticdc-overview.md#restrictions)を含まないテーブルの複製をスキップします

## TiCDCは、Canal形式でのデータ変更の出力をサポートしていますか？ {#does-ticdc-support-outputting-data-changes-in-the-canal-format}

はい。 Canal出力を有効にするには、 `--sink-uri`パラメーターでプロトコルを`canal`として指定します。例えば：

{{< copyable "" >}}

```shell
cdc cli changefeed create --pd=http://10.0.10.25:2379 --sink-uri="kafka://127.0.0.1:9092/cdc-test?kafka-version=2.4.0&protocol=canal" --config changefeed.toml
```

> **ノート：**
>
> -   この機能はTiCDC4.0.2で導入されました。
> -   TiCDCは現在、KafkaやPulsarなどのMQシンクにのみCanal形式でデータ変更を出力することをサポートしています。

詳細については、 [レプリケーションタスクを作成する](/ticdc/manage-ticdc.md#create-a-replication-task)を参照してください。

## TiCDCからKafkaまでのレイテンシーがますます高くなるのはなぜですか？ {#why-does-the-latency-from-ticdc-to-kafka-become-higher-and-higher}

-   [TiCDCレプリケーションタスクの状態を表示するにはどうすればよいですか](#how-do-i-view-the-state-of-ticdc-replication-tasks)を確認してください。
-   Kafkaの次のパラメータを調整します。

    -   `message.max.bytes`の値を`server.properties`から`1073741824` （1 GB）に増やします。
    -   `replica.fetch.max.bytes`の値を`server.properties`から`1073741824` （1 GB）に増やします。
    -   `consumer.properties`の`fetch.message.max.bytes`の値を増やして、 `message.max.bytes`の値より大きくします。

## TiCDCがデータをKafkaに複製するとき、トランザクション内のすべての変更を1つのメッセージに書き込みますか？そうでない場合、それはどのような基準で変更を分割しますか？ {#when-ticdc-replicates-data-to-kafka-does-it-write-all-the-changes-in-a-transaction-into-one-message-if-not-on-what-basis-does-it-divide-the-changes}

いいえ。構成されたさまざまな配布戦略に従って、 `row id`は`default` 、および`table`を含むさまざまなベースで変更を分割し`ts` 。

詳細については、 [レプリケーションタスク構成ファイル](/ticdc/manage-ticdc.md#task-configuration-file)を参照してください。

## TiCDCがKafkaにデータを複製するとき、TiDBの単一メッセージの最大サイズを制御できますか？ {#when-ticdc-replicates-data-to-kafka-can-i-control-the-maximum-size-of-a-single-message-in-tidb}

はい。 `max-message-bytes`パラメーターを設定して、毎回Kafkaブローカーに送信されるデータの最大サイズを制御できます（オプション、デフォルトでは`10MB` ）。 `max-batch-size`を設定して、各Kafkaメッセージの変更レコードの最大数を指定することもできます。現在、この設定は、Kafkaの`protocol`が`open-protocol` （オプション、デフォルトでは`16` ）の場合にのみ有効になります。

## TiCDCがデータをKafkaに複製するとき、メッセージには複数のタイプのデータ変更が含まれていますか？ {#when-ticdc-replicates-data-to-kafka-does-a-message-contain-multiple-types-of-data-changes}

はい。 1つのメッセージに複数の`update`または`delete`が含まれる場合があり、 `update`と`delete`が共存する場合があります。

## TiCDCがデータをKafkaに複製する場合、TiCDC Open Protocolの出力でタイムスタンプ、テーブル名、およびスキーマ名を表示するにはどうすればよいですか？ {#when-ticdc-replicates-data-to-kafka-how-do-i-view-the-timestamp-table-name-and-schema-name-in-the-output-of-ticdc-open-protocol}

この情報は、Kafkaメッセージのキーに含まれています。例えば：

```json
{
    "ts":<TS>,
    "scm":<Schema Name>,
    "tbl":<Table Name>,
    "t":1
}
```

詳細については、 [TiCDCOpenProtocolイベント形式](/ticdc/ticdc-open-protocol.md#event-format)を参照してください。

## TiCDCがデータをKafkaに複製するとき、メッセージ内のデータ変更のタイムスタンプをどのように知ることができますか？ {#when-ticdc-replicates-data-to-kafka-how-do-i-know-the-timestamp-of-the-data-changes-in-a-message}

Unixタイムスタンプを取得するには、Kafkaメッセージのキーの`ts`を18ビット右に移動します。

## TiCDC Open Protocolはどのように<code>null</code>を表しますか？ {#how-does-ticdc-open-protocol-represent-code-null-code}

TiCDC Open Protocolでは、タイプコード`6`は`null`を表します。

| タイプ | コード | 出力例                | ノート |
| :-- | :-- | :----------------- | :-- |
| ヌル  | 6   | `{"t":6,"v":null}` |     |

詳細については、 [TiCDCOpenProtocol列タイプコード](/ticdc/ticdc-open-protocol.md#column-type-code)を参照してください。

## TiCDC Open Protocolの行変更イベントが<code>INSERT</code>イベントなのか<code>UPDATE</code>イベントなのかはどうすればわかりますか？ {#how-can-i-tell-if-a-row-changed-event-of-ticdc-open-protocol-is-an-code-insert-code-event-or-an-code-update-code-event}

Old Value機能が有効になっていない場合、TiCDCOpenProtocolの行変更イベントが`INSERT`イベントであるか`UPDATE`イベントであるかを判断できません。この機能が有効になっている場合は、含まれているフィールドによってイベントタイプを判別できます。

-   `UPDATE`イベントには`"p"`フィールドと`"u"`フィールドの両方が含まれます
-   `INSERT`イベントには`"u"`フィールドのみが含まれます
-   `DELETE`イベントには`"d"`フィールドのみが含まれます

詳細については、 [オープンプロトコル行変更イベント形式](/ticdc/ticdc-open-protocol.md#row-changed-event)を参照してください。

## TiCDCはどのくらいのPDストレージを使用しますか？ {#how-much-pd-storage-does-ticdc-use}

TiCDCはPDでetcdを使用して、メタデータを保存し、定期的に更新します。 etcdのMVCCとPDのデフォルトの圧縮の間の時間間隔は1時間であるため、TiCDCが使用するPDストレージの量は、この1時間以内に生成されるメタデータバージョンの量に比例します。ただし、v4.0.5、v4.0.6、およびv4.0.7では、TiCDCに頻繁な書き込みの問題があるため、1時間に1000個のテーブルが作成またはスケジュールされている場合、etcdストレージをすべて使用し、 `etcdserver: mvcc: database space exceeded`のエラーを返します。 。このエラーが発生した後、etcdストレージをクリーンアップする必要があります。詳細については、 [etcdmaintainceスペースクォータ](https://etcd.io/docs/v3.4.0/op-guide/maintenance/#space-quota)を参照してください。クラスタをv4.0.9以降のバージョンにアップグレードすることをお勧めします。

## TiCDCは大規模なトランザクションの複製をサポートしていますか？リスクはありますか？ {#does-ticdc-support-replicating-large-transactions-is-there-any-risk}

TiCDCは、大規模なトランザクション（5 GBを超えるサイズ）を部分的にサポートします。さまざまなシナリオに応じて、次のリスクが存在する可能性があります。

-   TiCDCの内部処理能力が不十分な場合、レプリケーションタスクエラー`ErrBufferReachLimit`が発生する可能性があります。
-   TiCDCの内部処理能力が不十分な場合、またはTiCDCのダウンストリームのスループット能力が不十分な場合、メモリ不足（OOM）が発生する可能性があります。

上記のエラーが発生した場合は、BRを使用して大規模なトランザクションの増分データを復元することをお勧めします。詳細な操作は次のとおりです。

1.  大規模なトランザクションのために終了したチェンジフィードの`checkpoint-ts`を記録し、このTSOをBR増分バックアップの`--lastbackupts`として使用して、 [増分データバックアップ](/br/br-usage-backup.md#back-up-incremental-data)を実行します。
2.  インクリメンタルデータをバックアップした後、BRログ出力に`["Full backup Failed summary : total backup ranges: 0, total success: 0, total failed: 0"] [BackupTS=421758868510212097]`に類似したログレコードを見つけることができます。このログに`BackupTS`を記録します。
3.  [インクリメンタルデータを復元する](/br/br-usage-restore.md#restore-incremental-data) 。
4.  新しいチェンジフィードを作成し、 `BackupTS`からレプリケーションタスクを開始します。
5.  古いチェンジフィードを削除します。

## DDLステートメントをダウンストリームのMySQL 5.7に複製する場合、時間タイプフィールドのデフォルト値に一貫性がありません。私に何ができる？ {#the-default-value-of-the-time-type-field-is-inconsistent-when-replicating-a-ddl-statement-to-the-downstream-mysql-5-7-what-can-i-do}

`create table test (id int primary key, ts timestamp)`ステートメントがアップストリームTiDBで実行されると仮定します。 TiCDCがこのステートメントをダウンストリームのMySQL5.7に複製する場合、 MySQL 5.7はデフォルト構成を使用します。レプリケーション後のテーブルスキーマは次のとおりです。 `timestamp`フィールドのデフォルト値は`CURRENT_TIMESTAMP`になります：

{{< copyable "" >}}

```sql
mysql root@127.0.0.1:test> show create table test;
+-------+----------------------------------------------------------------------------------+
| Table | Create Table                                                                     |
+-------+----------------------------------------------------------------------------------+
| test  | CREATE TABLE `test` (                                                            |
|       |   `id` int(11) NOT NULL,                                                         |
|       |   `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, |
|       |   PRIMARY KEY (`id`)                                                             |
|       | ) ENGINE=InnoDB DEFAULT CHARSET=latin1                                           |
+-------+----------------------------------------------------------------------------------+
1 row in set
```

結果から、レプリケーションの前後のテーブルスキーマに一貫性がないことがわかります。これは、TiDBのデフォルト値`explicit_defaults_for_timestamp`がMySQLのデフォルト値と異なるためです。詳細については、 [MySQLの互換性](/mysql-compatibility.md#default-differences)を参照してください。

v5.0.1またはv4.0.13以降、MySQLへのレプリケーションごとに、TiCDCは自動的に`explicit_defaults_for_timestamp = ON`を設定して、時間タイプがアップストリームとダウンストリームの間で一貫していることを確認します。 v5.0.1またはv4.0.13より前のバージョンでは、TiCDCを使用して時間タイプデータを複製するときに、一貫性のない`explicit_defaults_for_timestamp`値によって引き起こされる互換性の問題に注意してください。

## TiCDCレプリケーションタスクを作成すると、 <code>enable-old-value</code>が<code>true</code>に設定されますが、アップストリームからの<code>INSERT</code> / <code>UPDATE</code>ステートメントは、ダウンストリームにレプリケートされた後、 <code>REPLACE INTO</code>になります。 {#code-enable-old-value-code-is-set-to-code-true-code-when-i-create-a-ticdc-replication-task-but-code-insert-code-code-update-code-statements-from-the-upstream-become-code-replace-into-code-after-being-replicated-to-the-downstream}

TiCDCでチェンジフィードが作成されると、 `safe-mode`の設定はデフォルトで`true`になり、アップストリームの`INSERT`ステートメントに対して実行する`REPLACE INTO`ステートメントが生成され`UPDATE` 。

現在、ユーザーは`safe-mode`の設定を変更できないため、この問題は現在解決策がありません。

## ダウンストリームのレプリケーションのシンクがTiDBまたはMySQLの場合、ダウンストリームデータベースのユーザーにはどのような権限が必要ですか？ {#when-the-sink-of-the-replication-downstream-is-tidb-or-mysql-what-permissions-do-users-of-the-downstream-database-need}

シンクがTiDBまたはMySQLの場合、ダウンストリームデータベースのユーザーには次の権限が必要です。

-   `Select`
-   `Index`
-   `Insert`
-   `Update`
-   `Delete`
-   `Create`
-   `Drop`
-   `Alter`
-   `Create View`

`recover table`をダウンストリームTiDBに複製する必要がある場合は、 `Super`の権限が必要です。

## TiCDCがディスクを使用するのはなぜですか？ TiCDCはいつディスクに書き込みますか？ TiCDCはレプリケーションパフォーマンスを向上させるためにメモリバッファを使用しますか？ {#why-does-ticdc-use-disks-when-does-ticdc-write-to-disks-does-ticdc-use-memory-buffer-to-improve-replication-performance}

アップストリームの書き込みトラフィックがピーク時にある場合、ダウンストリームはすべてのデータをタイムリーに消費できず、データが蓄積する可能性があります。 TiCDCは、ディスクを使用して、積み上げられたデータを処理します。 TiCDCは、通常の操作中にディスクにデータを書き込む必要があります。ただし、ディスクへの書き込みでは100ミリ秒以内の遅延しか発生しないため、これは通常、レプリケーションスループットとレプリケーション遅延のボトルネックにはなりません。 TiCDCはまた、メモリを使用してディスクからのデータの読み取りを高速化し、レプリケーションのパフォーマンスを向上させます。

## TiCDCを使用したレプリケーションが停止したり、 TiDB LightningとBRを使用したデータの復元後に停止したりするのはなぜですか？ {#why-does-replication-using-ticdc-stall-or-even-stop-after-data-restore-using-tidb-lightning-and-br}

現在、TiCDCはTiDB LightningおよびBRと完全には互換性がありません。したがって、TiCDCによって複製されるテーブルでTiDB LightningおよびBRを使用することは避けてください。
