---
title: FLASHBACK DATABASE
summary: Learn the usage of FLASHBACK DATABASE in TiDB databases.
---

# フラッシュバックデータベース {#flashback-database}

TiDB v6.4.0 では`FLASHBACK DATABASE`構文が導入されています。 `FLASHBACK DATABASE`使用すると、ガベージ コレクション (GC) の有効期間内に`DROP`ステートメントによって削除されたデータベースとそのデータを復元できます。

[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)システム変数を構成することで、履歴データの保存期間を設定できます。デフォルト値は`10m0s`です。次の SQL ステートメントを使用して、現在の`safePoint` 、つまり GC が実行された時点までをクエリできます。

```sql
SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
```

`tikv_gc_safe_point`回後に`DROP`でデータベースが削除されていれば、 `FLASHBACK DATABASE`を使用してデータベースを復元できます。

## 構文 {#syntax}

```sql
FLASHBACK DATABASE DBName [TO newDBName]
```

### あらすじ {#synopsis}

```ebnf+diagram
FlashbackDatabaseStmt ::=
    'FLASHBACK' DatabaseSym DBName FlashbackToNewName
FlashbackToNewName ::=
    ( 'TO' Identifier )?
```

## ノート {#notes}

-   `tikv_gc_safe_point`回より前にデータベースが削除された場合、 `FLASHBACK DATABASE`ステートメントを使用してデータを復元することはできません。 `FLASHBACK DATABASE`ステートメントは、 `ERROR 1105 (HY000): Can't find dropped database 'test' in GC safe point 2022-11-06 16:10:10 +0800 CST`と同様のエラーを返します。

-   `FLASHBACK DATABASE`ステートメントを使用して同じデータベースを複数回復元することはできません。 `FLASHBACK DATABASE`で復元されたデータベースは元のデータベースと同じスキーマ ID を持つため、同じデータベースを複数回復元するとスキーマ ID が重複します。 TiDB では、データベース スキーマ ID はグローバルに一意である必要があります。

-   TiDB Binlogが有効になっている場合、 `FLASHBACK DATABASE`を使用するときは次の点に注意してください。

    -   ダウンストリームのセカンダリ データベースは`FLASHBACK DATABASE`をサポートする必要があります。
    -   セカンダリ データベースの GC 存続期間は、プライマリ データベースの GC 存続期間よりも長い必要があります。そうしないと、アップストリームとダウンストリーム間のレイテンシー、ダウンストリームでのデータ復元エラーが発生する可能性があります。
    -   TiDB Binlogレプリケーションでエラーが発生した場合は、TiDB Binlog内のデータベースをフィルタリングして除外し、このデータベースの完全なデータを手動でインポートする必要があります。

## 例 {#example}

-   `DROP`によって削除された`test`データベースを復元します。

    ```sql
    DROP DATABASE test;
    ```

    ```sql
    FLASHBACK DATABASE test;
    ```

-   `DROP`によって削除された`test`データベースを復元し、名前を`test1`に変更します。

    ```sql
    DROP DATABASE test;
    ```

    ```sql
    FLASHBACK DATABASE test TO test1;
    ```

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。
