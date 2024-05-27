---
title: Naming Conventions for Data Import
summary: データのインポート時の CSV、Parquet、 Aurora Snapshot、SQL ファイルの命名規則について説明します。
---

# データインポートの命名規則 {#naming-conventions-for-data-import}

TiDB Cloudには、CSV、Parquet、 Aurora Snapshot、SQL のファイル形式でデータをインポートできます。データが正常にインポートされるようにするには、次の 2 種類のファイルを準備する必要があります。

-   **スキーマファイル**。データベーススキーマファイル（オプション）とテーブルスキーマファイルをSQL形式（ `.sql` ）で準備します。テーブルスキーマファイルが提供されていない場合は、事前にターゲットデータベースに対応するテーブルを手動で作成する必要があります。
-   **データ ファイル**。データをインポートするための命名規則に準拠したデータ ファイルを準備します。データ ファイル名が要件を満たせない場合は、 [**ファイルパターン**](#file-pattern)を使用してインポート タスクを実行することをお勧めします。そうしないと、インポート タスクはインポートするデータ ファイルをスキャンできません。

## スキーマファイルの命名規則 {#naming-conventions-for-schema-files}

このセクションでは、データベースおよびテーブル スキーマ ファイルの命名規則について説明します。スキーマ ファイルの命名規則は、CSV、Parquet、 Aurora Snapshot、SQL のすべての種類のソース ファイルで同じです。

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

このセクションでは、データ ファイルの命名規則について説明します。ソース ファイルの種類に応じて、データ ファイルの命名規則は異なります。

### CSVファイル {#csv}

CSV ファイルをインポートするときは、データ ファイルに次のように名前を付けます。

`${db_name}.${table_name}${suffix}.csv.${compress}`

`${suffix}`はオプションであり、次のいずれかの形式にすることができます。xxx *`xxx`*任意の数字にすることができます。

-   *`.xxx`* 、例えば`.01`
-   *`._xxx_xxx_xxx`* 、例えば`._0_0_01`
-   *`_xxx_xxx_xxx`* 、例えば`_0_0_01`

`${compress}`は圧縮形式で、オプションです。TiDB TiDB Cloud は、 `.gzip` 、 `.gz` 、 `.zstd` 、 `.zst` 、 `.snappy`の形式をサポートしています。

たとえば、次のすべてのファイルのターゲット データベースとテーブルは`import_db`と`test_table`です。

-   `import_db.test_table.csv`
-   `import_db.test_table.01.csv`
-   `import_db.test_table._0_0_01.csv`
-   `import_db.test_table_0_0_01.csv`
-   `import_db.test_table_0_0_01.csv.gz`

> **注記：**
>
> Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。Snappy 圧縮の他のバリエーションはサポートされていません。

### 寄木細工 {#parquet}

Parquet ファイルをインポートするときは、データ ファイルに次のように名前を付けます。

`${db_name}.${table_name}${suffix}.parquet` ( `${suffix}`はオプション)

例えば：

-   `import_db.test_table.parquet`
-   `import_db.test_table.01.parquet`

### Auroraスナップショット {#aurora-snapshot}

Auroraスナップショット ファイルの場合、 `${db_name}.${table_name}/`フォルダー内の`.parquet`サフィックスを持つすべてのファイルは命名規則に準拠しています。データ ファイル名には、「az、0-9、-、_、.」で構成される任意のプレフィックスと「.parquet」サフィックスを含めることができます。

例えば：

-   `import_db.test_table/mydata.parquet`
-   `import_db.test_table/part001/mydata.parquet`
-   `import_db.test_table/part002/mydata-part002.parquet`

### 構文 {#sql}

SQL ファイルをインポートするときは、データ ファイルに次のように名前を付けます。

`${db_name}.${table_name}${suffix}.sql.${compress}`

`${suffix}`はオプションであり、次のいずれかの形式にすることができます。xxx *`xxx`*任意の数字にすることができます。

-   *`.xxx`* 、例えば`.01`
-   *`._xxx_xxx_xxx`* 、例えば`._0_0_01`
-   *`_xxx_xxx_xxx`* 、例えば`_0_0_01`

`${compress}`は圧縮形式で、オプションです。TiDB TiDB Cloud は、 `.gzip` 、 `.gz` 、 `.zstd` 、 `.zst` 、 `.snappy`の形式をサポートしています。

例えば：

-   `import_db.test_table.sql`
-   `import_db.test_table.01.sql`
-   `import_db.test_table.01.sql.gz`

SQL ファイルがデフォルト設定で TiDB Dumplingを介してエクスポートされる場合、デフォルトで命名規則に準拠します。

> **注記：**
>
> Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)である必要があります。Snappy 圧縮の他のバリエーションはサポートされていません。

## ファイルパターン {#file-pattern}

CSV または Parquet のソース データ ファイルが命名規則に準拠していない場合は、ファイル パターン機能を使用して、ソース データ ファイルとターゲット テーブル間の名前マッピング関係を確立できます。この機能は、 Auroraスナップショットおよび SQL データ ファイルをサポートしていません。

-   CSVファイルについては、 [ステップ4. CSVファイルをTiDB Cloudにインポートする](/tidb-cloud/import-csv-files.md#step-4-import-csv-files-to-tidb-cloud)の**ファイルパターン**を参照してください。
-   Parquetファイルについては、 [ステップ4. ParquetファイルをTiDB Cloudにインポートする](/tidb-cloud/import-parquet-files.md#step-4-import-parquet-files-to-tidb-cloud)の**ファイルパターン**を参照してください。
