---
title: TiCDC FAQs
summary: Learn the FAQs you might encounter when you use TiCDC.
---

# TiCDC よくある質問 {#ticdc-faqs}

このドキュメントでは、TiCDC を使用する際に遭遇する可能性のある一般的な質問を紹介します。

> **ノート：**
>
> このドキュメントでは、 `cdc cli`コマンドで指定されたサーバーアドレスは`--server=http://127.0.0.1:8300`です。コマンドを使用するときは、アドレスを実際の PD アドレスに置き換えます。

## TiCDC でタスクを作成するときに<code>start-ts</code>選択するにはどうすればよいですか? {#how-do-i-choose-code-start-ts-code-when-creating-a-task-in-ticdc}

レプリケーション タスクの`start-ts`は、上流の TiDB クラスターのタイムスタンプ Oracle (TSO) に対応します。 TiCDC は、レプリケーション タスクでこの TSO からのデータを要求します。したがって、レプリケーション タスクの`start-ts`は次の要件を満たす必要があります。

-   `start-ts`の値は、現在の TiDB クラスターの`tikv_gc_safe_point`値よりも大きいです。そうしないと、タスクの作成時にエラーが発生します。
-   タスクを開始する前に、ダウンストリームに`start-ts`より前のすべてのデータがあることを確認してください。データをメッセージ キューにレプリケートするなどのシナリオで、アップストリームとダウンストリーム間のデータの一貫性が必要ない場合は、アプリケーションの必要に応じてこの要件を緩和できます。

`start-ts`を指定しない場合、または`start-ts`を`0`として指定した場合、レプリケーション タスクの開始時に、TiCDC は現在の TSO を取得し、この TSO からタスクを開始します。

## TiCDC でタスクを作成するときに一部のテーブルを複製できないのはなぜですか? {#why-can-t-some-tables-be-replicated-when-i-create-a-task-in-ticdc}

