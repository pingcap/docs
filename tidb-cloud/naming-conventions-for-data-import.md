---
title: Naming Conventions for Data Import
summary: Learn about the naming conventions for CSV, Parquet, Aurora Snapshot, and SQL files during data import.
---

# データ インポートの命名規則 {#naming-conventions-for-data-import}

次のファイル形式でTiDB Cloudにデータをインポートできます: CSV、Parquet、 Auroraスナップショット、および SQL。データが正常にインポートされるようにするには、次の 2 種類のファイルを準備する必要があります。

-   **スキーマ ファイル**.データベース スキーマ ファイル (オプション) とテーブル スキーマ ファイルを両方とも SQL 形式で準備します ( `.sql` )。テーブル スキーマ ファイルが提供されていない場合は、事前にターゲット データベースに対応するテーブルを手動で作成する必要があります。
-   **データ ファイル**.データをインポートするための命名規則に準拠したデータ ファイルを準備します。データ ファイル名が要件を満たさない場合は、 [**ファイル パターン**](#file-pattern)使用してインポート タスクを実行することをお勧めします。そうしないと、インポート タスクは、インポートするデータ ファイルをスキャンできません。

## スキーマ ファイルの命名規則 {#naming-conventions-for-schema-files}

このセクションでは、データベースおよびテーブル スキーマ ファイルの命名規則について説明します。スキーマ ファイルの命名規則は、CSV、Parquet、 Auroraスナップショット、および SQL のすべての種類のソース ファイルで同じです。

スキーマ ファイルの命名規則は次のとおりです。

-   データベース スキーマ ファイル (オプション): `${db_name}-schema-create.sql`
-   テーブル スキーマ ファイル: `${db_name}.${table_name}-schema.sql`

以下は、データベース スキーマ ファイルの例です。

-   名前: `import_db-schema-create.sql`
-   ファイルの内容:

    ```sql
    CREATE DATABASE import_db;
    ```

以下は、テーブル スキーマ ファイルの例です。

-   名前: `import_db.test_table-schema.sql`
-   ファイルの内容:

    ```sql
    CREATE TABLE test_table (
        id INTEGER PRIMARY KEY,
        val VARCHAR(255)
    );
    ```

## データ ファイルの命名規則 {#naming-conventions-for-data-files}

このセクションでは、データ ファイルの命名規則について説明します。ソース ファイルの種類によって、データ ファイルの命名規則は異なります。

### CSV {#csv}

CSV ファイルをインポートするときは、次のようにデータ ファイルに名前を付けます。

`${db_name}.${table_name}${suffix}.csv`

`${suffix}`はオプションで、次のいずれかの形式になります*`xxx`*任意の数字です。

-   *`.xxx`* 、 `.01`など
-   *`._xxx_xxx_xxx`* 、 `._0_0_01`など
-   *`_xxx_xxx_xxx`* 、 `_0_0_01`など

たとえば、次のすべてのファイルのターゲット データベースとテーブルは`import_db`と`test_table`です。

-   `import_db.test_table.csv`
-   `import_db.test_table.01.csv`
-   `import_db.test_table._0_0_01.csv`
-   `import_db.test_table_0_0_01.csv`

### 寄木細工 {#parquet}

Parquet ファイルをインポートするときは、次のようにデータ ファイルに名前を付けます。

-   `${db_name}.${table_name}${suffix}.parquet{.snappy|.gz|.lzo}` ( `${suffix}`と`{.snappy|.gz|.lzo}`はオプション)

例えば：

-   `import_db.test_table.parquet`
-   `import_db.test_table.01.parquet`
-   `import_db.test_table.parquet.gz`
-   `import_db.test_table.01.parquet.gz`

### Auroraのスナップショット {#aurora-snapshot}

Auroraスナップショット ファイルの場合、 `${db_name}.${table_name}/`フォルダー内の`.parquet`サフィックスを持つすべてのファイルは、命名規則に準拠しています。データ ファイル名には、「az、0-9、-、_、.」で構成されるプレフィックスを含めることができます。接尾辞「.parquet」。

例えば：

-   `import_db.test_table/mydata.parquet`
-   `import_db.test_table/part001/mydata.parquet`
-   `import_db.test_table/part002/mydata-part002.parquet`

### SQL {#sql}

SQL ファイルをインポートするときは、次のようにデータ ファイルに名前を付けます。

-   `${db_name}.${table_name}${suffix}.sql` ( `${suffix}`はオプション)

例えば：

-   `import_db.test_table.sql`
-   `import_db.test_table.01.sql`

デフォルト設定で TiDB Dumpling を介して SQL ファイルをエクスポートすると、デフォルトで命名規則に準拠します。

## ファイルパターン {#file-pattern}

CSV または Parquet のソース データ ファイルが命名規則に準拠していない場合、ファイル パターン機能を使用して、ソース データ ファイルとターゲット テーブル間の名前マッピング関係を確立できます。この機能は、 Auroraスナップショットと SQL データ ファイルをサポートしていません。

-   CSV ファイルについては、 [ステップ 4.CSV ファイルをTiDB Cloudにインポートする](/tidb-cloud/import-csv-files.md#step-4-import-csv-files-to-tidb-cloud)の**ファイル パターン**を参照してください。
-   Parquet ファイルについては、 [ステップ 4. Parquet ファイルをTiDB Cloudにインポートする](/tidb-cloud/import-parquet-files.md#step-4-import-parquet-files-to-tidb-cloud)の**ファイル パターン**を参照してください。
