---
title: Naming Conventions for Data Import
summary: データのインポート時の CSV、Parquet、 Aurora Snapshot、SQL ファイルの命名規則について説明します。
---

# データインポートの命名規則 {#naming-conventions-for-data-import}

TiDB Cloudには、CSV、Parquet、 Aurora Snapshot、SQL 形式のデータをインポートできます。データを確実にインポートするには、以下の 2 種類のファイルを準備する必要があります。

-   **スキーマファイル**。データベーススキーマファイル（オプション）とテーブルスキーマファイルをSQL形式（ `.sql` ）で用意します。テーブルスキーマファイルが提供されていない場合は、事前に対象データベースに対応するテーブルを手動で作成する必要があります。
-   **データファイル**。データのインポートに使用する命名規則に準拠したデータファイルを用意してください。データファイル名が要件を満たしていない場合は、 [**ファイルパターン**](#file-pattern)使用してインポートタスクを実行することをお勧めします。そうでない場合、インポートタスクはインポートするデータファイルをスキャンできません。

## スキーマファイルの命名規則 {#naming-conventions-for-schema-files}

このセクションでは、データベースとテーブルのスキーマファイルの命名規則について説明します。スキーマファイルの命名規則は、CSV、Parquet、 Aurora Snapshot、SQL のすべてのソースファイルで共通です。

スキーマ ファイルの命名規則は次のとおりです。

-   データベーススキーマファイル（オプション）: `${db_name}-schema-create.sql`
-   テーブルスキーマファイル: `${db_name}.${table_name}-schema.sql`

以下はデータベース スキーマ ファイルの例です。

-   名前: `import_db-schema-create.sql`
-   ファイルの内容:

    ```sql
    CREATE DATABASE import_db;
    ```

以下はテーブル スキーマ ファイルの例です。

-   名前: `import_db.test_table-schema.sql`
-   ファイルの内容:

    ```sql
    CREATE TABLE test_table (
        id INTEGER PRIMARY KEY,
        val VARCHAR(255)
    );
    ```

## データファイルの命名規則 {#naming-conventions-for-data-files}

このセクションでは、データファイルの命名規則について説明します。ソースファイルの種類に応じて、データファイルの命名規則は異なります。

### CSV {#csv}

CSV ファイルをインポートする場合は、データ ファイルに次のように名前を付けます。

`${db_name}.${table_name}${suffix}.csv.${compress}`

`${suffix}`はオプションであり、次のいずれかの形式を指定できます。xxx *`xxx`*任意の数字です。

-   *`.xxx`* （例： `.01`
-   *`._xxx_xxx_xxx`* （例： `._0_0_01`
-   *`_xxx_xxx_xxx`* （例： `_0_0_01`

`${compress}`は圧縮形式で、オプションです。TiDB TiDB Cloud は`.gzip` 、 `.gz` 、 `.zstd` 、 `.zst` 、 `.snappy`の形式をサポートしています。

たとえば、次のすべてのファイルのターゲット データベースとテーブルは`import_db`と`test_table`です。

-   `import_db.test_table.csv`
-   `import_db.test_table.01.csv`
-   `import_db.test_table._0_0_01.csv`
-   `import_db.test_table_0_0_01.csv`
-   `import_db.test_table_0_0_01.csv.gz`

> **注記：**
>
> Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。その他の Snappy 圧縮形式はサポートされていません。

### 寄木細工 {#parquet}

Parquet ファイルをインポートするときは、データ ファイルに次のように名前を付けます。

`${db_name}.${table_name}${suffix}.parquet` （ `${suffix}`はオプション）

例えば：

-   `import_db.test_table.parquet`
-   `import_db.test_table.01.parquet`

### Auroraスナップショット {#aurora-snapshot}

Aurora Snapshotファイルの場合、 `${db_name}.${table_name}/`フォルダ内のサフィックスが`.parquet`であるすべてのファイルは命名規則に準拠しています。データファイル名には、「az、0-9、-、_、.」からなる任意のプレフィックスと「.parquet」サフィックスを含めることができます。

例えば：

-   `import_db.test_table/mydata.parquet`
-   `import_db.test_table/part001/mydata.parquet`
-   `import_db.test_table/part002/mydata-part002.parquet`

### SQL {#sql}

SQL ファイルをインポートするときは、データ ファイルに次のように名前を付けます。

`${db_name}.${table_name}${suffix}.sql.${compress}`

`${suffix}`はオプションであり、次のいずれかの形式を指定できます。xxx *`xxx`*任意の数字です。

-   *`.xxx`* 、例えば`.01`
-   *`._xxx_xxx_xxx`* （例： `._0_0_01`
-   *`_xxx_xxx_xxx`* （例： `_0_0_01`

`${compress}`は圧縮形式で、オプションです。TiDB TiDB Cloud は`.gzip` 、 `.gz` 、 `.zstd` 、 `.zst` 、 `.snappy`の形式をサポートしています。

例えば：

-   `import_db.test_table.sql`
-   `import_db.test_table.01.sql`
-   `import_db.test_table.01.sql.gz`

SQL ファイルがデフォルト設定で TiDB Dumplingを介してエクスポートされる場合、デフォルトで命名規則に準拠します。

> **注記：**
>
> Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。その他の Snappy 圧縮形式はサポートされていません。

## ファイルパターン {#file-pattern}

CSVまたはParquetのソースデータファイルが命名規則に準拠していない場合、ファイルパターン機能を使用して、ソースデータファイルとターゲットテーブル間の名前マッピング関係を確立できます。この機能は、 Aurora SnapshotおよびSQLデータファイルはサポートしていません。

-   CSVファイルについては、 [ステップ4. CSVファイルをTiDB Cloudにインポートする](/tidb-cloud/import-csv-files.md#step-4-import-csv-files-to-tidb-cloud)の**「詳細設定」** &gt; **「マッピング設定」**を参照してください。
-   Parquetファイルについては、 [ステップ4. ParquetファイルをTiDB Cloudにインポートする](/tidb-cloud/import-parquet-files.md#step-4-import-parquet-files-to-tidb-cloud)の**「詳細設定」** &gt; **「マッピング設定」**を参照してください。
