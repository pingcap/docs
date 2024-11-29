---
title: Binlog Consumer Client User Guide
summary: Binlog Consumer Clientを使用して、Kafka から TiDB セカンダリbinlogデータを消費し、特定の形式でデータを出力します。
---

# Binlog Consumer Clientユーザー ガイド {#binlog-consumer-client-user-guide}

Binlog Consumer Client は、Kafka から TiDB セカンダリbinlogデータを消費し、特定の形式でデータを出力するために使用されます。現在、 Drainer は、MySQL、TiDB、ファイル、Kafka など、複数の種類のダウン ストリーミングをサポートしています。ただし、ユーザーが Elasticsearch や Hive などの他の形式でデータを出力するためのカスタマイズされた要件を持っている場合があるため、この機能が導入されています。

## Drainerの設定 {#configure-drainer}

Drainerの設定ファイルを変更し、データを Kafka に出力するように設定します。

    [syncer]
    db-type = "kafka"

    [syncer.to]
    # the Kafka address
    kafka-addrs = "127.0.0.1:9092"
    # the Kafka version
    kafka-version = "2.4.0"

## カスタマイズ開発 {#customized-development}

### データ形式 {#data-format}

まず、 Drainerによって Kafka に出力されるデータの形式情報を取得する必要があります。

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

データ形式の定義については[`secondary_binlog.proto`](https://github.com/pingcap/tidb/blob/release-8.1/pkg/tidb-binlog/proto/proto/secondary_binlog.proto)参照

### Driver {#driver}

[TiDB ツール](https://github.com/pingcap/tidb-tools/)プロジェクトは、Kafka でbinlogデータを読み取るために使用される[Driver](https://github.com/pingcap/tidb/tree/release-8.1/pkg/tidb-binlog/driver)提供します。これには次の機能があります。

-   Kafka データを読み取ります。
-   `commit ts`に基づいて、Kafka に保存されているbinlog を見つけます。

Driverを使用する場合は、次の情報を設定する必要があります。

-   `KafkaAddr` : Kafka クラスターのアドレス
-   `CommitTS` :binlogの読み取りを開始する`commit ts`から
-   `Offset` : どの Kafka `offset`からデータの読み取りを開始するか。4 `CommitTS`設定されている場合は、このパラメータを設定する必要はありません。
-   `ClusterID` : TiDBクラスタのクラスタID
-   `Topic` : Kafka のトピック名。Topic が空の場合は、 Drainer `<ClusterID>_obinlog`のデフォルト名を使用します。

パッケージ内のDriverコードを引用してDriverを使用し、 Driverによって提供されるサンプル コードを参照して、 Driverの使用方法とbinlogデータの解析方法を学習できます。

現在、2 つの例が提供されています。

-   Driverを使用してデータをMySQLに複製します。この例では、 binlogをSQLに変換する方法を示します。
-   Driverを使用してデータを印刷する

> **注記：**
>
> -   サンプルコードはDriverの使用方法のみを示しています。本番環境でDriver を使用する場合は、コードを最適化する必要があります。
> -   現在、 Golang版のDriverとサンプルコードのみ利用可能です。他の言語を使用する場合は、 binlog proto ファイルに基づいて該当言語のコードファイルを生成し、Kafka でbinlogデータを読み取り、データを解析して下流にデータを出力するアプリケーションを開発する必要があります。また、サンプルコードを最適化し、他の言語のサンプルコードを[TiDB ツール](https://github.com/pingcap/tidb-tools)に提出することも歓迎します。
