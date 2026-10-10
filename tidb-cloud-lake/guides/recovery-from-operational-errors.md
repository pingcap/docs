---
title: 運用エラーからのリカバリ
summary: このガイドでは、{{{ .lake }}} における一般的な運用エラーからリカバリするための手順を段階的に説明します。
---

# 運用エラーからのリカバリ

このガイドでは、{{{ .lake }}} における一般的な運用エラーからリカバリするための手順を段階的に説明します。

## はじめに {#introduction}

{{{ .lake }}} は、次のような一般的な運用エラーからのリカバリに役立ちます。

- **誤ってデータベースを削除した**
- **誤ってテーブルを削除した**
- **誤ったデータ変更（UPDATE/DELETE 操作）**
- **誤ってテーブルを TRUNCATE した**
- **データのロード (load) ミス**
- **Schema Evolution のロールバック**（テーブル構造の変更を元に戻すこと）
- **削除されたカラムまたは制約**

これらのリカバリ機能は、異なる時点のデータのスナップショットを維持する、Git ライクなストレージ設計を持つ {{{ .lake }}} の FUSE エンジンによって実現されています。

## リカバリのシナリオと解決策 {#recovery-scenarios-and-solutions}

### シナリオ: 誤ってデータベースを削除した {#scenario-accidentally-dropped-database}

誤ってデータベースを削除した場合は、`UNDROP DATABASE` コマンドを使用して復元できます。

1. 削除されたデータベースを特定します。

    ```sql
   SHOW DROP DATABASES LIKE '%sales_data%';
    ```

2. 削除されたデータベースを復元します。

   ```sql
   UNDROP DATABASE sales_data;
   ```

3. データベースが復元されたことを確認します。

   ```sql
   SHOW DATABASES;
   ```

4. 所有権を復元します（必要な場合）。

   ```sql
   GRANT OWNERSHIP on sales_data.* to ROLE <role_name>;
   ```

> **Important:**
>
> 削除されたデータベースを復元できるのは、保持期間内のみです（デフォルトは 24 時間）。

詳細は、[UNDROP DATABASE](/tidb-cloud-lake/sql/undrop-database.md) および [SHOW DROP DATABASES](/tidb-cloud-lake/sql/show-drop-databases.md) を参照してください。

### シナリオ: 誤ってテーブルを削除した {#scenario-accidentally-dropped-table}

誤ってテーブルを削除した場合は、`UNDROP TABLE` コマンドを使用して復元できます。

1. 削除されたテーブルを特定します。

   ```sql
   SHOW DROP TABLES LIKE '%order%';
   ```

2. 削除されたテーブルを復元します。

   ```sql
   UNDROP TABLE sales_data.orders;
   ```

3. テーブルが復元されたことを確認します。

   ```sql
   SHOW TABLES FROM sales_data;
   ```

4. 所有権を復元します（必要な場合）。

   ```sql
   GRANT OWNERSHIP on sales_data.orders to ROLE <role_name>;
   ```

> **Important:**
>
> 削除されたテーブルを復元できるのは、保持期間内のみです（デフォルトは 24 時間）。

詳細は、[UNDROP TABLE](/tidb-cloud-lake/sql/undrop-table.md) および [SHOW DROP TABLES](/tidb-cloud-lake/sql/show-drop-tables.md) を参照してください。

### シナリオ: 誤ったデータ更新または削除 {#scenario-incorrect-data-updates-or-deletions}

テーブル内のデータを誤って変更または削除した場合は、`FLASHBACK TABLE` コマンドを使用して以前の状態に復元できます。

1. 誤った操作を行う前の snapshot ID またはタイムスタンプを特定します。

    ```sql
    SELECT * FROM fuse_snapshot('sales_data', 'orders');
    ```

    ```text
    snapshot_id: c5c538d6b8bc42f483eefbddd000af7d
    snapshot_location: 29356/44446/_ss/c5c538d6b8bc42f483eefbddd000af7d_v2.json
    format_version: 2
    previous_snapshot_id: NULL
    [... ...]
    timestamp: 2023-04-19 04:20:25.062854
    ```

