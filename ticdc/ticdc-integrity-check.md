---
title: TiCDC Data Integrity Validation for Single-Row Data
summary: TiCDC データ整合性検証機能の実装原理と使用方法を紹介します。
---

# 単一行データの TiCDC データ整合性検証 {#ticdc-data-integrity-validation-for-single-row-data}

v7.1.0 以降、TiCDC ではデータ整合性検証機能が導入され、 [チェックサムアルゴリズム](#checksum-algorithms)を使用して単一行データの整合性を検証します。この機能は、TiDB からデータを書き込み、それを TiCDC で複製し、それを Kafka クラスターに書き込むプロセスでエラーが発生していないかどうかを確認するのに役立ちます。現在、この機能をサポートしているのは、ダウンストリームとして Kafka を使用し、プロトコルとして Simple または Avro を使用する変更フィードのみです。チェックサム アルゴリズムの詳細については、 [チェックサム計算アルゴリズム](#algorithm-for-checksum-calculation)参照してください。

## 機能を有効にする {#enable-the-feature}

TiCDC はデフォルトでデータ整合性検証を無効にします。有効にするには、次の手順を実行します。

1.  [`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710)システム変数を設定して、アップストリーム TiDB クラスター内の単一行データのチェックサム整合性検証機能を有効にします。

    ```sql
    SET GLOBAL tidb_enable_row_level_checksum = ON;
    ```

    この構成は新しく作成されたセッションに対してのみ有効になるため、TiDB に再接続する必要があります。

2.  changefeed を作成するときに、 `--config`パラメータで指定された[設定ファイル](/ticdc/ticdc-changefeed-config.md#changefeed-configuration-parameters)に次の構成を追加します。

    ```toml
    [integrity]
    integrity-check-level = "correctness"
    corruption-handle-level = "warn"
    ```

3.  データ エンコード形式として Avro を使用する場合は、 [`sink-uri`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)に[`enable-tidb-extension=true`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)設定する必要があります。ネットワーク転送中に数値精度が失われてチェックサム検証が失敗するのを防ぐには、 [`avro-decimal-handling-mode=string`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)と[`avro-bigint-unsigned-handling-mode=string`](/ticdc/ticdc-sink-to-kafka.md#configure-sink-uri-for-kafka)も設定する必要があります。次に例を示します。

    ```shell
    cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro-checksum" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro&enable-tidb-extension=true&avro-decimal-handling-mode=string&avro-bigint-unsigned-handling-mode=string" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
    ```

    上記の構成では、changefeed によって Kafka に書き込まれる各メッセージには、対応するデータのチェックサムが含まれます。これらのチェックサム値に基づいてデータの一貫性を検証できます。

    > **注記：**
    >
    > 既存の変更フィードの場合、 `avro-decimal-handling-mode`と`avro-bigint-unsigned-handling-mode`が設定されていない場合、チェックサム検証機能を有効にすると、スキーマの互換性の問題が発生する可能性があります。 この問題を解決するには、スキーマ レジストリの互換性タイプを`NONE`に変更できます。 詳細については、 [スキーマレジストリ](https://docs.confluent.io/platform/current/schema-registry/fundamentals/avro.html#no-compatibility-checking)参照してください。

## 機能を無効にする {#disable-the-feature}

TiCDC は、デフォルトでデータ整合性検証を無効にします。この機能を有効にした後に無効にするには、次の手順を実行します。

1.  [タスク構成の更新](/ticdc/ticdc-manage-changefeed.md#update-task-configuration)で説明した`Pause Task -> Modify Configuration -> Resume Task`プロセスに従い、changefeed の`--config`のパラメータで指定された構成ファイル内の`[integrity]`の構成をすべて削除します。

    ```toml
    [integrity]
    integrity-check-level = "none"
    corruption-handle-level = "warn"
    ```

2.  チェックサム整合性検証機能を無効にするには、アップストリームTiDBで次のSQL文を実行します（ [`tidb_enable_row_level_checksum`](/system-variables.md#tidb_enable_row_level_checksum-new-in-v710) ）。

    ```sql
    SET GLOBAL tidb_enable_row_level_checksum = OFF;
    ```

    上記の構成は、新しく作成されたセッションに対してのみ有効です。TiDB に書き込むすべてのクライアントが再接続されると、changefeed によって Kafka に書き込まれるメッセージには、対応するデータのチェックサムが含まれなくなります。

## チェックサムアルゴリズム {#checksum-algorithms}

### チェックサム V1 {#checksum-v1}

v8.4.0 より前では、TiDB と TiCDC はチェックサムの計算と検証に Checksum V1 を使用します。

単一行データのチェックサム整合性検証機能を有効にすると、TiDB は CRC32 アルゴリズムを使用して各行のチェックサムを計算し、データとともに TiKV に書き込みます。TiCDC は TiKV からデータを読み取り、同じアルゴリズムを使用してチェックサムを再計算します。2 つのチェックサムが等しい場合、TiDB から TiCDC への転送中にデータが一貫していることを示します。

次に、TiCDC はデータを特定の形式にエンコードし、Kafka に送信します。Kafka コンシューマーがデータを読み取った後、TiDB と同じ CRC32 アルゴリズムを使用して新しいチェックサムを計算します。新しいチェックサムがデータ内のチェックサムと等しい場合、TiCDC から Kafka コンシューマーへの送信中にデータが一貫していることを示します。

### チェックサム V2 {#checksum-v2}

v8.4.0 以降、TiDB と TiCDC では、 `ADD COLUMN`または`DROP COLUMN`操作後に更新または削除イベントで古い値を検証する際の Checksum V1 の問題に対処するために Checksum V2 が導入されています。

v8.4.0 以降で作成されたクラスター、または v8.4.0 以降にアップグレードされたクラスターの場合、単一行データのチェックサム検証が有効になっていると、TiDB はデフォルトで Checksum V2 を使用します。TiCDC は Checksum V1 と V2 の両方の処理をサポートしています。この変更は TiDB と TiCDC の内部実装にのみ影響し、下流の Kafka コンシューマーのチェックサム計算方法には影響しません。

## チェックサム計算アルゴリズム {#algorithm-for-checksum-calculation}

チェックサム計算アルゴリズムの疑似コードは次のとおりです。

    fn checksum(columns) {
        let result = 0
        for column in sort_by_schema_order(columns) {
            result = crc32.update(result, encode(column))
        }
        return result
    }

-   `columns`列 ID でソートする必要があります。Avro スキーマでは、フィールドはすでに列 ID でソートされているため、 `columns`の順序を直接使用できます。

-   `encode(column)`関数は列の値をバイトにエンコードします。エンコード ルールは列のデータ型によって異なります。具体的なルールは次のとおりです。

    -   TINYINT、SMALLINT、INT、BIGINT、MEDIUMINT、YEAR 型は UINT64 に変換され、リトルエンディアン形式でエンコードされます。たとえば、数値`0x0123456789abcdef`は`hex'0x0123456789abcdef'`としてエンコードされます。

    -   FLOAT および DOUBLE 型は DOUBLE に変換され、その後 IEEE754 形式の UINT64 としてエンコードされます。

    -   BIT、ENUM、SET 型は UINT64 に変換されます。

        -   BIT 型はバイナリ形式の UINT64 に変換されます。
        -   ENUM 型と SET 型は、UINT64 の対応する INT 値に変換されます。たとえば、 `SET('a','b','c')`型の列のデータ値が`'a,c'`の場合、値は`0b101`としてエンコードされ、10 進数では`5`なります。

    -   TIMESTAMP、DATE、DURATION、DATETIME、JSON、および DECIMAL 型は、最初に STRING に変換され、次にバイトに変換されます。

    -   CHAR、VARCHAR、VARSTRING、STRING、 TEXT、BLOB 型 (TINY、MEDIUM、LONG を含む) は、直接バイトに変換されます。

    -   NULL および GEOMETRY 型はチェックサム計算から除外され、この関数は空のバイトを返します。

Golang を使用したデータ消費とチェックサム検証の実装の詳細については、 [TiCDC 行データ チェックサム検証](/ticdc/ticdc-avro-checksum-verification.md)参照してください。

> **注記：**
>
> -   チェックサム検証機能を有効にすると、DECIMAL および UNSIGNED BIGINT 型のデータは STRING 型に変換されます。したがって、ダウンストリームのコンシューマー コードでは、チェックサム値を計算する前に、それらを対応する数値型に戻す必要があります。
> -   チェックサム検証プロセスには DELETE イベントは含まれません。これは、DELETE イベントにはハンドル キー列のみが含まれ、チェックサムはすべての列に基づいて計算されるためです。
