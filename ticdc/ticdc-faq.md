---
title: TiCDC FAQs
summary: TiCDC を使用する際に遭遇する可能性のある FAQ について説明します。
---

# TiCDC よくある質問 {#ticdc-faqs}

このドキュメントでは、TiCDC の使用時に発生する可能性のある一般的な質問について説明します。

> **注記：**
>
> このドキュメントでは、 `cdc cli`コマンドで指定されているサーバーアドレスは`--server=http://127.0.0.1:8300`です。コマンドを使用するときは、アドレスを実際の PD アドレスに置き換えてください。

## TiCDC でタスクを作成するときに<code>start-ts</code>選択するにはどうすればよいですか? {#how-do-i-choose-code-start-ts-code-when-creating-a-task-in-ticdc}

レプリケーション タスクの`start-ts` 、上流の TiDB クラスターの Timestamp Oracle (TSO) に対応します。TiCDC は、レプリケーション タスクでこの TSO からデータを要求します。したがって、レプリケーション タスクの`start-ts`次の要件を満たす必要があります。

-   `start-ts`の値は、現在の TiDB クラスターの`tikv_gc_safe_point`値よりも大きいです。それ以外の場合、タスクを作成するときにエラーが発生します。
-   タスクを開始する前に、ダウンストリームに`start-ts`より前のすべてのデータが揃っていることを確認してください。メッセージ キューにデータを複製するなどのシナリオでは、アップストリームとダウンストリーム間のデータの一貫性が必要ない場合は、アプリケーションのニーズに応じてこの要件を緩和できます。

`start-ts`指定しない場合、または`start-ts` `0`として指定した場合、レプリケーション タスクが開始されると、TiCDC は現在の TSO を取得し、この TSO からタスクを開始します。

## TiCDC でタスクを作成するときに、一部のテーブルを複製できないのはなぜですか? {#why-can-t-some-tables-be-replicated-when-i-create-a-task-in-ticdc}

