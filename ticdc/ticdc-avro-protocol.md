---
title: TiCDC Avro Protocol
summary: TiCDC Avro プロトコルの概念とその使用方法を学びます。
---

# TiCDC Avroプロトコル {#ticdc-avro-protocol}

TiCDC Avroプロトコルは、 [コンフルエントプラットフォーム](https://docs.confluent.io/platform/current/platform.html)で定義された[合流アブロ](https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/serdes-avro.html)データ交換プロトコルのサードパーティ実装です。Avroは[アパッチ アブロ™](https://avro.apache.org/)で定義されたデータ形式です。

このドキュメントでは、TiCDC が Confluent Avro プロトコルを実装する方法と、Avro と[Confluent スキーマレジストリ](https://docs.confluent.io/platform/current/schema-registry/index.html)間の相互作用について説明します。

> **警告：**
>
> v7.3.0 以降、TiCDC を[有効なインデックスのないテーブルを複製する](/ticdc/ticdc-manage-changefeed.md#replicate-tables-without-a-valid-index)に有効にすると、Avro プロトコルを使用する変更フィードを作成するときに TiCDC によってエラーが報告されます。

## Avroを使用する {#use-avro}

以下は Avro を使用した構成例です。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

値`--schema-registry`は、プロトコル`https`と認証`username:password`サポートします。ユーザー名とパスワードはURLエンコードされている必要があります。例： `--schema-registry=https://username:password@schema-registry-uri.com` 。

> **注記：**
>
> Avroプロトコルを使用する場合、1つのKafkaトピックには1つのテーブルのデータのみを含めることができます。設定ファイルで[トピックディスパッチャ](/ticdc/ticdc-sink-to-kafka.md#topic-dispatchers)設定する必要があります。

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

## データ形式の定義 {#definition-of-the-data-format}

TiCDC は DML イベントを Kafka イベントに変換し、イベントのキーと値は Avro プロトコルに従ってエンコードされます。

### キーデータ形式 {#key-data-format}

    {
        "name":"{{TableName}}",
        "namespace":"{{Namespace}}",
        "type":"record",
        "fields":[
            {{ColumnValueBlock}},
            {{ColumnValueBlock}},
        ]
    }

-   `{{TableName}}`イベントが発生したテーブルの名前を示します。
-   `{{Namespace}}`は Avro の名前空間です。
-   `{{ColumnValueBlock}}`データの各列の形式を定義します。

キーの`fields`には、主キー列または一意のインデックス列のみが含まれます。

### 値のデータ形式 {#value-data-format}

    {
        "name":"{{TableName}}",
        "namespace":"{{Namespace}}",
        "type":"record",
        "fields":[
            {{ColumnValueBlock}},
            {{ColumnValueBlock}},
        ]
    }

デフォルトでは、値のデータ形式はキーと同じです。ただし、値の`fields`にはすべての列が含まれます。

> **注記：**
>
> Avro プロトコルは、DML イベントを次のようにエンコードします。
>
> -   削除イベントの場合、Avro はキー部分のみをエンコードします。値部分は空です。
> -   挿入イベントの場合、Avro はすべての列データを値部分にエンコードします。
> -   更新イベントの場合、Avro は値部分に更新されるすべての列データのみをエンコードします。
>
> Avroプロトコルは、UpdateイベントとDeleteイベントの古い値をエンコードしません。さらに、削除を識別するために`null`レコードを使用するほとんどのConfluentシンクコネクタ（ `delete.on.null` ）との互換性を確保するため、 `enable-tidb-extension`が有効になっている場合でも、Deleteイベントには`_tidb_commit_ts`などの拡張情報は含まれません。これらの機能が必要な場合は、Canal-JSONやDebeziumなどの他のプロトコルの使用を検討してください。

## TiDB拡張フィールド {#tidb-extension-fields}

デフォルトでは、AvroはDMLイベント内の変更された行のデータのみを収集し、データ変更の種類やTiDB固有のCommitTS（トランザクションの一意の識別子）は収集しません。この問題に対処するため、TiCDCはAvroプロトコルメッセージに以下の3つのTiDB拡張フィールドを導入しています。7で`enable-tidb-extension` `true` （デフォルトは`false` ）に設定すると、TiCDC `sink-uri`メッセージ生成時にこれらの3つのフィールドをAvroメッセージに追加します。

-   `_tidb_op` : DML タイプ。「c」は挿入を示し、「u」は更新を示します。
-   `_tidb_commit_ts` : トランザクションの一意の識別子。
-   `_tidb_commit_physical_time` : トランザクション識別子内の物理的なタイムスタンプ。

以下は設定例です。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro-enable-extension" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro&enable-tidb-extension=true" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

[`enable-tidb-extension`](#tidb-extension-fields)有効にすると、値のデータ形式は次のようになります。

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

`enable-tidb-extension`無効になっている値のデータ形式と比較すると、 `_tidb_op` 、 `_tidb_commit_ts` 、 `_tidb_commit_physical_time` 3 つの新しいフィールドが追加されます。

### カラムデータ形式 {#column-data-format}

カラムデータは、キー/値データ形式の第`{{ColumnValueBlock}}`要素です。TiCDCはSQLタイプに基づいてカラムデータ形式を生成します。基本的なカラムデータ形式は次のとおりです。

    {
        "name":"{{ColumnName}}",
        "type":{
            "connect.parameters":{
                "tidb_type":"{{TIDB_TYPE}}"
            },
            "type":"{{AVRO_TYPE}}"
        }
    }

1 つの列が NULL になる可能性がある場合、カラムのデータ形式は次のようになります。

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

-   `{{ColumnName}}`列名を示します。
-   `{{TIDB_TYPE}}` TiDB 内の型を示します。これは SQL 型との 1 対 1 のマッピングではありません。
-   `{{AVRO_TYPE}}` [Avro仕様](https://avro.apache.org/docs/++version++/specification)内のタイプを示します。

| SQLタイプ            | TIDB_タイプ          | AVRO_TYPE | 説明                                                                                                |
| ----------------- | ----------------- | --------- | ------------------------------------------------------------------------------------------------- |
| ブール               | INT               | 整数        |                                                                                                   |
| タイニーイント           | INT               | 整数        | 符号なしの場合、TIDB_TYPE は INT UNSIGNED になります。                                                           |
| スモールイント           | INT               | 整数        | 符号なしの場合、TIDB_TYPE は INT UNSIGNED になります。                                                           |
| ミディアムミント          | INT               | 整数        | 符号なしの場合、TIDB_TYPE は INT UNSIGNED になります。                                                           |
| INT               | INT               | 整数        | 符号なしの場合、TIDB_TYPE は INT UNSIGNED になり、AVRO_TYPE は long になります。                                      |
| ビッグイント            | ビッグイント            | 長さ        | 符号なしの場合、TIDB_TYPEはBIGINT UNSIGNEDです。1 `avro-bigint-unsigned-handling-mode`文字列の場合、AVRO_TYPEは文字列です。 |
| タイニーブロブ           | ブロブ               | バイト       | <li></li>                                                                                         |
| ブロブ               | ブロブ               | バイト       | <li></li>                                                                                         |
| ミディアムブロブ          | ブロブ               | バイト       | <li></li>                                                                                         |
| ロングブロブ            | ブロブ               | バイト       | <li></li>                                                                                         |
| バイナリ              | ブロブ               | バイト       | <li></li>                                                                                         |
| VARBINARY         | ブロブ               | バイト       | <li></li>                                                                                         |
| 小さなテキスト           | TEXT              | 弦         | <li></li>                                                                                         |
| TEXT              | TEXT              | 弦         | <li></li>                                                                                         |
| 中テキスト             | TEXT              | 弦         | <li></li>                                                                                         |
| 長文                | TEXT              | 弦         | <li></li>                                                                                         |
| チャー               | TEXT              | 弦         | <li></li>                                                                                         |
| 可変長文字             | TEXT              | 弦         | <li></li>                                                                                         |
| フロート              | フロート              | ダブル       | <li></li>                                                                                         |
| ダブル               | ダブル               | ダブル       | <li></li>                                                                                         |
| 日付                | 日付                | 弦         | <li></li>                                                                                         |
| 日時                | 日時                | 弦         | <li></li>                                                                                         |
| タイムスタンプ           | タイムスタンプ           | 弦         | <li></li>                                                                                         |
| 時間                | 時間                | 弦         | <li></li>                                                                                         |
| 年                 | 年                 | 整数        | <li></li>                                                                                         |
| 少し                | 少し                | バイト       | <li></li>                                                                                         |
| JSON              | JSON              | 弦         | <li></li>                                                                                         |
| 列挙型               | 列挙型               | 弦         | <li></li>                                                                                         |
| セット               | セット               | 弦         | <li></li>                                                                                         |
| 小数点               | 小数点               | バイト       | `avro-decimal-handling-mode`文字列の場合、AVRO_TYPE は文字列です。                                              |
| TiDBVECTORFloat32 | TiDBVECTORFloat32 | 弦         | <li></li>                                                                                         |

Avro プロトコルでは、他の 2 つの`sink-uri`パラメータ`avro-decimal-handling-mode`と`avro-bigint-unsigned-handling-mode`もカラムデータ形式に影響する可能性があります。

-   `avro-decimal-handling-mode` 、Avro が小数フィールドを処理する方法を制御します。これには以下が含まれます。

    -   文字列: Avro は小数フィールドを文字列として処理します。
    -   precise: Avro は 10 進フィールドをバイトとして処理します。

-   `avro-bigint-unsigned-handling-mode` 、Avro が BIGINT UNSIGNED フィールドを処理する方法を制御します。これには以下が含まれます。

    -   文字列: Avro は BIGINT UNSIGNED フィールドを文字列として処理します。
    -   long: AvroはBIGINT UNSIGNEDフィールドを64ビット符号付き整数として扱います。値が`9223372036854775807`より大きい場合、オーバーフローが発生します。

以下は設定例です。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro-string-option" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro&avro-decimal-handling-mode=string&avro-bigint-unsigned-handling-mode=string" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

ほとんどのSQL型は基本のカラムデータ形式にマッピングされます。他のSQL型の中には、基本データ形式を拡張してより多くの情報を提供するものもあります。

ビット(64)

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

列挙型/セット(a,b,c)

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

10進数(10, 4)

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

## DDLイベントとスキーマの変更 {#ddl-events-and-schema-changes}

AvroはDDLイベントとウォーターマークイベントを下流に送信しません。DMLイベントが発生するたびに、スキーマが変更されているかどうかを確認します。スキーマが変更された場合、Avroは新しいスキーマを生成し、スキーマレジストリに登録します。スキーマ変更が互換性チェックに合格しない場合、登録は失敗します。TiCDCはスキーマ互換性の問題を解決しません。

例えば、Confluent Schema Registry のデフォルトの[互換性ポリシー](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html#compatibility-types) `BACKWARD`設定されており、ソーステーブルに空でない列を追加したとします。この場合、Avro は新しいスキーマを生成しますが、互換性の問題により Schema Registry への登録に失敗します。このとき、changefeed はエラー状態になります。

スキーマの変更が互換性チェックに合格し、新しいバージョンが登録された場合でも、データのプロデューサーとコンシューマーはデータのエンコードとデコードのために新しいスキーマを取得する必要があることに注意してください。

スキーマの詳細については、 [スキーマレジストリ関連ドキュメント](https://docs.confluent.io/platform/current/schema-registry/avro.html)を参照してください。

## 消費者実装 {#consumer-implementation}

TiCDC Avro プロトコルは[`io.confluent.kafka.serializers.KafkaAvroDeserializer`](https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/serdes-avro.html#avro-deserializer)で逆シリアル化できます。

コンシューマー プログラムは[スキーマレジストリAPI](https://docs.confluent.io/platform/current/schema-registry/develop/api.html)を介して最新のスキーマを取得し、そのスキーマを使用して TiCDC Avro プロトコルによってエンコードされたデータを逆シリアル化できます。

### イベントの種類を区別する {#distinguish-event-types}

コンシューマー プログラムは、次のルールによって DML イベント タイプを区別できます。

-   Key部分のみの場合はDeleteイベントになります。
-   キーと値の両方がある場合、挿入イベントまたは更新イベントのいずれかです。1 [TiDB拡張フィールド](#tidb-extension-fields)有効になっている場合は、 `_tidb_op`フィールドを使用して挿入イベントか更新イベントかを識別できます。TiDB拡張フィールドが有効になっていない場合は、それらを区別できません。

## トピックの分布 {#topic-distribution}

スキーマレジストリは、TopicNameStrategy、RecordNameStrategy、TopicRecordNameStrategyの3つの[件名戦略](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#subject-name-strategy)サポートしています。現在、TiCDC AvroはTopicNameStrategyのみをサポートしており、Kafkaトピックは1つのデータ形式でのみデータを受信できます。そのため、TiCDC Avroでは複数のテーブルを同じトピックにマッピングすることは禁止されています。変更フィードを作成する際、トピックルールに設定された分散ルールの`{schema}`と`{table}`プレースホルダーが含まれていない場合、エラーが報告されます。

## 互換性 {#compatibility}

TiCDC クラスターを v7.0.0 にアップグレードする際、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合は、アップグレード前に Confluent Schema Registry の互換性ポリシーを手動で`None`に調整し、changefeed がスキーマを正常に更新できるようにする必要があります。そうしないと、アップグレード後に changefeed がスキーマを更新できなくなり、エラー状態になります。詳細については、 [＃8490](https://github.com/pingcap/tiflow/issues/8490)参照してください。