`cdc cli changefeed create`を実行してレプリケーション タスクを作成すると、TiCDC はアップストリーム テーブルが[複製要件](/ticdc/ticdc-overview.md#best-practices)を満たすかどうかをチェックします。一部のテーブルが要件を満たしていない場合、不適格なテーブルのリストとともに`some tables are not eligible to replicate`が返されます。タスクの作成を続行するには、 `Y`または`y`を選択できます。これらのテーブルに対するすべての更新は、レプリケーション中に自動的に無視されます。 `Y`または`y`以外の入力を選択すると、レプリケーション タスクは作成されません。

## TiCDC レプリケーション タスクの状態を表示するにはどうすればよいですか? {#how-do-i-view-the-state-of-ticdc-replication-tasks}

TiCDC レプリケーション タスクのステータスを表示するには、 `cdc cli`を使用します。例えば：

{{< copyable "" >}}

```shell
cdc cli changefeed list --server=http://127.0.0.1:8300
```

予想される出力は次のとおりです。

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

-   `checkpoint` : TiCDC は、このタイムスタンプより前のすべてのデータをダウンストリームに複製しました。
-   `state` : このレプリケーション タスクの状態:
    -   `normal` : タスクは正常に実行されます。
    -   `stopped` : タスクは手動で停止されたか、エラーが発生しました。
    -   `removed` : タスクは削除されます。

> **ノート：**
>
> この機能は TiCDC 4.0.3 で導入されました。

## TiCDC の<code>gc-ttl</code>は何ですか? {#what-is-code-gc-ttl-code-in-ticdc}

v4.0.0-rc.1 以降、PD はサービスレベル GC セーフポイントの設定で外部サービスをサポートします。どのサービスも、その GC セーフポイントを登録および更新できます。 PD は、この GC セーフポイントより後のキー値データが GC によって消去されないようにします。

レプリケーション タスクが利用できないか中断されている場合、この機能により、TiCDC によって消費されるデータが GC によってクリーニングされることなく TiKV に保持されます。

TiCDCサーバーを起動するときに、 `gc-ttl`を構成することで、GC セーフポイントの Time To Live (TTL) 期間を指定できます。 [TiUPを使用して変更する](/ticdc/deploy-ticdc.md#modify-ticdc-cluster-configurations-using-tiup) `gc-ttl`もできます。デフォルト値は 24 時間です。 TiCDC では、この値は次のことを意味します。

-   TiCDC サービスが停止した後、PD で GC セーフポイントが保持される最大時間。
-   タスクが中断または手動で停止された後、レプリケーション タスクを一時停止できる最大時間。中断されたレプリケーション タスクの時間が`gc-ttl`で設定された値よりも長い場合、レプリケーション タスクは`failed`ステータスになり、再開できず、GC セーフポイントの進行に影響を与え続けることはできません。

上記の 2 番目の動作は、TiCDC v4.0.13 以降のバージョンで導入されています。目的は、TiCDC でのレプリケーション タスクが長時間中断され、上流の TiKV クラスターの GC セーフポイントが長時間継続されず、古いデータ バージョンが保持されすぎて、上流のクラスターのパフォーマンスに影響を与えるのを防ぐことです。

> **ノート：**
>
> 一部のシナリオでは、たとえばDumpling/ BRを使用した完全レプリケーションの後に TiCDC を増分レプリケーションに使用する場合、デフォルトの 24 時間の`gc-ttl`では不十分な場合があります。 TiCDCサーバーを起動するときに、 `gc-ttl`に適切な値を指定する必要があります。

## TiCDCガベージコレクション(GC) セーフポイントの完全な動作は何ですか? {#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint}

TiCDC サービスの開始後にレプリケーション タスクが開始された場合、TiCDC 所有者は PD サービスの GC セーフポイントを、すべてのレプリケーション タスクの中で最小の値`checkpoint-ts`で更新します。サービス GC セーフポイントは、TiCDC がその時点およびそれ以降に生成されたデータを削除しないことを保証します。複製タスクが中断された場合、または手動で停止された場合、このタスクの`checkpoint-ts`は変更されません。一方、PD の対応するサービス GC セーフポイントも更新されません。

レプリケーション タスクが`gc-ttl`で指定された時間より長く中断された場合、レプリケーション タスクは`failed`ステータスになり、再開できません。 PD対応サービスGCセーフポイントは継続します。

TiCDC がサービス GC セーフポイントに設定する Time-To-Live (TTL) は 24 時間です。つまり、TiCDC サービスが中断されてから 24 時間以内に回復できる場合、GC メカニズムはデータを削除しません。

## TiCDC タイム ゾーンとアップストリーム/ダウンストリーム データベースのタイム ゾーンとの関係を理解するにはどうすればよいですか? {#how-to-understand-the-relationship-between-the-ticdc-time-zone-and-the-time-zones-of-the-upstream-downstream-databases}

|              |                           アップストリーム タイム ゾーン                           |                                   TiCDC タイムゾーン                                  |                            ダウンストリーム タイム ゾーン                            |
| :----------: | :------------------------------------------------------------------: | :-----------------------------------------------------------------------------: | :--------------------------------------------------------------------: |
| コンフィグレーション方法 |            [タイムゾーンのサポート](/configure-time-zone.md)を参照してください           |                        TiCDCサーバーの起動時に`--tz`パラメーターを使用して構成                        |                   `sink-uri`の`time-zone`パラメータを使用して設定                   |
|      説明      | タイムスタンプ型の DML 操作と、タイムスタンプ型の列に関連する DDL 操作に影響するアップストリーム TiDB のタイム ゾーン。 | TiCDC は、上流の TiDB のタイム ゾーンが TiCDC タイム ゾーンの構成と同じであると想定し、タイムスタンプ列に対して関連する操作を実行します。 | ダウンストリームの MySQL は、ダウンストリームのタイム ゾーン設定に従って、DML および DDL 操作のタイムスタンプを処理します。 |

> **ノート：**
>
> TiCDCサーバーのタイム ゾーンを設定するときは注意してください。このタイム ゾーンは時間型の変換に使用されるためです。アップストリームのタイム ゾーン、TiCDC タイム ゾーン、およびダウンストリームのタイム ゾーンの一貫性を保ちます。 TiCDCサーバーは、次の優先順位でタイム ゾーンを選択します。
>
> -   TiCDC は、最初に`--tz`を使用して指定されたタイム ゾーンを使用します。
> -   `--tz`が使用できない場合、TiCDC は`TZ`環境変数を使用して設定されたタイム ゾーンを読み取ろうとします。
> -   `TZ`環境変数が使用できない場合、TiCDC はマシンの既定のタイム ゾーンを使用します。

## <code>--config</code>で構成ファイルを指定せずにレプリケーション タスクを作成した場合、TiCDC の既定の動作はどのようになりますか? {#what-is-the-default-behavior-of-ticdc-if-i-create-a-replication-task-without-specifying-the-configuration-file-in-code-config-code}

`-config`パラメータを指定せずに`cdc cli changefeed create`コマンドを使用すると、TiCDC は次のデフォルトの動作でレプリケーション タスクを作成します。

-   システム テーブルを除くすべてのテーブルをレプリケートします。
-   古い値機能を有効にします
-   [有効なインデックス](/ticdc/ticdc-overview.md#best-practices)を含むテーブルのみをレプリケートします

## TiCDC は Canal 形式でのデータ変更の出力をサポートしていますか? {#does-ticdc-support-outputting-data-changes-in-the-canal-format}

はい。 Canal 出力を有効にするには、 `--sink-uri`パラメータでプロトコルを`canal`に指定します。例えば：

{{< copyable "" >}}

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="kafka://127.0.0.1:9092/cdc-test?kafka-version=2.4.0&protocol=canal" --config changefeed.toml
```

> **ノート：**
>
> -   この機能は TiCDC 4.0.2 で導入されました。
> -   TiCDC は現在、Kafka などの MQ シンクへの Canal 形式でのデータ変更の出力のみをサポートしています。

詳細については、 [TiCDC 変更フィード構成](/ticdc/ticdc-changefeed-config.md)を参照してください。

## TiCDC から Kafka へのレイテンシーがますます高くなるのはなぜですか? {#why-does-the-latency-from-ticdc-to-kafka-become-higher-and-higher}

-   [TiCDC レプリケーション タスクの状態を表示する方法](#how-do-i-view-the-state-of-ticdc-replication-tasks)を確認してください。
-   Kafka の次のパラメーターを調整します。

    -   `server.properties` `message.max.bytes`値を`1073741824` (1 GB) に増やします。
    -   `server.properties` `replica.fetch.max.bytes`値を`1073741824` (1 GB) に増やします。
    -   `consumer.properties`の`fetch.message.max.bytes`値を増やして`message.max.bytes`値よりも大きくします。

## TiCDC がデータを Kafka にレプリケートする場合、TiDB で単一メッセージの最大サイズを制御できますか? {#when-ticdc-replicates-data-to-kafka-can-i-control-the-maximum-size-of-a-single-message-in-tidb}

`protocol`が`avro`または`canal-json`に設定されている場合、行の変更ごとにメッセージが送信されます。 1 つの Kafka メッセージには 1 行の変更のみが含まれ、通常は Kafka の制限を超えません。したがって、1 つのメッセージのサイズを制限する必要はありません。 1 つの Kafka メッセージのサイズが Kafka の制限を超える場合は、 [TiCDC から Kafka へのレイテンシーがますます高くなるのはなぜですか?](/ticdc/ticdc-faq.md#why-does-the-latency-from-ticdc-to-kafka-become-higher-and-higher)を参照してください。

`protocol`が`open-protocol`に設定されている場合、メッセージはバッチで送信されます。したがって、1 つの Kafka メッセージが過度に大きくなる可能性があります。この状況を回避するには、 `max-message-bytes`パラメータを設定して、毎回 Kafka ブローカに送信されるデータの最大サイズを制御できます (オプション、デフォルトでは`10MB` )。 `max-batch-size`パラメーター (オプション、デフォルトでは`16` ) を構成して、各 Kafka メッセージ内の変更レコードの最大数を指定することもできます。

## トランザクションで行を複数回変更すると、TiCDC は複数の行変更イベントを出力しますか? {#if-i-modify-a-row-multiple-times-in-a-transaction-will-ticdc-output-multiple-row-change-events}

いいえ。1 つのトランザクションで同じ行を複数回変更すると、TiDB は最新の変更のみを TiKV に送信します。したがって、TiCDC は最新の変更の結果しか取得できません。

## TiCDC がデータを Kafka にレプリケートする場合、メッセージには複数の種類のデータ変更が含まれますか? {#when-ticdc-replicates-data-to-kafka-does-a-message-contain-multiple-types-of-data-changes}

はい。 1 つのメッセージに複数の`update`または`delete`が含まれる場合があり、 `update`と`delete`共存する場合があります。

## TiCDC がデータを Kafka にレプリケートする場合、TiCDC Open Protocol の出力でタイムスタンプ、テーブル名、およびスキーマ名を表示するにはどうすればよいですか? {#when-ticdc-replicates-data-to-kafka-how-do-i-view-the-timestamp-table-name-and-schema-name-in-the-output-of-ticdc-open-protocol}

この情報は、Kafka メッセージのキーに含まれています。例えば：

```json
{
    "ts":<TS>,
    "scm":<Schema Name>,
    "tbl":<Table Name>,
    "t":1
}
```

詳細については、 [TiCDC Open Protocol イベント形式](/ticdc/ticdc-open-protocol.md#event-format)を参照してください。

## TiCDC がデータを Kafka にレプリケートするとき、メッセージ内のデータ変更のタイムスタンプを知るにはどうすればよいですか? {#when-ticdc-replicates-data-to-kafka-how-do-i-know-the-timestamp-of-the-data-changes-in-a-message}

Kafka メッセージのキーの`ts` 18 ビット右に移動することで、UNIX タイムスタンプを取得できます。

## TiCDC Open Protocol は<code>null</code>をどのように表しますか? {#how-does-ticdc-open-protocol-represent-code-null-code}

TiCDC Open Protocol では、タイプ コード`6`は`null`を表します。

| タイプ | コード | 出力例                | ノート |
| :-- | :-- | :----------------- | :-- |
| ヌル  | 6   | `{"t":6,"v":null}` |     |

詳細については、 [TiCDC Open Protocol カラム タイプ コード](/ticdc/ticdc-open-protocol.md#column-type-code)を参照してください。

## TiCDC Open Protocol の Row Changed Event が<code>INSERT</code>イベントなのか<code>UPDATE</code>イベントなのか、どうすればわかりますか? {#how-can-i-tell-if-a-row-changed-event-of-ticdc-open-protocol-is-an-code-insert-code-event-or-an-code-update-code-event}

Old Value 機能が有効になっていない場合、TiCDC Open Protocol の Row Changed Event が`INSERT`イベントか`UPDATE`イベントかを判断できません。この機能が有効になっている場合は、含まれるフィールドによってイベント タイプを判別できます。

-   `UPDATE`イベントには`"p"`と`"u"`フィールドの両方が含まれます
-   `INSERT`イベントには`"u"`フィールドのみが含まれます
-   `DELETE`イベントには`"d"`フィールドのみが含まれます

詳細については、 [オープンプロトコル行変更イベント形式](/ticdc/ticdc-open-protocol.md#row-changed-event)を参照してください。

## TiCDC はどのくらいの PDstorageを使用しますか? {#how-much-pd-storage-does-ticdc-use}

TiCDC は PD で etcd を使用してメタデータを保存し、定期的に更新します。 etcd の MVCC と PD のデフォルトの圧縮の間の時間間隔は 1 時間であるため、TiCDC が使用する PDstorageの量は、この時間内に生成されたメタデータ バージョンの量に比例します。ただし、v4.0.5、v4.0.6、および v4.0.7 では、TiCDC は頻繁に書き込みを行うという問題があるため、1 時間に 1000 個のテーブルが作成またはスケジュールされている場合、etcdstorageをすべて占有し、 `etcdserver: mvcc: database space exceeded`エラーを返します。 .このエラーが発生した後、etcdstorageをクリーンアップする必要があります。詳細は[etcd メンテナンス スペース クォータ](https://etcd.io/docs/v3.4.0/op-guide/maintenance/#space-quota)参照してください。クラスターを v4.0.9 以降のバージョンにアップグレードすることをお勧めします。

## TiCDC は大規模なトランザクションの複製をサポートしていますか?リスクはありますか？ {#does-ticdc-support-replicating-large-transactions-is-there-any-risk}

TiCDC は、大規模なトランザクション (サイズが 5 GB を超える) の部分的なサポートを提供します。さまざまなシナリオに応じて、次のリスクが存在する可能性があります。

-   プライマリ/セカンダリ レプリケーションのレイテンシーが大幅に増加する可能性があります。
-   TiCDC の内部処理能力が不足している場合、レプリケーションタスクのエラー`ErrBufferReachLimit`が発生することがあります。
-   TiCDC の内部処理能力が不足している場合、または TiCDC のダウンストリームのスループット能力が不足している場合、メモリ不足 (OOM) が発生する可能性があります。

v6.2 以降、TiCDC は単一テーブルのトランザクションを複数のトランザクションに分割することをサポートしています。これにより、大規模なトランザクションをレプリケートする際のレイテンシーとメモリ消費を大幅に削減できます。したがって、トランザクションのアトミシティに対する要件がアプリケーションにあまりない場合は、大きなトランザクションの分割を有効にして、レプリケーションのレイテンシーと OOM の可能性を回避することをお勧めします。分割を有効にするには、シンク uri パラメーターの値を[`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb)から`none`に設定します。

それでも上記のエラーが発生する場合は、 BRを使用して大規模なトランザクションの増分データを復元することをお勧めします。詳細な操作は次のとおりです。

1.  大規模なトランザクションのために終了した変更フィードの`checkpoint-ts`記録し、この TSO をBR増分バックアップの`--lastbackupts`として使用して、 [増分データ バックアップ](/br/br-incremental-guide.md#back-up-incremental-data)を実行します。
2.  増分データをバックアップした後、 BRログ出力で`["Full backup Failed summary : total backup ranges: 0, total success: 0, total failed: 0"] [BackupTS=421758868510212097]`のようなログ レコードを見つけることができます。このログに`BackupTS`を記録します。
3.  [増分データを復元する](/br/br-incremental-guide.md#restore-incremental-data) .
4.  新しい変更フィードを作成し、レプリケーション タスクを`BackupTS`から開始します。
5.  古い変更フィードを削除します。

## DDL ステートメントを下流のMySQL 5.7にレプリケートする場合、時間型フィールドのデフォルト値は矛盾しています。私に何ができる？ {#the-default-value-of-the-time-type-field-is-inconsistent-when-replicating-a-ddl-statement-to-the-downstream-mysql-5-7-what-can-i-do}

`create table test (id int primary key, ts timestamp)`ステートメントが上流の TiDB で実行されるとします。 TiCDC がこのステートメントをダウンストリームのMySQL 5.7に複製すると、MySQL はデフォルトの構成を使用します。レプリケーション後のテーブル スキーマは次のとおりです。 `timestamp`フィールドのデフォルト値は`CURRENT_TIMESTAMP`になります。

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

この結果から、レプリケーションの前後でテーブル スキーマに一貫性がないことがわかります。これは、TiDB のデフォルト値`explicit_defaults_for_timestamp` MySQL のデフォルト値と異なるためです。詳細は[MySQL の互換性](/mysql-compatibility.md#default-differences)参照してください。

v5.0.1 または v4.0.13 以降、MySQL へのレプリケーションごとに、TiCDC は自動的に`explicit_defaults_for_timestamp = ON`を設定して、アップストリームとダウンストリームの間で時刻タイプが一致するようにします。 v5.0.1 または v4.0.13 より前のバージョンでは、TiCDC を使用して時間型データを複製するときに、 `explicit_defaults_for_timestamp`値が一致しないために発生する互換性の問題に注意してください。

## TiCDC レプリケーション タスクを作成するときに<code>safe-mode</code>を<code>true</code>に設定すると、アップストリームからの<code>INSERT</code> / <code>UPDATE</code>ステートメントがダウンストリームにレプリケートされた後に<code>REPLACE INTO</code>になるのはなぜですか? {#why-do-code-insert-code-code-update-code-statements-from-the-upstream-become-code-replace-into-code-after-being-replicated-to-the-downstream-if-i-set-code-safe-mode-code-to-code-true-code-when-i-create-a-ticdc-replication-task}

TiCDC は、すべてのデータが少なくとも 1 回レプリケートされることを保証します。下流に重複データがあると、書き込み競合が発生します。この問題を回避するために、TiCDC は`INSERT`ステートメントと`UPDATE`ステートメントを`REPLACE INTO`ステートメントに変換します。この動作は、 `safe-mode`パラメータによって制御されます。

v6.1.3 より前のバージョンでは、 `safe-mode`デフォルトは`true`です。これは、すべての`INSERT`および`UPDATE`ステートメントが`REPLACE INTO`ステートメントに変換されることを意味します。 v6.1.3 以降のバージョンでは、TiCDC はダウンストリームに重複データがあるかどうかを自動的に判断でき、デフォルト値の`safe-mode`は`false`に変更されます。重複データが検出されない場合、TiCDC は`INSERT`と`UPDATE`ステートメントを変換せずに複製します。

## レプリケーション ダウンストリームのシンクが TiDB または MySQL の場合、ダウンストリーム データベースのユーザーにはどのようなアクセス許可が必要ですか? {#when-the-sink-of-the-replication-downstream-is-tidb-or-mysql-what-permissions-do-users-of-the-downstream-database-need}

シンクが TiDB または MySQL の場合、ダウンストリーム データベースのユーザーには次の権限が必要です。

-   `Select`
-   `Index`
-   `Insert`
-   `Update`
-   `Delete`
-   `Create`
-   `Drop`
-   `Alter`
-   `Create View`

`recover table`下流の TiDB に複製する必要がある場合は、 `Super`権限が必要です。

## TiCDC がディスクを使用するのはなぜですか? TiCDC はいつディスクに書き込みますか? TiCDC はメモリバッファーを使用してレプリケーションのパフォーマンスを向上させますか? {#why-does-ticdc-use-disks-when-does-ticdc-write-to-disks-does-ticdc-use-memory-buffer-to-improve-replication-performance}

アップストリームの書き込みトラフィックがピーク時になると、ダウンストリームはタイムリーにすべてのデータを消費できず、データの山積みが発生する可能性があります。 TiCDC はディスクを使用して、積み上げられたデータを処理します。 TiCDC は、通常の操作中にデータをディスクに書き込む必要があります。ただし、ディスクへの書き込みは 100 ミリ秒以内のレイテンシーしか発生しないため、これは通常、レプリケーション スループットとレプリケーションレイテンシーのボトルネックにはなりません。また、TiCDC はメモリを使用してディスクからのデータの読み取りを加速し、レプリケーションのパフォーマンスを向上させます。

## アップストリームからTiDB LightningとBRを使用してデータを復元した後、TiCDC を使用したレプリケーションがストールしたり停止したりするのはなぜですか? {#why-does-replication-using-ticdc-stall-or-even-stop-after-data-restore-using-tidb-lightning-and-br-from-upstream}

現在、TiCDC はまだTiDB LightningおよびBRと完全に互換性がありません。したがって、TiCDC によって複製されたテーブルでTiDB LightningおよびBRを使用することは避けてください。

## 変更フィードが一時停止から再開した後、そのレプリケーションレイテンシーはますます高くなり、数分後にのみ通常に戻ります。なぜ？ {#after-a-changefeed-resumes-from-pause-its-replication-latency-gets-higher-and-higher-and-returns-to-normal-only-after-a-few-minutes-why}

変更フィードが再開されると、TiCDC は TiKV 内のデータの履歴バージョンをスキャンして、一時停止中に生成された増分データ ログに追いつく必要があります。レプリケーション プロセスは、スキャンが完了した後にのみ続行されます。スキャン処理には数分から数十分かかる場合があります。

## 異なるリージョンにある 2 つの TiDB クラスター間でデータをレプリケートするには、TiCDC をデプロイする方法を教えてください。 {#how-should-i-deploy-ticdc-to-replicate-data-between-two-tidb-cluster-located-in-different-regions}

ダウンストリームの TiDB クラスターに TiCDC をデプロイすることをお勧めします。アップストリームとダウンストリーム間のネットワークレイテンシーが大きい場合 (たとえば、100 ミリ秒を超える場合)、TiCDC がダウンストリームに対して SQL ステートメントを実行するときに生成されるレイテンシーは、MySQL 伝送プロトコルの問題により劇的に増加する可能性があります。これにより、システムのスループットが低下します。ただし、TiCDC をダウンストリームにデプロイすると、この問題を大幅に緩和できます。

## DML および DDL ステートメントを実行する順序は? {#what-is-the-order-of-executing-dml-and-ddl-statements}

実行順序は、DML -&gt; DDL -&gt; DML です。データ レプリケーション中に DML イベントがダウンストリームで実行されるときにテーブル スキーマが正しいことを確認するには、DDL ステートメントと DML ステートメントの実行順序を調整する必要があります。現在、TiCDC は単純なアプローチを採用しています。DDL ts の前にすべての DML ステートメントを最初にダウンストリームに複製し、次に DDL ステートメントを複製します。

## アップストリームとダウンストリームのデータが一致しているかどうかを確認するにはどうすればよいですか? {#how-should-i-check-whether-the-upstream-and-downstream-data-is-consistent}

ダウンストリームが TiDB クラスターまたは MySQL インスタンスである場合は、 [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)使用してデータを比較することをお勧めします。

## 1 つのテーブルのレプリケーションは、1 つの TiCDC ノードでのみ実行できます。複数の TiCDC ノードを使用して、複数のテーブルのデータを複製することは可能ですか? {#replication-of-a-single-table-can-only-be-run-on-a-single-ticdc-node-will-it-be-possible-to-use-multiple-ticdc-nodes-to-replicate-data-of-multiple-tables}

この機能は現在サポートされていません。将来のリリースでサポートされる可能性があります。それまでに、TiCDC は TiKVリージョンにデータ変更ログをレプリケートする可能性があります。これは、スケーラブルな処理能力を意味します。

## アップストリームに長期間実行されているコミットされていないトランザクションがある場合、TiCDC レプリケーションは停止しますか? {#does-ticdc-replication-get-stuck-if-the-upstream-has-long-running-uncommitted-transactions}

TiDB にはトランザクション タイムアウト メカニズムがあります。トランザクションが[`max-txn-ttl`](/tidb-configuration-file.md#max-txn-ttl)よりも長い期間実行されると、TiDB はそれを強制的にロールバックします。 TiCDC は、トランザクションがコミットされるのを待ってからレプリケーションを続行するため、レプリケーションの遅延が発生します。
