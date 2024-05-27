---
title: TiCDC Avro Protocol
summary: TiCDC Avro プロトコルの概念とその使用方法を学びます。
---

# TiCDC Avro プロトコル {#ticdc-avro-protocol}

Avro は、 [アパッチアブロ™](https://avro.apache.org/)で定義され、 [合流プラットフォーム](https://docs.confluent.io/platform/current/platform.html)によってデフォルトのデータ交換形式として選択されたデータ交換形式プロトコルです。このドキュメントでは、TiDB 拡張フィールド、Avro データ形式の定義、および Avro と[Confluent スキーマ レジストリ](https://docs.confluent.io/platform/current/schema-registry/index.html)間の相互作用を含む、TiCDC での Avro データ形式の実装について説明します。

> **警告：**
>
> v7.3.0 以降では、TiCDC を[有効なインデックスのないテーブルを複製する](/ticdc/ticdc-manage-changefeed.md#replicate-tables-without-a-valid-index)に有効にすると、Avro プロトコルを使用する変更フィードを作成するときに TiCDC によってエラーが報告されます。

## Avroを使用する {#use-avro}

メッセージ キュー (MQ) をダウンストリーム シンクとして使用する場合、 `sink-uri`で Avro を指定できます。TiCDC は TiDB DML イベントをキャプチャし、これらのイベントから Avro メッセージを作成し、メッセージをダウンストリームに送信します。Avro はスキーマの変更を検出すると、最新のスキーマをスキーマ レジストリに登録します。

以下は Avro を使用した構成例です。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

値`--schema-registry`は、 `https`プロトコルと`username:password`認証をサポートします (例: `--schema-registry=https://username:password@schema-registry-uri.com` 。ユーザー名とパスワードは URL エンコードされている必要があります。

## TiDB拡張フィールド {#tidb-extension-fields}

デフォルトでは、Avro は DML イベントで変更された行のデータのみを収集し、データ変更の種類や TiDB 固有の CommitTS (トランザクションの一意の識別子) は収集しません。この問題に対処するために、TiCDC は Avro プロトコル メッセージに次の 3 つの TiDB 拡張フィールドを導入します。7 で`enable-tidb-extension`が`true` ( `sink-uri`では`false` ) に設定されている場合、TiCDC はメッセージ生成中にこれらの 3 つのフィールドを Avro メッセージに追加します。

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

デフォルトでは、値のデータ形式はキーのデータ形式と同じです。ただし、値の`fields`には主キー列だけでなく、すべての列が含まれます。

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
-   `{{AVRO_TYPE}}` [アブロスペック](https://avro.apache.org/docs/current/spec.html)の型を示します。

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
| 浮く       | 浮く       | ダブル      | <li></li>                                                                                             |
| ダブル      | ダブル      | ダブル      | <li></li>                                                                                             |
| 日付       | 日付       | 弦        | <li></li>                                                                                             |
| 日付時刻     | 日付時刻     | 弦        | <li></li>                                                                                             |
| タイムスタンプ  | タイムスタンプ  | 弦        | <li></li>                                                                                             |
| 時間       | 時間       | 弦        | <li></li>                                                                                             |
| 年        | 年        | 整数       | <li></li>                                                                                             |
| 少し       | 少し       | バイト      | <li></li>                                                                                             |
| 翻訳       | 翻訳       | 弦        | <li></li>                                                                                             |
| 列挙       | 列挙       | 弦        | <li></li>                                                                                             |
| セット      | セット      | 弦        | <li></li>                                                                                             |
| 小数点      | 小数点      | バイト      | `avro-decimal-handling-mode`文字列の場合、AVRO_TYPE は文字列になります。                                               |

Avro プロトコルでは、他の 2 つの`sink-uri`パラメータ`avro-decimal-handling-mode`と`avro-bigint-unsigned-handling-mode`もカラムデータ形式に影響する可能性があります。

-   `avro-decimal-handling-mode` 、Avro が 10 進数フィールドを処理する方法を制御します。これには以下が含まれます。

    -   文字列: Avro は小数フィールドを文字列として処理します。
    -   precise: Avro は 10 進数フィールドをバイトとして処理します。

-   `avro-bigint-unsigned-handling-mode` 、Avro が BIGINT UNSIGNED フィールドを処理する方法を制御します。これには以下が含まれます。

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

Avro は下流で DDL イベントを生成しません。DML イベントが発生するたびに、スキーマが変更されているかどうかを確認します。スキーマが変更されると、Avro は新しいスキーマを生成し、それをスキーマ レジストリに登録します。スキーマの変更が互換性チェックに合格しない場合、登録は失敗します。TiCDC はスキーマの互換性の問題を解決しません。

スキーマの変更が互換性チェックに合格し、新しいバージョンが登録された場合でも、システムが正常に実行されるようにするには、データ プロデューサーとコンシューマーがアップグレードを実行する必要があることに注意してください。

Confluent Schema Registry のデフォルトの互換性ポリシーが`BACKWARD`であると仮定し、ソース テーブルに空でない列を追加します。この状況では、Avro は新しいスキーマを生成しますが、互換性の問題により Schema Registry への登録に失敗します。この時点で、changefeed はエラー状態になります。

スキーマの詳細については、 [スキーマレジストリ関連ドキュメント](https://docs.confluent.io/platform/current/schema-registry/avro.html)を参照してください。

## トピックの分布 {#topic-distribution}

スキーマ レジストリは、TopicNameStrategy、RecordNameStrategy、TopicRecordNameStrategy の 3 [件名戦略](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#subject-name-strategy)をサポートしています。現在、TiCDC Avro は TopicNameStrategy のみをサポートしています。つまり、Kafka トピックは 1 つのデータ形式でのみデータを受信できます。したがって、TiCDC Avro では、複数のテーブルを同じトピックにマッピングすることは禁止されています。変更フィードを作成すると、トピック ルールに、構成された配布ルールの`{schema}`および`{table}`プレースホルダーが含まれていない場合、エラーが報告されます。

## 互換性 {#compatibility}

TiCDC クラスターを v7.0.0 にアップグレードする際、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合は、アップグレード前に Confluent Schema Registry の互換性ポリシーを手動で`None`に調整して、changefeed がスキーマを正常に更新できるようにする必要があります。そうしないと、アップグレード後に changefeed がスキーマを更新できず、エラー状態になります。詳細については、 [＃8490](https://github.com/pingcap/tiflow/issues/8490)を参照してください。
