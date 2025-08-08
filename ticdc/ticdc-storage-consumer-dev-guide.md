---
title: Guide for Developing a Storage Sink Consumer
summary: storageシンク内のデータの変更を消費するコンシューマーを設計および実装する方法を学習します。
---

# ストレージシンクコンシューマーの開発ガイド {#guide-for-developing-a-storage-sink-consumer}

このドキュメントでは、TiDB データ変更コンシューマーを設計および実装する方法について説明します。

> **注記：**
>
> storageシンクは`DROP DATABASE` DDLを処理できません。そのため、このDDLの実行は避けてください。このDDLを実行する必要がある場合は、下流のMySQLで手動で実行してください。

TiCDC は、コンシューマーを実装するための標準的な方法を提供していません。このドキュメントでは、 Golangで記述されたコンシューマーのサンプルプログラムを提供します。このプログラムは、storageサービスからデータを読み取り、MySQL 互換データベースに書き込むことができます。このサンプルで提供されているデータ形式と手順を参考に、独自にコンシューマーを実装できます。

[Golangで書かれたコンシューマープログラム](https://github.com/pingcap/tiflow/tree/release-8.5/cmd/storage-consumer)

## 消費者をデザインする {#design-a-consumer}

次の図は、消費者の全体的な消費プロセスを示しています。

![TiCDC storage consumer overview](/media/ticdc/ticdc-storage-consumer-overview.png)

コンシューマーのコンポーネントとその機能は次のように説明されます。

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

## DDLイベントを処理する {#process-ddl-events}

コンシューマーが初めてディレクトリをトラバースします。以下は例です。

    ├── metadata
    └── test
        ├── tbl_1
        │   └── 437752935075545091
        │       ├── CDC000001.json
        │       └── schema.json

コンシューマーは`schema.json`ファイルのテーブル スキーマを解析し、DDL クエリ ステートメントを取得します。

-   クエリ ステートメントが見つからない場合、または`TableVersion`コンシューマー チェックポイントより小さい場合、コンシューマーはこのステートメントをスキップします。
-   クエリ ステートメントが存在する場合、または`TableVersion`コンシューマー チェックポイント以上の場合、コンシューマーはダウンストリーム MySQL で DDL ステートメントを実行します。

次に、コンシューマーは`CDC000001.json`ファイルの複製を開始します。

次の例では、 `test/tbl_1/437752935075545091/schema.json`ファイル内の DDL クエリ ステートメントが空ではありません。

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

コンシューマーがディレクトリを再度走査すると、テーブルの新しいバージョンディレクトリが見つかります。コンシューマーが新しいディレクトリのデータを使用できるのは、 `test/tbl_1/437752935075545091`のディレクトリ内のすべてのファイルが消費された後のみであることに注意してください。

    ├── metadata
    └── test
        ├── tbl_1
        │   ├── 437752935075545091
        │   │   ├── CDC000001.json
        │   │   └── schema.json
        │   └── 437752935075546092
        │   │   └── CDC000001.json
        │   │   └── schema.json

消費ロジックは一貫しています。具体的には、コンシューマーは`schema.json`ファイルのテーブルスキーマを解析し、それに応じたDDLクエリステートメントを取得して処理します。その後、コンシューマーは`CDC000001.json`ファイルのレプリケーションを開始します。

## DMLイベントを処理する {#process-dml-events}

DDL イベントが適切に処理された後、特定のファイル形式 (CSV または Canal-JSON) とファイル番号に基づいて、 `{schema}/{table}/{table-version-separator}/`ディレクトリ内の DML イベントを処理できます。

TiCDCは、データが少なくとも1回は複製されることを保証します。そのため、重複データが存在する可能性があります。変更データのコミットtsをコンシューマーチェックポイントと比較する必要があります。コミットtsがコンシューマーチェックポイントより小さい場合は、重複排除を実行する必要があります。
