---
title: FLASHBACK DATABASE
summary: TiDB データベースでの FLASHBACK DATABASE の使用方法を学習します。
---

# フラッシュバックデータベース {#flashback-database}

TiDB v6.4.0 では`FLASHBACK DATABASE`構文が導入されています。3 `FLASHBACK DATABASE`使用すると、ガベージ コレクション (GC) の有効期間内に`DROP`ステートメントによって削除されたデータベースとそのデータを復元できます。

[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50)システム変数を設定することで、履歴データの保持時間を設定できます。デフォルト値は`10m0s`です。次の SQL 文を使用して、現在の`safePoint` 、つまり GC が実行された時点を照会できます。

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

-   `tikv_gc_safe_point`回目より前にデータベースが削除された場合、 `FLASHBACK DATABASE`ステートメントを使用してデータを復元することはできません。 `FLASHBACK DATABASE`ステートメントは`ERROR 1105 (HY000): Can't find dropped database 'test' in GC safe point 2022-11-06 16:10:10 +0800 CST`と同様のエラーを返します。

-   `FLASHBACK DATABASE`ステートメントを使用して同じデータベースを複数回復元することはできません`FLASHBACK DATABASE`で復元されたデータベースは元のデータベースと同じスキーマ ID を持つため、同じデータベースを複数回復元するとスキーマ ID が重複します。TiDB では、データベース スキーマ ID はグローバルに一意である必要があります。

-   TiDB Binlogが有効になっている場合、 `FLASHBACK DATABASE`使用するときは次の点に注意してください。

    -   ダウンストリームセカンダリデータベースは`FLASHBACK DATABASE`サポートする必要があります。
    -   セカンダリ データベースの GC ライフタイムは、プライマリ データベースの GC ライフタイムよりも長くする必要があります。そうしないと、アップストリームとダウンストリーム間のレイテンシーにより、ダウンストリームでのデータ復元が失敗する可能性があります。
    -   TiDB Binlogレプリケーションでエラーが発生した場合は、TiDB Binlog内のデータベースをフィルター処理し、このデータベースの完全なデータを手動でインポートする必要があります。

## 例 {#example}

-   `DROP`によって削除された`test`データベースを復元します。

    ```sql
    DROP DATABASE test;
    ```

    ```sql
    FLASHBACK DATABASE test;
    ```

-   `DROP`で削除された`test`データベースを復元し、名前を`test1`に変更します。

    ```sql
    DROP DATABASE test;
    ```

    ```sql
    FLASHBACK DATABASE test TO test1;
    ```

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。
