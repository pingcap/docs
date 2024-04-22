---
title: TiCDC FAQs
summary: TiCDCはデフォルトでポート番号8301を使用するため、TiDB OperatorによってデプロイされたTiCDCクラスターを操作するには、--serverパラメーターを明示的に指定する必要があります。ポート番号8300ではなく、ポート番号8301を使用してください。
---

# TiCDC よくある質問 {#ticdc-faqs}

このドキュメントでは、TiCDC の使用時に遭遇する可能性のある一般的な質問を紹介します。

> **注記：**
>
> このドキュメントでは、 `cdc cli`コマンドで指定するサーバーアドレスは`--server=http://127.0.0.1:8300`です。コマンドを使用するときは、アドレスを実際の PD アドレスに置き換えてください。

## TiCDC でタスクを作成するときに<code>start-ts</code>選択するにはどうすればよいですか? {#how-do-i-choose-code-start-ts-code-when-creating-a-task-in-ticdc}

レプリケーション タスクの`start-ts`は、上流の TiDB クラスターのタイムスタンプ Oracle (TSO) に対応します。 TiCDC は、レプリケーション タスクでこの TSO にデータを要求します。したがって、レプリケーション タスクの`start-ts`は次の要件を満たす必要があります。

-   値`start-ts`は、現在の TiDB クラスターの値`tikv_gc_safe_point`よりも大きくなります。そうしないと、タスクの作成時にエラーが発生します。
-   タスクを開始する前に、ダウンストリームに`start-ts`より前のすべてのデータがあることを確認してください。データをメッセージ キューにレプリケートするなどのシナリオで、アップストリームとダウンストリームの間でデータの整合性が必要ない場合は、アプリケーションのニーズに応じてこの要件を緩和できます。

`start-ts`を指定しない場合、または`start-ts`を`0`として指定した場合、レプリケーション タスクの開始時に、TiCDC は現在の TSO を取得し、この TSO からタスクを開始します。

## TiCDC でタスクを作成するときに一部のテーブルを複製できないのはなぜですか? {#why-can-t-some-tables-be-replicated-when-i-create-a-task-in-ticdc}

