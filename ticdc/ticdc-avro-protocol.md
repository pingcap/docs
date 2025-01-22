---
title: TiCDC Avro Protocol
summary: TiCDC Avro プロトコルの概念とその使用方法を学びます。
---

# TiCDC Avro プロトコル {#ticdc-avro-protocol}

TiCDC Avroプロトコルは、 [合流プラットフォーム](https://docs.confluent.io/platform/current/platform.html)で定義された[合流アブロ](https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/serdes-avro.html)データ交換プロトコルのサードパーティ実装です。Avroは[アパッチアブロ™](https://avro.apache.org/)で定義されたデータ形式です。

このドキュメントでは、TiCDC が Confluent Avro プロトコルを実装する方法と、Avro と[Confluent スキーマ レジストリ](https://docs.confluent.io/platform/current/schema-registry/index.html)間の相互作用について説明します。

> **警告：**
>
> v7.3.0 以降では、TiCDC を[有効なインデックスのないテーブルを複製する](/ticdc/ticdc-manage-changefeed.md#replicate-tables-without-a-valid-index)に有効にすると、Avro プロトコルを使用する変更フィードを作成するときに TiCDC によってエラーが報告されます。

## Avroを使用する {#use-avro}

以下は Avro を使用した構成例です。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

値`--schema-registry`は、 `https`プロトコルと`username:password`認証をサポートします。ユーザー名とパスワードは URL エンコードされている必要があります。たとえば、 `--schema-registry=https://username:password@schema-registry-uri.com`です。

> **注記：**
>
> Avro プロトコルを使用する場合、1 つの Kafka トピックには 1 つのテーブルのデータのみを含めることができます。構成ファイルで[トピックディスパッチャ](/ticdc/ticdc-sink-to-kafka.md#topic-dispatchers)を構成する必要があります。

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
-   `{{Namespace}}` Avro の名前空間です。
-   `{{ColumnValueBlock}}`データの各列の形式を定義します。

キーの`fields`には、主キー列または一意のインデックス列のみが含まれます。

### 値データ形式 {#value-data-format}

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
> -   削除イベントの場合、Avro はキー部分のみをエンコードします。値の部分は空です。
> -   挿入イベントの場合、Avro はすべての列データを値部分にエンコードします。
> -   更新イベントの場合、Avro は値部分に更新されるすべての列データのみをエンコードします。
>
> Avro プロトコルは、Update イベントと Delete イベントの古い値をエンコードしません。さらに、削除を識別するために`null`レコードに依存するほとんどの Confluent シンク コネクタ ( `delete.on.null` ) との互換性を保つために、 `enable-tidb-extension`が有効になっている場合でも、Delete イベントには`_tidb_commit_ts`などの拡張情報は含まれません。これらの機能が必要な場合は、Canal-JSON や Debezium などの他のプロトコルの使用を検討してください。

## TiDB拡張フィールド {#tidb-extension-fields}

デフォルトでは、Avro は DML イベントで変更された行のデータのみを収集し、データ変更の種類や TiDB 固有の CommitTS (トランザクションの一意の識別子) は収集しません。この問題に対処するために、TiCDC は Avro プロトコル メッセージに次の 3 つの TiDB 拡張フィールドを導入します`sink-uri`で`enable-tidb-extension`が`true` (デフォルトでは`false` ) に設定されている場合、TiCDC はメッセージ生成中にこれらの 3 つのフィールドを Avro メッセージに追加します。

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

`enable-tidb-extension`無効になっている値データ形式と比較すると、 `_tidb_op` 、 `_tidb_commit_ts` 、 `_tidb_commit_physical_time` 3 つの新しいフィールドが追加されます。

### カラムデータ形式 {#column-data-format}

カラムデータは、キー/値データ形式の`{{ColumnValueBlock}}`部分です。TiCDC は、SQL タイプに基づいてカラムデータ形式を生成します。基本的なカラムデータ形式は次のとおりです。

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

| SQL タイプ  | TIDB_タイプ | AVRO_タイプ | 説明                                                                                                    |
| -------- | -------- | -------- | ----------------------------------------------------------------------------------------------------- |
| ブール      | 内部       | 整数       |                                                                                                       |
| 小さな      | 内部       | 整数       | 符号なしの場合、TIDB_TYPE は INT UNSIGNED になります。                                                               |
| スモールイント  | 内部       | 整数       | 符号なしの場合、TIDB_TYPE は INT UNSIGNED になります。                                                               |
| ミディアムミント | 内部       | 整数       | 符号なしの場合、TIDB_TYPE は INT UNSIGNED になります。                                                               |
| 内部       | 内部       | 整数       | 符号なしの場合、TIDB_TYPE は INT UNSIGNED になり、AVRO_TYPE は long になります。                                          |
| ビッグイント   | ビッグイント   | 長さ       | 符号なしの場合、TIDB_TYPE は BIGINT UNSIGNED です。1 `avro-bigint-unsigned-handling-mode`文字列の場合、AVRO_TYPE は文字列です。 |
| タイニーブロブ  | ブロブ      | バイト      | <li></li>                                                                                             |
| ブロブ      | ブロブ      | バイト      | <li></li>                                                                                             |
| ミディアムブロブ | ブロブ      | バイト      | <li></li>                                                                                             |
| ロングロブ    | ブロブ      | バイト      | <li></li>                                                                                             |
| バイナリ     | ブロブ      | バイト      | <li></li>                                                                                             |
| バイナリ     | ブロブ      | バイト      | <li></li>                                                                                             |
| 小さなテキスト  | TEXT     | 弦        | <li></li>                                                                                             |
| TEXT     | TEXT     | 弦        | <li></li>                                                                                             |
| 中テキスト    | TEXT     | 弦        | <li></li>                                                                                             |
| 長文       | TEXT     | 弦        | <li></li>                                                                                             |
| 文字       | TEXT     | 弦        | <li></li>                                                                                             |
| バルチャー    | TEXT     | 弦        | <li></li>                                                                                             |
| フロート     | フロート     | ダブル      | <li></li>                                                                                             |
| ダブル      | ダブル      | ダブル      | <li></li>                                                                                             |
| 日付       | 日付       | 弦        | <li></li>                                                                                             |
| 日時       | 日時       | 弦        | <li></li>                                                                                             |
| タイムスタンプ  | タイムスタンプ  | 弦        | <li></li>                                                                                             |
| 時間       | 時間       | 弦        | <li></li>                                                                                             |
| 年        | 年        | 整数       | <li></li>                                                                                             |
| 少し       | 少し       | バイト      | <li></li>                                                                                             |
| 翻訳       | 翻訳       | 弦        | <li></li>                                                                                             |
| 列挙       | 列挙       | 弦        | <li></li>                                                                                             |
| セット      | セット      | 弦        | <li></li>                                                                                             |
| 小数点      | 小数点      | バイト      | `avro-decimal-handling-mode`文字列の場合、AVRO_TYPE は文字列になります。                                               |

Avro プロトコルでは、他の 2 つの`sink-uri`パラメータ ( `avro-decimal-handling-mode`と`avro-bigint-unsigned-handling-mode`もカラムデータ形式に影響する可能性があります。

-   `avro-decimal-handling-mode` 、Avro が 10 進数フィールドを処理する方法を制御します。これには以下が含まれます。

    -   文字列: Avro は小数フィールドを文字列として処理します。
    -   precise: Avro は 10 進数フィールドをバイトとして処理します。

-   `avro-bigint-unsigned-handling-mode` Avro が BIGINT UNSIGNED フィールドを処理する方法を制御します。これには以下が含まれます。

    -   文字列: Avro は BIGINT UNSIGNED フィールドを文字列として処理します。
    -   long: Avro は BIGINT UNSIGNED フィールドを 64 ビットの符号付き整数として処理します。値が`9223372036854775807`より大きい場合、オーバーフローが発生します。

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

ほとんどの SQL タイプは、基本のカラムデータ形式にマップされます。その他の一部の SQL タイプは、基本データ形式を拡張して、より多くの情報を提供します。

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

列挙/セット(a,b,c)

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

## DDL イベントとスキーマの変更 {#ddl-events-and-schema-changes}

Avro は、DDL イベントとウォーターマーク イベントを下流に送信しません。DML イベントが発生するたびに、スキーマが変更されたかどうかを確認します。スキーマが変更されると、Avro は新しいスキーマを生成し、それをスキーマ レジストリに登録します。スキーマの変更が互換性チェックに合格しない場合、登録は失敗します。TiCDC は、スキーマの互換性の問題を解決しません。

たとえば、Confluent Schema Registry のデフォルトの[互換性ポリシー](https://docs.confluent.io/platform/current/schema-registry/fundamentals/schema-evolution.html#compatibility-types) `BACKWARD`で、ソース テーブルに空でない列を追加します。この状況では、Avro は新しいスキーマを生成しますが、互換性の問題により Schema Registry への登録に失敗します。この時点で、changefeed はエラー状態になります。

スキーマの変更が互換性チェックに合格し、新しいバージョンが登録された場合でも、データ プロデューサーとコンシューマーはデータのエンコードとデコードのために新しいスキーマを取得する必要があることに注意してください。

スキーマの詳細については、 [スキーマレジストリ関連ドキュメント](https://docs.confluent.io/platform/current/schema-registry/avro.html)を参照してください。

## 消費者実装 {#consumer-implementation}

TiCDC Avro プロトコルは[`io.confluent.kafka.serializers.KafkaAvroDeserializer`](https://docs.confluent.io/platform/current/schema-registry/fundamentals/serdes-develop/serdes-avro.html#avro-deserializer)で逆シリアル化できます。

コンシューマー プログラムは[スキーマレジストリ API](https://docs.confluent.io/platform/current/schema-registry/develop/api.html)を介して最新のスキーマを取得し、そのスキーマを使用して TiCDC Avro プロトコルによってエンコードされたデータを逆シリアル化できます。

### イベントの種類を区別する {#distinguish-event-types}

コンシューマー プログラムは、次のルールによって DML イベント タイプを区別できます。

-   Key部分のみの場合はDeleteイベントとなります。
-   キー部分と値部分の両方がある場合は、挿入イベントまたは更新イベントのいずれかです。 [TiDB拡張フィールド](#tidb-extension-fields)が有効になっている場合は、 `_tidb_op`フィールドを使用して、挿入イベントか更新イベントかを識別できます。 TiDB 拡張フィールドが有効になっていない場合、それらを区別することはできません。

## トピックの分布 {#topic-distribution}

スキーマ レジストリは、TopicNameStrategy、RecordNameStrategy、TopicRecordNameStrategy の[件名戦略](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#subject-name-strategy)つをサポートしています。現在、TiCDC Avro は TopicNameStrategy のみをサポートしています。つまり、Kafka トピックは 1 つのデータ形式でのみデータを受信できます。したがって、TiCDC Avro では、複数のテーブルを同じトピックにマッピングすることは禁止されています。変更フィードを作成すると、トピック ルールに、構成された配布ルールの`{schema}`および`{table}`プレースホルダーが含まれていない場合、エラーが報告されます。

## 互換性 {#compatibility}

TiCDC クラスターを v7.0.0 にアップグレードする際、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合は、アップグレード前に Confluent Schema Registry の互換性ポリシーを手動で`None`に調整して、changefeed がスキーマを正常に更新できるようにする必要があります。そうしないと、アップグレード後に changefeed がスキーマを更新できず、エラー状態になります。詳細については、 [＃8490](https://github.com/pingcap/tiflow/issues/8490)参照してください。
