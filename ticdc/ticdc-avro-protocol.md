---
title: TiCDC Avro Protocol
summary: Learn the concept of TiCDC Avro Protocol and how to use it.
---

# TiCDC Avro プロトコル {#ticdc-avro-protocol}

Avro は、 [アパッチ アブロ™](https://avro.apache.org/)によって定義され、デフォルトのデータ交換フォーマットとして[コンフルエントなプラットフォーム](https://docs.confluent.io/platform/current/platform.html)によって選択されたデータ交換フォーマット プロトコルです。このドキュメントでは、TiDB 拡張フィールド、Avro データ形式の定義、および Avro と[コンフルエント スキーマ レジストリ](https://docs.confluent.io/platform/current/schema-registry/index.html)の間の相互作用を含む、TiCDC での Avro データ形式の実装について説明します。

## アブロを使用 {#use-avro}

Message Queue (MQ) をダウンストリーム シンクとして使用する場合、 Avro を`sink-uri`で指定できます。 TiCDC は TiDB DML イベントをキャプチャし、これらのイベントから Avro メッセージを作成して、メッセージをダウンストリームに送信します。 Avro は、スキーマの変更を検出すると、最新のスキーマをスキーマ レジストリに登録します。

以下は、Avro を使用した構成例です。

{{< copyable "" >}}

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

値`--schema-registry`は`https`プロトコルと`username:password`認証をサポートします (例: `--schema-registry=https://username:password@schema-registry-uri.com` )。ユーザー名とパスワードは URL エンコードする必要があります。

## TiDB 拡張フィールド {#tidb-extension-fields}

デフォルトでは、Avro は DML イベントで変更された行のデータのみを収集し、データ変更のタイプや TiDB 固有の CommitTS (トランザクションの一意の識別子) は収集しません。この問題に対処するために、TiCDC は次の 3 つの TiDB 拡張フィールドを Avro プロトコル メッセージに導入します。 `sink-uri`で`enable-tidb-extension`が`true` (デフォルトでは`false` ) に設定されている場合、TiCDC はメッセージ生成中にこれら 3 つのフィールドを Avro メッセージに追加します。

-   `_tidb_op` : DML タイプ。 「c」は挿入を示し、「u」は更新を示します。
-   `_tidb_commit_ts` : トランザクションの一意の識別子。
-   `_tidb_commit_physical_time` : トランザクション ID の物理タイムスタンプ。

次に設定例を示します。

{{< copyable "" >}}

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

### 鍵データ形式 {#key-data-format}

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

-   `{{TableName}}`イベントが発生したテーブルの名前を示します。
-   `{{Namespace}}`は Avro の名前空間です。
-   `{{ColumnValueBlock}}`データの各列の形式を定義します。

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

デフォルトでは、Value のデータ形式は Key と同じです。ただし、値の`fields`には、主キー列だけでなく、すべての列が含まれます。

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

`enable-tidb-extension`が無効になっている値のデータ形式と比較すると、3 つの新しいフィールドが追加されています: `_tidb_op` 、 `_tidb_commit_ts` 、および`_tidb_commit_physical_time` 。

### カラムデータ形式 {#column-data-format}

カラムデータは、キー/値データ形式の`{{ColumnValueBlock}}`の部分です。 TiCDC は、SQL タイプに基づいてカラムデータ形式を生成します。基本的なカラムデータ形式は次のとおりです。

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

1 つの列が NULL になる可能性がある場合、カラムのデータ形式は次のようになります。

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

-   `{{ColumnName}}`列名を示します。
-   `{{TIDB_TYPE}}` TiDB の型を示します。これは、SQL 型との 1 対 1 のマッピングではありません。
-   `{{AVRO_TYPE}}` [アブロスペック](https://avro.apache.org/docs/current/spec.html)のタイプを示します。

| SQL タイプ   | TIDB_TYPE | AVRO_TYPE | 説明                                                                                                       |
| --------- | --------- | --------- | -------------------------------------------------------------------------------------------------------- |
| ブール       | INT       | 整数        |                                                                                                          |
| TINYINT   | INT       | 整数        | unsigned の場合、TIDB_TYPE は INT UNSIGNED です。                                                                |
| SMALLINT  | INT       | 整数        | unsigned の場合、TIDB_TYPE は INT UNSIGNED です。                                                                |
| ミディアムミント  | INT       | 整数        | unsigned の場合、TIDB_TYPE は INT UNSIGNED です。                                                                |
| INT       | INT       | 整数        | unsigned の場合、TIDB_TYPE は INT UNSIGNED で、AVRO_TYPE は long です。                                             |
| BIGINT    | BIGINT    | 長さ        | 署名されていない場合、TIDB_TYPE は BIGINT UNSIGNED です。 `avro-bigint-unsigned-handling-mode`が文字列の場合、AVRO_TYPE は文字列です。 |
| 小さな塊      | BLOB      | バイト       | <li></li>                                                                                                |
| BLOB      | BLOB      | バイト       | <li></li>                                                                                                |
| ミディアムブロブ  | BLOB      | バイト       | <li></li>                                                                                                |
| ロングブロブ    | BLOB      | バイト       | <li></li>                                                                                                |
| バイナリ      | BLOB      | バイト       | <li></li>                                                                                                |
| VARBINARY | BLOB      | バイト       | <li></li>                                                                                                |
| 小さなテキスト   | TEXT      | 弦         | <li></li>                                                                                                |
| TEXT      | TEXT      | 弦         | <li></li>                                                                                                |
| 中文        | TEXT      | 弦         | <li></li>                                                                                                |
| ロングテキスト   | TEXT      | 弦         | <li></li>                                                                                                |
| CHAR      | TEXT      | 弦         | <li></li>                                                                                                |
| VARCHAR   | TEXT      | 弦         | <li></li>                                                                                                |
| 浮く        | 浮く        | ダブル       | <li></li>                                                                                                |
| ダブル       | ダブル       | ダブル       | <li></li>                                                                                                |
| 日にち       | 日にち       | 弦         | <li></li>                                                                                                |
| 日付時刻      | 日付時刻      | 弦         | <li></li>                                                                                                |
| タイムスタンプ   | タイムスタンプ   | 弦         | <li></li>                                                                                                |
| 時間        | 時間        | 弦         | <li></li>                                                                                                |
| 年         | 年         | 整数        | <li></li>                                                                                                |
| 少し        | 少し        | バイト       | <li></li>                                                                                                |
| JSON      | JSON      | 弦         | <li></li>                                                                                                |
| 列挙型       | 列挙型       | 弦         | <li></li>                                                                                                |
| 設定        | 設定        | 弦         | <li></li>                                                                                                |
| 小数        | 小数        | バイト       | `avro-decimal-handling-mode`が文字列の場合、AVRO_TYPE は文字列です。                                                    |

Avro プロトコルでは、他の 2 つの`sink-uri`パラメーター ( `avro-decimal-handling-mode`および`avro-bigint-unsigned-handling-mode`もカラムデータ形式に影響を与える可能性があります。

-   `avro-decimal-handling-mode` 、Avro が以下を含む小数フィールドを処理する方法を制御します。

    -   string: Avro は 10 進数フィールドを文字列として処理します。
    -   正確: Avro は 10 進数フィールドをバイトとして処理します。

-   `avro-bigint-unsigned-handling-mode`次のような BIGINT UNSIGNED フィールドを Avro が処理する方法を制御します。

    -   string: Avro は BIGINT UNSIGNED フィールドを文字列として処理します。
    -   long: Avro は BIGINT UNSIGNED フィールドを 64 ビット符号付き整数として処理します。値が`9223372036854775807`より大きい場合、オーバーフローが発生します。

次に設定例を示します。

{{< copyable "" >}}

```shell
cdc cli changefeed create --server=http://127.0.0.1:8300 --changefeed-id="kafka-avro-string-option" --sink-uri="kafka://127.0.0.1:9092/topic-name?protocol=avro&avro-decimal-handling-mode=string&avro-bigint-unsigned-handling-mode=string" --schema-registry=http://127.0.0.1:8081 --config changefeed_config.toml
```

```shell
[sink]
dispatchers = [
 {matcher = ['*.*'], topic = "tidb_{schema}_{table}"},
]
```

ほとんどの SQL タイプは、基本カラムデータ形式にマップされます。他の一部の SQL タイプは、基本データ形式を拡張して、より多くの情報を提供します。

ビット(64)

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

ENUM/SET(a,b,c)

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

DECIMAL(10, 4)

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

## DDL イベントとスキーマの変更 {#ddl-events-and-schema-changes}

Avro はダウンストリームの DDL イベントを生成しません。 DML イベントが発生するたびにスキーマが変更されているかどうかを確認します。スキーマが変更されると、Avro は新しいスキーマを生成し、スキーマ レジストリに登録します。スキーマの変更が互換性チェックに合格しない場合、登録は失敗します。 TiCDC は、スキーマの互換性の問題を解決しません。

スキーマの変更が互換性チェックに合格し、新しいバージョンが登録された場合でも、データのプロデューサーとコンシューマーは、システムを正常に実行するためにアップグレードを実行する必要があることに注意してください。

Confluent Schema Registry のデフォルトの互換性ポリシーが`BACKWARD`であると仮定し、ソース テーブルに空でない列を追加します。この状況では、Avro は新しいスキーマを生成しますが、互換性の問題によりスキーマ レジストリへの登録に失敗します。このとき、changefeed はエラー状態になります。

スキーマの詳細については、 [スキーマ レジストリ関連ドキュメント](https://docs.confluent.io/platform/current/schema-registry/avro.html)を参照してください。

## トピックの配布 {#topic-distribution}

スキーマ レジストリは、TopicNameStrategy、RecordNameStrategy、および TopicRecordNameStrategy の 3 つ[サブジェクト名戦略](https://docs.confluent.io/platform/current/schema-registry/serdes-develop/index.html#subject-name-strategy)をサポートします。現在、TiCDC Avro は TopicNameStrategy のみをサポートしています。つまり、Kafka トピックは 1 つのデータ形式でしかデータを受信できません。したがって、TiCDC Avro では、複数のテーブルを同じトピックにマッピングすることを禁止しています。変更フィードを作成するときに、構成された配布ルールにトピック ルールに`{schema}`と`{table}`プレースホルダーが含まれていない場合、エラーが報告されます。

## 互換性 {#compatibility}

TiCDC クラスターを v6.5.2 以降の v6.5.x バージョンにアップグレードするときに、Avro を使用してレプリケートされたテーブルに`FLOAT`データ型が含まれている場合、アップグレードする前に Confluent Schema Registry の互換性ポリシーを手動で`None`に調整する必要があります。 changefeed はスキーマを正常に更新できます。そうしないと、アップグレード後に変更フィードがスキーマを更新できず、エラー状態になります。詳細については、 [#8490](https://github.com/pingcap/tiflow/issues/8490)を参照してください。
