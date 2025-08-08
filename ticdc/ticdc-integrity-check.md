---
title: TiCDC Data Integrity Validation for Single-Row Data
summary: TiCDC データ整合性検証機能の実装原理と使用方法を紹介します。
---

# 単一行データの TiCDC データ整合性検証 {#ticdc-data-integrity-validation-for-single-row-data}

v7.1.0以降、TiCDCはデータ整合性検証機能を導入しました。この機能は、 [チェックサムアルゴリズム](#checksum-algorithms)使用して単一行データの整合性を検証します。この機能は、TiDBからデータを書き込み、TiCDCを介して複製し、Kafkaクラスターに書き込むプロセスでエラーが発生していないかどうかを検証するのに役立ちます。現在、この機能は、ダウンストリームとしてKafkaを使用し、プロトコルとしてSimpleまたはAvroを使用するチェンジフィードのみでサポートされています。チェックサムアルゴリズムの詳細については、 [チェックサム計算アルゴリズム](#algorithm-for-checksum-calculation)参照してください。

## 機能を有効にする {#enable-the-feature}

TiCDCはデフォルトでデータ整合性検証を無効にしています。有効にするには、以下の手順を実行してください。

1.  [`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710)システム変数を設定して、アップストリーム TiDB クラスター内の単一行データのチェックサム整合性検証機能を有効にします。

    ```sql
    SET GLOBAL tidb_enable_row_level_checksum = ON;
    ```

    この構成は新しく作成されたセッションに対してのみ有効になるため、TiDB に再接続する必要があります。

2.  In the [設定ファイル](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters) specified by the `--config` parameter when you create a changefeed, add the following configurations:

    ```toml
    [integrity]
    integrity-check-level = "correctness"
    corruption-handle-level = "warn"
    ```

3.  データエンコード形式としてAvroを使用する場合は、 [`sink-uri`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)に[`enable-tidb-extension=true`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)設定する必要があります。ネットワーク転送中に数値精度が失われ、チェックサム検証エラーが発生するのを防ぐため、 [`avro-decimal-handling-mode=string`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)と[`avro-bigint-unsigned-handling-mode=string`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)設定する必要があります。以下に例を示します。

    ```shell
    cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro-checksum" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro&enable-tidb-extension=true&avro-decimal-handling-mode=string&avro-bigint-unsigned-handling-mode=string" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
    ```

    上記の設定により、changefeed によって Kafka に書き込まれる各メッセージには、対応するデータのチェックサムが含まれます。これらのチェックサム値に基づいてデータの整合性を検証できます。

    > **注記：**
    >
    > 既存の変更フィードにおいて、 `avro-decimal-handling-mode`と`avro-bigint-unsigned-handling-mode`設定されていない場合、チェックサム検証機能を有効にするとスキーマ互換性の問題が発生する可能性があります。この問題を解決するには、スキーマレジストリの互換性タイプを`NONE`に変更してください。詳細については、 [スキーマレジストリ](https://docs.confluent.io/platform/current/schema-registry/fundamentals/avro.html#no-compatibility-checking)参照してください。

## 機能を無効にする {#disable-the-feature}

TiCDC disables data integrity validation by default. To disable this feature after enabling it, perform the following steps:

1.  [Update task configuration](/ticdc/ticdc-manage-changefeed.md#update-task-configuration)で説明した`Pause Task -> Modify Configuration -> Resume Task`プロセスに従い、changefeed の`--config`パラメータで指定された構成ファイル内の`[integrity]`構成をすべて削除します。

    ```toml
    [integrity]
    integrity-check-level = "none"
    corruption-handle-level = "warn"
    ```

2.  チェックサム整合性検証機能を無効にするには、上流のTiDBで次のSQL文を実行します（ [`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710) ）。

    ```sql
    SET GLOBAL tidb_enable_row_level_checksum = OFF;
    ```

    上記の設定は、新しく作成されたセッションにのみ適用されます。TiDBに書き込みを行っているすべてのクライアントが再接続すると、changefeedによってKafkaに書き込まれるメッセージには、対応するデータのチェックサムが含まれなくなります。

## チェックサムアルゴリズム {#checksum-algorithms}

### チェックサムV1 {#checksum-v1}

v8.4.0 より前では、TiDB および TiCDC はチェックサムの計算と検証に Checksum V1 を使用します。

単一行データのチェックサム整合性検証機能を有効にすると、TiDBはCRC32アルゴリズムを使用して各行のチェックサムを計算し、データと共にTiKVに書き込みます。TiCDCはTiKVからデータを読み取り、同じアルゴリズムを使用してチェックサムを再計算します。2つのチェックサムが等しい場合、TiDBからTiCDCへの転送中にデータの整合性が保たれていることを示します。

TiCDCはデータを特定の形式にエンコードし、Kafkaに送信します。Kafkaコンシューマーがデータを読み取ると、TiDBと同じCRC32アルゴリズムを使用して新しいチェックサムを計算します。新しいチェックサムがデータ内のチェックサムと一致する場合、TiCDCからKafkaコンシューマーへの送信中にデータの一貫性が保たれていることを示します。

### チェックサムV2 {#checksum-v2}

v8.4.0 以降、TiDB および TiCDC では、 `ADD COLUMN`または`DROP COLUMN`操作後に更新イベントまたは削除イベントで古い値を検証する際の Checksum V1 の問題に対処するために Checksum V2 が導入されています。

For clusters created in v8.4.0 or later, or clusters upgraded to v8.4.0 or later, TiDB uses Checksum V2 by default when single-row data checksum verification is enabled. TiCDC supports handling both Checksum V1 and V2. This change only affects TiDB and TiCDC internal implementation and does not affect checksum calculation methods for downstream Kafka consumers.

## チェックサム計算アルゴリズム {#algorithm-for-checksum-calculation}

チェックサム計算アルゴリズムの疑似コードは次のとおりです。

    fn checksum(columns) {
        let result = 0
        for column in sort_by_schema_order(columns) {
            result = crc32.update(result, encode(column))
        }
        return result
    }

-   `columns`列IDでソートする必要があります。Avroスキーマでは、フィールドは既に列IDでソートされているため、 `columns`の順序をそのまま使用できます。

-   `encode(column)`関数は列の値をバイト列にエンコードします。エンコードのルールは列のデータ型によって異なります。具体的なルールは以下のとおりです。

    -   TINYINT, SMALLINT, INT, BIGINT, MEDIUMINT, and YEAR types are converted to UINT64 and encoded in little-endian. For example, the number `0x0123456789abcdef` is encoded as `hex'0x0123456789abcdef'`.

    -   FLOAT および DOUBLE 型は DOUBLE に変換され、その後 IEEE754 形式の UINT64 としてエンコードされます。

    -   BIT, ENUM, and SET types are converted to UINT64.

        -   BIT 型はバイナリ形式の UINT64 に変換されます。
        -   ENUM型とSET型は、UINT64の対応するINT値に変換されます。例えば、 `SET('a','b','c')`型の列のデータ値が`'a,c'`場合、その値は`0b101` （10進数では`5`としてエンコードされます。

    -   TIMESTAMP、DATE、DURATION、DATETIME、JSON、および DECIMAL 型は、最初に STRING に変換され、次にバイトに変換されます。

    -   CHAR、VARCHAR、VARSTRING、STRING、 TEXT、および BLOB 型 (TINY、MEDIUM、および LONG を含む) は、直接バイトに変換されます。

    -   NULL および GEOMETRY 型はチェックサム計算から除外され、この関数は空のバイトを返します。

Golangを使用したデータ消費とチェックサム検証の実装の詳細については、 [TiCDC 行データチェックサム検証](/ticdc/ticdc-avro-checksum-verification.md)参照してください。

> **注記：**
>
> -   チェックサム検証機能を有効にすると、DECIMAL型およびUNSIGNED BIGINT型のデータはSTRING型に変換されます。そのため、下流のコンシューマーコードでは、チェックサム値を計算する前に、これらのデータを対応する数値型に戻す必要があります。
> -   チェックサム検証プロセスにはDELETEイベントは含まれません。これは、DELETEイベントにはハンドルキー列のみが含まれるのに対し、チェックサムはすべての列に基づいて計算されるためです。