`cdc cli changefeed create`を実行してレプリケーション タスクを作成すると、TiCDC はアップストリーム テーブルが[レプリケーション要件](/ticdc/ticdc-overview.md#best-practices)を満たすかどうかを確認します。一部のテーブルが要件を満たしていない場合は、不適格なテーブルのリストとともに`some tables are not eligible to replicate`が返されます。 `Y`または`y`を選択してタスクの作成を続行すると、これらのテーブルのすべての更新はレプリケーション中に自動的に無視されます。 `Y`または`y`以外の入力を選択した場合、レプリケーション タスクは作成されません。

## TiCDC レプリケーション タスクの状態を表示するにはどうすればよいですか? {#how-do-i-view-the-state-of-ticdc-replication-tasks}

TiCDC レプリケーション タスクのステータスを表示するには、 `cdc cli`を使用します。例えば：

```shell
cdc cli changefeed list --server=http://127.0.0.1:8300
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

-   `checkpoint` : TiCDC は、このタイムスタンプより前のすべてのデータをダウンストリームに複製しました。
-   `state` : このレプリケーション タスクの状態。各状態とその意味の詳細については、 [フィード状態の変更](/ticdc/ticdc-changefeed-overview.md#changefeed-state-transfer)を参照してください。

> **注記：**
>
> この機能は TiCDC 4.0.3 で導入されました。

## TiCDC の<code>gc-ttl</code>は何ですか? {#what-is-code-gc-ttl-code-in-ticdc}

v4.0.0-rc.1 以降、PD はサービス レベルの GC セーフポイントの設定において外部サービスをサポートしています。どのサービスでも GC セーフポイントを登録および更新できます。 PD は、この GC セーフポイントより後のキーと値のデータが GC によってクリーンアップされないことを保証します。

この機能により、レプリケーション タスクが利用できないか中断された場合、TiCDC によって消費されるデータが GC によってクリーンアップされずに TiKV に保持されることが保証されます。

TiCDCサーバーを起動するときに、 `gc-ttl`を構成することで GC セーフポイントの存続時間 (TTL) 期間を指定できます。 [TiUPを使用して変更します](/ticdc/deploy-ticdc.md#modify-ticdc-cluster-configurations-using-tiup) `gc-ttl`もできます。デフォルト値は 24 時間です。 TiCDC では、この値は次のことを意味します。

-   TiCDC サービスが停止した後、GC セーフポイントが PD に保持される最大時間。
-   TiKV の GC が TiCDC の GC セーフポイントによってブロックされている場合、 `gc-ttl` TiCDC レプリケーション タスクの最大レプリケ​​ーション遅延を示します。レプリケーション タスクの遅延が`gc-ttl`で設定された値を超えると、レプリケーション タスクは`failed`状態になり、 `ErrGCTTLExceeded`エラーを報告します。これは回復できず、GC セーフポイントの進行を妨げなくなります。

上記の 2 番目の動作は、TiCDC v4.0.13 以降のバージョンで導入されています。目的は、TiCDC のレプリケーション タスクが長時間中断され、上流の TiKV クラスターの GC セーフポイントが長期間継続できなくなり、古いデータ バージョンが多すぎる状態で保持され、上流クラスターのパフォーマンスに影響を与えることを防ぐことです。

> **注記：**
>
> たとえば、 Dumpling/ BRによる完全レプリケーション後の増分レプリケーションに TiCDC を使用する場合など、一部のシナリオでは、デフォルトの 24 時間の`gc-ttl`では不十分な場合があります。 TiCDCサーバーを開始するときに、 `gc-ttl`に適切な値を指定する必要があります。

## TiCDCガベージコレクション(GC) セーフポイントの完全な動作は何ですか? {#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint}

TiCDC サービスの開始後にレプリケーション タスクが開始されると、TiCDC 所有者は、すべてのレプリケーション タスクの中で最小値`checkpoint-ts`で PD サービス GC セーフポイントを更新します。サービス GC セーフポイントにより、TiCDC はその時点およびその時点以降に生成されたデータを削除しません。レプリケーション タスクが中断された場合、または手動で停止された場合、このタスクの`checkpoint-ts`変更されません。一方、PD の対応するサービス GC セーフポイントも更新されません。

レプリケーション タスクが`gc-ttl`で指定された時間より長く一時停止されている場合、レプリケーション タスクは`failed`ステータスになり、再開できません。 PD対応サービスGCセーフポイントは継続します。

TiCDC がサービス GC セーフポイントに設定するデフォルトの Time-To-Live (TTL) は 24 時間です。つまり、TiCDC サービスが GC セーフポイントから 24 時間以内に回復できる場合、レプリケーションを継続するために TiCDC が必要とするデータは GC メカニズムによって削除されません。中断されます。

## レプリケーション タスクが失敗した後に回復するにはどうすればよいですか? {#how-to-recover-a-replication-task-after-it-fails}

1.  レプリケーション タスクのエラー情報をクエリし、できるだけ早くエラーを修正するには、 `cdc cli changefeed query`を使用します。
2.  値`gc-ttl`を増やすと、エラーを修正するまでの時間が長くなり、エラーが修正された後にレプリケーション遅延が`gc-ttl`を超えるためにレプリケーション タスクが`failed`ステータスにならないようになります。
3.  システムへの影響を評価した後、TiDB の値[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)増やして GC をブロックしてデータを保持し、エラー修正後に GC クリーニング データによってレプリケーション タスクが`failed`ステータスにならないようにします。

## TiCDC タイム ゾーンとアップストリーム/ダウンストリーム データベースのタイム ゾーンの関係を理解するにはどうすればよいですか? {#how-to-understand-the-relationship-between-the-ticdc-time-zone-and-the-time-zones-of-the-upstream-downstream-databases}

|              |                                アップストリームのタイムゾーン                                |                                     TiCDC タイムゾーン                                    |                               下流タイムゾーン                               |
| :----------: | :---------------------------------------------------------------------------: | :---------------------------------------------------------------------------------: | :------------------------------------------------------------------: |
| コンフィグレーション方法 |                   [タイムゾーンのサポート](/configure-time-zone.md)を参照                   |                        TiCDCサーバーの起動時に`--tz`パラメーターを使用して構成されます                        |                `sink-uri`の`time-zone`パラメータを使用して構成されます                |
|      説明      | アップストリーム TiDB のタイム ゾーン。タイムスタンプ タイプの DML 操作およびタイムスタンプ タイプの列に関連する DDL 操作に影響します。 | TiCDC は、アップストリーム TiDB のタイム ゾーンが TiCDC タイム ゾーン構成と同じであると想定し、タイムスタンプ列に対して関連する操作を実行します。 | ダウンストリーム MySQL は、ダウンストリームのタイムゾーン設定に従って、DML および DDL 操作のタイムスタンプを処理します。 |

> **注記：**
>
> このタイム ゾーンは時間タイプの変換に使用されるため、TiCDCサーバーのタイム ゾーンを設定するときは注意してください。アップストリーム タイム ゾーン、TiCDC タイム ゾーン、およびダウンストリーム タイム ゾーンを一貫した状態に保ちます。 TiCDCサーバーは、次の優先順位でタイム ゾーンを選択します。
>
> -   TiCDC は、最初に`--tz`を使用して指定されたタイム ゾーンを使用します。
> -   `--tz`が使用できない場合、TiCDC は`TZ`環境変数を使用してタイム ゾーン セットを読み取ろうとします。
> -   `TZ`環境変数が使用できない場合、TiCDC はマシンのデフォルトのタイムゾーンを使用します。

## <code>--config</code>で構成ファイルを指定せずにレプリケーション タスクを作成した場合、TiCDC のデフォルトの動作はどうなりますか? {#what-is-the-default-behavior-of-ticdc-if-i-create-a-replication-task-without-specifying-the-configuration-file-in-code-config-code}

`-config`パラメータを指定せずに`cdc cli changefeed create`コマンドを使用すると、TiCDC は次のデフォルト動作でレプリケーション タスクを作成します。

-   システムテーブルを除くすべてのテーブルをレプリケートします
-   [有効なインデックス](/ticdc/ticdc-overview.md#best-practices)を含むテーブルのみをレプリケートします

## TiCDC は、Canal プロトコルでのデータ変更の出力をサポートしていますか? {#does-ticdc-support-outputting-data-changes-in-the-canal-protocol}

はい。 Canal プロトコルの場合、TiCDC は JSON 出力形式のみをサポートし、protobuf 形式はまだ正式にサポートされていないことに注意してください。 Canal 出力を有効にするには、 `--sink-uri`構成で`protocol`を`canal-json`に指定します。例えば：

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="kafka://127.0.0.1:9092/cdc-test?kafka-version=2.4.0&protocol=canal-json" --config changefeed.toml
```

> **注記：**
>
> -   この機能は TiCDC 4.0.2 で導入されました。
> -   TiCDC は現在、Kafka などの MQ シンクへの Canal-JSON 形式でのデータ変更の出力のみをサポートしています。

詳細については、 [TiCDC 変更フィード構成](/ticdc/ticdc-changefeed-config.md)を参照してください。

## TiCDC から Kafka までのレイテンシーがますます高くなるのはなぜですか? {#why-does-the-latency-from-ticdc-to-kafka-become-higher-and-higher}

-   チェック[TiCDC レプリケーション タスクの状態を表示するにはどうすればよいですか](#how-do-i-view-the-state-of-ticdc-replication-tasks) 。
-   Kafka の次のパラメータを調整します。

    -   `server.properties` `message.max.bytes`値を`1073741824` (1 GB) に増やします。
    -   `server.properties` `replica.fetch.max.bytes`値を`1073741824` (1 GB) に増やします。
    -   `consumer.properties`の`fetch.message.max.bytes`値を増やして、 `message.max.bytes`値よりも大きくします。

## TiCDC がデータを Kafka にレプリケートする場合、TiDB 内の単一メッセージの最大サイズを制御できますか? {#when-ticdc-replicates-data-to-kafka-can-i-control-the-maximum-size-of-a-single-message-in-tidb}

`protocol`を`avro`または`canal-json`に設定すると、行の変更ごとにメッセージが送信されます。 1 つの Kafka メッセージには 1 行の変更のみが含まれ、通常は Kafka の制限を超えることはありません。したがって、1 つのメッセージのサイズを制限する必要はありません。単一の Kafka メッセージのサイズが Kakfa の制限を超える場合は、 [TiCDC から Kafka までのレイテンシーがますます高くなるのはなぜですか?](/ticdc/ticdc-faq.md#why-does-the-latency-from-ticdc-to-kafka-become-higher-and-higher)を参照してください。

`protocol`を`open-protocol`に設定すると、メッセージはバッチで送信されます。したがって、1 つの Kafka メッセージが過度に大きくなる可能性があります。この状況を回避するには、 `max-message-bytes`パラメーターを構成して、毎回 Kafka ブローカーに送信されるデータの最大サイズを制御できます (オプション、デフォルトでは`10MB` )。また、 `max-batch-size`パラメーター (オプション、デフォルトでは`16` ) を構成して、各 Kafka メッセージ内の変更レコードの最大数を指定することもできます。

## トランザクション内で行を複数回変更した場合、TiCDC は複数の行変更イベントを出力しますか? {#if-i-modify-a-row-multiple-times-in-a-transaction-will-ticdc-output-multiple-row-change-events}

いいえ。1 つのトランザクションで同じ行を複数回変更すると、TiDB は最新の変更のみを TiKV に送信します。したがって、TiCDC は最新の変更の結果しか取得できません。

## TiCDC がデータを Kafka にレプリケートするとき、メッセージには複数のタイプのデータ変更が含まれますか? {#when-ticdc-replicates-data-to-kafka-does-a-message-contain-multiple-types-of-data-changes}

はい。 1 つのメッセージに複数の`update`または`delete`が含まれる場合があり、 `update`と`delete`共存する場合もあります。

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

詳細については、 [TiCDC オープン プロトコル イベント形式](/ticdc/ticdc-open-protocol.md#event-format)を参照してください。

## TiCDC がデータを Kafka にレプリケートするとき、メッセージ内のデータ変更のタイムスタンプを確認するにはどうすればよいですか? {#when-ticdc-replicates-data-to-kafka-how-do-i-know-the-timestamp-of-the-data-changes-in-a-message}

Kafka メッセージのキーの`ts`右に 18 ビット移動すると、UNIX タイムスタンプを取得できます。

## TiCDC オープン プロトコルは<code>null</code>をどのように表現しますか? {#how-does-ticdc-open-protocol-represent-code-null-code}

TiCDC オープン プロトコルでは、タイプ コード`6`は`null`を表します。

| タイプ | コード | 出力例                | 注記 |
| :-- | :-- | :----------------- | :- |
| ヌル  | 6   | `{"t":6,"v":null}` |    |

詳細については、 [TiCDC オープン プロトコルの列タイプ コード](/ticdc/ticdc-open-protocol.md#column-type-code)を参照してください。

## TiCDC オープン プロトコルの行変更イベントが<code>INSERT</code>イベントであるか<code>UPDATE</code>イベントであるかをどのように判断できますか? {#how-can-i-tell-if-a-row-changed-event-of-ticdc-open-protocol-is-an-code-insert-code-event-or-an-code-update-code-event}

-   `UPDATE`イベントには`"p"`と`"u"`フィールドの両方が含まれます
-   `INSERT`イベントには`"u"`フィールドのみが含まれます
-   `DELETE`イベントには`"d"`フィールドのみが含まれます

詳細については、 [オープンプロトコル行変更イベント形式](/ticdc/ticdc-open-protocol.md#row-changed-event)を参照してください。

## TiCDC はどのくらいの PDstorageを使用しますか? {#how-much-pd-storage-does-ticdc-use}

TiCDC は PD で etcd を使用してメタデータを保存し、定期的に更新します。 etcd の MVCC と PD のデフォルト圧縮の間の時間間隔は 1 時間であるため、TiCDC が使用する PDstorageの量は、この 1 時間以内に生成されるメタデータ バージョンの量に比例します。ただし、v4.0.5、v4.0.6、および v4.0.7 では、TiCDC には頻繁な書き込みの問題があるため、1 時間に 1000 のテーブルが作成またはスケジュールされている場合、etcdstorageがすべて占有され、 `etcdserver: mvcc: database space exceeded`エラーが返されます。 。このエラーが発生した後は、etcdstorageをクリーンアップする必要があります。詳細は[etcd メンテナンス スペースの割り当て](https://etcd.io/docs/v3.4.0/op-guide/maintenance/#space-quota)参照してください。クラスターを v4.0.9 以降のバージョンにアップグレードすることをお勧めします。

## TiCDC は大規模なトランザクションのレプリケーションをサポートしていますか?リスクはありますか? {#does-ticdc-support-replicating-large-transactions-is-there-any-risk}

TiCDC は、大規模トランザクション (サイズが 5 GB を超える) を部分的にサポートします。さまざまなシナリオに応じて、次のリスクが存在する可能性があります。

-   プライマリとセカンダリのレプリケーションのレイテンシーが大幅に増加する可能性があります。
-   TiCDC の内部処理能力が不足している場合、レプリケーションタスクエラー`ErrBufferReachLimit`が発生する可能性があります。
-   TiCDC の内部処理能力が不足している場合、または TiCDC のダウンストリームのスループット能力が不足している場合、メモリ不足 (OOM) が発生する可能性があります。

v6.2 以降、TiCDC は単一テーブルのトランザクションを複数のトランザクションに分割することをサポートしています。これにより、大規模なトランザクションをレプリケートする際のレイテンシーとメモリ消費量を大幅に削減できます。したがって、アプリケーションにトランザクションのアトミック性に対する高度な要件がない場合は、発生する可能性のあるレプリケーションのレイテンシーと OOM を回避するために、大規模なトランザクションの分割を有効にすることをお勧めします。分割を有効にするには、シンク URI パラメーターの値を[`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb)から`none`に設定します。

それでも上記のエラーが発生する場合は、 BRを使用して大規模なトランザクションの増分データを復元することをお勧めします。詳細な操作は次のとおりです。

1.  大規模なトランザクションにより終了した変更フィードの`checkpoint-ts`記録し、この TSO をBR増分バックアップの`--lastbackupts`として使用し、 [増分データバックアップ](/br/br-incremental-guide.md#back-up-incremental-data)を実行します。
2.  増分データをバックアップした後、 BRログ出力で`["Full backup Failed summary : total backup ranges: 0, total success: 0, total failed: 0"] [BackupTS=421758868510212097]`のようなログ レコードを見つけることができます。このログに`BackupTS`を記録します。
3.  [増分データを復元する](/br/br-incremental-guide.md#restore-incremental-data) 。
4.  新しい変更フィードを作成し、レプリケーション タスクを`BackupTS`から開始します。
5.  古い変更フィードを削除します。

## TiCDC は、損失のある DDL 操作によって発生したデータ変更をダウンストリームにレプリケートしますか? {#does-ticdc-replicate-data-changes-caused-by-lossy-ddl-operations-to-the-downstream}

非可逆 DDL は、TiDB で実行するとデータ変更を引き起こす可能性のある DDL を指します。一般的な非可逆 DDL 操作には次のようなものがあります。

-   列の型の変更 (INT -&gt; VARCHAR など)
-   列の長さの変更 (例: VARCHAR(20) -&gt; VARCHAR(10))
-   列の精度の変更 (例: DECIMAL(10, 3) -&gt; DECIMAL(10, 2))
-   列の UNSIGNED または SIGNED 属性の変更 (たとえば、INT UNSIGNED -&gt; INT SIGNED)

TiDB v7.1.0 より前では、TiCDC は同一の新旧データを含む DML イベントをダウンストリームにレプリケートします。ダウンストリームが MySQL の場合、ダウンストリームが DDL ステートメントを受信して​​実行するまで、これらの DML イベントによってデータは変更されません。ただし、ダウンストリームが Kafka またはクラウドstorageサービスである場合、TiCDC は冗長データの行をダウンストリームに書き込みます。

TiDB v7.1.0 以降、TiCDC ではこれらの冗長な DML イベントが削除され、ダウンストリームにレプリケートされなくなりました。

## DDL ステートメントをダウンストリームMySQL 5.7にレプリケートする場合、時間タイプ フィールドのデフォルト値は一貫性がありません。私に何ができる？ {#the-default-value-of-the-time-type-field-is-inconsistent-when-replicating-a-ddl-statement-to-the-downstream-mysql-5-7-what-can-i-do}

`create table test (id int primary key, ts timestamp)`ステートメントが上流の TiDB で実行されるとします。 TiCDC がこのステートメントをダウンストリームのMySQL 5.7に複製するとき、MySQL はデフォルトの構成を使用します。レプリケーション後のテーブルスキーマは以下のようになります。 `timestamp`フィールドのデフォルト値は`CURRENT_TIMESTAMP`になります。

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

結果から、レプリケーションの前後でテーブルのスキーマが矛盾していることがわかります。これは、TiDB のデフォルト値`explicit_defaults_for_timestamp` MySQL のデフォルト値と異なるためです。詳細は[MySQL の互換性](/mysql-compatibility.md#default-differences)参照してください。

v5.0.1 または v4.0.13 以降、MySQL へのレプリケーションごとに、TiCDC は自動的に`explicit_defaults_for_timestamp = ON`を設定して、アップストリームとダウンストリームの間で時間タイプが一貫していることを確認します。 v5.0.1 または v4.0.13 より前のバージョンの場合は、TiCDC を使用して時間型データをレプリケートするときに、一貫性のない`explicit_defaults_for_timestamp`値によって引き起こされる互換性の問題に注意してください。

## TiCDC レプリケーション タスクを作成するときに<code>safe-mode</code>を<code>true</code>に設定すると、アップストリームからの<code>INSERT</code> / <code>UPDATE</code>ステートメントがダウンストリームにレプリケートされた後に<code>REPLACE INTO</code>になるのはなぜですか? {#why-do-code-insert-code-code-update-code-statements-from-the-upstream-become-code-replace-into-code-after-being-replicated-to-the-downstream-if-i-set-code-safe-mode-code-to-code-true-code-when-i-create-a-ticdc-replication-task}

TiCDC は、すべてのデータが少なくとも 1 回複製されることを保証します。下流に重複データがあると書き込み競合が発生します。この問題を回避するために、TiCDC は`INSERT`と`UPDATE`ステートメントを`REPLACE INTO`のステートメントに変換します。この動作は`safe-mode`パラメータによって制御されます。

v6.1.3 より前のバージョンでは、 `safe-mode`デフォルトは`true`で、これはすべての`INSERT`および`UPDATE`ステートメントが`REPLACE INTO`ステートメントに変換されることを意味します。 v6.1.3 以降のバージョンでは、TiCDC はダウンストリームに重複データがあるかどうかを自動的に判断できるため、デフォルト値`safe-mode`が`false`に変更されます。重複データが検出されない場合、TiCDC は`INSERT`および`UPDATE`ステートメントを変換せずに複製します。

## レプリケーションのダウンストリームのシンクが TiDB または MySQL の場合、ダウンストリーム データベースのユーザーにはどのような権限が必要ですか? {#when-the-sink-of-the-replication-downstream-is-tidb-or-mysql-what-permissions-do-users-of-the-downstream-database-need}

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

`recover table`ダウンストリーム TiDB にレプリケートする必要がある場合は、 `Super`権限が必要です。

## TiCDC はなぜディスクを使用するのですか? TiCDC はいつディスクに書き込みますか? TiCDC はレプリケーションのパフォーマンスを向上させるためにメモリバッファを使用しますか? {#why-does-ticdc-use-disks-when-does-ticdc-write-to-disks-does-ticdc-use-memory-buffer-to-improve-replication-performance}

アップストリームの書き込みトラフィックがピーク時間にある場合、ダウンストリームはすべてのデータをタイムリーに消費できず、データの蓄積が発生する可能性があります。 TiCDC は、蓄積されたデータをディスクを使用して処理します。 TiCDC は、通常の動作中にデータをディスクに書き込む必要があります。ただし、ディスクへの書き込みのレイテンシーが100 ミリ秒以内であることを考慮すると、これは通常、レプリケーションのスループットとレプリケーションのレイテンシーのボトルネックにはなりません。 TiCDC はまた、メモリを使用してディスクからのデータの読み取りを高速化し、レプリケーションのパフォーマンスを向上させます。

## アップストリームからTiDB LightningおよびBRを使用してデータを復元した後、TiCDC を使用したレプリケーションが停止したり停止したりするのはなぜですか? {#why-does-replication-using-ticdc-stall-or-even-stop-after-data-restore-using-tidb-lightning-and-br-from-upstream}

現在、TiCDC はまだTiDB LightningおよびBRと完全な互換性はありません。したがって、TiCDC によってレプリケートされるテーブルではTiDB LightningおよびBRを使用しないでください。そうしないと、TiCDC レプリケーションの停止、レプリケーションレイテンシーの大幅なスパイク、またはデータ損失などの不明なエラーが発生する可能性があります。

TiDB LightningまたはBRを使用して、TiCDC によってレプリケートされた一部のテーブルのデータを復元する必要がある場合は、次の手順を実行します。

1.  これらのテーブルに関連する TiCDC レプリケーション タスクを削除します。

2.  TiDB LightningまたはBRを使用して、TiCDC の上流クラスターと下流クラスターでデータを個別に復元します。

3.  復元が完了し、上流クラスターと下流クラスター間のデータの整合性が確認されたら、上流バックアップのタイムスタンプ (TSO) をタスクの`start-ts`として、増分レプリケーション用の新しい TiCDC レプリケーション タスクを作成します。たとえば、アップストリーム クラスターのBRバックアップのスナップショット タイムスタンプが`431434047157698561`であると仮定すると、次のコマンドを使用して新しい TiCDC レプリケーション タスクを作成できます。

    ```shell
    cdc cli changefeed create -c "upstream-to-downstream-some-tables" --start-ts=431434047157698561 --sink-uri="mysql://root@127.0.0.1:4000? time-zone="
    ```

## チェンジフィードが一時停止から再開すると、そのレプリケーションのレイテンシーはますます長くなり、数分後にのみ通常の状態に戻ります。なぜ？ {#after-a-changefeed-resumes-from-pause-its-replication-latency-gets-higher-and-higher-and-returns-to-normal-only-after-a-few-minutes-why}

チェンジフィードが再開されると、TiCDC は TiKV 内のデータの履歴バージョンをスキャンして、一時停止中に生成された増分データ ログに追いつく必要があります。レプリケーション プロセスは、スキャンが完了した後にのみ続行されます。スキャンプロセスには数分から数十分かかる場合があります。

## 異なるリージョンにある 2 つの TiDB クラスター間でデータをレプリケートするには、TiCDC をデプロイするにはどうすればよいですか? {#how-should-i-deploy-ticdc-to-replicate-data-between-two-tidb-cluster-located-in-different-regions}

v6.5.2 より前の TiCDC バージョンの場合は、ダウンストリーム TiDB クラスターに TiCDC をデプロイすることをお勧めします。アップストリームとダウンストリーム間のネットワークレイテンシーが長い場合 (たとえば、100 ミリ秒を超える場合)、MySQL 伝送プロトコルの問題により、TiCDC がダウンストリームに対して SQL ステートメントを実行するときに生成されるレイテンシーが大幅に増加する可能性があります。これにより、システムのスループットが低下します。ただし、ダウンストリームに TiCDC を導入すると、この問題を大幅に軽減できます。 TiCDC v6.5.2 以降、最適化後は、上流の TiDB クラスターに TiCDC をデプロイすることをお勧めします。

## DML ステートメントと DDL ステートメントを実行する順序は何ですか? {#what-is-the-order-of-executing-dml-and-ddl-statements}

現在、TiCDC は次の順序を採用しています。

1.  TiCDC は、DDL `CommiTs`まで、DDL ステートメントの影響を受けるテーブルのレプリケーションの進行をブロックします。これにより、DDL `CommiTs`より前に実行された DML ステートメントが最初にダウンストリームに正常にレプリケートされることが保証されます。
2.  TiCDC は DDL ステートメントのレプリケーションを続行します。複数の DDL ステートメントがある場合、TiCDC はそれらをシリアル方式で複製します。
3.  DDL ステートメントがダウンストリームで実行された後、TiCDC は DDL `CommiTs`の後に実行された DML ステートメントのレプリケーションを続行します。

## 上流と下流のデータが一貫しているかどうかを確認するにはどうすればよいですか? {#how-should-i-check-whether-the-upstream-and-downstream-data-is-consistent}

ダウンストリームが TiDB クラスターまたは MySQL インスタンスの場合は、 [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)使用してデータを比較することをお勧めします。

## 単一テーブルのレプリケーションは、単一の TiCDC ノード上でのみ実行できます。複数の TiCDC ノードを使用して複数のテーブルのデータを複製することは可能ですか? {#replication-of-a-single-table-can-only-be-run-on-a-single-ticdc-node-will-it-be-possible-to-use-multiple-ticdc-nodes-to-replicate-data-of-multiple-tables}

v7.1.0 以降、TiCDC は、TiKV リージョンの粒度でデータ変更ログをレプリケートする MQ シンクをサポートします。これにより、スケーラブルな処理能力が実現され、TiCDC が多数のリージョンを含む単一のテーブルをレプリケートできるようになります。この機能を有効にするには、 [TiCDC 構成ファイル](/ticdc/ticdc-changefeed-config.md)で次のパラメータを設定します。

```toml
[scheduler]
enable-table-across-nodes = true
```

## アップストリームに長時間実行されているコミットされていないトランザクションがある場合、TiCDC レプリケーションは停止しますか? {#does-ticdc-replication-get-stuck-if-the-upstream-has-long-running-uncommitted-transactions}

TiDB にはトランザクション タイムアウト メカニズムがあります。トランザクションが[`max-txn-ttl`](/tidb-configuration-file.md#max-txn-ttl)より長い期間実行されると、TiDB はトランザクションを強制的にロールバックします。 TiCDC はトランザクションがコミットされるのを待ってからレプリケーションを続行するため、レプリケーションの遅延が発生します。

## TiDB Operatorによってデプロイされた TiCDC クラスターを操作するために<code>cdc cli</code>コマンドを使用できないのはなぜですか? {#why-can-t-i-use-the-code-cdc-cli-code-command-to-operate-a-ticdc-cluster-deployed-by-tidb-operator}

これは、 TiDB Operatorによってデプロイされた TiCDC クラスターのデフォルトのポート番号が`8301`であるのに対し、TiCDCサーバーに接続する`cdc cli`コマンドのデフォルトのポート番号が`8300`であるためです。 `cdc cli`コマンドを使用してTiDB Operatorによってデプロイされた TiCDC クラスターを操作する場合は、次のように`--server`パラメーターを明示的に指定する必要があります。

```shell
./cdc cli changefeed list --server "127.0.0.1:8301"
[
  {
    "id": "4k-table",
    "namespace": "default",
    "summary": {
      "state": "stopped",
      "tso": 441832628003799353,
      "checkpoint": "2023-05-30 22:41:57.910",
      "error": null
    }
  },
  {
    "id": "big-table",
    "namespace": "default",
    "summary": {
      "state": "normal",
      "tso": 441872834546892882,
      "checkpoint": "2023-06-01 17:18:13.700",
      "error": null
    }
  }
]
```
