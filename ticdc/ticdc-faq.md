---
title: TiCDC FAQs
summary: Learn the FAQs you might encounter when you use TiCDC.
---

# TiCDC よくある質問 {#ticdc-faqs}

このドキュメントでは、TiCDC の使用時に発生する可能性のある一般的な質問について説明します。

> **注記：**
>
> このドキュメントでは、 `cdc cli`コマンドで指定されているサーバーアドレスは`--server=http://127.0.0.1:8300`です。コマンドを使用する際は、このアドレスを実際の PD アドレスに置き換えてください。

## TiCDC でタスクを作成するときに<code>start-ts</code>を選択するにはどうすればよいですか? {#how-do-i-choose-code-start-ts-code-when-creating-a-task-in-ticdc}

レプリケーションタスクの`start-ts` 、上流TiDBクラスタ内のタイムスタンプOracle（TSO）に対応します。TiCDCは、レプリケーションタスクでこのTSOにデータを要求します。したがって、レプリケーションタスクの`start-ts` 、以下の要件を満たす必要があります。

-   `start-ts`という値は、現在の TiDB クラスターの`tikv_gc_safe_point`値よりも大きいです。それ以外の場合、タスクの作成時にエラーが発生します。
-   Before starting a task, ensure that the downstream has all data before `start-ts`. For scenarios such as replicating data to message queues, if the data consistency between upstream and downstream is not required, you can relax this requirement according to your application need.

`start-ts`指定しない場合、または`start-ts` `0`として指定した場合、レプリケーション タスクが開始されると、TiCDC は現在の TSO を取得し、この TSO からタスクを開始します。

## TiCDC でタスクを作成するときに一部のテーブルを複製できないのはなぜですか? {#why-can-t-some-tables-be-replicated-when-i-create-a-task-in-ticdc}