2. テーブルを以前の状態に復元します。

    ```sql
    -- Using snapshot ID
    ALTER TABLE sales_data.orders FLASHBACK TO (SNAPSHOT => 'c5c538d6b8bc42f483eefbddd000af7d');

    -- Or using timestamp
    ALTER TABLE sales_data.orders FLASHBACK TO (TIMESTAMP => '2023-04-19 04:20:25.062854'::TIMESTAMP);
    ```

3. データが復元されたことを確認します。

    ```sql
    SELECT * FROM sales_data.orders LIMIT 3;
    ```

> **Important:**
>
> Flashback 操作は、既存のテーブルに対してのみ、かつ保持期間内でのみ実行できます。

詳細は、[FLASHBACK TABLE](/tidb-cloud-lake/sql/flashback-table.md) を参照してください。

### シナリオ: Schema Evolution のロールバック {#scenario-schema-evolution-rollbacks}

テーブル構造に意図しない変更を加えてしまった場合は、以前のスキーマに戻すことができます。

1. テーブルを作成し、データを追加します。

    ```sql
    CREATE OR REPLACE TABLE customers (id INT, name VARCHAR, email VARCHAR);
    INSERT INTO customers VALUES (1, 'John', 'john@example.com');
    ```

2. スキーマを変更します。

    ```sql
    ALTER TABLE customers ADD COLUMN phone VARCHAR;
    DESC customers;
    ```

    出力:

    ```text
    ┌─────────┬─────────┬──────┬─────────┬─────────┐
    │ Field   │ Type    │ Null │ Default │ Extra   │
    ├─────────┼─────────┼──────┼─────────┼─────────┤
    │ id      │ INT     │ YES  │ NULL    │         │
    │ name    │ VARCHAR │ YES  │ NULL    │         │
    │ email   │ VARCHAR │ YES  │ NULL    │         │
    │ phone   │ VARCHAR │ YES  │ NULL    │         │
    └─────────┴─────────┴──────┴─────────┴─────────┘
    ```

3. スキーマ変更前の snapshot ID を見つけます。

    ```sql
    SELECT * FROM fuse_snapshot('default', 'customers');
    ```

    出力:

    ```text
    snapshot_id: 01963cefafbb785ea393501d2e84a425  timestamp: 2025-04-16 04:51:03.227000  previous_snapshot_id: 01963ce9cc29735b87886a08d3ca7e2f
    snapshot_id: 01963ce9cc29735b87886a08d3ca7e2f  timestamp: 2025-04-16 04:44:37.289000  previous_snapshot_id: NULL
    ```

4. 以前のスキーマに戻します（前の snapshot を使用）。

    ```sql
    ALTER TABLE customers FLASHBACK TO (SNAPSHOT => '01963ce9cc29735b87886a08d3ca7e2f');
    ```

5. スキーマが復元されたことを確認します。

    ```sql
    DESC customers;
    ```

    出力:

    ```text
    ┌─────────┬─────────┬──────┬─────────┬─────────┐
    │ Field   │ Type    │ Null │ Default │ Extra   │
    ├─────────┼─────────┼──────┼─────────┼─────────┤
    │ id      │ INT     │ YES  │ NULL    │         │
    │ name    │ VARCHAR │ YES  │ NULL    │         │
    │ email   │ VARCHAR │ YES  │ NULL    │         │
    └─────────┴─────────┴──────┴─────────┴─────────┘
    ```

## 重要な考慮事項と制限 {#important-considerations-and-limitations}

- **時間の制約**: リカバリは保持期間内でのみ機能します（デフォルト: 24 時間）。
- **名前の競合**: 同じ名前のオブジェクトが存在する場合、undrop はできません。先に[データベース名を変更](/tidb-cloud-lake/sql/alter-database.md)または[テーブル名を変更](/tidb-cloud-lake/sql/rename-table.md)してください。
- **所有権**: 所有権は自動的には復元されないため、リカバリ後に手動で付与してください。
- **Transient Tables**: transient table では Flashback は機能しません（snapshot が保存されないため）。

**緊急時**: 重大なデータ損失が発生した場合は、すぐに {{{ .lake }}} Support に連絡して支援を受けてください。