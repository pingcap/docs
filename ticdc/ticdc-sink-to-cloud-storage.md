---
title: Replicate Data to Storage Services
summary: Learn how to replicate data to storage services using TiCDC, and learn about the storage path of the replicated data.
---

# ストレージ サービスへのデータのレプリケーション {#replicate-data-to-storage-services}

TiDB v6.5.0 以降、TiCDC は、Amazon S3、GCS、Azure Blob Storage、NFS などのstorageサービスへの行変更イベントの保存をサポートします。このドキュメントでは、TiCDC を使用して増分データをそのようなstorageサービスにレプリケートする変更フィードを作成する方法と、データがどのように保存されるかについて説明します。この文書の構成は次のとおりです。

-   [データをstorageサービスにレプリケートする方法](#replicate-change-data-to-storage-services) 。
-   [データがstorageサービスに保存される仕組み](#storage-path-structure) 。

## 変更データをstorageサービスにレプリケートする {#replicate-change-data-to-storage-services}

次のコマンドを実行して、変更フィード タスクを作成します。

```shell
cdc cli changefeed create \
    --server=http://10.0.10.25:8300 \
    --sink-uri="s3://logbucket/storage_test?protocol=canal-json" \
    --changefeed-id="simple-replication-task"
```

出力は次のとおりです。

```shell
Info: {"upstream_id":7171388873935111376,"namespace":"default","id":"simple-replication-task","sink_uri":"s3://logbucket/storage_test?protocol=canal-json","create_time":"2022-11-29T18:52:05.566016967+08:00","start_ts":437706850431664129,"engine":"unified","config":{"case_sensitive":true,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":false,"sync_point_interval":600000000000,"sync_point_retention":86400000000000,"filter":{"rules":["*.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"canal-json","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v6.5.0-master-dirty"}
```

-   `--server` : TiCDC クラスター内の任意の TiCDCサーバーのアドレス。
-   `--changefeed-id` : チェンジフィードの ID。形式は`^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`正規表現と一致する必要があります。この ID が指定されていない場合、TiCDC は UUID (バージョン 4 形式) を ID として自動的に生成します。
-   `--sink-uri` : チェンジフィードの下流アドレス。詳細は[シンク URI を構成する](#configure-sink-uri)を参照してください。
-   `--start-ts` : チェンジフィードの開始 TSO。 TiCDC は、この TSO からのデータの取得を開始します。デフォルト値は現在時刻です。
-   `--target-ts` : チェンジフィードの終了 TSO。 TiCDC は、この TSO が発生するまでデータのプルを停止します。デフォルト値は空です。これは、TiCDC がデータのプルを自動的に停止しないことを意味します。
-   `--config` : チェンジフィードの設定ファイル。詳細は[TiCDC チェンジフィード構成パラメータ](/ticdc/ticdc-changefeed-config.md)を参照してください。

## シンク URI を構成する {#configure-sink-uri}

このセクションでは、Amazon S3、GCS、Azure Blob Storage、NFS などのstorageサービスのシンク URI を構成する方法について説明します。シンク URI は、TiCDC ターゲット システムの接続情報を指定するために使用されます。形式は次のとおりです。

```shell
[scheme]://[host]/[path]?[query_parameters]
```

URI の`[query_parameters]`については、次のパラメータを設定できます。

| パラメータ                   | 説明                                                                                                                                                                                                                                   | デフォルト値     | 値の範囲                   |
| :---------------------- | :----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | :--------- | :--------------------- |
| `worker-count`          | データ変更をダウンストリームのクラウドstorageに保存するための同時実行。                                                                                                                                                                                              | `16`       | `[1, 512]`             |
| `flush-interval`        | データの変更をダウンストリームのクラウドstorageに保存する間隔。                                                                                                                                                                                                  | `5s`       | `[2s, 10m]`            |
| `file-size`             | バイト数がこのパラメータの値を超える場合、データ変更ファイルはクラウドstorageに保存されます。                                                                                                                                                                                   | `67108864` | `[1048576, 536870912]` |
| `protocol`              | ダウンストリームに送信されるメッセージのプロトコル形式。                                                                                                                                                                                                         | 該当なし       | `canal-json`と`csv`     |
| `enable-tidb-extension` | `protocol`が`canal-json`に設定され、 `enable-tidb-extension` `true`に設定されている場合、TiCDC は[ウォーターマークイベント](/ticdc/ticdc-canal-json.md#watermark-event)送信し、 [TiDB 拡張フィールド](/ticdc/ticdc-canal-json.md#tidb-extension-field) Canal-JSON メッセージに追加します。 | `false`    | `false`と`true`         |

> **注記：**
>
> `flush-interval`または`file-size`いずれかが要件を満たす場合、データ変更ファイルはダウンストリームに保存されます。 `protocol`パラメータは必須です。変更フィードの作成時に TiCDC がこのパラメーターを受け取らない場合、 `CDC:ErrSinkUnknownProtocol`エラーが返されます。

### 外部storageのシンク URI を構成する {#configure-sink-uri-for-external-storage}

以下は、Amazon S3 の設定例です。

```shell
--sink-uri="s3://bucket/prefix?protocol=canal-json"
```

以下は GCS の構成例です。

```shell
--sink-uri="gcs://bucket/prefix?protocol=canal-json"
```

以下は、Azure Blob Storage の構成例です。

```shell
--sink-uri="azure://bucket/prefix?protocol=canal-json"
```

> **ヒント：**
>
> TiCDC の Amazon S3、GCS、および Azure Blob Storage の URI パラメーターは、 BRの URI パラメーターと同じです。詳細は[バックアップstorageのURI形式](/br/backup-and-restore-storages.md#uri-format-description)を参照してください。

### NFS のシンク URI を構成する {#configure-sink-uri-for-nfs}

次に、NFS の構成例を示します。

```shell
--sink-uri="file:///my-directory/prefix?protocol=canal-json"
```

## ストレージパス構造 {#storage-path-structure}

このセクションでは、データ変更レコード、メタデータ、および DDL イベントのstorageパス構造について説明します。

### データ変更記録 {#data-change-records}

データ変更レコードは次のパスに保存されます。

```shell
{scheme}://{prefix}/{schema}/{table}/{table-version-separator}/{partition-separator}/{date-separator}/CDC{num}.{extension}
```

-   `scheme` :storageタイプを指定します (たとえば、 `s3` 、 `gcs` 、 `azure` 、または`file` 。
-   `prefix` : ユーザー定義の親ディレクトリを指定します (例: `s3:// **bucket/bbb/ccc**` )。
-   `schema` : スキーマ名を指定します (例: `s3://bucket/bbb/ccc/ **test**` 。
-   `table` : テーブル名を指定します (例: `s3://bucket/bbb/ccc/test/ **table1**` 。
-   `table-version-separator` : テーブルのバージョンごとにパスを区切る区切り文字を指定します (例`s3://bucket/bbb/ccc/test/table1/ **9999**` )。
-   `partition-separator` : テーブル パーティションごとにパスを区切る区切り文字を指定します (例`s3://bucket/bbb/ccc/test/table1/9999/ **20**` 。
-   `date-separator` : トランザクションのコミット日によってファイルを分類します。デフォルト値は`day`です。値のオプションは次のとおりです。
    -   `none` : いいえ`date-separator` 。たとえば、バージョン`test.table1`が`9999`であるすべてのファイルは`s3://bucket/bbb/ccc/test/table1/9999`に保存されます。
    -   `year` : 区切り文字はトランザクションのコミット日の年です (例`s3://bucket/bbb/ccc/test/table1/9999/ **2022**` 。
    -   `month` : 区切り文字はトランザクションのコミット日の年と月です (例`s3://bucket/bbb/ccc/test/table1/9999/ **2022-01**` 。
    -   `day` : 区切り文字はトランザクションコミット日の年、月、日です (例: `s3://bucket/bbb/ccc/test/table1/9999/ **2022-01-02**` 。
-   `num` : データ変更を記録するファイルのシリアル番号を保存します (例`s3://bucket/bbb/ccc/test/table1/9999/2022-01-02/CDC **000005** .csv` 。
-   `extension` : ファイルの拡張子を指定します。 TiDB v6.5.0 は、CSV および Canal-JSON 形式をサポートしています。

> **注記：**
>
> テーブル バージョンは、アップストリーム テーブルで DDL 操作が実行された後にのみ変更され、アップストリーム TiDB が DDL の実行を完了すると、新しいテーブル バージョンが TSO になります。ただし、テーブルのバージョンの変更はテーブルのスキーマの変更を意味しません。たとえば、列にコメントを追加しても、スキーマ ファイルの内容は変更されません。

### インデックスファイル {#index-files}

インデックスファイルは、書き込まれたデータが誤って上書きされることを防ぐために使用されます。データ変更レコードと同じパスに保存されます。

```shell
{scheme}://{prefix}/{schema}/{table}/{table-version-separator}/{partition-separator}/{date-separator}/meta/CDC.index
```

インデックス ファイルには、現在のディレクトリで使用されている最大のファイル名が記録されます。例えば：

    CDC000005.csv

この例では、このディレクトリ内のファイル`CDC000001.csv` ～ `CDC000004.csv`が占有されています。 TiCDC クラスターでテーブルのスケジューリングまたはノードの再起動が発生すると、新しいノードはインデックス ファイルを読み取り、 `CDC000005.csv`が占有されているかどうかを判断します。占有されていない場合、新しいノードは`CDC000005.csv`から始まるファイルを書き込みます。占有されている場合は`CDC000006.csv`から書き込みを開始するため、他のノードによって書き込まれたデータの上書きが防止されます。

### メタデータ {#metadata}

メタデータは次のパスに保存されます。

```shell
{protocol}://{prefix}/metadata
```

メタデータは、次のような JSON 形式のファイルです。

```json
{
    "checkpoint-ts":433305438660591626
}
```

-   `checkpoint-ts` : `commit-ts`が`checkpoint-ts`より小さいトランザクションは、ダウンストリームのターゲットstorageに書き込まれます。

### DDLイベント {#ddl-events}

### テーブルレベルのDDLイベント {#ddl-events-at-the-table-level}

アップストリーム テーブルの DDL イベントによってテーブル バージョンが変更されると、TiCDC は自動的に次の処理を実行します。

-   新しいパスに切り替えてデータ変更レコードを書き込みます。たとえば、バージョン`test.table1`が`441349361156227074`に変更されると、TiCDC はデータ変更レコードを書き込むためにパス`s3://bucket/bbb/ccc/test/table1/441349361156227074/2022-01-02/`に変更します。
-   次のパスにスキーマ ファイルを生成して、テーブル スキーマ情報を保存します。

    ```shell
    {scheme}://{prefix}/{schema}/{table}/meta/schema_{table-version}_{hash}.json
    ```

`schema_441349361156227074_3131721815.json`スキーマ ファイルを例に挙げると、このファイル内のテーブル スキーマ情報は次のとおりです。

```json
{
    "Table":"table1",
    "Schema":"test",
    "Version":1,
    "TableVersion":441349361156227074,
    "Query":"ALTER TABLE test.table1 ADD OfficeLocation blob(20)",
    "Type":5,
    "TableColumns":[
        {
            "ColumnName":"Id",
            "ColumnType":"INT",
            "ColumnNullable":"false",
            "ColumnIsPk":"true"
        },
        {
            "ColumnName":"LastName",
            "ColumnType":"CHAR",
            "ColumnLength":"20"
        },
        {
            "ColumnName":"FirstName",
            "ColumnType":"VARCHAR",
            "ColumnLength":"30"
        },
        {
            "ColumnName":"HireDate",
            "ColumnType":"DATETIME"
        },
        {
            "ColumnName":"OfficeLocation",
            "ColumnType":"BLOB",
            "ColumnLength":"20"
        }
    ],
    "TableColumnsTotal":"5"
}
```

-   `Table` : テーブル名。
-   `Schema` : スキーマ名。
-   `Version` :storageシンクのプロトコル バージョン。
-   `TableVersion` : テーブルバージョン。
-   `Query` : DDL ステートメント。
-   `Type` : DDL タイプ。
-   `TableColumns` : 1 つ以上のマップの配列。各マップはソース テーブル内の列を記述します。
    -   `ColumnName` :カラム名。
    -   `ColumnType` :カラムのタイプ。詳細は[データ・タイプ](#data-type)を参照してください。
    -   `ColumnLength` :カラムの長さ。詳細は[データ・タイプ](#data-type)を参照してください。
    -   `ColumnPrecision` :カラムの精度。詳細は[データ・タイプ](#data-type)を参照してください。
    -   `ColumnScale` : 小数点以下の桁数(スケール)。詳細は[データ・タイプ](#data-type)を参照してください。
    -   `ColumnNullable` : このオプションの値が`true`の場合、列は NULL にすることができます。
    -   `ColumnIsPk` : このオプションの値が`true`の場合、列は主キーの一部です。
-   `TableColumnsTotal` : `TableColumns`配列のサイズ。

### データベースレベルの DDL イベント {#ddl-events-at-the-database-level}

データベース レベルの DDL イベントがアップストリーム データベースで実行されると、TiCDC はデータベース スキーマ情報を保存するために次のパスにスキーマ ファイルを自動的に生成します。

```shell
{scheme}://{prefix}/{schema}/meta/schema_{table-version}_{hash}.json
```

`schema_441349361156227000_3131721815.json`スキーマ ファイルを例に挙げると、このファイル内のデータベース スキーマ情報は次のとおりです。

```json
{
  "Table": "",
  "Schema": "schema1",
  "Version": 1,
  "TableVersion": 441349361156227000,
  "Query": "CREATE DATABASE `schema1`",
  "Type": 1,
  "TableColumns": null,
  "TableColumnsTotal": 0
}
```

### データ・タイプ {#data-type}

このセクションでは、 `schema_{table-version}_{hash}.json`ファイル (以降のセクションでは「スキーマ ファイル」と呼びます) で使用されるデータ型について説明します。データ型は`T(M[, D])`として定義されています。詳細は[データ型](/data-type-overview.md)を参照してください。

#### 整数型 {#integer-types}

TiDB の整数型は`IT[(M)] [UNSIGNED]`として定義されます。

-   `IT`は整数型で、 `TINYINT` 、 `SMALLINT` 、 `MEDIUMINT` 、 `INT` 、 `BIGINT` 、または`BIT`のいずれかになります。
-   `M`はタイプの表示幅です。

整数型は、スキーマ ファイル内で次のように定義されます。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{IT} [UNSIGNED]",
    "ColumnPrecision":"{M}"
}
```

#### 10 進数の型 {#decimal-types}

TiDB の 10 進数タイプは`DT[(M,D)][UNSIGNED]`として定義されます。

-   `DT`は浮動小数点型で、 `FLOAT` 、 `DOUBLE` 、 `DECIMAL` 、または`NUMERIC`のいずれかになります。
-   `M`はデータ型の精度、または合計桁数です。
-   `D`は小数点以下の桁数です。

Decimal タイプは、スキーマ ファイル内で次のように定義されます。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{DT} [UNSIGNED]",
    "ColumnPrecision":"{M}",
    "ColumnScale":"{D}"
}
```

#### 日付と時刻のタイプ {#date-and-time-types}

TiDB の日付タイプは`DT`として定義されます。

-   `DT`は日付タイプで、 `DATE`または`YEAR`になります。

日付タイプはスキーマ ファイル内で次のように定義されます。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{DT}"
}
```

TiDB の時間タイプは`TT[(M)]`として定義されます。

-   `TT`は時間のタイプで、 `TIME` 、 `DATETIME` 、または`TIMESTAMP`のいずれかになります。
-   `M`は、0 ～ 6 の範囲の秒の精度です。

時間タイプはスキーマ ファイル内で次のように定義されます。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{TT}",
    "ColumnScale":"{M}"
}
```

#### 文字列型 {#string-types}

TiDB の文字列タイプは`ST[(M)]`として定義されます。

-   `ST`は文字列タイプで、 `CHAR` 、 `VARCHAR` 、 `TEXT` 、 `BINARY` 、 `BLOB` 、または`JSON`のいずれかになります。
-   `M`は文字列の最大長です。

文字列タイプはスキーマ ファイル内で次のように定義されます。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{ST}",
    "ColumnLength":"{M}"
}
```

#### 列挙型とセット型 {#enum-and-set-types}

Enum 型と Set 型は、スキーマ ファイル内で次のように定義されます。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{ENUM/SET}",
}
```
