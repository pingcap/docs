---
title: RECOVER TABLE
summary: TiDB データベースの RECOVER TABLE の使用法の概要。
---

# テーブルの回復 {#recover-table}

`RECOVER TABLE` 、 `DROP TABLE`ステートメントが実行された後、GC (ガベージ コレクション) の有効期間内に削除されたテーブルとその上のデータを回復するために使用されます。

## 構文 {#syntax}

```sql
RECOVER TABLE table_name;
```

```sql
RECOVER TABLE BY JOB JOB_ID;
```

## 概要 {#synopsis}

```ebnf+diagram
RecoverTableStmt ::=
    'RECOVER' 'TABLE' ( 'BY' 'JOB' Int64Num | TableName Int64Num? )

TableName ::=
    Identifier ( '.' Identifier )?

Int64Num ::= NUM

NUM ::= intLit
```

> **注記：**
>
> テーブルが削除され、GCの有効期間が過ぎた場合、 `RECOVER TABLE`ではテーブルを回復できません。このシナリオで`RECOVER TABLE`実行すると、 `snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST`ようなエラーが返されます。

## 例 {#examples}

-   テーブル名に従って削除されたテーブルを回復します。

    ```sql
    DROP TABLE t;
    ```

    ```sql
    RECOVER TABLE t;
    ```

    このメソッドは、最近の DDL ジョブ履歴を検索し、 `DROP TABLE`タイプの最初の DDL 操作を見つけ、 `RECOVER TABLE`ステートメントで指定された 1 つのテーブル名と同じ名前を持つ削除されたテーブルを回復します。

-   使用されたテーブル`DDL JOB ID`に応じて、削除されたテーブルを回復します。

    テーブル`t`削除して別の`t`を作成し、さらに新しく作成したテーブル`t`を削除したとします。この場合、最初に削除した`t`復元するには、テーブル`DDL JOB ID`指定するメソッドを使用する必要があります。

    ```sql
    DROP TABLE t;
    ```

    ```sql
    ADMIN SHOW DDL JOBS 1;
    ```

    上記の2番目のステートメントは、テーブルの`DDL JOB ID`を検索して`t`削除するために使用されます。次の例では、IDは`53`です。

        +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
        | JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE   | SCHEMA_STATE | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | STATE  |
        +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
        | 53     | test    |            | drop table | none         | 1         | 41       | 0         | 2019-07-10 13:23:18.277 +0800 CST | synced |
        +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+

    ```sql
    RECOVER TABLE BY JOB 53;
    ```

    このメソッドは、 `DDL JOB ID`を介して削除されたテーブルを回復します。対応するDDLジョブが`DROP TABLE`タイプでない場合は、エラーが発生します。

## 実施原則 {#implementation-principle}

テーブルを削除する際、TiDBはテーブルメタデータのみを削除し、削除対象のテーブルデータ（行データとインデックスデータ）を`mysql.gc_delete_range`テーブルに書き込みます。TiDBのバックグラウンドにあるGCワーカーは、GCの有効期間を超えたキーを`mysql.gc_delete_range`テーブルから定期的に削除します。

したがって、テーブルをリカバリするには、GCワーカーがテーブルデータを削除する前に、テーブルメタデータをリカバリし、 `mysql.gc_delete_range`のテーブルから対応する行レコードを削除するだけで済みます。TiDBのスナップショット読み取りを使用して、テーブルメタデータをリカバリできます。詳細は[履歴データを読む](/read-historical-data.md)を参照してください。

テーブルのリカバリは、TiDBがスナップショット読み取りによってテーブルメタデータを取得し、 `CREATE TABLE`と同様のテーブル作成プロセスを実行することで実行されます。したがって、 `RECOVER TABLE`自体は本質的には一種のDDL操作です。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。