When you execute `cdc cli changefeed create` to create a replication task, TiCDC checks whether the upstream tables meet the [レプリケーション要件](/ticdc/ticdc-overview.md#best-practices). If some tables do not meet the requirements, `some tables are not eligible to replicate` is returned with a list of ineligible tables. You can choose `Y` or `y` to continue creating the task, and all updates on these tables are automatically ignored during the replication. If you choose an input other than `Y` or `y`, the replication task is not created.

## TiCDC レプリケーション タスクの状態を確認するにはどうすればよいですか? {#how-do-i-view-the-state-of-ticdc-replication-tasks}

TiCDC レプリケーションタスクのステータスを表示するには、 `cdc cli`使用します。例:

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
-   `state` : このレプリケーションタスクの状態。各状態とその意味の詳細については、 [チェンジフィードの状態](/ticdc/ticdc-changefeed-overview.md#changefeed-state-transfer)参照してください。

> **注記：**
>
> この機能は TiCDC 4.0.3 で導入されました。

## アップストリームが更新を停止した後、TiCDC がすべての更新を複製したかどうかを確認するにはどうすればよいでしょうか? {#how-to-verify-if-ticdc-has-replicated-all-updates-after-upstream-stops-updating}

上流 TiDB クラスタの更新が停止した後、上流 TiDB クラスタの最新の[TSO](/glossary.md#timestamp-oracle-tso)スタンプと TiCDC のレプリケーション進行状況を比較することで、レプリケーションが完了したかどうかを確認できます。TiCDC のレプリケーション進行状況のタイムスタンプが上流 TiDB クラスタの TSO 以上であれば、すべての更新がレプリケートされています。レプリケーションの完了を確認するには、以下の手順を実行してください。

1.  アップストリーム TiDB クラスターから最新の TSO タイムスタンプを取得します。

    > **注記：**
    >
    > 現在の時刻を返す`NOW()`ような関数を使用する代わりに、 [`TIDB_CURRENT_TSO()`](/functions-and-operators/tidb-functions.md#tidb_current_tso)関数を使用して現在の TSO を取得します。

    次の例では、 [`TIDB_PARSE_TSO()`](/functions-and-operators/tidb-functions.md#tidb_parse_tso)使用して TSO を読み取り可能な時刻形式に変換し、さらに比較します。

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

        すべてのレプリケーション タスクのチェックポイントを表示するには、 [TiCDC command-line tool](/ticdc/ticdc-manage-changefeed.md) `cdc cli`使用します。

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

        出力の`"checkpoint": "2024-11-12 20:36:01.447"`は、TiCDCがこの時刻までに上流TiDBのすべての変更をレプリケートしたことを示します。このタイムスタンプが、手順1で取得した上流TiDBクラスタのTSO以上であれば、すべての更新が下流にレプリケートされています。

    -   **方法 2** : ダウンストリーム TiDB から Syncpoint をクエリします。

        ダウンストリームが TiDB クラスターであり、 [TiCDC 同期ポイント機能](/ticdc/ticdc-upstream-downstream-check.md)有効になっている場合は、ダウンストリーム TiDB の Syncpoint を照会することでレプリケーションの進行状況を取得できます。

        > **注記：**
        >
        > The Syncpoint update interval is controlled by the [`sync-point-interval`](/ticdc/ticdc-upstream-downstream-check.md#enable-syncpoint) configuration item. For the most up-to-date replication progress, use method 1.

        下流TiDBで次のSQL文を実行して上流TSO（ `primary_ts` ）と下流TSO（ `secondary_ts` ）を取得します。

        ```sql
        SELECT * FROM tidb_cdc.syncpoint_v1;
        ```

        The output is as follows:

        ```sql
        +------------------+------------+--------------------+--------------------+---------------------+
        | ticdc_cluster_id | changefeed | primary_ts         | secondary_ts       | created_at          |
        +------------------+------------+--------------------+--------------------+---------------------+
        | default          | syncpoint  | 453879870259200000 | 453879870545461257 | 2024-11-12 20:25:01 |
        | default          | syncpoint  | 453879948902400000 | 453879949214351361 | 2024-11-12 20:30:01 |
        | default          | syncpoint  | 453880027545600000 | 453880027751907329 | 2024-11-12 20:35:00 |
        +------------------+------------+--------------------+--------------------+---------------------+
        ```

        In the output, each row shows the upstream TiDB snapshot at `primary_ts` matches the downstream TiDB snapshot at `secondary_ts`.

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

        If the time corresponding to the latest `primary_ts` is greater than or equal to the upstream TiDB cluster's TSO obtained in step 1, then TiCDC has replicated all updates downstream.

## What is <code>gc-ttl</code> in TiCDC? {#what-is-code-gc-ttl-code-in-ticdc}

v4.0.0-rc.1以降、PDはサービスレベルのGCセーフポイントの設定において外部サービスをサポートします。どのサービスでもGCセーフポイントを登録・更新できます。PDは、このGCセーフポイント以降のキーバリューデータがGCによってクリーンアップされないようにします。

レプリケーション タスクが利用できないか中断された場合、この機能により、TiCDC によって消費されるデータが GC によってクリーンアップされることなく TiKV に保持されます。

When starting the TiCDC server, you can specify the Time To Live (TTL) duration of GC safepoint by configuring `gc-ttl`. You can also [TiUPを使用して変更する](/ticdc/deploy-ticdc.md#modify-ticdc-cluster-configurations-using-tiup) `gc-ttl`. The default value is 24 hours. In TiCDC, this value means:

-   TiCDC サービスが停止した後、GC セーフポイントが PD に保持される最大時間。
-   TiKVのGCがTiCDCのGCセーフポイントによってブロックされている場合、 `gc-ttl` TiCDCレプリケーションタスクの最大レプリケーション遅延を示します。レプリケーションタスクの遅延が`gc-ttl`で設定された値を超えると、レプリケーションタスクは`failed`状態になり、 `ErrGCTTLExceeded`エラーを報告します。この状態は回復できず、GCセーフポイントの進行をブロックしなくなります。

上記の2番目の動作は、TiCDC v4.0.13以降のバージョンで導入されました。これは、TiCDCのレプリケーションタスクが長時間停止し、上流TiKVクラスタのGCセーフポイントが長時間継続せず、古いデータバージョンが過度に保持され、上流クラスタのパフォーマンスに影響を及ぼすのを防ぐことを目的としています。

> **注記：**
>
> 一部のシナリオ、例えばDumpling/ BRを使用した完全レプリケーション後にTiCDCを使用して増分レプリケーションを行う場合、デフォルトの24時間（ `gc-ttl`では不十分な場合があります。TiCDCサーバーを起動する際に、適切な値（ `gc-ttl`を指定する必要があります。

## TiCDCガベージコレクション(GC) セーフポイントの完全な動作は何ですか? {#what-is-the-complete-behavior-of-ticdc-garbage-collection-gc-safepoint}

TiCDCサービスの起動後にレプリケーションタスクが開始された場合、TiCDCオーナーはPDのサービスGCセーフポイントを、すべてのレプリケーションタスクの中で最も小さい値である`checkpoint-ts`更新します。サービスGCセーフポイントは、TiCDCがその時点およびそれ以降に生成されたデータを削除しないことを保証します。レプリケーションタスクが中断された場合、または手動で停止された場合、このタスクの`checkpoint-ts`変更されません。一方、PDの対応するサービスGCセーフポイントも更新されません。

レプリケーションタスクが`gc-ttl`で指定された時間を超えて中断された場合、レプリケーションタスクは`failed`状態になり、再開できなくなります。PDに対応するサービスGCセーフポイントは継続されます。

TiCDC がサービス GC セーフポイントに設定するデフォルトの Time-To-Live (TTL) は 24 時間です。つまり、TiCDC サービスが中断されてから 24 時間以内に回復できる場合、GC メカニズムは、レプリケーションを続行するために TiCDC が必要とするデータを削除しません。

## How to recover a replication task after it fails? {#how-to-recover-a-replication-task-after-it-fails}

1.  `cdc cli changefeed query`使用してレプリケーション タスクのエラー情報を照会し、できるだけ早くエラーを修正します。
2.  値を`gc-ttl`に増やすと、エラーを修正するための時間が長くなり、エラーが修正された後にレプリケーションの遅延が`gc-ttl`超えたためにレプリケーション タスクが`failed`ステータスにならないようになります。
3.  システムへの影響を評価した後、TiDB の値を[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)増やして GC をブロックし、データを保持して、エラーが修正された後に GC によるデータのクリーニングによってレプリケーション タスクが`failed`ステータスにならないようにします。

## TiCDC タイムゾーンと上流/下流データベースのタイムゾーンの関係を理解するにはどうすればよいでしょうか? {#how-to-understand-the-relationship-between-the-ticdc-time-zone-and-the-time-zones-of-the-upstream-downstream-databases}

|                      |                                   上流タイムゾーン                                  |                                     TiCDCタイムゾーン                                    |                               下流タイムゾーン                               |
| :------------------: | :-------------------------------------------------------------------------: | :--------------------------------------------------------------------------------: | :------------------------------------------------------------------: |
| Configuration method |                  See [タイムゾーンのサポート](/configure-time-zone.md)                 |                       TiCDCサーバーを起動するときに`--tz`パラメータを使用して設定されます                      |                  `sink-uri`の`time-zone`パラメータを使用して構成                  |
|          説明          | アップストリーム TiDB のタイムゾーン。タイムスタンプ タイプの DML 操作と、タイムスタンプ タイプの列に関連する DDL 操作に影響します。 | TiCDC は、アップストリーム TiDB のタイムゾーンが TiCDC のタイムゾーン構成と同じであると想定し、タイムスタンプ列に対して関連する操作を実行します。 | ダウンストリーム MySQL は、ダウンストリームのタイムゾーン設定に従って、DML および DDL 操作のタイムスタンプを処理します。 |

> **注記：**
>
> TiCDCサーバーのタイムゾーンを設定する際は、時刻型の変換に使用されるため、注意してください。上流のタイムゾーン、TiCDCのタイムゾーン、下流のタイムゾーンは統一してください。TiCDCサーバーは、以下の優先順位でタイムゾーンを選択します。
>
> -   TiCDC はまず`--tz`を使用して指定されたタイムゾーンを使用します。
> -   When `--tz` is not available, TiCDC tries to read the time zone set using the `TZ` environment variable.
> -   When the `TZ` environment variable is not available, TiCDC uses the default time zone of the machine.

## What is the default behavior of TiCDC if I create a replication task without specifying the configuration file in <code>--config</code>? {#what-is-the-default-behavior-of-ticdc-if-i-create-a-replication-task-without-specifying-the-configuration-file-in-code-config-code}

If you use the `cdc cli changefeed create` command without specifying the `-config` parameter, TiCDC creates the replication task in the following default behaviors:

-   システムテーブルを除くすべてのテーブルを複製します
-   [有効なインデックス](/ticdc/ticdc-overview.md#best-practices)含むテーブルのみを複製します

## TiCDC は Canal プロトコルでのデータ変更の出力をサポートしていますか? {#does-ticdc-support-outputting-data-changes-in-the-canal-protocol}

はい。Canalプロトコルの場合、TiCDCはJSON出力形式のみをサポートしており、protobuf形式はまだ公式にはサポートされていません。Canal出力を有効にするには、 `--sink-uri`設定で`protocol`を`canal-json`に指定します。例：

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --sink-uri="kafka://127.0.0.1:9092/cdc-test?kafka-version=2.4.0&protocol=canal-json" --config changefeed.toml
```

> **注記：**
>
> -   この機能は TiCDC 4.0.2 で導入されました。
> -   TiCDC は現在、Kafka などの MQ シンクへのデータ変更の Canal-JSON 形式での出力のみをサポートしています。

For more information, refer to [TiCDC チェンジフィード構成](/ticdc/ticdc-changefeed-config.md).

## TiCDC から Kafka へのレイテンシーがどんどん高くなるのはなぜですか? {#why-does-the-latency-from-ticdc-to-kafka-become-higher-and-higher}

-   チェック[TiCDC レプリケーションタスクの状態を確認するにはどうすればいいですか](#how-do-i-view-the-state-of-ticdc-replication-tasks) 。
-   Kafka の次のパラメータを調整します。

    -   `server.properties`の`message.max.bytes`値を`1073741824` (1 GB) に増やします。
    -   Increase the `replica.fetch.max.bytes` value in `server.properties` to `1073741824` (1 GB).
    -   `consumer.properties`の`fetch.message.max.bytes`値を増やして、 `message.max.bytes`値より大きくします。

## TiCDC がデータを Kafka に複製する場合、TiDB 内の単一メッセージの最大サイズを制御できますか? {#when-ticdc-replicates-data-to-kafka-can-i-control-the-maximum-size-of-a-single-message-in-tidb}

`protocol` `avro`または`canal-json`に設定すると、行の変更ごとにメッセージが送信されます。1 つの Kafka メッセージには 1 つの行の変更のみが含まれ、通常は Kafka の制限を超えることはありません。したがって、1 つのメッセージのサイズを制限する必要はありません。1 つの Kafka メッセージのサイズが Kafka の制限を超える場合は、 [TiCDC から Kafka へのレイテンシーがどんどん高くなるのはなぜですか?](/ticdc/ticdc-faq.md#why-does-the-latency-from-ticdc-to-kafka-become-higher-and-higher)を参照してください。

`protocol` `open-protocol`に設定すると、メッセージはバッチで送信されます。そのため、1 つの Kafka メッセージのサイズが過度に大きくなる可能性があります。この状況を回避するには、 `max-message-bytes`のパラメータを設定して、Kafka ブローカーに送信されるデータの最大サイズを制御できます（オプション、デフォルトは`10MB` ）。また、 `max-batch-size`パラメータを設定して（オプション、デフォルトは`16` ）、各 Kafka メッセージに含まれる変更レコードの最大数を指定することもできます。

## トランザクションで行を複数回変更した場合、TiCDC は複数の行変更イベントを出力しますか? {#if-i-modify-a-row-multiple-times-in-a-transaction-will-ticdc-output-multiple-row-change-events}

いいえ。1つのトランザクションで同じ行を複数回変更した場合、TiDBは最新の変更のみをTiKVに送信します。したがって、TiCDCは最新の変更の結果のみを取得できます。

## TiCDC がデータを Kafka に複製する場合、メッセージには複数の種類のデータ変更が含まれますか? {#when-ticdc-replicates-data-to-kafka-does-a-message-contain-multiple-types-of-data-changes}

はい。1 つのメッセージに複数の`update`または`delete`含まれる場合があり、 `update`と`delete`共存することもあります。

## TiCDC がデータを Kafka に複製する場合、TiCDC オープン プロトコルの出力でタイムスタンプ、テーブル名、スキーマ名をどのように表示すればよいですか? {#when-ticdc-replicates-data-to-kafka-how-do-i-view-the-timestamp-table-name-and-schema-name-in-the-output-of-ticdc-open-protocol}

情報はKafkaメッセージのキーに含まれます。例:

```json
{
    "ts":<TS>,
    "scm":<Schema Name>,
    "tbl":<Table Name>,
    "t":1
}
```

詳細については[TiCDCオープンプロトコルイベントフォーマット](/ticdc/ticdc-open-protocol.md#event-format)を参照してください。

## TiCDC がデータを Kafka に複製する場合、メッセージ内のデータ変更のタイムスタンプをどのように確認すればよいですか? {#when-ticdc-replicates-data-to-kafka-how-do-i-know-the-timestamp-of-the-data-changes-in-a-message}

Kafka メッセージのキーの`ts` 18 ビット右に移動すると、Unix タイムスタンプを取得できます。

## TiCDC オープン プロトコルは<code>null</code>どのように表現しますか? {#how-does-ticdc-open-protocol-represent-code-null-code}

TiCDC オープン プロトコルでは、タイプ コード`6` `null`表します。

| タイプ | Code | 出力例                | Note |
| :-- | :--- | :----------------- | :--- |
| ヌル  | 6    | `{"t":6,"v":null}` |      |

詳細については[TiCDCオープンプロトコル列タイプコード](/ticdc/ticdc-open-protocol.md#column-type-code)を参照してください。

## TiCDC オープン プロトコルの行変更イベントが<code>INSERT</code>イベントなのか<code>UPDATE</code>イベントなのかをどのように判断すればよいですか? {#how-can-i-tell-if-a-row-changed-event-of-ticdc-open-protocol-is-an-code-insert-code-event-or-an-code-update-code-event}

-   `UPDATE`イベントには`"p"`と`"u"`両方のフィールドが含まれます
-   `INSERT`イベントには`"u"`フィールドのみが含まれます
-   `DELETE`イベントには`"d"`フィールドのみが含まれます

For more information, refer to [オープンプロトコル行変更イベント形式](/ticdc/ticdc-open-protocol.md#row-changed-event).

## TiCDC はどのくらいの PDstorageを使用しますか? {#how-much-pd-storage-does-ticdc-use}

TiCDC を使用するときに、 `etcdserver: mvcc: database space exceeded`エラーが発生する可能性があります。これは主に、TiCDC が PD で etcd を使用してメタデータを保存するメカニズムに関連しています。

etcdはデータの保存に多版型同時実行制御（MVCC）を使用します。PDにおけるデフォルトのコンパクション間隔は1時間です。つまり、etcdはコンパクションを行う前に、すべてのデータの複数のバージョンを1時間保持します。

v6.0.0より前のバージョンでは、TiCDCはPD内のetcdを使用して、変更フィード内のすべてのテーブルのメタデータを保存および更新していました。そのため、TiCDCが使用するPDstorage容量は、変更フィードによって複製されるテーブルの数に比例します。TiCDCが多数のテーブルを複製する場合、etcdstorage容量がすぐにいっぱいになり、 `etcdserver: mvcc: database space exceeded`エラーが発生する可能性が高くなります。

このエラーが発生した場合は、 [etcd メンテナンス スペースクォータ](https://etcd.io/docs/v3.4.0/op-guide/maintenance/#space-quota)を参照して etcdstorageスペースをクリーンアップしてください。

v6.0.0以降、TiCDCはメタデータstorageメカニズムを最適化し、前述の理由によるetcdstorage容量の問題を効果的に回避します。TiCDCのバージョンがv6.0.0より前の場合は、v6.0.0以降へのアップグレードをお勧めします。

## TiCDC は大規模なトランザクションのレプリケーションをサポートしていますか? リスクはありますか? {#does-ticdc-support-replicating-large-transactions-is-there-any-risk}

TiCDCは、大規模トランザクション（5GBを超える）を部分的にサポートしています。シナリオによっては、以下のリスクが発生する可能性があります。

-   プライマリ-セカンダリレプリケーションのレイテンシーが大幅に増加する可能性があります。
-   When TiCDC's internal processing capacity is insufficient, the replication task error `ErrBufferReachLimit` might occur.
-   TiCDC の内部処理能力が不足している場合、または TiCDC のダウンストリームのスループット能力が不足している場合、メモリ不足 (OOM) が発生する可能性があります。

TiCDC v6.2以降、単一テーブルトランザクションを複数のトランザクションに分割できるようになりました。これにより、大規模トランザクションのレプリケーションにおけるレイテンシーとメモリ消費量を大幅に削減できます。したがって、アプリケーションでトランザクションのアトミック性に対する要件がそれほど高くない場合は、レプリケーションのレイテンシーとOOM（オブジェクトオーバーヘッド）を回避するために、大規模トランザクションの分割を有効にすることを推奨します。分割を有効にするには、シンクURIパラメータの値を[`transaction-atomicity`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb)から`none`に設定してください。

上記のエラーが引き続き発生する場合は、 BRを使用して大規模トランザクションの増分データを復元することをお勧めします。詳細な手順は次のとおりです。

1.  大規模トランザクションにより終了した changefeed の`checkpoint-ts`記録し、この TSO をBR増分バックアップの`--lastbackupts`として使用して[増分データバックアップ](/br/br-incremental-guide.md#back-up-incremental-data)実行します。
2.  増分データをバックアップした後、 BRログ出力に`["Full backup Failed summary : total backup ranges: 0, total success: 0, total failed: 0"] [BackupTS=421758868510212097]`に似たログレコードが見つかります。このログに`BackupTS`を記録してください。
3.  [増分データを復元する](/br/br-incremental-guide.md#restore-incremental-data) 。
4.  新しい変更フィードを作成し、レプリケーション タスクを`BackupTS`から開始します。
5.  古い変更フィードを削除します。

## TiCDC は、損失のある DDL 操作によって発生したデータの変更をダウンストリームに複製しますか? {#does-ticdc-replicate-data-changes-caused-by-lossy-ddl-operations-to-the-downstream}

非可逆DDLとは、TiDBで実行された際にデータ変更を引き起こす可能性のあるDDLを指します。一般的な非可逆DDL操作には、以下のようなものがあります。

-   列の型を変更する（例：INT -&gt; VARCHAR）
-   列の長さを変更する（例：VARCHAR(20) -&gt; VARCHAR(10)）
-   列の精度を変更する。例：DECIMAL(10, 3) -&gt; DECIMAL(10, 2)
-   列の UNSIGNED または SIGNED 属性の変更 (例: INT UNSIGNED -&gt; INT SIGNED)

TiDB v7.1.0より前のバージョンでは、TiCDCは新旧のデータが同一のDMLイベントを下流に複製します。下流がMySQLの場合、これらのDMLイベントは、下流がDDL文を受信して実行するまでデータ変更を引き起こしません。しかし、下流がKafkaまたはクラウドstorageサービスの場合、TiCDCは冗長データの行を下流に書き込みます。

TiDB v7.1.0 以降、TiCDC はこれらの冗長な DML イベントを削除し、ダウンストリームに複製しなくなりました。

## The default value of the time type field is inconsistent when replicating a DDL statement to the downstream MySQL 5.7. What can I do? {#the-default-value-of-the-time-type-field-is-inconsistent-when-replicating-a-ddl-statement-to-the-downstream-mysql-5-7-what-can-i-do}

上流のTiDBで`create table test (id int primary key, ts timestamp)`の文が実行されたとします。TiCDCがこの文を下流のMySQL 5.7に複製する際、MySQLはデフォルト設定を使用します。複製後のテーブルスキーマは以下のとおりです。3 `timestamp`フィールドのデフォルト値は`CURRENT_TIMESTAMP`なります。

```sql
mysql root@127.0.0.1:test> show create table test;
+-------+----------------------------------------------------------------------------------+
| Table | Create Table                                                                     |
+-------+----------------------------------------------------------------------------------+
| test  | CREATE TABLE `test` (                                                            |
|       |   `id` int NOT NULL,                                                         |
|       |   `ts` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP, |
|       |   PRIMARY KEY (`id`)                                                             |
|       | ) ENGINE=InnoDB DEFAULT CHARSET=latin1                                           |
+-------+----------------------------------------------------------------------------------+
1 row in set
```

結果から、レプリケーション前後のテーブルスキーマが不整合になっていることがわかります。これは、TiDBのデフォルト値`explicit_defaults_for_timestamp`がMySQLのデフォルト値と異なるためです。詳細は[MySQLの互換性](/mysql-compatibility.md#default-differences)ご覧ください。

v5.0.1 または v4.0.13 以降、MySQL へのレプリケーションごとに、TiCDC は上流と下流の間で時刻型の一貫性を保つために、自動的に`explicit_defaults_for_timestamp = ON`設定します。v5.0.1 または v4.0.13 より前のバージョンでは、TiCDC を使用して時刻型データをレプリケーションする際に、不一致な`explicit_defaults_for_timestamp`値によって発生する互換性の問題にご注意ください。

## TiCDC レプリケーション タスクを作成するときに<code>safe-mode</code>を<code>true</code>に設定すると、アップストリームからの<code>INSERT</code> / <code>UPDATE</code>ステートメントがダウンストリームにレプリケートされた後に<code>REPLACE INTO</code>になるのはなぜですか? {#why-do-code-insert-code-code-update-code-statements-from-the-upstream-become-code-replace-into-code-after-being-replicated-to-the-downstream-if-i-set-code-safe-mode-code-to-code-true-code-when-i-create-a-ticdc-replication-task}

TiCDCは、すべてのデータが少なくとも1回は複製されることを保証します。下流に重複データが存在する場合、書き込み競合が発生します。この問題を回避するために、TiCDCは`INSERT`と`UPDATE`ステートメントを`REPLACE INTO`ステートメントに変換します。この動作は`safe-mode`パラメータによって制御されます。

v6.1.3 より前のバージョンでは、デフォルト値`safe-mode`は`true`であり、これは`INSERT`と`UPDATE`ステートメントがすべて`REPLACE INTO`ステートメントに変換されることを意味します。

v6.1.3以降のバージョンでは、デフォルト値の`safe-mode`が`false`に変更され、TiCDCは下流に重複データがあるかどうかを自動的に判断できるようになりました。重複データが検出されない場合、TiCDCは`INSERT`と`UPDATE`ステートメントを変換せずに直接複製します。重複データが検出された場合、TiCDCは`INSERT`と`UPDATE`ステートメントを`REPLACE INTO`ステートメントに変換してから複製します。

## TiCDC はなぜディスクを使用するのですか？ TiCDC はいつディスクに書き込みますか？ TiCDC はレプリケーションのパフォーマンスを向上させるためにメモリバッファを使用しますか？ {#why-does-ticdc-use-disks-when-does-ticdc-write-to-disks-does-ticdc-use-memory-buffer-to-improve-replication-performance}

上流の書き込みトラフィックがピーク時になると、下流側ですべてのデータをタイムリーに消費できず、データが蓄積される可能性があります。TiCDCは、蓄積されたデータをディスクで処理します。TiCDCは通常の動作中にディスクにデータを書き込む必要がありますが、ディスクへの書き込みは100ミリ秒以内のレイテンシーにしかならないため、これがレプリケーションのスループットとレイテンシーネックになることは通常ありません。TiCDCはメモリを使用してディスクからのデータの読み取りを高速化し、レプリケーションのパフォーマンスを向上させます。

## Why does replication using TiCDC stall or even stop after data restore using TiDB Lightning physical import mode and BR from upstream? {#why-does-replication-using-ticdc-stall-or-even-stop-after-data-restore-using-tidb-lightning-physical-import-mode-and-br-from-upstream}

現在、TiCDC は[TiDB Lightning物理インポートモード](/tidb-lightning/tidb-lightning-physical-import-mode.md)およびBRと完全に互換性がありません。そのため、TiCDC によってレプリケートされたテーブルでは、 TiDB Lightning物理インポートモードとBRの使用は避けてください。そうしないと、TiCDC レプリケーションの停止、レプリケーションレイテンシーの大幅な上昇、データ損失などの未知のエラーが発生する可能性があります。

TiCDC によって複製された一部のテーブルのデータを復元するために、 TiDB Lightning物理インポート モードまたはBRを使用する必要がある場合は、次の手順を実行します。

1.  これらのテーブルに関連する TiCDC レプリケーション タスクを削除します。

2.  Use TiDB Lightning physical import mode or BR to restore data separately in the upstream and downstream clusters of TiCDC.

3.  復元が完了し、上流クラスターと下流クラスター間のデータ整合性が検証されたら、上流バックアップのタイムスタンプ（TSO）をタスクの`start-ts`として、増分レプリケーション用の新しい TiCDC レプリケーションタスクを作成します。例えば、上流クラスターのBRバックアップのスナップショットのタイムスタンプが`431434047157698561`であると仮定すると、以下のコマンドを使用して新しい TiCDC レプリケーションタスクを作成できます。

    ```shell
    cdc cli changefeed create -c "upstream-to-downstream-some-tables" --start-ts=431434047157698561 --sink-uri="mysql://root@127.0.0.1:4000? time-zone="
    ```

## 変更フィードが一時停止から再開すると、レプリケーションのレイテンシーがどんどん長くなり、数分後にようやく正常に戻ります。なぜでしょうか？ {#after-a-changefeed-resumes-from-pause-its-replication-latency-gets-higher-and-higher-and-returns-to-normal-only-after-a-few-minutes-why}

変更フィードが再開されると、TiCDC は TiKV 内のデータの履歴バージョンをスキャンし、一時停止中に生成された増分データログに追いつく必要があります。レプリケーションプロセスはスキャンが完了した後にのみ続行されます。スキャンプロセスには数分から数十分かかる場合があります。

## 異なるリージョンにある 2 つの TiDB クラスター間でデータをレプリケートするには、TiCDC をどのようにデプロイすればよいですか? {#how-should-i-deploy-ticdc-to-replicate-data-between-two-tidb-cluster-located-in-different-regions}

For TiCDC versions earlier than v6.5.2, it is recommended that you deploy TiCDC in the downstream TiDB cluster. If the network latency between the upstream and downstream is high, for example, more than 100 ms, the latency produced when TiCDC executes SQL statements to the downstream might increase dramatically due to the MySQL transmission protocol issues. This results in a decrease in system throughput. However, deploying TiCDC in the downstream can greatly ease this problem. After optimization, starting from TiCDC v6.5.2, it is recommended that you deploy TiCDC in the upstream TiDB cluster.

## DML および DDL ステートメントの実行順序は何ですか? {#what-is-the-order-of-executing-dml-and-ddl-statements}

現在、TiCDC は次の順序を採用しています。

1.  TiCDCは、DDL `commitTS`まで、DDL文の影響を受けるテーブルのレプリケーションの進行をブロックします。これにより、DDL `commitTS`より前に実行されたDML文が、まず下流に正常にレプリケーションされることが保証されます。
2.  TiCDCはDDLステートメントのレプリケーションを継続します。複数のDDLステートメントがある場合、TiCDCはそれらを順次レプリケーションします。
3.  DDL ステートメントがダウンストリームで実行された後、TiCDC は DDL `commitTS`後に実行された DML ステートメントのレプリケーションを続行します。

## アップストリーム データとダウンストリーム データが一貫しているかどうかをどのように確認すればよいですか? {#how-should-i-check-whether-the-upstream-and-downstream-data-is-consistent}

If the downstream is a TiDB cluster or MySQL instance, it is recommended that you compare the data using [同期差分インスペクター](/sync-diff-inspector/sync-diff-inspector-overview.md).

## 単一テーブルのレプリケーションは単一のTiCDCノードでのみ実行できます。複数のTiCDCノードを使用して複数テーブルのデータをレプリケーションすることは可能ですか？ {#replication-of-a-single-table-can-only-be-run-on-a-single-ticdc-node-will-it-be-possible-to-use-multiple-ticdc-nodes-to-replicate-data-of-multiple-tables}

v7.1.0以降、TiCDCはMQシンクをサポートし、TiKVリージョンの粒度でデータ変更ログを複製します。これによりスケーラブルな処理能力が実現され、TiCDCは単一のテーブルを多数のリージョンに複製できるようになります。この機能を有効にするには、 [TiCDC 構成ファイル](/ticdc/ticdc-changefeed-config.md)で以下のパラメータを設定します。

```toml
[scheduler]
enable-table-across-nodes = true
```

## アップストリームに長時間実行されているコミットされていないトランザクションがある場合、TiCDC レプリケーションは停止しますか? {#does-ticdc-replication-get-stuck-if-the-upstream-has-long-running-uncommitted-transactions}

TiDBにはトランザクションタイムアウト機構があります。トランザクションの実行時間が[`max-txn-ttl`](/tidb-configuration-file.md#max-txn-ttl)秒を超えると、TiDBは強制的にロールバックします。TiCDCはトランザクションがコミットされるまで待機してからレプリケーションを続行するため、レプリケーションの遅延が発生します。

## TiDB Operatorによってデプロイされた TiCDC クラスターを<code>cdc cli</code>コマンドを使用して操作できないのはなぜですか? {#why-can-t-i-use-the-code-cdc-cli-code-command-to-operate-a-ticdc-cluster-deployed-by-tidb-operator}

これは、 TiDB OperatorによってデプロイされたTiCDCクラスタのデフォルトポート番号が`8301`であるのに対し、TiCDCサーバーに接続するためのコマンド`cdc cli`のデフォルトポート番号が`8300`あるためです。TiDB TiDB OperatorによってデプロイされたTiCDCクラスタをコマンド`cdc cli`で操作する場合は、以下のように`--server`パラメータを明示的に指定する必要があります。

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

生成列には、仮想生成列と保存生成列が含まれます。TiCDCは仮想生成列を無視し、保存生成列のみを下流に複製します。ただし、下流がMySQLまたはMySQL互換データベース（Kafkaなどのstorageサービスではない）である場合、保存生成列も無視されます。

> **Note:**
>
> When replicating stored generated columns to Kafka or a storage service and then writing them back to MySQL, `Error 3105 (HY000): The value specified for generated column 'xx' in table 'xxx' is not allowed` might occur. To avoid this error, you can use [オープンプロトコル](/ticdc/ticdc-open-protocol.md#ticdc-open-protocol) for replication. The output of this protocol includes [列のビットフラグ](/ticdc/ticdc-open-protocol.md#bit-flags-of-columns), which can distinguish whether a column is a generated column.

## 頻繁に発生する<code>CDC:ErrMySQLDuplicateEntryCDC</code>エラーを解決するにはどうすればよいですか? {#how-do-i-resolve-frequent-code-cdc-errmysqlduplicateentrycdc-code-errors}

TiCDC を使用してデータを TiDB または MySQL に複製する場合、アップストリームの SQL ステートメントが特定のパターンで実行されると、次のエラーが発生する可能性があります。

`CDC:ErrMySQLDuplicateEntryCDC`

エラーの原因：TiDBは、同一トランザクション内の同一行に対する`DELETE + INSERT`操作を、1つの`UPDATE`行の変更として結合します。TiCDCがこれらの変更を更新として下流に複製する際、一意のキー値を交換しようとする`UPDATE`操作によって競合が発生する可能性があります。

Taking the following table as an example:

```sql
CREATE TABLE data_table (
    id BIGINT(20) NOT NULL PRIMARY KEY,
    value BINARY(16) NOT NULL,
    UNIQUE KEY value_index (value)
) CHARSET=utf8mb4 COLLATE=utf8mb4_bin;
```

If the upstream attempts to swap the `value` field of the two rows in the table:

```sql
DELETE FROM data_table WHERE id = 1;
DELETE FROM data_table WHERE id = 2;
INSERT INTO data_table (id, value) VALUES (1, 'v3');
INSERT INTO data_table (id, value) VALUES (2, 'v1');
```

TiDB は 2 つの`UPDATE`行の変更を生成するため、TiCDC はそれを下流へのレプリケーション用の 2 つの`UPDATE`文に変換します。

```sql
UPDATE data_table SET value = 'v3' WHERE id = 1;
UPDATE data_table SET value = 'v1' WHERE id = 2;
```

2 番目`UPDATE`ステートメントを実行するときにダウンストリーム テーブルにまだ`v1`が含まれている場合、 `value`列の一意キー制約に違反し、 `CDC:ErrMySQLDuplicateEntryCDC`エラーが発生します。

If the `CDC:ErrMySQLDuplicateEntryCDC` error occurs frequently, you can enable TiCDC safe mode by setting the `safe-mode=true` parameter in the [`sink-uri`](/ticdc/ticdc-sink-to-mysql.md#configure-sink-uri-for-mysql-or-tidb) configuration:

    mysql://user:password@host:port/?safe-mode=true

セーフ モードでは、TiCDC は`UPDATE`操作を`DELETE + REPLACE INTO`に分割して実行し、一意のキーの競合エラーを回避します。
