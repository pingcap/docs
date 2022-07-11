---
title: TiCDC Avro Protocol
summary: Learn the concept of TiCDC Avro Protocol and how to use it.
---

# TiCDCAvroプロトコル {#ticdc-avro-protocol}

Avroは、 [ApacheAvro™](https://avro.apache.org/)で定義され、デフォルトのデータ交換フォーマットとして[コンフルエントなプラットフォーム](https://docs.confluent.io/platform/current/platform.html)で選択されるデータ交換フォーマットプロトコルです。このドキュメントでは、TiDB拡張フィールド、Avroデータ形式の定義、Avroと[コンフルエントなスキーマレジストリ](https://docs.confluent.io/platform/current/schema-registry/index.html)の間の相互作用など、TiCDCでのAvroデータ形式の実装について説明します。

## Avroを使用する {#use-avro}

メッセージキュー（MQ）をダウンストリームシンクとして使用する場合、 `sink-uri`でAvroを指定できます。 TiCDCはTiDBDMLイベントをキャプチャし、これらのイベントからAvroメッセージを作成し、メッセージをダウンストリームに送信します。 Avroはスキーマの変更を検出すると、最新のスキーマをスキーマレジストリに登録します。

次に、Avroを使用した構成例を示します。

{{< copyable "" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --changefeed-id="kafka-avro" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

値`--schema-registry`は、 `https`プロトコルと`username:password`認証をサポートします（例： `--schema-registry=https://username:password@schema-registry-uri.com` ）。ユーザー名とパスワードはURLエンコードされている必要があります。

## TiDB拡張フィールド {#tidb-extension-fields}

デフォルトでは、AvroはDMLイベントで変更された行のデータのみを収集し、データ変更のタイプまたはTiDB固有のCommitTS（トランザクションの一意の識別子）を収集しません。この問題に対処するために、TiCDCは次の3つのTiDB拡張フィールドをAvroプロトコルメッセージに導入します。 `sink-uri`で`enable-tidb-extension`が`true` （デフォルトでは`false` ）に設定されている場合、TiCDCはメッセージ生成中にこれらの3つのフィールドをAvroメッセージに追加します。

-   `_tidb_op` ：DMLタイプ。 「c」は挿入を示し、「u」は更新を示します。
-   `_tidb_commit_ts` ：トランザクションの一意の識別子。
-   `_tidb_commit_physical_time` ：トランザクション識別子の物理タイムスタンプ。

次に、構成例を示します。

{{< copyable "" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --changefeed-id="kafka-avro-enable-extension" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro&enable-tidb-extension=true" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

## データ形式の定義 {#definition-of-the-data-format}

TiCDCはDMLイベントをKafkaイベントに変換し、イベントのキーと値はAvroプロトコルに従ってエンコードされます。

### キーデータ形式 {#key-data-format}

```
{
    "name":"{{TableName}}",
    "namespace":"{{Namespace}}",
    "type":"record",
    "fields":[
        {{ColumnValueBlock}},
        {{ColumnValueBlock}},
    ]
}
```

-   `{{TableName}}`は、イベントが発生するテーブルの名前を示します。
-   `{{Namespace}}`はAvroの名前空間です。
-   `{{ColumnValueBlock}}`は、データの各列の形式を定義します。

キーの`fields`には、主キー列または一意のインデックス列のみが含まれます。

### 値のデータ形式 {#value-data-format}

```
{
    "name":"{{TableName}}",
    "namespace":"{{Namespace}}",
    "type":"record",
    "fields":[
        {{ColumnValueBlock}},
        {{ColumnValueBlock}},
    ]
}
```

デフォルトでは、Valueのデータ形式はKeyのデータ形式と同じです。ただし、値の`fields`には、主キー列だけでなく、すべての列が含まれます。

[`enable-tidb-extension`](#tidb-extension-fields)を有効にすると、値のデータ形式は次のようになります。

```
{
    "name":"{{TableName}}",
    "namespace":"{{Namespace}}",
    "type":"record",
    "fields":[
        {{ColumnValueBlock}},
        {{ColumnValueBlock}},
        {
            "name":"_tidb_op",
            "type":"string"
        },
        {
            "name":"_tidb_commit_ts",
            "type":"long"
        },
        {
            "name":"_tidb_commit_physical_time",
            "type":"long"
        }
    ]
}
```

`enable-tidb-extension`が無効になっている値データ形式と比較して、 `_tidb_op` 、および`_tidb_commit_physical_time`の`_tidb_commit_ts`つの新しいフィールドが追加されています。

### カラムデータ形式 {#column-data-format}

カラムデータは、キー/値データ形式の`{{ColumnValueBlock}}`の部分です。 TiCDCは、SQLタイプに基づいてカラムデータ形式を生成します。基本的なカラムデータ形式は次のとおりです。

```
{
    "name":"{{ColumnName}}",
    "type":{
        "connect.parameters":{
            "tidb_type":"{{TIDB_TYPE}}"
        },
        "type":"{{AVRO_TYPE}}"
    }
}
```

1つの列がNULLになる可能性がある場合、カラムのデータ形式は次のようになります。

```
{
    "default":null,
    "name":"{{ColumnName}}",
    "type":[
        "null",
        {
            "connect.parameters":{
                "tidb_type":"{{TIDB_TYPE}}"
            },
            "type":"{{AVRO_TYPE}}"
        }
    ]
}
```

-   `{{ColumnName}}`は列名を示します。
-   `{{TIDB_TYPE}}`は、TiDBのタイプを示します。これは、SQLタイプとの1対1のマッピングではありません。
-   `{{AVRO_TYPE}}`は[avroスペック](https://avro.apache.org/docs/current/spec.html)のタイプを示します。

| SQLタイプ     | TIDB_TYPE | AVRO_TYPE | 説明                                                                                               |
| ---------- | --------- | --------- | ------------------------------------------------------------------------------------------------ |
| BOOL       | INT       | int       |                                                                                                  |
| TINYINT    | INT       | int       | 符号なしの場合、TIDB_TYPEはINTUNSIGNEDです。                                                                 |
| SMALLINT   | INT       | int       | 符号なしの場合、TIDB_TYPEはINTUNSIGNEDです。                                                                 |
| MEDIUMINT  | INT       | int       | 符号なしの場合、TIDB_TYPEはINTUNSIGNEDです。                                                                 |
| INT        | INT       | int       | 符号なしの場合、TIDB_TYPEはINT UNSIGNEDであり、AVRO_TYPEは長いです。                                                |
| BIGINT     | BIGINT    | 長いです      | 符号なしの場合、TIDB_TYPEはBIGINTUNSIGNEDです。 `avro-bigint-unsigned-handling-mode`が文字列の場合、AVRO_TYPEは文字列です。 |
| TINYBLOB   | BLOB      | バイト       |                                                                                                  |
| BLOB       | BLOB      | バイト       |                                                                                                  |
| MEDIUMBLOB | BLOB      | バイト       |                                                                                                  |
| LONGBLOB   | BLOB      | バイト       |                                                                                                  |
| バイナリ       | BLOB      | バイト       |                                                                                                  |
| VARBINARY  | BLOB      | バイト       |                                                                                                  |
| TINYTEXT   | 文章        | ストリング     |                                                                                                  |
| 文章         | 文章        | ストリング     |                                                                                                  |
| MEDIUMTEXT | 文章        | ストリング     |                                                                                                  |
| LONGTEXT   | 文章        | ストリング     |                                                                                                  |
| CHAR       | 文章        | ストリング     |                                                                                                  |
| VARCHAR    | 文章        | ストリング     |                                                                                                  |
| 浮く         | 浮く        | ダブル       |                                                                                                  |
| ダブル        | ダブル       | ダブル       |                                                                                                  |
| 日にち        | 日にち       | ストリング     |                                                                                                  |
| 日付時刻       | 日付時刻      | ストリング     |                                                                                                  |
| タイムスタンプ    | タイムスタンプ   | ストリング     |                                                                                                  |
| 時間         | 時間        | ストリング     |                                                                                                  |
| 年          | 年         | int       |                                                                                                  |
| 少し         | 少し        | バイト       |                                                                                                  |
| JSON       | JSON      | ストリング     |                                                                                                  |
| ENUM       | ENUM      | ストリング     |                                                                                                  |
| 設定         | 設定        | ストリング     |                                                                                                  |
| 10進数       | 10進数      | バイト       | `avro-decimal-handling-mode`が文字列の場合、AVRO_TYPEは文字列です。                                             |

Avroプロトコルでは、他の2つの`sink-uri`パラメーターがカラムデータ形式にも影響を与える可能性があります： `avro-decimal-handling-mode`と`avro-bigint-unsigned-handling-mode` 。

-   `avro-decimal-handling-mode`は、Avroが次のような10進フィールドを処理する方法を制御します。

    -   string：Avroは10進フィールドを文字列として処理します。
    -   正確：Avroは10進フィールドをバイトとして処理します。

-   `avro-bigint-unsigned-handling-mode`は、AvroがBIGINTUNSIGNEDフィールドを処理する方法を制御します。

    -   文字列：AvroはBIGINTUNSIGNEDフィールドを文字列として処理します。
    -   long：Avroは、BIGINTUNSIGNEDフィールドを64ビットの符号付き整数として処理します。値が`9223372036854775807`より大きい場合、オーバーフローが発生します。

次に、構成例を示します。

{{< copyable "" >}}

```shell
cdc cli changefeed create --pd=http://127.0.0.1:2379 --changefeed-id="kafka-avro-string-option" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro&avro-decimal-handling-mode=string&avro-bigint-unsigned-handling-mode=string" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

ほとんどのSQLタイプは、基本のカラムデータ形式にマップされます。他のいくつかのSQLタイプは、基本データ形式を拡張してより多くの情報を提供します。

BIT（64）

```
{
    "name":"{{ColumnName}}",
    "type":{
        "connect.parameters":{
            "tidb_type":"BIT",
            "length":"64"
        },
        "type":"bytes"
    }
}
```

ENUM / SET（a、b、c）

```
{
    "name":"{{ColumnName}}",
    "type":{
        "connect.parameters":{
            "tidb_type":"ENUM/SET",
            "allowed":"a,b,c"
        },
        "type":"string"
    }
}
```

DECIMAL（10、4）

```
{
    "name":"{{ColumnName}}",
    "type":{
        "connect.parameters":{
            "tidb_type":"DECIMAL",
        },
        "logicalType":"decimal",
        "precision":10,
        "scale":4,
        "type":"bytes"
    }
}
```

## DDLイベントとスキーマの変更 {#ddl-events-and-schema-changes}

AvroはダウンストリームでDDLイベントを生成しません。 DMLイベントが発生するたびにスキーマが変更されるかどうかをチェックします。スキーマが変更されると、Avroは新しいスキーマを生成し、それをスキーマレジストリに登録します。スキーマの変更が互換性チェックに合格しない場合、登録は失敗します。 Avroは、スキーマの互換性の問題を解決しません。

スキーマの変更が互換性チェックに合格し、新しいバージョンが登録された場合でも、データプロデューサーとコンシューマーはシステムの正常な実行を保証するためにアップグレードを実行する必要があることに注意してください。

Confluent Schema Registryのデフォルトの互換性ポリシーが`BACKWARD`であると想定し、空でない列をソーステーブルに追加します。この状況では、Avroは新しいスキーマを生成しますが、互換性の問題のためにスキーマレジストリへの登録に失敗します。このとき、チェンジフィードはエラー状態になります。

スキーマの詳細については、 [スキーマレジストリ関連ドキュメント](https://docs.confluent.io/platform/current/schema-registry/avro.html)を参照してください。

## トピックの配布 {#topic-distribution}

スキーマレジストリは、TopicNameStrategy、RecordNameStrategy、およびTopicRecordNameStrategyの3つの[主題名戦略](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#subject-name-strategy)をサポートします。現在、TiCDC AvroはTopicNameStrategyのみをサポートしています。つまり、Kafkaトピックは1つのデータ形式のデータしか受信できません。したがって、TiCDC Avroは、複数のテーブルを同じトピックにマッピングすることを禁止しています。チェンジフィードを作成するときに、トピックルールに構成済みの配布ルールに`{schema}`と`{table}`のプレースホルダーが含まれていない場合、エラーが報告されます。