`cdc cli changefeed create`実行してレプリケーション タスクを作成すると、TiCDC はアップストリーム テーブルが[レプリケーション要件](/ticdc/ticdc-overview.md#best-practices)を満たしているかどうかを確認します。一部のテーブルが要件を満たしていない場合、不適格なテーブルのリストとともに`some tables are not eligible to replicate`が返されます。タスクの作成を続行するには`Y`または`y`選択できます。その場合、レプリケーション中はこれらのテーブルのすべての更新が自動的に無視されます。 `Y`または`y`以外の入力を選択した場合、レプリケーション タスクは作成されません。

## TiCDC レプリケーション タスクの状態を確認するにはどうすればよいですか? {#how-do-i-view-the-state-of-ticdc-replication-tasks}

TiCDC レプリケーション タスクのステータスを表示するには、 `cdc cli`使用します。例:

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

-   `checkpoint` : TiCDC はこのタイムスタンプより前のすべてのデータをダウンストリームに複製しました。
-   `state` : このレプリケーション タスクの状態。各状態とその意味の詳細については、 [チェンジフィードの状態](/ticdc/ticdc-changefeed-overview.md#changefeed-state-transfer)参照してください。

> **注記：**
>
> この機能は TiCDC 4.0.3 で導入されました。

## アップストリームが更新を停止した後、TiCDC がすべての更新を複製したかどうかを確認するにはどうすればよいですか? {#how-to-verify-if-ticdc-has-replicated-all-updates-after-upstream-stops-updating}

アップストリーム TiDB クラスターの更新が停止したら、アップストリーム TiDB クラスターの最新の[TSO](/glossary.md#tso)のタイムスタンプと TiCDC のレプリケーションの進行状況を比較して、レプリケーションが完了したかどうかを確認できます。TiCDC のレプリケーション進行状況のタイムスタンプがアップストリーム TiDB クラスターの TSO 以上である場合、すべての更新がレプリケートされています。レプリケーションの完了を確認するには、次の手順を実行します。

1.  アップストリーム TiDB クラスターから最新の TSO タイムスタンプを取得します。

    > **注記：**
    >
    > 現在の時刻を返す`NOW()`ような関数を使用する代わりに、 [`TIDB_CURRENT_TSO()`](/functions-and-operators/tidb-functions.md#tidb_current_tso)関数を使用して現在の TSO を取得します。

    次の例では、 [`TIDB_PARSE_TSO()`](/functions-and-operators/tidb-functions.md#tidb_parse_tso)使用して TSO を読み取り可能な時間形式に変換し、さらに比較します。

    ```sql
    BEGIN;
    SELECT TIDB_PARSE_TSO(TIDB_CURRENT_TSO());
    ROLLBACK;
    ```

    出力は次のようになります。

    ```sql
    +------------------------------------+
    | TIDB_PARSE_TSO(TIDB_CURRENT_TSO()) |
    +------------------------------------+
    | 2024-11-12 20:35:34.848000         |
    +------------------------------------+
    ```

2.  TiCDC でレプリケーションの進行状況を取得します。

    次のいずれかの方法を使用して、TiCDC でレプリケーションの進行状況を確認できます。

    -   **方法 1** : 変更フィードのチェックポイントを照会します (推奨)。

        すべてのレプリケーション タスクのチェックポイントを表示するには、 [TiCDC コマンドラインツール](/ticdc/ticdc-manage-changefeed.md) `cdc cli`を使用します。

        ```shell
        cdc cli changefeed list --server=http://127.0.0.1:8300
        ```

        出力は次のようになります。

        ```json
        [
          {
            "id": "syncpoint",
            "namespace": "default",
            "summary": {
              "state": "normal",
              "tso": 453880043653562372,
              "checkpoint": "2024-11-12 20:36:01.447",
              "error": null
            }
          }
        ]
        ```

        出力の`"checkpoint": "2024-11-12 20:36:01.447"`は、TiCDC がこの時間より前にすべてのアップストリーム TiDB 変更をレプリケートしたことを示します。このタイムスタンプが、手順 1 で取得したアップストリーム TiDB クラスターの TSO 以上である場合、すべての更新がダウンストリームにレプリケートされています。

    -   **方法 2** : ダウンストリーム TiDB から Syncpoint をクエリします。

        ダウンストリームが TiDB クラスターであり、 [TiCDC 同期ポイント機能](/ticdc/ticdc-upstream-downstream-check.md)が有効になっている場合は、ダウンストリーム TiDB の Syncpoint を照会することでレプリケーションの進行状況を取得できます。

        > **注記：**
        >
        > 同期ポイントの更新間隔は、 [`sync-point-interval`](/ticdc/ticdc-upstream-downstream-check.md#enable-syncpoint)構成項目によって制御されます。最新のレプリケーションの進行状況を取得するには、方法 1 を使用します。

        下流TiDBで次のSQL文を実行して、上流TSO（ `primary_ts` ）と下流TSO（ `secondary_ts` ）を取得します。

        ```sql
        SELECT * FROM tidb_cdc.syncpoint_v1;
        ```

        出力は次のようになります。

        ```sql
        +------------------+------------+--------------------+--------------------+---------------------+
        | ticdc_cluster_id | changefeed | primary_ts         | secondary_ts       | created_at          |
        +------------------+------------+--------------------+--------------------+---------------------+
        | default          | syncpoint  | 453879870259200000 | 453879870545461257 | 2024-11-12 20:25:01 |
        | default          | syncpoint  | 453879948902400000 | 453879949214351361 | 2024-11-12 20:30:01 |
        | default          | syncpoint  | 453880027545600000 | 453880027751907329 | 2024-11-12 20:35:00 |
        +------------------+------------+--------------------+--------------------+---------------------+
        ```

        出力では、各行は、上流の TiDB スナップショット`primary_ts`が下流の TiDB スナップショット`secondary_ts`と一致していることを示しています。

        レプリケーションの進行状況を表示するには、最新の`primary_ts`読み取り可能な時間形式に変換します。

        ```sql
        SELECT TIDB_PARSE_TSO(453880027545600000);
        ```

        出力は次のようになります。

        ```sql
        +------------------------------------+
        | TIDB_PARSE_TSO(453880027545600000) |
        +------------------------------------+
        | 2024-11-12 20:35:00                |
        +------------------------------------+
        ```

        最新の`primary_ts`に対応する時間が、手順 1 で取得した上流 TiDB クラスターの TSO 以上である場合、TiCDC はすべての更新を下流に複製しています。

## TiCDC の<code>gc-ttl</code>とは何ですか? {#what-is-code-gc-ttl-code-in-ticdc}

v4.0.0-rc.1 以降、PD はサービス レベルの GC セーフポイントの設定において外部サービスをサポートします。どのサービスでも GC セーフポイントを登録および更新できます。PD は、この GC セーフポイント以降のキー値データが GC によってクリーンアップされないようにします。

この機能により、レプリケーション タスクが利用できないか中断された場合、TiCDC によって消費されるデータは GC によってクリーンアップされることなく TiKV に保持されます。

TiCDCサーバーを起動するときに、 `gc-ttl`設定して GC セーフポイントの Time To Live (TTL) 期間を指定できます。 [TiUPを使用して変更する](/ticdc/deploy-ticdc.md#modify-ticdc-cluster-configurations-using-tiup) `gc-ttl`も指定できます。デフォルト値は 24 時間です。TiCDC では、この値は次の意味を持ちます。

-   TiCDC サービスが停止された後、GC セーフポイントが PD に保持される最大時間。
-   TiKV の GC が TiCDC の GC セーフポイントによってブロックされている場合、 `gc-ttl` TiCDC レプリケーション タスクの最大レプリケーション遅延を示します。レプリケーション タスクの遅延が`gc-ttl`で設定された値を超えると、レプリケーション タスクは`failed`状態になり、 `ErrGCTTLExceeded`エラーが報告されます。回復できず、GC セーフポイントの進行をブロックしなくなります。

上記の 2 番目の動作は、TiCDC v4.0.13 以降のバージョンで導入されています。その目的は、TiCDC のレプリケーション タスクが長時間中断され、上流 TiKV クラスターの GC セーフポイントが長時間継続せず、古いデータ バージョンが多すぎるままになり、上流クラスターのパフォーマンスに影響が出るのを防ぐことです。

> **注記：**
>
> 一部のシナリオでは、たとえばDumpling/ BRによる完全レプリケーション後に TiCDC を使用して増分レプリケーションを行う場合、デフォルトの 24 時間である`gc-ttl`では不十分な場合があります。TiCDCサーバーを起動するときに、適切な値`gc-ttl`を指定する必要があります。

## TiCDCガベージコレクション(GC) セーフポイントの完全な動作は何ですか? {#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint}

TiCDC サービスの開始後にレプリケーション タスクが開始されると、TiCDC 所有者は、すべてのレプリケーション タスクの中で最小値`checkpoint-ts`で PD サービス GC セーフポイントを更新します。サービス GC セーフポイントにより、TiCDC はその時点およびその時点以降に生成されたデータを削除しません。レプリケーション タスクが中断された場合、または手動で停止された場合、このタスクの`checkpoint-ts`変更されません。一方、PD の対応するサービス GC セーフポイントも更新されません。

レプリケーションタスクが`gc-ttl`で指定した時間より長く中断された場合、レプリケーションタスクは`failed`状態になり、再開できなくなります。PD 対応サービス GC セーフポイントは継続されます。

TiCDC がサービス GC セーフポイントに設定するデフォルトの Time-To-Live (TTL) は 24 時間です。つまり、TiCDC サービスが中断されてから 24 時間以内に回復できる場合、GC メカニズムは TiCDC がレプリケーションを続行するために必要なデータを削除しません。

## レプリケーション タスクが失敗した後に回復するにはどうすればよいですか? {#how-to-recover-a-replication-task-after-it-fails}

1.  `cdc cli changefeed query`使用してレプリケーション タスクのエラー情報を照会し、できるだけ早くエラーを修正します。
2.  値を`gc-ttl`に増やすと、エラーを修正するための時間が長くなり、エラーが修正された後にレプリケーション遅延が`gc-ttl`超えたためにレプリケーション タスクが`failed`ステータスにならないようになります。
3.  システムへの影響を評価した後、TiDB の値を[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)増やして GC をブロックし、データを保持して、エラーが修正された後に GC によるデータのクリーニングによってレプリケーション タスクが`failed`ステータスにならないようにします。

## TiCDC タイム ゾーンと上流/下流データベースのタイム ゾーンの関係を理解するにはどうすればよいでしょうか? {#how-to-understand-the-relationship-between-the-ticdc-time-zone-and-the-time-zones-of-the-upstream-downstream-databases}

|              |                                   上流タイムゾーン                                   |                                   TiCDC タイムゾーン                                  |                               下流タイムゾーン                               |
| :----------: | :--------------------------------------------------------------------------: | :-----------------------------------------------------------------------------: | :------------------------------------------------------------------: |
| コンフィグレーション方法 |                   [タイムゾーンのサポート](/configure-time-zone.md)参照                   |                     TiCDCサーバーを起動するときに`--tz`パラメータを使用して設定されます                     |                  `sink-uri`の`time-zone`パラメータを使用して構成                  |
|      説明      | アップストリーム TiDB のタイム ゾーン。タイムスタンプ タイプの DML 操作と、タイムスタンプ タイプの列に関連する DDL 操作に影響します。 | TiCDC は、上流の TiDB のタイム ゾーンが TiCDC のタイム ゾーン構成と同じであると想定し、タイムスタンプ列に対して関連する操作を実行します。 | ダウンストリーム MySQL は、ダウンストリームのタイムゾーン設定に従って、DML および DDL 操作のタイムスタンプを処理します。 |

> **注記：**
>
> TiCDCサーバーのタイム ゾーンを設定するときは注意してください。このタイム ゾーンは時間タイプの変換に使用されるためです。アップストリーム タイム ゾーン、TiCDC タイム ゾーン、ダウンストリーム タイム ゾーンの一貫性を維持してください。TiCDCサーバーは、次の優先順位でタイム ゾーンを選択します。
>
> -   TiCDC はまず`--tz`使用して指定されたタイム ゾーンを使用します。
> -   `--tz`が利用できない場合、TiCDC は`TZ`環境変数を使用してタイム ゾーン セットを読み取ろうとします。
> -   `TZ`環境変数が使用できない場合、TiCDC はマシンのデフォルトのタイム ゾーンを使用します。

## <code>--config</code>で構成ファイルを指定せずにレプリケーション タスクを作成した場合、TiCDC のデフォルトの動作はどうなりますか? {#what-is-the-default-behavior-of-ticdc-if-i-create-a-replication-task-without-specifying-the-configuration-file-in-code-config-code}

`-config`パラメータを指定せずに`cdc cli changefeed create`コマンドを使用すると、TiCDC は次のデフォルト動作でレプリケーション タスクを作成します。

-   システムテーブルを除くすべてのテーブルを複製します
-   [有効なインデックス](/ticdc/ticdc-overview.md#best-practices)含むテーブルのみを複製します

## TiCDC は Canal プロトコルでのデータ変更の出力をサポートしていますか? {#does-ticdc-support-outputting-data-changes-in-the-canal-protocol}

はい。Canal プロトコルの場合、TiCDC は JSON 出力形式のみをサポートしており、protobuf 形式はまだ正式にサポートされていないことに注意してください。Canal 出力を有効にするには、 `--sink-uri`構成で`protocol` `canal-json`に指定します。例:

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="kafka://127.0.0.1:9092/cdc-test?kafka-version=2.4.0&protocol=canal-json" --config changefeed.toml
```

> **注記：**
>
> -   この機能は TiCDC 4.0.2 で導入されました。
> -   TiCDC は現在、Kafka などの MQ シンクにのみ、Canal-JSON 形式でデータ変更を出力することをサポートしています。

詳細については[TiCDC チェンジフィード構成](/ticdc/ticdc-changefeed-config.md)を参照してください。

## TiCDC から Kafka へのレイテンシーがどんどん高くなるのはなぜですか? {#why-does-the-latency-from-ticdc-to-kafka-become-higher-and-higher}

-   チェック[TiCDC レプリケーション タスクの状態を表示するにはどうすればいいですか?](#how-do-i-view-the-state-of-ticdc-replication-tasks) 。
-   Kafka の次のパラメータを調整します。

    -   `server.properties`の`message.max.bytes`値を`1073741824` (1 GB) に増やします。
    -   `server.properties`の`replica.fetch.max.bytes`値を`1073741824` (1 GB) に増やします。
    -   `consumer.properties`の`fetch.message.max.bytes`値を増やして、 `message.max.bytes`値より大きくします。

## TiCDC がデータを Kafka に複製する場合、TiDB 内の単一メッセージの最大サイズを制御できますか? {#when-ticdc-replicates-data-to-kafka-can-i-control-the-maximum-size-of-a-single-message-in-tidb}

`protocol` `avro`または`canal-json`に設定すると、行の変更ごとにメッセージが送信されます。1 つの Kafka メッセージには 1 つの行の変更のみが含まれ、通常は Kafka の制限を超えることはありません。したがって、1 つのメッセージのサイズを制限する必要はありません。1 つの Kafka メッセージのサイズが Kafka の制限を超える場合は、 [TiCDC から Kafka へのレイテンシーがどんどん高くなるのはなぜですか?](/ticdc/ticdc-faq.md#why-does-the-latency-from-ticdc-to-kafka-become-higher-and-higher)を参照してください。

`protocol` `open-protocol`に設定すると、メッセージはバッチで送信されます。そのため、1 つの Kafka メッセージは大きすぎる可能性があります。この状況を回避するには、 `max-message-bytes`パラメータを設定して、Kafka ブローカーに毎回送信されるデータの最大サイズを制御できます (オプション、デフォルトは`10MB` )。また、 `max-batch-size`パラメータを設定して (オプション、デフォルトは`16` )、各 Kafka メッセージの変更レコードの最大数を指定することもできます。

## トランザクションで行を複数回変更した場合、TiCDC は複数の行変更イベントを出力しますか? {#if-i-modify-a-row-multiple-times-in-a-transaction-will-ticdc-output-multiple-row-change-events}

いいえ。1 つのトランザクションで同じ行を複数回変更した場合、TiDB は最新の変更のみを TiKV に送信します。したがって、TiCDC は最新の変更の結果のみを取得できます。

## TiCDC がデータを Kafka に複製する場合、メッセージには複数の種類のデータ変更が含まれますか? {#when-ticdc-replicates-data-to-kafka-does-a-message-contain-multiple-types-of-data-changes}

はい。1 つのメッセージに複数の`update`または`delete`が含まれる場合があり、 `update`と`delete`共存する場合もあります。

## TiCDC がデータを Kafka に複製する場合、TiCDC Open Protocol の出力でタイムスタンプ、テーブル名、スキーマ名をどのように表示すればよいですか? {#when-ticdc-replicates-data-to-kafka-how-do-i-view-the-timestamp-table-name-and-schema-name-in-the-output-of-ticdc-open-protocol}

情報は Kafka メッセージのキーに含まれます。例:

```json
{
    "ts":<TS>,
    "scm":<Schema Name>,
    "tbl":<Table Name>,
    "t":1
}
```

詳細については[TiCDC オープン プロトコル イベント形式](/ticdc/ticdc-open-protocol.md#event-format)を参照してください。

## TiCDC がデータを Kafka に複製する場合、メッセージ内のデータ変更のタイムスタンプをどのように確認すればよいですか? {#when-ticdc-replicates-data-to-kafka-how-do-i-know-the-timestamp-of-the-data-changes-in-a-message}

Kafka メッセージのキーの`ts` 18 ビット右に移動すると、UNIX タイムスタンプを取得できます。

## TiCDC オープン プロトコルは<code>null</code>どのように表現しますか? {#how-does-ticdc-open-protocol-represent-code-null-code}

TiCDC オープン プロトコルでは、タイプ コード`6`は`null`表します。

| タイプ | コード | 出力例                | 注記 |
| :-- | :-- | :----------------- | :- |
| ヌル  | 6   | `{"t":6,"v":null}` |    |

詳細については[TiCDC オープンプロトコル列タイプコード](/ticdc/ticdc-open-protocol.md#column-type-code)を参照してください。

## TiCDC オープン プロトコルの行変更イベントが<code>INSERT</code>イベントなのか<code>UPDATE</code>イベントなのかをどのように判断すればよいですか? {#how-can-i-tell-if-a-row-changed-event-of-ticdc-open-protocol-is-an-code-insert-code-event-or-an-code-update-code-event}

-   `UPDATE`イベントには`"p"`フィールドと`"u"`フィールドの両方が含まれます
-   `INSERT`イベントには`"u"`フィールドのみが含まれます
-   `DELETE`イベントには`"d"`フィールドのみが含まれます

詳細については[オープンプロトコル行変更イベント形式](/ticdc/ticdc-open-protocol.md#row-changed-event)を参照してください。

## TiCDC はどのくらいの PDstorageを使用しますか? {#how-much-pd-storage-does-ticdc-use}

TiCDC は、PD の etcd を使用してメタデータを保存し、定期的に更新します。etcd の MVCC と PD のデフォルトの圧縮の間の時間間隔は 1 時間であるため、TiCDC が使用する PDstorageの量は、この 1 時間以内に生成されるメタデータ バージョンの量に比例します。ただし、v4.0.5、v4.0.6、v4.0.7 では、TiCDC に頻繁な書き込みの問題があるため、1 時間に 1000 個のテーブルが作成またはスケジュールされると、etcdstorageがすべて消費され、 `etcdserver: mvcc: database space exceeded`エラーが返されます。このエラーが発生したら、etcdstorageをクリーンアップする必要があります。詳細については、 [etcd メンテナンス スペース クォータ](https://etcd.io/docs/v3.4.0/op-guide/maintenance/#space-quota)参照してください。クラスターを v4.0.9 以降のバージョンにアップグレードすることをお勧めします。

## TiCDC は大規模なトランザクションの複製をサポートしていますか? リスクはありますか? {#does-ticdc-support-replicating-large-transactions-is-there-any-risk}

TiCDC は、大規模なトランザクション (サイズが 5 GB を超える) を部分的にサポートします。さまざまなシナリオに応じて、次のリスクが存在する可能性があります。

-   プライマリ - セカンダリ レプリケーションのレイテンシーが大幅に増加する可能性があります。
-   TiCDC の内部処理能力が不足すると、レプリケーション タスク エラー`ErrBufferReachLimit`が発生する可能性があります。
-   TiCDC の内部処理能力が不足している場合、または TiCDC のダウンストリームのスループット能力が不足している場合、メモリ不足 (OOM) が発生する可能性があります。

v6.2 以降、TiCDC は単一テーブル トランザクションを複数のトランザクションに分割することをサポートしています。これにより、大規模なトランザクションをレプリケートする際のレイテンシーとメモリ消費を大幅に削減できます。したがって、アプリケーションでトランザクションの原子性に対する要件が高くない場合は、レプリケーションのレイテンシーと OOM を回避するために、大規模なトランザクションの分割を有効にすることをお勧めします。分割を有効にするには、sink uri パラメータの値を[`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb)から`none`に設定します。

上記のエラーが引き続き発生する場合は、 BR を使用して大規模トランザクションの増分データを復元することをお勧めします。詳細な操作は次のとおりです。

1.  大規模なトランザクションにより終了した変更フィードの`checkpoint-ts`記録し、この TSO をBR増分バックアップの`--lastbackupts`として使用し、 [増分データバックアップ](/br/br-incremental-guide.md#back-up-incremental-data)実行します。
2.  増分データをバックアップした後、 BRログ出力に`["Full backup Failed summary : total backup ranges: 0, total success: 0, total failed: 0"] [BackupTS=421758868510212097]`に似たログ レコードが見つかります。このログに`BackupTS`を記録します。
3.  [増分データを復元する](/br/br-incremental-guide.md#restore-incremental-data) 。
4.  新しい変更フィードを作成し、レプリケーション タスクを`BackupTS`から開始します。
5.  古い変更フィードを削除します。

## TiCDC は、損失のある DDL 操作によって発生したデータの変更をダウンストリームに複製しますか? {#does-ticdc-replicate-data-changes-caused-by-lossy-ddl-operations-to-the-downstream}

非可逆 DDL とは、TiDB で実行されたときにデータの変更を引き起こす可能性がある DDL を指します。一般的な非可逆 DDL 操作には次のようなものがあります。

-   列の型を変更する（例：INT -&gt; VARCHAR）
-   列の長さを変更する。例：VARCHAR(20) -&gt; VARCHAR(10)
-   列の精度を変更する。例: DECIMAL(10, 3) -&gt; DECIMAL(10, 2)
-   列の UNSIGNED または SIGNED 属性の変更 (例: INT UNSIGNED -&gt; INT SIGNED)

TiDB v7.1.0 より前では、TiCDC は、古いデータと新しいデータが同一の DML イベントをダウンストリームに複製します。ダウンストリームが MySQL の場合、ダウンストリームが DDL ステートメントを受信して​​実行するまで、これらの DML イベントによってデータが変更されることはありません。ただし、ダウンストリームが Kafka またはクラウドstorageサービスの場合、TiCDC は冗長データの行をダウンストリームに書き込みます。

TiDB v7.1.0 以降、TiCDC はこれらの冗長な DML イベントを排除し、ダウンストリームに複製しなくなりました。

## DDL ステートメントをダウンストリームMySQL 5.7に複製するときに、時間型フィールドのデフォルト値が一致しません。どうすればよいでしょうか? {#the-default-value-of-the-time-type-field-is-inconsistent-when-replicating-a-ddl-statement-to-the-downstream-mysql-5-7-what-can-i-do}

上流の TiDB で`create table test (id int primary key, ts timestamp)`文が実行されたとします。TiCDC がこの文`timestamp`下流のMySQL 5.7に複製すると、MySQL はデフォルト設定を使用します。複製後のテーブル スキーマは次のようになります。3 フィールドのデフォルト値は`CURRENT_TIMESTAMP`になります。

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

結果から、レプリケーション前後のテーブルスキーマが不整合になっていることがわかります。これは、TiDB のデフォルト値`explicit_defaults_for_timestamp`が MySQL のデフォルト値と異なるためです。詳細は[MySQL 互換性](/mysql-compatibility.md#default-differences)参照してください。

v5.0.1 または v4.0.13 以降では、MySQL へのレプリケーションごとに、TiCDC は自動的に`explicit_defaults_for_timestamp = ON`設定して、アップストリームとダウンストリームの間で時間タイプが一貫していることを確認します。v5.0.1 または v4.0.13 より前のバージョンでは、TiCDC を使用して時間タイプ データをレプリケートするときに、不一致な`explicit_defaults_for_timestamp`値によって発生する互換性の問題に注意してください。

## TiCDC レプリケーション タスクを作成するときに<code>safe-mode</code> <code>true</code>に設定すると、アップストリームからの<code>INSERT</code> / <code>UPDATE</code>ステートメントがダウンストリームにレプリケートされた後に<code>REPLACE INTO</code>になるのはなぜですか? {#why-do-code-insert-code-code-update-code-statements-from-the-upstream-become-code-replace-into-code-after-being-replicated-to-the-downstream-if-i-set-code-safe-mode-code-to-code-true-code-when-i-create-a-ticdc-replication-task}

TiCDC は、すべてのデータが少なくとも 1 回は複製されることを保証します。ダウンストリームに重複データがあると、書き込み競合が発生します。この問題を回避するために、TiCDC は`INSERT`および`UPDATE`ステートメントを`REPLACE INTO`ステートメントに変換します。この動作は`safe-mode`パラメータによって制御されます。

v6.1.3 より前のバージョンでは、 `safe-mode`デフォルトで`true`に設定され、 `INSERT`と`UPDATE`のステートメントはすべて`REPLACE INTO`ステートメントに変換されます。v6.1.3 以降のバージョンでは、TiCDC はダウンストリームに重複データがあるかどうかを自動的に判断し、デフォルト値の`safe-mode`は`false`に変更されます。重複データが検出されない場合、TiCDC は`INSERT`と`UPDATE`ステートメントを変換せずに複製します。

## TiCDC がディスクを使用するのはなぜですか? TiCDC はいつディスクに書き込みますか? TiCDC はレプリケーション パフォーマンスを向上させるためにメモリバッファーを使用しますか? {#why-does-ticdc-use-disks-when-does-ticdc-write-to-disks-does-ticdc-use-memory-buffer-to-improve-replication-performance}

アップストリームの書き込みトラフィックがピーク時になると、ダウンストリームがすべてのデータをタイムリーに消費できず、データが蓄積される可能性があります。TiCDC は、蓄積されたデータを処理するためにディスクを使用します。TiCDC は通常の動作中にディスクにデータを書き込む必要があります。ただし、ディスクへの書き込みでは 100 ミリ秒以内のレイテンシーしか発生しないため、これは通常、レプリケーション スループットとレプリケーションレイテンシーのボトルネックにはなりません。TiCDC は、メモリを使用してディスクからのデータの読み取りを高速化し、レプリケーション パフォーマンスを向上させます。

## TiDB Lightning物理インポート モードとアップストリームからのBR を使用してデータを復元した後、TiCDC を使用したレプリケーションが停止したり、停止したりするのはなぜですか? {#why-does-replication-using-ticdc-stall-or-even-stop-after-data-restore-using-tidb-lightning-physical-import-mode-and-br-from-upstream}

現在、TiCDC は[TiDB Lightning物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)およびBRとまだ完全に互換性がありません。したがって、TiCDC によってレプリケートされるテーブルでは、 TiDB Lightning物理インポート モードとBR を使用しないでください。そうしないと、TiCDC レプリケーションが停止したり、レプリケーションレイテンシーが著しく増加したり、データが失われたりといった不明なエラーが発生する可能性があります。

TiCDC によってレプリケートされた一部のテーブルのデータを復元するためにTiDB Lightning物理インポート モードまたはBR を使用する必要がある場合は、次の手順を実行します。

1.  これらのテーブルに関連する TiCDC レプリケーション タスクを削除します。

2.  TiCDC の上流クラスターと下流クラスターでデータを個別に復元するには、 TiDB Lightning物理インポート モードまたはBR を使用します。

3.  復元が完了し、上流クラスターと下流クラスター間のデータの整合性が検証されたら、上流バックアップのタイムスタンプ (TSO) をタスクの`start-ts`として、増分レプリケーション用の新しい TiCDC レプリケーション タスクを作成します。たとえば、上流クラスターのBRバックアップのスナップショット タイムスタンプが`431434047157698561`であると仮定すると、次のコマンドを使用して新しい TiCDC レプリケーション タスクを作成できます。

    ```shell
    cdc cli changefeed create -c "upstream-to-downstream-some-tables" --start-ts=431434047157698561 --sink-uri="mysql://root@127.0.0.1:4000? time-zone="
    ```

## 変更フィードが一時停止から再開すると、レプリケーションのレイテンシーがどんどん長くなり、数分後にようやく正常に戻ります。なぜでしょうか? {#after-a-changefeed-resumes-from-pause-its-replication-latency-gets-higher-and-higher-and-returns-to-normal-only-after-a-few-minutes-why}

変更フィードが再開されると、TiCDC は、一時停止中に生成された増分データ ログに追いつくために、TiKV 内のデータの履歴バージョンをスキャンする必要があります。レプリケーション プロセスは、スキャンが完了した後にのみ続行されます。スキャン プロセスには数分から数十分かかる場合があります。

## 異なるリージョンにある 2 つの TiDB クラスター間でデータを複製するには、TiCDC をどのようにデプロイすればよいですか? {#how-should-i-deploy-ticdc-to-replicate-data-between-two-tidb-cluster-located-in-different-regions}

v6.5.2 より前のバージョンの TiCDC の場合、ダウンストリーム TiDB クラスターに TiCDC をデプロイすることをお勧めします。アップストリームとダウンストリーム間のネットワークレイテンシーが高い場合 (たとえば、100 ミリ秒を超える場合)、MySQL 転送プロトコルの問題により、TiCDC がダウンストリームに対して SQL ステートメントを実行するときに発生するレイテンシーが大幅に増加する可能性があります。これにより、システム スループットが低下します。ただし、ダウンストリームに TiCDC をデプロイすると、この問題が大幅に軽減されます。最適化後、TiCDC v6.5.2 以降では、アップストリーム TiDB クラスターに TiCDC をデプロイすることをお勧めします。

## DML および DDL ステートメントの実行順序は何ですか? {#what-is-the-order-of-executing-dml-and-ddl-statements}

現在、TiCDC は次の順序を採用しています。

1.  TiCDC は、DDL `commitTS`まで、DDL ステートメントの影響を受けるテーブルのレプリケーションの進行をブロックします。これにより、DDL `commitTS`より前に実行された DML ステートメントがダウンストリームに正常にレプリケートされることが保証されます。
2.  TiCDC は DDL ステートメントのレプリケーションを続行します。複数の DDL ステートメントがある場合、TiCDC はそれらを順番にレプリケートします。
3.  DDL ステートメントがダウンストリームで実行された後、TiCDC は DDL `commitTS`の後に実行された DML ステートメントのレプリケーションを続行します。

## アップストリーム データとダウンストリーム データが一貫しているかどうかをどのように確認すればよいですか? {#how-should-i-check-whether-the-upstream-and-downstream-data-is-consistent}

ダウンストリームが TiDB クラスターまたは MySQL インスタンスの場合は、 [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md)使用してデータを比較することをお勧めします。

## 単一テーブルのレプリケーションは、単一の TiCDC ノードでのみ実行できます。複数の TiCDC ノードを使用して複数のテーブルのデータをレプリケートすることは可能ですか? {#replication-of-a-single-table-can-only-be-run-on-a-single-ticdc-node-will-it-be-possible-to-use-multiple-ticdc-nodes-to-replicate-data-of-multiple-tables}

v7.1.0 以降、TiCDC は、TiKV リージョンの粒度でデータ変更ログをレプリケートする MQ シンクをサポートしています。これにより、スケーラブルな処理能力が実現され、TiCDC は多数のリージョンで単一のテーブルをレプリケートできます。この機能を有効にするには、 [TiCDC 構成ファイル](/ticdc/ticdc-changefeed-config.md)で次のパラメータを設定します。

```toml
[scheduler]
enable-table-across-nodes = true
```

## アップストリームに長時間実行されているコミットされていないトランザクションがある場合、TiCDC レプリケーションは停止しますか? {#does-ticdc-replication-get-stuck-if-the-upstream-has-long-running-uncommitted-transactions}

TiDB にはトランザクション タイムアウト メカニズムがあります。トランザクションが[`max-txn-ttl`](/tidb-configuration-file.md#max-txn-ttl)より長い期間実行されると、TiDB はそれを強制的にロールバックします。TiCDC は、レプリケーションを続行する前にトランザクションがコミットされるのを待つため、レプリケーションの遅延が発生します。

## TiDB Operatorによってデプロイされた TiCDC クラスターを<code>cdc cli</code>コマンドを使用して操作できないのはなぜですか? {#why-can-t-i-use-the-code-cdc-cli-code-command-to-operate-a-ticdc-cluster-deployed-by-tidb-operator}

これは、 TiDB Operatorによってデプロイされた TiCDC クラスターのデフォルトのポート番号が`8301`であるのに対し、 TiCDCサーバーに接続するための`cdc cli`コマンドのデフォルトのポート番号が`8300`であるためです。 TiDB Operatorによってデプロイされた TiCDC クラスターを`cdc cli`コマンドを使用して操作する場合は、次のように`--server`パラメータを明示的に指定する必要があります。

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

## TiCDC は DML 操作で生成された列を複製しますか? {#does-ticdc-replicate-generated-columns-of-dml-operations}

生成された列には、仮想生成された列と保存された生成された列が含まれます。TiCDC は仮想生成された列を無視し、保存された生成された列のみをダウンストリームに複製します。ただし、ダウンストリームが MySQL または別の MySQL 互換データベース (Kafka またはその他のstorageサービスではない) である場合、保存された生成された列も無視されます。

> **注記：**
>
> 保存された生成列を Kafka またはstorageサービスに複製し、それを MySQL に書き戻すと、 `Error 3105 (HY000): The value specified for generated column 'xx' in table 'xxx' is not allowed`発生する可能性があります。このエラーを回避するには、レプリケーションに[オープンプロトコル](/ticdc/ticdc-open-protocol.md#ticdc-open-protocol)使用します。このプロトコルの出力には[列のビットフラグ](/ticdc/ticdc-open-protocol.md#bit-flags-of-columns)含まれており、列が生成列であるかどうかを区別できます。
