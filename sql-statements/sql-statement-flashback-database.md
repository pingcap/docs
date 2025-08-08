---
title: FLASHBACK DATABASE
summary: TiDB データベースでの FLASHBACK DATABASE の使用方法を学習します。
---

# フラッシュバックデータベース {#flashback-database}

TiDB v6.4.0 では`FLASHBACK DATABASE`構文が導入されました。3 `FLASHBACK DATABASE`使用すると、ガベージコレクション (GC) の有効期間内に`DROP`ステートメントによって削除されたデータベースとそのデータを復元できます。

履歴データの保持期間は、システム変数[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)設定することで設定できます。デフォルト値は`10m0s`です。現在の`safePoint` 、つまりGCが実行された時点までを照会するには、次のSQL文を使用します。

```sql
SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
```

`tikv_gc_safe_point`回目以降に`DROP`でデータベースが削除されていれば、 `FLASHBACK DATABASE`使用してデータベースを復元できます。

## 構文 {#syntax}

```sql
FLASHBACK DATABASE DBName [TO newDBName]
```

### 概要 {#synopsis}

```ebnf+diagram
FlashbackDatabaseStmt ::=
    'FLASHBACK' DatabaseSym DBName FlashbackToNewName
FlashbackToNewName ::=
    ( 'TO' Identifier )?
```

## 注記 {#notes}

-   `tikv_gc_safe_point`回目より前にデータベースが削除された場合、 `FLASHBACK DATABASE`ステートメントを使用してデータを復元することはできません。5 `FLASHBACK DATABASE`目のステートメントは`ERROR 1105 (HY000): Can't find dropped database 'test' in GC safe point 2022-11-06 16:10:10 +0800 CST`と同様のエラーを返します。

-   `FLASHBACK DATABASE`ステートメントを使用して、同じデータベースを複数回リストアすることはできません。3 でリストアされ`FLASHBACK DATABASE`データベースは元のデータベースと同じスキーマ ID を持つため、同じデータベースを複数回リストアするとスキーマ ID が重複します。TiDB では、データベースのスキーマ ID はグローバルに一意である必要があります。

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

このステートメントは、MySQL 構文に対する TiDB 拡張です。
