---
title: Guide for Developing a Storage Sink Consumer
summary: Learn how to design and implement a consumer to consume data changes in storage sinks.
---

# ストレージ シンク コンシューマの開発ガイド {#guide-for-developing-a-storage-sink-consumer}

このドキュメントでは、TiDB データ変更コンシューマーを設計および実装する方法について説明します。

> **注記：**
>
> storageシンクは`DROP DATABASE` DDL を処理できません。したがって、この DDL は実行しないでください。この DDL を実行する必要がある場合は、ダウンストリーム MySQL で手動で実行してください。

TiCDC は、コンシューマーを実装するための標準的な方法を提供しません。このドキュメントでは、 Golangで書かれた消費者向けサンプル プログラムを提供します。このプログラムは、storageサービスからデータを読み取り、そのデータを MySQL 互換データベースに書き込むことができます。この例で提供されているデータ形式と手順を参照して、コンシューマーを独自に実装できます。

[Golangで書かれたコンシューマ プログラム](https://github.com/pingcap/tiflow/tree/release-7.5/cmd/storage-consumer)

## 消費者をデザインする {#design-a-consumer}

次の図は、消費者の全体的な消費プロセスを示しています。

![TiCDC storage consumer overview](/media/ticdc/ticdc-storage-consumer-overview.png)

コンシューマのコンポーネントとその機能は次のように説明されます。

```go
type StorageReader struct {
}
// Read the files from storage.
// Add new files and delete files that do not exist in storage.
func (c *StorageReader) ReadFiles() {}

// Query newly added files and the latest checkpoint from storage. One file can only be returned once.
func (c *StorageReader) ExposeNewFiles() (int64, []string) {}

// ConsumerManager is responsible for assigning tasks to TableConsumer.
// Different consumers can consume data concurrently,
// but data of one table must be processed by the same TableConsumer.
type ConsumerManager struct {
  // StorageCheckpoint is recorded in the metadata file, and it can be fetched by calling `StorageReader.ExposeNewFiles()`.
  // This checkpoint indicates that the data whose transaction commit time is less than this checkpoint has been stored in storage.
  StorageCheckpoint int64
  // This checkpoint indicates where the consumer has consumed.
  // ConsumerManager periodically collects TableConsumer.Checkpoint,
  // then Checkpoint is updated to the minimum value of all TableConsumer.Checkpoint.
  Checkpoint int64

  tableFiles[schema][table]*TableConsumer
}

// Query newly added files from StorageReader.
// For a newly created table, create a TableConsumer for it.
// If any, send new files to the corresponding TableConsumer.
func (c *ConsumerManager) Dispatch() {}
type TableConsumer struct {
  // This checkpoint indicates where this TableConsumer has consumed.
  // Its initial value is ConsumerManager.Checkpoint.
  // TableConsumer.Checkpoint is equal to TableVersionConsumer.Checkpoint.
  Checkpoint int64

  schema,table string
  // Must be consumed sequentially according to the order of table versions.
  verConsumers map[version int64]*TableVersionConsumer
  currentVer, previousVer int64
}

// Send newly added files to the corresponding TableVersionConsumer.
// For any DDL, assign a TableVersionConsumer for the new table version.
func (tc *TableConsumer) Dispatch() {}

// If DDL query is empty or its tableVersion is less than TableConsumer.Checkpoint,
// - ignore this DDL, and consume the data under the table version.
// Otherwise,
// - execute the DDL first, and then consume the data under the table version.
// - For tables that are dropped, auto-recycling is performed after the drop table DDL is executed.
func (tc *TableConsumer) ExecuteDDL() {}

type TableVersionConsumer struct {
  // This checkpoint indicates where the TableVersionConsumer has consumed.
  // Its initial value is TableConsumer.Checkpoint.
  Checkpoint int64

  schema,table,version string
  // For the same table version, data in different partitions can be consumed concurrently.
  # partitionNum int64
  // Must be consumed sequentially according to the data file number.
  fileSet map[filename string]*TableVersionConsumer
  currentVersion
}
// If data commit ts is less than TableConsumer.Checkpoint
// or bigger than ConsumerManager.StorageCheckpoint,
// - ignore this data.
// Otherwise,
// - process this data and write it to MySQL.
func (tc *TableVersionConsumer) ExecuteDML() {}
```

## DDL イベントを処理する {#process-ddl-events}

コンシューマは初めてディレクトリを横断します。以下は例です。

    ├── metadata
    └── test
        ├── tbl_1
        │   └── 437752935075545091
        │       ├── CDC000001.json
        │       └── schema.json

コンシューマは`schema.json`ファイルのテーブル スキーマを解析し、DDL クエリ ステートメントを取得します。

-   Query ステートメントが見つからないか、コンシューマ チェックポイントより`TableVersion`が小さい場合、コンシューマはこのステートメントをスキップします。
-   Query ステートメントが存在するか、 `TableVersion`がコンシューマ チェックポイント以上の場合、コンシューマはダウンストリーム MySQL で DDL ステートメントを実行します。

次に、コンシューマは`CDC000001.json`ファイルの複製を開始します。

次の例では、 `test/tbl_1/437752935075545091/schema.json`ファイルの DDL Query ステートメントは空ではありません。

```json
{
    "Table":"test",
    "Schema":"tbl_1",
    "Version": 1,
    "TableVersion":437752935075545091,
    "Query": "create table tbl_1 (Id int primary key, LastName char(20), FirstName varchar(30), HireDate datetime, OfficeLocation Blob(20))",
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

コンシューマがディレクトリを再度トラバースすると、テーブルの新しいバージョンのディレクトリが見つかります。コンシューマは、 `test/tbl_1/437752935075545091`ディレクトリ内のすべてのファイルが消費された後でのみ、新しいディレクトリ内のデータを消費できることに注意してください。

    ├── metadata
    └── test
        ├── tbl_1
        │   ├── 437752935075545091
        │   │   ├── CDC000001.json
        │   │   └── schema.json
        │   └── 437752935075546092
        │   │   └── CDC000001.json
        │   │   └── schema.json

消費ロジックは一貫しています。具体的には、コンシューマは`schema.json`ファイルのテーブル スキーマを解析し、それに応じて DDL クエリ ステートメントを取得して処理します。次に、コンシューマは`CDC000001.json`ファイルの複製を開始します。

## DML イベントの処理 {#process-dml-events}

DDL イベントが適切に処理されると、特定のファイル形式 (CSV または Canal-JSON) とファイル番号に基づいて`{schema}/{table}/{table-version-separator}/`ディレクトリ内の DML イベントを処理できます。

TiCDC は、データが少なくとも 1 回複製されることを保証します。したがって、重複したデータが存在する可能性があります。変更データのコミット ts をコンシューマ チェックポイントと比較する必要があります。コミット ts がコンシューマー チェックポイントより小さい場合は、重複排除を実行する必要があります。
