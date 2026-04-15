---
title: Naming Conventions for Data Import
summary: データインポート時のCSV、Parquet、 Aurora Snapshot、およびSQLファイルの命名規則について学びましょう。
---

# データインポートの命名規則 {#naming-conventions-for-data-import}

TiDB Cloudには、CSV、Parquet、 Aurora Snapshot、SQLといったファイル形式でデータをインポートできます。データが正常にインポートされるようにするには、以下の2種類のファイルを準備する必要があります。

-   **スキーマファイル**。データベーススキーマファイル（オプション）とテーブルスキーマファイルを、両方ともSQL形式（ `.sql` ）で準備します。テーブルスキーマファイルが提供されていない場合は、対象データベースに該当するテーブルを事前に手動で作成する必要があります。
-   **データファイル**。データインポート用の命名規則に準拠したデータファイルを用意してください。データファイル名が要件を満たしていない場合は、[**ファイルパターン**](#file-pattern)を使用してインポートタスクを実行することをお勧めします。そうしないと、インポートタスクはインポート対象のデータファイルをスキャンできません。

## スキーマファイルの命名規則 {#naming-conventions-for-schema-files}

このセクションでは、データベースおよびテーブルのスキーマファイルの命名規則について説明します。スキーマファイルの命名規則は、CSV、Parquet、 Aurora Snapshot、SQLといったすべてのソースファイルの種類で共通です。

スキーマファイルの命名規則は以下のとおりです。

-   データベーススキーマファイル（オプション）： `${db_name}-schema-create.sql`
-   テーブルスキーマファイル: `${db_name}.${table_name}-schema.sql`

以下はデータベーススキーマファイルの例です。

-   名前: `import_db-schema-create.sql`
-   ファイルの内容:

    ```sql
    CREATE DATABASE import_db;
    ```

以下はテーブルスキーマファイルの例です。

-   名前: `import_db.test_table-schema.sql`
-   ファイルの内容:

    ```sql
    CREATE TABLE test_table (
        id INTEGER PRIMARY KEY,
        val VARCHAR(255)
    );
    ```

## データファイルの命名規則 {#naming-conventions-for-data-files}

このセクションでは、データファイルの命名規則について説明します。データファイルの命名規則は、ソースファイルの種類によって異なります。

### CSV {#csv}

CSVファイルをインポートする際は、データファイルに以下の名前を付けてください。

`${db_name}.${table_name}${suffix}.csv.${compress}`

`${suffix}`はオプションであり、 *`xxx`*任意の数字で、以下のいずれかの形式になります。

-   *`.xxx`* 、例えば`.01`
-   *`._xxx_xxx_xxx`* 、例えば`._0_0_01`
-   *`_xxx_xxx_xxx`* 、例えば`_0_0_01`

`${compress}`は圧縮フォーマットであり、オプションです。TiDB TiDB Cloud は、 `.gzip` 、 `.gz` 、 `.zstd` 、 `.zst` 、および`.snappy` 。

例えば、以下のすべてのファイルのターゲットデータベースとテーブルは`import_db`と`test_table`です。

-   `import_db.test_table.csv`
-   `import_db.test_table.01.csv`
-   `import_db.test_table._0_0_01.csv`
-   `import_db.test_table_0_0_01.csv`
-   `import_db.test_table_0_0_01.csv.gz`

> **注記：**
>
> Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)に存在する必要があります。 Snappy 圧縮の他のバリアントはサポートされていません。

### 寄木細工 {#parquet}

Parquetファイルをインポートする際は、データファイルに以下の名前を付けてください。

`${db_name}.${table_name}${suffix}.parquet` （ `${suffix}`は省略可能です）

例えば：

-   `import_db.test_table.parquet`
-   `import_db.test_table.01.parquet`

### Auroraのスナップショット {#aurora-snapshot}

Aurora Snapshot ファイルの場合、 `.parquet`フォルダー内の`${db_name}.${table_name}/`サフィックスを持つすべてのファイルは、命名規則に準拠します。データファイル名には、「az、0-9、-、_、.&quot;」で構成される任意のプレフィックスとサフィックス「.parquet」を含めることができます。

例えば：

-   `import_db.test_table/mydata.parquet`
-   `import_db.test_table/part001/mydata.parquet`
-   `import_db.test_table/part002/mydata-part002.parquet`

### SQL {#sql}

SQLファイルをインポートする際は、データファイルに以下の名前を付けてください。

`${db_name}.${table_name}${suffix}.sql.${compress}`

`${suffix}`はオプションであり、 *`xxx`*任意の数字で、以下のいずれかの形式になります。

-   *`.xxx`* 、例えば`.01`
-   *`._xxx_xxx_xxx`* 、例えば`._0_0_01`
-   *`_xxx_xxx_xxx`* 、例えば`_0_0_01`

`${compress}`は圧縮フォーマットであり、オプションです。TiDB TiDB Cloud は、 `.gzip` 、 `.gz` 、 `.zstd` 、 `.zst` 、および`.snappy` 。

例えば：

-   `import_db.test_table.sql`
-   `import_db.test_table.01.sql`
-   `import_db.test_table.01.sql.gz`

TiDB Dumplingを使用してデフォルト設定でSQLファイルをエクスポートした場合、デフォルトで命名規則に準拠します。

> **注記：**
>
> Snappy 圧縮ファイルは[公式Snappyフォーマット](https://github.com/google/snappy)に存在する必要があります。 Snappy 圧縮の他のバリアントはサポートされていません。

## ファイルパターン {#file-pattern}

ソースデータファイル（CSVまたはParquet）が命名規則に準拠していない場合は、ファイル名パターンを使用してソースデータファイルをターゲットテーブルに手動でマッピングできます。この機能は、 Aurora SnapshotおよびSQLデータファイルには対応していません。

インポートウィザードの**「宛先マッピング」**ステップで、 **「TiDB ファイル命名規則を使用して自動マッピングを行う」の**選択を解除し、 **「ソース」** 、 **「ターゲットデータベース」** 、 **「ターゲットテーブル**」の各フィールドに入力します。「**ソース」**フィールドには`*`および`?`ワイルドカードをサポートするファイル名パターンを指定できます。

-   CSV ファイルについては[ステップ4. CSVファイルをTiDB Cloudにインポートする](/tidb-cloud/import-csv-files.md#step-4-import-csv-files-to-tidb-cloud)。
-   Parquet ファイルについては、 [ステップ4. ParquetファイルをTiDB Cloudにインポートする](/tidb-cloud/import-parquet-files.md#step-4-import-parquet-files-to-tidb-cloud)。
