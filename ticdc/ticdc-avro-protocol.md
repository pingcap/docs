---
title: TiCDC Avro Protocol
summary: Learn the concept of TiCDC Avro Protocol and how to use it.
---

# TiCDC Avro プロトコル {#ticdc-avro-protocol}

Avro は、 [Apache Avro™](https://avro.apache.org/)によって定義され、 [コンフルエントなプラットフォーム](https://docs.confluent.io/platform/current/platform.html)によってデフォルトのデータ交換形式として選択されるデータ交換形式プロトコルです。このドキュメントでは、TiDB 拡張フィールド、Avro データ形式の定義、Avro と[Confluent スキーマ レジストリ](https://docs.confluent.io/platform/current/schema-registry/index.html)の間の対話など、TiCDC での Avro データ形式の実装について説明します。

> **警告：**
>
> v7.3.0 以降、TiCDC を[有効なインデックスのないテーブルを複製する](/ticdc/ticdc-manage-changefeed.md#replicate-tables-without-a-valid-index)に有効にすると、Avro プロトコルを使用する変更フィードを作成するときに TiCDC はエラーを報告します。

## アブロを使用する {#use-avro}

Message Queue (MQ) をダウンストリーム シンクとして使用する場合、 `sink-uri`で Avro を指定できます。 TiCDC は、TiDB DML イベントをキャプチャし、これらのイベントから Avro メッセージを作成し、メッセージをダウンストリームに送信します。 Avro はスキーマの変更を検出すると、最新のスキーマをスキーマ レジストリに登録します。

以下は、Avro を使用した構成例です。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

値`--schema-registry`は、 `https`プロトコルと`username:password`認証をサポートします (例: `--schema-registry=https://username:password@schema-registry-uri.com` )。ユーザー名とパスワードは URL エンコードする必要があります。

## TiDB 拡張フィールド {#tidb-extension-fields}

デフォルトでは、Avro は DML イベント内の変更された行のデータのみを収集し、データ変更のタイプや TiDB 固有の CommitTS (トランザクションの一意の識別子) は収集しません。この問題に対処するために、TiCDC は、Avro プロトコル メッセージに次の 3 つの TiDB 拡張フィールドを導入しました。 `sink-uri`で`enable-tidb-extension`が`true` (デフォルトでは`false` ) に設定されている場合、TiCDC はメッセージ生成中にこれらの 3 つのフィールドを Avro メッセージに追加します。

-   `_tidb_op` : DML タイプ。 「c」は挿入を示し、「u」は更新を示します。
-   `_tidb_commit_ts` : トランザクションの一意の識別子。
-   `_tidb_commit_physical_time` : トランザクション識別子の物理タイムスタンプ。

以下に設定例を示します。

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

デフォルトでは、Value のデータ形式は Key のデータ形式と同じです。ただし、値の`fields`には主キー列だけでなくすべての列が含まれます。

[`enable-tidb-extension`](#tidb-extension-fields)を有効にすると、値のデータ形式は次のようになります。

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

`enable-tidb-extension`を無効にした値のデータ形式と比較すると、 `_tidb_op` 、 `_tidb_commit_ts` 、および`_tidb_commit_physical_time`の 3 つの新しいフィールドが追加されています。

### カラムのデータ形式 {#column-data-format}

カラムデータは、キー/値データ形式の`{{ColumnValueBlock}}`です。 TiCDC は、SQL タイプに基づいてカラムデータ形式を生成します。基本的なカラムデータ形式は次のとおりです。

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
-   `{{TIDB_TYPE}}` TiDB のタイプを示します。これは SQL タイプと 1 対 1 のマッピングではありません。
-   `{{AVRO_TYPE}}` [アブロ仕様](https://avro.apache.org/docs/current/spec.html)のタイプを示します。

| SQLの種類   | TIDB_TYPE | AVRO_TYPE | 説明                                                                                                          |
| -------- | --------- | --------- | ----------------------------------------------------------------------------------------------------------- |
| ブール      | INT       | 整数        |                                                                                                             |
| タイイント    | INT       | 整数        | 署名されていない場合、TIDB_TYPE は INT UNSIGNED になります。                                                                  |
| スモールント   | INT       | 整数        | 署名されていない場合、TIDB_TYPE は INT UNSIGNED になります。                                                                  |
| ミディアムミント | INT       | 整数        | 署名されていない場合、TIDB_TYPE は INT UNSIGNED になります。                                                                  |
| INT      | INT       | 整数        | 署名されていない場合、TIDB_TYPE は INT UNSIGNED で、AVRO_TYPE はlongになります。                                                 |
| BIGINT   | BIGINT    | 長さ        | 署名されていない場合、TIDB_TYPE は BIGINT UNSIGNED になります。 `avro-bigint-unsigned-handling-mode`が文字列の場合、AVRO_TYPE は文字列です。 |
| タイニーブロブ  | BLOB      | バイト       | <li></li>                                                                                                   |
| BLOB     | BLOB      | バイト       | <li></li>                                                                                                   |
| ミディアムブロブ | BLOB      | バイト       | <li></li>                                                                                                   |
| ロングブロブ   | BLOB      | バイト       | <li></li>                                                                                                   |
| バイナリ     | BLOB      | バイト       | <li></li>                                                                                                   |
| ヴァービナリー  | BLOB      | バイト       | <li></li>                                                                                                   |
| 小さなテキスト  | TEXT      | 弦         | <li></li>                                                                                                   |
| TEXT     | TEXT      | 弦         | <li></li>                                                                                                   |
| メディアテキスト | TEXT      | 弦         | <li></li>                                                                                                   |
| 長文       | TEXT      | 弦         | <li></li>                                                                                                   |
| チャー      | TEXT      | 弦         | <li></li>                                                                                                   |
| VARCHAR  | TEXT      | 弦         | <li></li>                                                                                                   |
| 浮く       | 浮く        | ダブル       | <li></li>                                                                                                   |
| ダブル      | ダブル       | ダブル       | <li></li>                                                                                                   |
| 日付       | 日付        | 弦         | <li></li>                                                                                                   |
| 日付時刻     | 日付時刻      | 弦         | <li></li>                                                                                                   |
| タイムスタンプ  | タイムスタンプ   | 弦         | <li></li>                                                                                                   |
| 時間       | 時間        | 弦         | <li></li>                                                                                                   |
| 年        | 年         | 整数        | <li></li>                                                                                                   |
| 少し       | 少し        | バイト       | <li></li>                                                                                                   |
| JSON     | JSON      | 弦         | <li></li>                                                                                                   |
| ENUM     | ENUM      | 弦         | <li></li>                                                                                                   |
| セット      | セット       | 弦         | <li></li>                                                                                                   |
| 10進数     | 10進数      | バイト       | `avro-decimal-handling-mode`が文字列の場合、AVRO_TYPE は文字列です。                                                       |

Avro プロトコルでは、他の 2 つの`sink-uri`パラメーター ( `avro-decimal-handling-mode`と`avro-bigint-unsigned-handling-mode`もカラムデータ形式に影響を与える可能性があります。

-   `avro-decimal-handling-mode` 、Avro が次のような 10 進フィールドを処理する方法を制御します。

    -   string: Avro は 10 進フィールドを文字列として処理します。
    -   正確: Avro は 10 進フィールドをバイトとして処理します。

-   `avro-bigint-unsigned-handling-mode` 、Avro が次のような BIGINT UNSIGNED フィールドを処理する方法を制御します。

    -   string: Avro は、BIGINT UNSIGNED フィールドを文字列として処理します。
    -   long: Avro は、BIGINT UNSIGNED フィールドを 64 ビットの符号付き整数として処理します。値が`9223372036854775807`より大きい場合、オーバーフローが発生します。

以下に設定例を示します。

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro-string-option" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro&avro-decimal-handling-mode=string&avro-bigint-unsigned-handling-mode=string" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

ほとんどの SQL タイプは、基本のカラムデータ形式にマップされます。他の一部の SQL タイプは、基本データ形式を拡張して、より多くの情報を提供します。

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

ENUM/SET(a,b,c)

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

DECIMAL(10, 4)

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

Avro はダウンストリームで DDL イベントを生成しません。 DML イベントが発生するたびにスキーマが変更されるかどうかをチェックします。スキーマが変更された場合、Avro は新しいスキーマを生成し、スキーマ レジストリに登録します。スキーマの変更が互換性チェックに合格しない場合、登録は失敗します。 TiCDC はスキーマの互換性の問題を解決しません。

スキーマの変更が互換性チェックに合格し、新しいバージョンが登録された場合でも、データのプロデューサーとコンシューマーは、システムが正常に動作するようにアップグレードを実行する必要があることに注意してください。

Confluent Schema Registry のデフォルトの互換性ポリシーが`BACKWARD`であると仮定し、空でない列をソース テーブルに追加します。この状況では、Avro は新しいスキーマを生成しますが、互換性の問題によりスキーマ レジストリへの登録に失敗します。このとき、チェンジフィードはエラー状態になります。

スキーマの詳細については、 [スキーマレジストリ関連ドキュメント](https://docs.confluent.io/platform/current/schema-registry/avro.html)を参照してください。

## トピック配信 {#topic-distribution}

スキーマ レジストリは、TopicNameStrategy、RecordNameStrategy、および TopicRecordNameStrategy の 3 つの[件名名戦略](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#subject-name-strategy)をサポートします。現在、TiCDC Avro は TopicNameStrategy のみをサポートしています。これは、Kafka トピックが 1 つのデータ形式でのみデータを受信できることを意味します。したがって、TiCDC Avro では、複数のテーブルを同じトピックにマッピングすることを禁止しています。変更フィードを作成するとき、トピック ルールに設定された配布ルールに`{schema}`と`{table}`プレースホルダーが含まれていない場合、エラーが報告されます。

## 互換性 {#compatibility}

TiCDC クラスターを v7.0.0 にアップグレードするときに、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合、変更フィードがスキーマを正常に更新できるように、アップグレードする前に Confluent Schema Registry の互換性ポリシーを手動で`None`に調整する必要があります。そうしないと、アップグレード後に変更フィードがスキーマを更新できなくなり、エラー状態になります。詳細については、 [#8490](https://github.com/pingcap/tiflow/issues/8490)を参照してください。
