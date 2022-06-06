---
title: Binlog Consumer Client User Guide
summary: Use Binlog Consumer Client to consume TiDB secondary binlog data from Kafka and output the data in a specific format.
---

# Binlogコンシューマークライアントユーザーガイド {#binlog-consumer-client-user-guide}

Binlog Consumer Clientは、KafkaからのTiDBセカンダリbinlogデータを消費し、特定の形式でデータを出力するために使用されます。現在、Drainerは、MySQL、TiDB、ファイル、Kafkaなど、複数の種類のダウンストリーミングをサポートしています。ただし、ElasticsearchやHiveなど、他の形式にデータを出力するための要件をカスタマイズしている場合があるため、この機能が導入されています。

## ドレイナーを構成する {#configure-drainer}

Drainerの構成ファイルを変更し、Kafkaにデータを出力するように設定します。

```
[syncer]
db-type = "kafka"

[syncer.to]
# the Kafka address
kafka-addrs = "127.0.0.1:9092"
# the Kafka version
kafka-version = "0.8.2.0"
```

## カスタマイズされた開発 {#customized-development}

### データ形式 {#data-format}

まず、DrainerによってKafkaに出力されるデータのフォーマット情報を取得する必要があります。

```
// `Column` stores the column data in the corresponding variable based on the data type.
message Column {
  // Indicates whether the data is null
  optional bool is_null = 1 [ default = false ];
  // Stores `int` data
  optional int64 int64_value = 2;
  // Stores `uint`, `enum`, and `set` data
  optional uint64 uint64_value = 3;
  // Stores `float` and `double` data
  optional double double_value = 4;
  // Stores `bit`, `blob`, `binary` and `json` data
  optional bytes bytes_value = 5;
  // Stores `date`, `time`, `decimal`, `text`, `char` data
  optional string string_value = 6;
}

// `ColumnInfo` stores the column information, including the column name, type, and whether it is the primary key.
message ColumnInfo {
  optional string name = 1 [ (gogoproto.nullable) = false ];
  // the lower case column field type in MySQL
  // https://dev.mysql.com/doc/refman/8.0/en/data-types.html
  // for the `numeric` type: int bigint smallint tinyint float double decimal bit
  // for the `string` type: text longtext mediumtext char tinytext varchar
  // blob longblob mediumblob binary tinyblob varbinary
  // enum set
  // for the `json` type: json
  optional string mysql_type = 2 [ (gogoproto.nullable) = false ];
  optional bool is_primary_key = 3 [ (gogoproto.nullable) = false ];
}

// `Row` stores the actual data of a row.
message Row { repeated Column columns = 1; }

// `MutationType` indicates the DML type.
enum MutationType {
  Insert = 0;
  Update = 1;
  Delete = 2;
}

// `Table` contains mutations in a table.
message Table {
  optional string schema_name = 1;
  optional string table_name = 2;
  repeated ColumnInfo column_info = 3;
  repeated TableMutation mutations = 4;
}

// `TableMutation` stores mutations of a row.
message TableMutation {
  required MutationType type = 1;
  // data after modification
  required Row row = 2;
  // data before modification. It only takes effect for `Update MutationType`.
  optional Row change_row = 3;
}

// `DMLData` stores all the mutations caused by DML in a transaction.
message DMLData {
  // `tables` contains all the table changes in the transaction.
  repeated Table tables = 1;
}

// `DDLData` stores the DDL information.
message DDLData {
  // the database used currently
  optional string schema_name = 1;
  // the relates table
  optional string table_name = 2;
  // `ddl_query` is the original DDL statement query.
  optional bytes ddl_query = 3;
}

// `BinlogType` indicates the binlog type, including DML and DDL.
enum BinlogType {
  DML = 0; //  Has `dml_data`
  DDL = 1; //  Has `ddl_query`
}

// `Binlog` stores all the changes in a transaction. Kafka stores the serialized result of the structure data.
message Binlog {
  optional BinlogType type = 1 [ (gogoproto.nullable) = false ];
  optional int64 commit_ts = 2 [ (gogoproto.nullable) = false ];
  optional DMLData dml_data = 3;
  optional DDLData ddl_data = 4;
}
```

データ形式の定義については、 [`secondary_binlog.proto`](https://github.com/pingcap/tidb-tools/blob/master/tidb-binlog/proto/proto/secondary_binlog.proto)を参照してください。

### 運転者 {#driver}

[TiDB-ツール](https://github.com/pingcap/tidb-tools/)のプロジェクトは[運転者](https://github.com/pingcap/tidb-tools/tree/master/tidb-binlog/driver)を提供します。これは、Kafkaのbinlogデータを読み取るために使用されます。次の機能があります。

-   Kafkaデータを読み取ります。
-   `commit ts`に基づいてKafkaに保存されているbinlogを見つけます。

Driverを使用する場合は、次の情報を構成する必要があります。

-   `KafkaAddr` ：Kafkaクラスタのアドレス
-   `CommitTS` ：どの`commit ts`からbinlogの読み取りを開始するか
-   `Offset` ： `offset`がデータの読み取りを開始する場所。 `CommitTS`が設定されている場合、このパラメーターを構成する必要はありません。
-   `ClusterID` ：TiDBクラスタのクラスタID
-   `Topic` ：カフカのトピック名。トピックが空の場合は、 `<ClusterID>_obinlog`のデフォルト名を使用します。

パッケージ内のドライバーコードを引用してドライバーを使用し、ドライバーが提供するサンプルコードを参照して、ドライバーの使用方法とbinlogデータの解析方法を学ぶことができます。

現在、2つの例が提供されています。

-   Driverを使用してデータをMySQLに複製します。この例は、binlogをSQLに変換する方法を示しています
-   ドライバを使用してデータを印刷する

> **ノート：**
>
> -   サンプルコードは、ドライバーの使用方法のみを示しています。実稼働環境でDriverを使用する場合は、コードを最適化する必要があります。
> -   現在、Golangバージョンのドライバーとサンプルコードのみが利用可能です。他の言語を使用する場合は、binlog protoファイルに基づいて対応する言語でコードファイルを生成し、Kafkaでbinlogデータを読み取り、データを解析して、データをダウンストリームに出力するアプリケーションを開発する必要があります。サンプルコードを最適化し、他の言語のサンプルコードを[TiDB-ツール](https://github.com/pingcap/tidb-tools)に送信することもできます。
