---
title: Replicate Data to Storage Services
summary: TiCDC を使用してデータをstorageサービスに複製する方法と、複製されたデータのstorageパスについて学習します。
---

# ストレージサービスにデータを複製する {#replicate-data-to-storage-services}

TiDB v6.5.0 以降、TiCDC は、Amazon S3、GCS、Azure Blob Storage、NFS などのstorageサービスへの行変更イベントの保存をサポートしています。このドキュメントでは、TiCDC を使用して増分データをこのようなstorageサービスに複製する変更フィードを作成する方法と、データを保存する方法について説明します。このドキュメントの構成は次のとおりです。

-   [storageサービスにデータを複製する方法](#replicate-change-data-to-storage-services) 。
-   [storageサービスにデータを保存する方法](#storage-path-structure) 。

## 変更データをstorageサービスに複製する {#replicate-change-data-to-storage-services}

次のコマンドを実行して、changefeed タスクを作成します。

```shell
cdc cli changefeed create \
    --server=http://10.0.10.25:8300 \
    --sink-uri="s3://logbucket/storage_test?protocol=canal-json" \
    --changefeed-id="simple-replication-task"
```

出力は次のようになります。

```shell
Info: {"upstream_id":7171388873935111376,"namespace":"default","id":"simple-replication-task","sink_uri":"s3://logbucket/storage_test?protocol=canal-json","create_time":"2024-08-05T18:52:05.566016967+08:00","start_ts":437706850431664129,"engine":"unified","config":{"case_sensitive":false,"enable_old_value":true,"force_replicate":false,"ignore_ineligible_table":false,"check_gc_safe_point":true,"enable_sync_point":false,"sync_point_interval":600000000000,"sync_point_retention":86400000000000,"filter":{"rules":["*.*"],"event_filters":null},"mounter":{"worker_num":16},"sink":{"protocol":"canal-json","schema_registry":"","csv":{"delimiter":",","quote":"\"","null":"\\N","include_commit_ts":false},"column_selectors":null,"transaction_atomicity":"none","encoder_concurrency":16,"terminator":"\r\n","date_separator":"none","enable_partition_separator":false},"consistent":{"level":"none","max_log_size":64,"flush_interval":2000,"storage":""}},"state":"normal","creator_version":"v7.5.3"}
```

-   `--server` : TiCDC クラスター内の任意の TiCDCサーバーのアドレス。
-   `--changefeed-id` : 変更フィードの ID。形式は`^[a-zA-Z0-9]+(\-[a-zA-Z0-9]+)*$`正規表現に一致する必要があります。この ID が指定されていない場合、TiCDC は ID として UUID (バージョン 4 形式) を自動的に生成します。
-   `--sink-uri` : チェンジフィードのダウンストリームアドレス。詳細については[シンクURIを構成する](#configure-sink-uri)を参照してください。
-   `--start-ts` : 変更フィードの開始 TSO。TiCDC はこの TSO からデータの取得を開始します。デフォルト値は現在の時刻です。
-   `--target-ts` : 変更フィード終了 TSO。TiCDC はこの TSO までデータのプルを停止します。デフォルト値は空で、TiCDC はデータのプルを自動的に停止しないことを意味します。
-   `--config` : チェンジフィードの設定ファイル。詳細は[TiCDC チェンジフィード構成パラメータ](/ticdc/ticdc-changefeed-config.md)を参照してください。

## シンクURIを構成する {#configure-sink-uri}

このセクションでは、Amazon S3、GCS、Azure Blob Storage、NFS などのstorageサービスのシンク URI を構成する方法について説明します。シンク URI は、TiCDC ターゲット システムの接続情報を指定するために使用されます。形式は次のとおりです。

```shell
[scheme]://[host]/[path]?[query_parameters]
```

URI の`[query_parameters]`には、次のパラメータを設定できます。

| パラメータ                   | 説明                                                                                                                                                                                                                                    | デフォルト値     | 値の範囲                   |
| :---------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ | :--------- | :--------------------- |
| `worker-count`          | ダウンストリームのクラウドstorageにデータの変更を保存するための同時実行性。                                                                                                                                                                                             | `16`       | `[1, 512]`             |
| `flush-interval`        | ダウンストリームのクラウドstorageにデータの変更を保存する間隔。                                                                                                                                                                                                   | `5s`       | `[2s, 10m]`            |
| `file-size`             | バイト数がこのパラメータの値を超えると、データ変更ファイルはクラウドstorageに保存されます。                                                                                                                                                                                     | `67108864` | `[1048576, 536870912]` |
| `protocol`              | ダウンストリームに送信されるメッセージのプロトコル形式。                                                                                                                                                                                                          | 該当なし       | `canal-json`と`csv`     |
| `enable-tidb-extension` | `protocol`が`canal-json`に設定され、 `enable-tidb-extension` `true`に設定されている場合、 TiCDC は[ウォーターマークイベント](/ticdc/ticdc-canal-json.md#watermark-event)を送信し、 [TiDB拡張フィールド](/ticdc/ticdc-canal-json.md#tidb-extension-field) Canal-JSON メッセージに追加します。 | `false`    | `false`と`true`         |

> **注記：**
>
> `flush-interval`または`file-size`いずれか`CDC:ErrSinkUnknownProtocol` `protocol`が返されます。

### 外部storageのシンクURIを構成する {#configure-sink-uri-for-external-storage}

クラウドstorageシステムにデータを保存する場合、クラウド サービス プロバイダーに応じて異なる認証パラメータを設定する必要があります。このセクションでは、Amazon S3、Google Cloud Storage (GCS)、Azure Blob Storage を使用する場合の認証方法と、対応するstorageサービスにアクセスするためのアカウントの構成方法について説明します。

<SimpleTab groupId="storage">
<div label="Amazon S3" value="amazon">

以下は Amazon S3 の設定例です。

```shell
--sink-uri="s3://bucket/prefix?protocol=canal-json"
```

データを複製する前に、Amazon S3 のディレクトリに適切なアクセス権限を設定する必要があります。

-   TiCDC に必要な最小限の権限: `s3:ListBucket` `s3:PutObject`および`s3:GetObject` 。
-   changefeed 構成項目`sink.cloud-storage-config.flush-concurrency`が 1 より大きい場合、つまり単一ファイルの並列アップロードが有効になっている場合は、 [リストパーツ](https://docs.aws.amazon.com/AmazonS3/latest/API/API_ListParts.html)に関連する権限を追加する必要があります。
    -   `s3:AbortMultipartUpload`
    -   `s3:ListMultipartUploadParts`
    -   `s3:ListBucketMultipartUploads`

レプリケーションデータstorageディレクトリを作成していない場合は、 [バケットを作成する](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-bucket.html)を参考に指定リージョンに S3 バケットを作成してください。必要に応じて[フォルダを使用して Amazon S3 コンソールでオブジェクトを整理する](https://docs.aws.amazon.com/AmazonS3/latest/user-guide/create-folder.html)を参考にバケット内にフォルダを作成することもできます。

次の方法で Amazon S3 にアクセスするようにアカウントを設定できます。

-   方法1: アクセスキーを指定する

    アクセスキーとシークレットアクセスキーを指定すると、それらに従って認証が行われます。URI でキーを指定する方法に加えて、次の方法がサポートされています。

    -   TiCDC は環境変数`$AWS_ACCESS_KEY_ID`と`$AWS_SECRET_ACCESS_KEY`読み取ります。
    -   TiCDC は環境変数`$AWS_ACCESS_KEY`と`$AWS_SECRET_KEY`読み取ります。
    -   TiCDC は、 `$AWS_SHARED_CREDENTIALS_FILE`環境変数で指定されたパスにある共有資格情報ファイルを読み取ります。
    -   TiCDC は`~/.aws/credentials`パスの共有資格情報ファイルを読み取ります。

-   方法2: IAMロールに基づくアクセス

    TiCDCサーバーを実行している EC2 インスタンスに[Amazon S3 にアクセスするための権限が設定されたIAMロール](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_roles_use_switch-role-ec2.html)を関連付けます。セットアップが成功すると、TiCDC は追加の設定なしで Amazon S3 内の対応するディレクトリに直接アクセスできるようになります。

</div>
<div label="GCS" value="gcs">

以下は GCS の構成例です。

```shell
--sink-uri="gcs://bucket/prefix?protocol=canal-json"
```

アクセス キーを指定して、GCS へのアクセスに使用するアカウントを設定できます。認証は指定された`credentials-file`に従って実行されます。URI でキーを指定することに加えて、次の方法がサポートされています。

-   TiCDC は、 `$GOOGLE_APPLICATION_CREDENTIALS`環境変数で指定されたパス内のファイルを読み取ります。
-   TiCDC はファイル`~/.config/gcloud/application_default_credentials.json`を読み取ります。
-   TiCDC は、クラスターが GCE または GAE で実行されているときにメタデータサーバーから資格情報を取得します。

</div>
<div label="Azure Blob Storage" value="azure">

以下は、Azure Blob Storage の構成例です。

```shell
--sink-uri="azure://bucket/prefix?protocol=canal-json"
```

次の方法で、Azure Blob Storage にアクセスするようにアカウントを構成できます。

-   方法1: 共有アクセス署名を指定する

    URI で`account-name`と`sas-token`を構成すると、このパラメーターで指定されたstorageアカウント名と共有アクセス署名トークンが使用されます。共有アクセス署名トークンには`&`文字があるため、URI に追加する前に`%26`としてエンコードする必要があります。パーセント エンコードを使用して`sas-token`全体を直接エンコードすることもできます。

-   方法2: アクセスキーを指定する

    URI に`account-name`と`account-key`を設定すると、このパラメータで指定したstorageアカウント名とキーが使用されます。URI にキー ファイルを指定するだけでなく、TiCDC は環境変数`$AZURE_STORAGE_KEY`からキーを読み取ることもできます。

-   方法3: Azure ADを使用してバックアップを復元する

    環境`$AZURE_TENANT_ID` `$AZURE_CLIENT_ID` `$AZURE_CLIENT_SECRET`設定します。

</div>
</SimpleTab>

> **ヒント：**
>
> TiCDC における Amazon S3、GCS、Azure Blob Storage の URI パラメータの詳細については、 [外部ストレージサービスの URI 形式](/external-storage-uri.md)参照してください。

### NFSのシンクURIを構成する {#configure-sink-uri-for-nfs}

以下は NFS の設定例です。

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

-   `scheme` :storageタイプを指定します (例: `s3` 、 `gcs` 、 `azure` 、 `file` 。
-   `prefix` : ユーザー定義の親ディレクトリを指定します (例: `s3:// **bucket/bbb/ccc**` )。
-   `schema` : スキーマ名を指定します (例: `s3://bucket/bbb/ccc/ **test**` 。
-   `table` : テーブル名を指定します (例: `s3://bucket/bbb/ccc/test/ **table1**` 。
-   `table-version-separator` : テーブルバージョンでパスを区切る区切り文字を指定します (例: `s3://bucket/bbb/ccc/test/table1/ **9999**` 。
-   `partition-separator` : テーブルパーティションによってパスを区切る区切り文字を指定します (例: `s3://bucket/bbb/ccc/test/table1/9999/ **20**` 。
-   `date-separator` : トランザクションのコミット日でファイルを分類します。デフォルト値は`day`です。値のオプションは次のとおりです。
    -   `none` : `date-separator`なし。たとえば、バージョン`test.table1`のファイルはすべて`9999`として`s3://bucket/bbb/ccc/test/table1/9999`に保存されます。
    -   `year` : 区切り文字はトランザクションコミット日の年です。例: `s3://bucket/bbb/ccc/test/table1/9999/ **2022**` 。
    -   `month` : 区切り文字はトランザクションコミット日の年と月です。例: `s3://bucket/bbb/ccc/test/table1/9999/ **2022-01**` 。
    -   `day` : 区切り文字はトランザクションコミット日の年、月、日です。例: `s3://bucket/bbb/ccc/test/table1/9999/ **2022-01-02**` 。
-   `num` : データの変更を記録したファイルのシリアル番号を保存します (例: `s3://bucket/bbb/ccc/test/table1/9999/2022-01-02/CDC **000005** .csv` 。
-   `extension` : ファイルの拡張子を指定します。TiDB v6.5.0 は CSV および Canal-JSON 形式をサポートしています。

> **注記：**
>
> テーブル バージョンは、上流テーブルで DDL 操作が実行された後にのみ変更され、上流 TiDB が DDL の実行を完了すると、新しいテーブル バージョンが TSO になります。ただし、テーブル バージョンの変更は、テーブル スキーマの変更を意味するものではありません。たとえば、列にコメントを追加しても、スキーマ ファイルの内容は変更されません。

### インデックスファイル {#index-files}

インデックス ファイルは、書き込まれたデータが誤って上書きされるのを防ぐために使用され、データ変更レコードと同じパスに保存されます。

```shell
{scheme}://{prefix}/{schema}/{table}/{table-version-separator}/{partition-separator}/{date-separator}/meta/CDC.index
```

インデックス ファイルには、現在のディレクトリで使用されている最大のファイル名が記録されます。例:

    CDC000005.csv

この例では、このディレクトリ内のファイル`CDC000001.csv`から`CDC000004.csv`が使用されています。TiCDC クラスターでテーブル スケジューリングまたはノードの再起動が発生すると、新しいノードはインデックス ファイルを読み取り、 `CDC000005.csv`が使用されているかどうかを判断します。使用されていない場合、新しいノードは`CDC000005.csv`からファイルを書き込みます。使用されている場合は、 `CDC000006.csv`から書き込みを開始し、他のノードによって書き込まれたデータが上書きされるのを防ぎます。

### メタデータ {#metadata}

メタデータは次のパスに保存されます:

```shell
{protocol}://{prefix}/metadata
```

メタデータは JSON 形式のファイルです。例:

```json
{
    "checkpoint-ts":433305438660591626
}
```

-   `checkpoint-ts` : `commit-ts`が`checkpoint-ts`より小さいトランザクションは、ダウンストリームのターゲットstorageに書き込まれます。

### DDLイベント {#ddl-events}

### テーブルレベルのDDLイベント {#ddl-events-at-the-table-level}

アップストリーム テーブルの DDL イベントによってテーブル バージョンが変更されると、TiCDC は自動的に次の処理を実行します。

-   データ変更レコードを書き込むための新しいパスに切り替えます。たとえば、バージョン`test.table1`が`441349361156227074`に変更されると、TiCDC はデータ変更レコードを書き込むために`s3://bucket/bbb/ccc/test/table1/441349361156227074/2022-01-02/`パスに変更します。
-   テーブル スキーマ情報を格納するために、次のパスにスキーマ ファイルを生成します。

    ```shell
    {scheme}://{prefix}/{schema}/{table}/meta/schema_{table-version}_{hash}.json
    ```

`schema_441349361156227074_3131721815.json`スキーマ ファイルを例にとると、このファイル内のテーブル スキーマ情報は次のようになります。

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
-   `Version` :storageシンクのプロトコルバージョン。
-   `TableVersion` : テーブルバージョン。
-   `Query` : DDL ステートメント。
-   `Type` : DDL タイプ。
-   `TableColumns` : 1 つ以上のマップの配列。各マップはソース テーブル内の列を表します。
    -   `ColumnName` :カラム名。
    -   `ColumnType` :カラムタイプ。詳細は[データ・タイプ](#data-type)を参照してください。
    -   `ColumnLength` :カラムの長さ。詳細は[データ・タイプ](#data-type)を参照してください。
    -   `ColumnPrecision` :カラムの精度。詳細については[データ・タイプ](#data-type)を参照してください。
    -   `ColumnScale` : 小数点以下の桁数（スケール）。詳細は[データ・タイプ](#data-type)を参照。
    -   `ColumnNullable` : このオプションの値が`true`場合、列は NULL になることができます。
    -   `ColumnIsPk` : このオプションの値が`true`の場合、列は主キーの一部になります。
-   `TableColumnsTotal` : `TableColumns`配列のサイズ。

### データベース レベルの DDL イベント {#ddl-events-at-the-database-level}

アップストリーム データベースでデータベース レベルの DDL イベントが実行されると、TiCDC は次のパスにスキーマ ファイルを自動的に生成し、データベース スキーマ情報を格納します。

```shell
{scheme}://{prefix}/{schema}/meta/schema_{table-version}_{hash}.json
```

`schema_441349361156227000_3131721815.json`スキーマ ファイルを例にとると、このファイル内のデータベース スキーマ情報は次のようになります。

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

このセクションでは、 `schema_{table-version}_{hash}.json`ファイル（以下、スキーマファイルと呼ぶ）で使用されるデータ型について説明します。データ型は`T(M[, D])`として定義されています。詳細については[データ型](/data-type-overview.md)を参照してください。

#### 整数型 {#integer-types}

TiDBの整数型は`IT[(M)] [UNSIGNED]`と定義され、

-   `IT`は整数型で、 `TINYINT` 、 `SMALLINT` 、 `MEDIUMINT` 、 `INT` 、 `BIGINT` 、または`BIT`になります。
-   `M`はタイプの表示幅です。

整数型はスキーマ ファイル内で次のように定義されます。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{IT} [UNSIGNED]",
    "ColumnPrecision":"{M}"
}
```

#### 10進数型 {#decimal-types}

TiDBの10進数型は`DT[(M,D)][UNSIGNED]`と定義され、

-   `DT`は浮動小数点型で、 `FLOAT` 、 `DOUBLE` 、 `DECIMAL` 、または`NUMERIC`になります。
-   `M`はデータ型の精度、つまり合計桁数です。
-   `D`小数点以下の桁数です。

10 進数型はスキーマ ファイルで次のように定義されます。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{DT} [UNSIGNED]",
    "ColumnPrecision":"{M}",
    "ColumnScale":"{D}"
}
```

#### 日付と時刻の種類 {#date-and-time-types}

TiDBの日付型は`DT`として定義され、

-   `DT`は日付型で、 `DATE`または`YEAR`になります。

日付タイプはスキーマ ファイルで次のように定義されます。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{DT}"
}
```

TiDBにおける時間型は`TT[(M)]`として定義され、

-   `TT`は時間タイプで、 `TIME` 、 `DATETIME` 、または`TIMESTAMP`になります。
-   `M`は 0 から 6 までの範囲の秒の精度です。

時間タイプはスキーマ ファイルで次のように定義されます。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{TT}",
    "ColumnScale":"{M}"
}
```

#### 文字列型 {#string-types}

TiDBの文字列型は`ST[(M)]`として定義され、

-   `ST`は文字列型で、 `CHAR` 、 `VARCHAR` 、 `TEXT` 、 `BINARY` 、 `BLOB` 、または`JSON`になります。
-   `M`文字列の最大長です。

文字列型はスキーマ ファイル内で次のように定義されます。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{ST}",
    "ColumnLength":"{M}"
}
```

#### 列挙型とセット型 {#enum-and-set-types}

Enum 型と Set 型は、スキーマ ファイルで次のように定義されます。

```json
{
    "ColumnName":"COL1",
    "ColumnType":"{ENUM/SET}",
}
```
