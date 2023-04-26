---
title: Replicate Data to Storage Services
summary: Learn how to replicate data to storage services using TiCDC, and learn about the storage path of the replicated data.
---

# ストレージ サービスへのデータのレプリケート {#replicate-data-to-storage-services}

> **警告：**
>
> この機能は実験的です。本番環境で使用することはお勧めしません。

v6.5.0 以降、TiCDC は Amazon S3、Azure Blob Storage、NFS などのstorageサービスへの行変更イベントの保存をサポートしています。このドキュメントでは、TiCDC を使用してそのようなstorageサービスに増分データをレプリケートする変更フィードを作成する方法と、データを保存する方法について説明します。このドキュメントの構成は次のとおりです。

-   [データをstorageサービスにレプリケートする方法](#replicate-change-data-to-storage-services) .
-   [storageサービスでのデータの保存方法](#storage-path-structure) .

## 変更データをstorageサービスにレプリケートする {#replicate-change-data-to-storage-services}

次のコマンドを実行して、changefeed タスクを作成します。

```shell
cdc cli changefeed create \
    --server=http://10.0.10.25:8300 \
    --sink-uri="s3://logbucket/storage_test?protocol=canal-json" \
    --changefeed-id="simple-replication-task"
```

出力は次のとおりです。

```shell
Info: {"upstream_id":7171388873935111376,"namespace":"default","id":"simple-replication-task","sink_uri":"s3://logbucket/storage_test?protocol=canal-json","create_time":"2023-03-10T18:52:05.566016967+08:00","start_ts":437706850431664129,"engine":"unified","config":{"case_sensitive":true,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":false,"sync_point_interval":600000000000,"sync_point_retention":86400000000000,"filter":{"rules":["*.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"canal-json","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v6.5.2-master-dirty"}
```

-   `--changefeed-id` : 変更フィードの ID。形式は`^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`正規表現と一致する必要があります。この ID が指定されていない場合、TiCDC は ID として UUID (バージョン 4 形式) を自動的に生成します。
-   `--sink-uri` : changefeed のダウンストリーム アドレス。詳細については、 [シンク URI を構成する](#configure-sink-uri)を参照してください。
-   `--start-ts` : 変更フィードの開始 TSO。 TiCDC は、この TSO からデータのプルを開始します。デフォルト値は現在の時刻です。
-   `--target-ts` : changefeed の終了 TSO。 TiCDC は、この TSO までデータのプルを停止します。デフォルト値は空です。これは、TiCDC がデータのプルを自動的に停止しないことを意味します。
-   `--config` : changefeed の構成ファイル。詳細については、 [TiCDC changefeed 構成パラメーター](/ticdc/ticdc-changefeed-config.md)を参照してください。

## シンク URI を構成する {#configure-sink-uri}

このセクションでは、Amazon S3、Azure Blob Storage、NFS など、changefeed URI でstorageサービスを構成する方法について説明します。

### Amazon S3 または Azure Blob Storage を構成する {#configure-amazon-s3-or-azure-blob-storage}

TiCDC の Amazon S3 と Azure Blob Storage の URI パラメーターは、 BRの URL パラメーターと同じです。詳細については、 [バックアップstorageのURL 形式](/br/backup-and-restore-storages.md#url-format-description)を参照してください。

### NFS の構成 {#configure-nfs}

次の構成では、行変更イベントが NFS に保存されます。

```shell
--sink-uri="file:///my-directory/prefix"
```

### オプションのパラメーター {#optional-parameters}

URI のその他のオプション パラメータは次のとおりです。

| パラメータ            | 説明                                                | デフォルト値     | 値の範囲                   |
| :--------------- | :------------------------------------------------ | :--------- | :--------------------- |
| `worker-count`   | データの変更をダウンストリームのクラウドstorageに保存するための同時実行性。         | `16`       | `[1, 512]`             |
| `flush-interval` | データの変更をダウンストリームのクラウドstorageに保存する間隔。               | `5s`       | `[2s, 10m]`            |
| `file-size`      | バイト数がこのパラメータの値を超えると、データ変更ファイルがクラウドstorageに保存されます。 | `67108864` | `[1048576, 536870912]` |
| `protocol`       | ダウンストリームに送信されるメッセージのプロトコル形式。                      | なし         | `canal-json`と`csv`     |

> **ノート：**
>
> `flush-interval`または`file-size`いずれかが要件を満たしている場合、データ変更ファイルはダウンストリームに保存されます。

## ストレージパス構造 {#storage-path-structure}

このセクションでは、データ変更レコード、メタデータ、および DDL イベントのstorageパス構造について説明します。

### データ変更記録 {#data-change-records}

データ変更レコードは次のパスに保存されます。

```shell
{scheme}://{prefix}/{schema}/{table}/{table-version-separator}/{partition-separator}/{date-separator}/CDC{num}.{extension}
```

-   `scheme` : データ転送プロトコルまたはstorageタイプを指定します (例: `**s3** ://xxxxx` )。
-   `prefix` : ユーザー定義の親ディレクトリを指定します (例: `s3:// **bucket/bbb/ccc**` )。
-   `schema` : スキーマ名を指定します (例: `s3://bucket/bbb/ccc/ **test**` 。
-   `table` : テーブル名を指定します (例: `s3://bucket/bbb/ccc/test/ **table1**` 。
-   `table-version-separator` : s3: `s3://bucket/bbb/ccc/test/table1/ **9999**`のように、パスをテーブル バージョンで区切るセパレータを指定します。
-   `partition-separator` : s3: `s3://bucket/bbb/ccc/test/table1/9999/ **20**`ように、パスをテーブル パーティションで区切るセパレータを指定します。
-   `date-separator` : トランザクションのコミット日によってファイルを分類します。値のオプションは次のとおりです。
    -   `none` : いいえ`date-separator` 。たとえば、バージョン`test.table1`が`9999`のすべてのファイルは`s3://bucket/bbb/ccc/test/table1/9999`に保存されます。
    -   `year` : 区切り文字は、トランザクションのコミット日の年です (例`s3://bucket/bbb/ccc/test/table1/9999/ **2022**` 。
    -   `month` : 区切り文字は、トランザクションのコミット日の年と月です (例`s3://bucket/bbb/ccc/test/table1/9999/ **2022-01**` 。
    -   `day` : 区切り文字は、トランザクションのコミット日の年、月、日です (例`s3://bucket/bbb/ccc/test/table1/9999/ **2022-01-02**` 。
-   `num` : データの変更を記録するファイルのシリアル番号を保存します (例`s3://bucket/bbb/ccc/test/table1/9999/2022-01-02/CDC **000005** .csv` 。
-   `extension` : ファイルの拡張子を指定します。 v6.5.0 以降、TiDB は CSV および Canal-JSON 形式をサポートします。

> **ノート：**
>
> テーブル バージョンは、次の 2 つのケースで変更されます。
>
> -   DDL 操作の実行後、アップストリームの TiDB で DDL が実行されたときのテーブル バージョンは TSO です。ただし、テーブル バージョンの変更は、テーブル スキーマの変更を意味するものではありません。たとえば、列にコメントを追加しても、 `schema.json`ファイルの内容は変更されません。
> -   changefeed プロセスが再起動します。テーブル バージョンは、プロセスの再起動時のチェックポイント TSO です。多くのテーブルがあり、プロセスが再起動すると、すべてのディレクトリを走査し、各テーブルが最後に書き込まれた位置を見つけるのに長い時間がかかります。したがって、データは、以前のディレクトリーではなく、バージョンがチェックポイント TSO である新しいディレクトリーに書き込まれます。

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

### DDL イベント {#ddl-events}

DDL イベントによってテーブルのバージョンが変更されると、TiCDC は新しいパスに切り替えてデータ変更レコードを書き込みます。たとえば、 `test.table1`のバージョンが`9999`から`10000`に変わると、パス`s3://bucket/bbb/ccc/test/table1/10000/2022-01-02/CDC000001.csv`にデータが書き込まれます。さらに、DDL イベントが発生すると、TiCDC は`schema.json`ファイルを生成して、テーブル スキーマ情報を保存します。

テーブル スキーマ情報は、次のパスに保存されます。

```shell
{scheme}://{prefix}/{schema}/{table}/{table-version-separator}/schema.json
```

以下は`schema.json`ファイルです。

```json
{
    "Table":"table1",
    "Schema":"test",
    "Version":1,
    "TableVersion":10000,
    "Query": "ALTER TABLE test.table1 ADD OfficeLocation blob(20)",
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
-   `TableVersion` : テーブルのバージョン。
-   `Query` ：DDL文。
-   `TableColumns` : 1 つ以上のマップの配列。それぞれがソース テーブルの列を記述します。
    -   `ColumnName` :カラム名。
    -   `ColumnType` :カラムのタイプ。詳細については、 [データ・タイプ](#data-type)を参照してください。
    -   `ColumnLength` :カラムの長さ。詳細については、 [データ・タイプ](#data-type)を参照してください。
    -   `ColumnPrecision` :カラムの精度。詳細については、 [データ・タイプ](#data-type)を参照してください。
    -   `ColumnScale` : 小数点以下の桁数 (スケール)。詳細については、 [データ・タイプ](#data-type)を参照してください。
    -   `ColumnNullable` : このオプションの値が`true`の場合、列は NULL にすることができます。
    -   `ColumnIsPk` : このオプションの値が`true`の場合、列は主キーの一部です。
-   `TableColumnsTotal` : `TableColumns`配列のサイズ。

### データ・タイプ {#data-type}

このセクションでは、 `schema.json`ファイルで使用されるデータ型について説明します。データ型は`T(M[, D])`として定義されています。詳細については、 [データ型](/data-type-overview.md)を参照してください。

#### 整数型 {#integer-types}

TiDB の整数型は`IT[(M)] [UNSIGNED]`として定義されます。

-   `IT`は整数型で、 `TINYINT` 、 `SMALLINT` 、 `MEDIUMINT` 、 `INT` 、 `BIGINT` 、または`BIT`のいずれかです。
-   `M`は、タイプの表示幅です。

`schema.json`では、整数型は次のように定義されています。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{IT} [UNSIGNED]",
    "ColumnPrecision":"{M}"
}
```

#### 10 進数型 {#decimal-types}

TiDB の Decimal 型は`DT[(M,D)][UNSIGNED]`として定義されます。

-   `DT`は浮動小数点型で、 `FLOAT` 、 `DOUBLE` 、 `DECIMAL` 、または`NUMERIC`のいずれかです。
-   `M`はデータ型の精度、または合計桁数です。
-   `D`は小数点以下の桁数です。

Decimal 型は`schema.json`で次のように定義されています。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{DT} [UNSIGNED]",
    "ColumnPrecision":"{M}",
    "ColumnScale":"{D}"
}
```

#### 日付と時刻の種類 {#date-and-time-types}

TiDB の日付型は`DT`として定義されています。

-   `DT`は日付タイプで、 `DATE`または`YEAR`です。

`schema.json`では、日付型は次のように定義されています。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{DT}"
}
```

TiDB の時刻型は`TT[(M)]`として定義されています。

-   `TT`は時間タイプで、 `TIME` 、 `DATETIME` 、または`TIMESTAMP`のいずれかです。
-   `M`は、0 ～ 6 の範囲の秒の精度です。

時間タイプは、 `schema.json`で次のように定義されています。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{TT}",
    "ColumnScale":"{M}"
}
```

#### 文字列型 {#string-types}

TiDB の文字列型は`ST[(M)]`として定義されています。

-   `ST`は文字列型で、 `CHAR` 、 `VARCHAR` 、 `TEXT` 、 `BINARY` 、 `BLOB` 、または`JSON`のいずれかです。
-   `M`は文字列の最大長です。

文字列型は`schema.json`で次のように定義されています。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{ST}",
    "ColumnLength":"{M}"
}
```

#### 列挙型とセット型 {#enum-and-set-types}

Enum および Set 型は、 `schema.json`で次のように定義されています。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{ENUM/SET}",
}
```
