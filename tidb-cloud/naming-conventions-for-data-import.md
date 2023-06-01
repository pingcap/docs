---
title: Naming Conventions for Data Import
summary: Learn about the naming conventions for CSV, Parquet, Aurora Snapshot, and SQL files during data import.
---

# データインポートの命名規則 {#naming-conventions-for-data-import}

データは、CSV、Parquet、 Aurora Snapshot、SQL のファイル形式でTiDB Cloudにインポートできます。データが正常にインポートされていることを確認するには、次の 2 種類のファイルを準備する必要があります。

-   **スキーマ ファイル**。データベース スキーマ ファイル (オプション) とテーブル スキーマ ファイルを両方とも SQL 形式で準備します ( `.sql` )。テーブル スキーマ ファイルが提供されていない場合は、事前にターゲット データベースに対応するテーブルを手動で作成する必要があります。
-   **データファイル**。データをインポートするための命名規則に従ったデータファイルを準備します。データ ファイル名が要件を満たさない場合は、 [**ファイルパターン**](#file-pattern)使用してインポート タスクを実行することをお勧めします。そうしないと、インポート タスクはインポートするデータ ファイルをスキャンできません。

## スキーマファイルの命名規則 {#naming-conventions-for-schema-files}

このセクションでは、データベースおよびテーブル スキーマ ファイルの命名規則について説明します。スキーマ ファイルの命名規則は、CSV、Parquet、 Aurora Snapshot、SQL のすべてのタイプのソース ファイルで同じです。

スキーマ ファイルの命名規則は次のとおりです。

-   データベース スキーマ ファイル (オプション): `${db_name}-schema-create.sql`
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

このセクションでは、データ ファイルの命名規則について説明します。ソース ファイルの種類に応じて、データ ファイルの命名規則が異なります。

### CSV {#csv}

CSV ファイルをインポートするときは、データ ファイルに次の名前を付けます。

-   `${db_name}.${table_name}[.XXXXXX].csv` ([.XXXXXX] はオプションです)

例えば：

-   `import_db.test_table.csv`
-   `import_db.test_table.01.csv`

### 寄木細工 {#parquet}

Parquet ファイルをインポートするときは、データ ファイルに次のような名前を付けます。

-   `${db_name}.${table_name}[.XXXXXX].parquet[.{snappy|gz|lzo}]` ( `[.XXXXXXX]`と`[.{snappy|gz|lzo}]`はオプション)

例えば：

-   `import_db.test_table.parquet`
-   `import_db.test_table.01.parquet`
-   `import_db.test_table.parquet.gz`
-   `import_db.test_table.01.parquet.gz`

### Auroraのスナップショット {#aurora-snapshot}

Aurora Snapshot ファイルの場合、 `${db_name}.${table_name}/`フォルダー内の`.parquet`サフィックスを持つすべてのファイルは命名規則に従います。データ ファイル名には、「az、0 ～ 9、-、_、.」で構成される任意のプレフィックスを含めることができます。接尾辞「.parquet」。

例えば：

-   `import_db.test_table/mydata.parquet`
-   `import_db.test_table/part001/mydata.parquet`
-   `import_db.test_table/part002/mydata-part002.parquet`

### SQL {#sql}

SQL ファイルをインポートするときは、データ ファイルに次のような名前を付けます。

-   `${db_name}.${table_name}[.XXXXXXX].sql` ([.XXXXXXX] はオプションです)

例えば：

-   `import_db.test_table.sql`
-   `import_db.test_table.01.sql`

SQL ファイルがデフォルト構成の TiDB Dumplingを介してエクスポートされる場合、デフォルトで命名規則に従います。

## ファイルパターン {#file-pattern}

CSV または Parquet のソース データ ファイルが命名規則に準拠していない場合は、ファイル パターン機能を使用して、ソース データ ファイルとターゲット テーブルの間に名前マッピング関係を確立できます。この機能は、 Auroraスナップショットと SQL データ ファイルをサポートしていません。

-   CSV ファイルについては、 [ステップ 4. CSV ファイルをTiDB Cloudにインポートする](/tidb-cloud/import-csv-files.md#step-4-import-csv-files-to-tidb-cloud)の**ファイル パターン**を参照してください。
-   Parquet ファイルについては、 [ステップ 4. Parquet ファイルをTiDB Cloudにインポートする](/tidb-cloud/import-parquet-files.md#step-4-import-parquet-files-to-tidb-cloud)の**ファイル パターン**を参照してください。
