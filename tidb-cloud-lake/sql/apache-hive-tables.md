---
title: Apache Hive Tables
summary: "Apache Hive によってカタログ化されたデータは、コピーせずに {{{ .lake }}} からクエリできます。Hive Metastore を {{{ .lake }}} のカタログとして登録し、テーブルデータを保持するオブジェクトストレージを指定すると、それらのテーブルを {{{ .lake }}} ネイティブのオブジェクトであるかのようにクエリできます。"
---

# Apache Hive Tables

Apache Hive によってカタログ化されたデータは、コピーせずに {{{ .lake }}} からクエリできます。Hive Metastore を {{{ .lake }}} のカタログとして登録し、テーブルデータを保持するオブジェクトストレージを指定すると、それらのテーブルを {{{ .lake }}} ネイティブのオブジェクトであるかのようにクエリできます。

## クイックスタート {#quick-start}

1. **Hive Metastore を登録する**

   ```sql
   CREATE CATALOG hive_prod
   TYPE = HIVE
   CONNECTION = (
     METASTORE_ADDRESS = '127.0.0.1:9083'
     URL = 's3://lakehouse/'
     ACCESS_KEY_ID = '<your_key_id>'
     SECRET_ACCESS_KEY = '<your_secret_key>'
   );
   ```

2. **カタログを確認する**

   ```sql
   USE CATALOG hive_prod;
   SHOW DATABASES;
   SHOW TABLES FROM tpch;
   ```

3. **Hive テーブルをクエリする**

   ```sql
   SELECT l_orderkey, SUM(l_extendedprice) AS revenue
   FROM tpch.lineitem
   GROUP BY l_orderkey
   ORDER BY revenue DESC
   LIMIT 10;
   ```

## メタデータを最新の状態に保つ {#keep-metadata-fresh}

Hive のスキーマやパーティションは、{{{ .lake }}} の外部で変更されることがあります。その場合は、{{{ .lake }}} にキャッシュされたメタデータを更新してください。

```sql
ALTER TABLE tpch.lineitem REFRESH CACHE;
```

## データ型のマッピング {#data-type-mapping}

クエリ実行時、{{{ .lake }}} は Hive のプリミティブ型を最も近いネイティブ型に自動変換します。

| Hive 型 | {{{ .lake }}} 型 |
| --------- | ------------- |
| `BOOLEAN` | [BOOLEAN](/tidb-cloud-lake/sql/boolean.md) |
| `TINYINT`, `SMALLINT`, `INT`, `BIGINT` | [整数型](/tidb-cloud-lake/sql/numeric.md#integer-data-types) |
| `FLOAT`, `DOUBLE` | [浮動小数点型](/tidb-cloud-lake/sql/numeric.md#floating-point-data-types) |
| `DECIMAL(p,s)` | [DECIMAL](/tidb-cloud-lake/sql/decimal.md) |
| `STRING`, `VARCHAR`, `CHAR` | [STRING](/tidb-cloud-lake/sql/string.md) |
| `DATE`, `TIMESTAMP` | [DATETIME](/tidb-cloud-lake/sql/datetime.md) |
| `ARRAY<type>` | [ARRAY](/tidb-cloud-lake/sql/array.md) |
| `MAP<key,value>` | [MAP](/tidb-cloud-lake/sql/map.md) |

`STRUCT` のようなネストされた構造は、[VARIANT](/tidb-cloud-lake/sql/variant.md) 型として公開されます。

## 注意事項と制限 {#notes-and-limitations}

- Hive カタログは {{{ .lake }}} では**読み取り専用**です（書き込みは Hive 互換エンジン経由で行う必要があります）。
- 基盤となるオブジェクトストレージへのアクセスが必要です。認証情報は [接続パラメータ](/tidb-cloud-lake/sql/connection-parameters.md) を使用して設定してください。
- テーブルレイアウトが変更された場合（たとえば新しいパーティションが追加された場合）は、クエリ結果を最新の状態に保つために `ALTER TABLE ... REFRESH CACHE` を使用してください。