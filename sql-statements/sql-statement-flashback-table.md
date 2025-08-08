---
title: FLASHBACK TABLE
summary: FLASHBACK TABLE` ステートメントを使用してテーブルを回復する方法を学習します。
---

# フラッシュバックテーブル {#flashback-table}

`FLASHBACK TABLE`構文は TiDB 4.0 以降で導入されました。3 ステートメント`FLASHBACK TABLE`使用すると、ガベージコレクション (GC) の有効期間中に`DROP`または`TRUNCATE`操作によって削除されたテーブルとデータを復元できます。

システム変数[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) （デフォルト: `10m0s` ）は、以前のバージョンの行の保持期間を定義します。ガベージコレクションが実行された現在の`safePoint`間は、次のクエリで取得できます。

```sql
SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
```

`tikv_gc_safe_point`回目以降に`DROP`または`TRUNCATE`ステートメントでテーブルが削除されている限り、 `FLASHBACK TABLE`ステートメントを使用してテーブルを復元できます。

## 構文 {#syntax}

```sql
FLASHBACK TABLE table_name [TO other_table_name]
```

## 概要 {#synopsis}

```ebnf+diagram
FlashbackTableStmt ::=
    'FLASHBACK' 'TABLE' TableName FlashbackToNewName

TableName ::=
    Identifier ( '.' Identifier )?

FlashbackToNewName ::=
    ( 'TO' Identifier )?
```

## 注記 {#notes}

テーブルが削除され、GCの有効期間が過ぎた場合、 `FLASHBACK TABLE`ステートメントを使用して削除されたデータを回復することはできなくなります。そうでない場合は、 `Can't find dropped / truncated table 't' in GC safe point 2020-03-16 16:34:52 +0800 CST`ようなエラーが返されます。

## 例 {#example}

-   `DROP`操作で削除されたテーブル データを回復します。

    ```sql
    DROP TABLE t;
    ```

    ```sql
    FLASHBACK TABLE t;
    ```

-   操作`TRUNCATE`で削除されたテーブルデータを復元します。切り捨てられたテーブル`t`まだ存在するため、復元するテーブル`t`名前を変更する必要があります。変更しないと、テーブル`t`既に存在するためエラーが返されます。

    ```sql
    TRUNCATE TABLE t;
    ```

    ```sql
    FLASHBACK TABLE t TO t1;
    ```

## 実施原則 {#implementation-principle}

テーブルを削除する際、TiDBはテーブルメタデータのみを削除し、削除対象のテーブルデータ（行データとインデックスデータ）を`mysql.gc_delete_range`テーブルに書き込みます。TiDBのバックグラウンドにあるGCワーカーは、GCの有効期間を超えたキーを`mysql.gc_delete_range`テーブルから定期的に削除します。

したがって、テーブルをリカバリするには、GCワーカーがテーブルデータを削除する前に、テーブルメタデータをリカバリし、 `mysql.gc_delete_range`のテーブルから対応する行レコードを削除するだけで済みます。テーブルメタデータのリカバリには、TiDBのスナップショット読み取りを使用できます。スナップショット読み取りの詳細については、 [履歴データを読む](/read-historical-data.md)を参照してください。

`FLASHBACK TABLE t TO t1`の作業工程は以下のとおりです。

1.  TiDBは最近のDDL履歴ジョブを検索し、テーブル`t`で最初のDDL操作（タイプ`DROP TABLE`またはタイプ`truncate table`を見つけます。TiDBが見つけられなかった場合は、エラーが返されます。
2.  TiDBは、DDLジョブの開始時刻が`tikv_gc_safe_point`より前かどうかを確認します。3 `tikv_gc_safe_point`前の場合、 `DROP`または`TRUNCATE`操作で削除されたテーブルがGCによってクリーンアップされたことを意味し、エラーが返されます。
3.  TiDB は、DDL ジョブの開始時刻をスナップショットとして使用して、履歴データを読み取り、テーブル メタデータを読み取ります。
4.  TiDB は`mysql.gc_delete_range`のテーブル`t`に関連する GC タスクを削除します。
5.  TiDBはテーブルのメタデータの`name` `t1`に変更し、このメタデータを使用して新しいテーブルを作成します。テーブル名のみが変更され、テーブルIDは変更されないことに注意してください。テーブルIDは、以前に削除されたテーブル`t`と同じです。

上記のプロセスから、TiDBは常にテーブルのメタデータに対して操作を行い、テーブルのユーザーデータは変更されていないことがわかります。復元されたテーブル`t1` 、以前に削除されたテーブル`t`と同じIDを持つため、テーブル`t1` `t`のユーザーデータを読み取ることができます。

> **注記：**
>
> 復元されたテーブルの ID は削除されたテーブルの ID と同じであり、TiDB では既存のすべてのテーブルにグローバルに一意のテーブル ID が必要であるため、 `FLASHBACK`ステートメントを使用して同じ削除されたテーブルを複数回復元することはできません。

`FLASHBACK TABLE`操作は、TiDBがスナップショット読み取りによってテーブルメタデータを取得し、 `CREATE TABLE`と同様のテーブル作成プロセスを実行することで実行されます。したがって、 `FLASHBACK TABLE`本質的には一種のDDL操作です。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。
