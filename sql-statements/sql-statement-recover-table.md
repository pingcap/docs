---
title: RECOVER TABLE
summary: TiDB データベースの RECOVER TABLE の使用法の概要。
---

# テーブルの回復 {#recover-table}

`RECOVER TABLE` 、 `DROP TABLE`ステートメントが実行された後、GC (ガベージ コレクション) の有効期間内に削除されたテーブルとそのテーブル上のデータを回復するために使用されます。

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
> テーブルが削除され、GC の有効期間が過ぎた場合、 `RECOVER TABLE`ではテーブルを回復できません。このシナリオで`RECOVER TABLE`実行すると、 `snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST`のようなエラーが返されます。

## 例 {#examples}

-   テーブル名に従って削除されたテーブルを回復します。

    ```sql
    DROP TABLE t;
    ```

    ```sql
    RECOVER TABLE t;
    ```

    このメソッドは、最近の DDL ジョブ履歴を検索し、 `DROP TABLE`番目のタイプの最初の DDL 操作を見つけて、 `RECOVER TABLE`のステートメントで指定された 1 つのテーブル名と同じ名前を持つ削除されたテーブルを回復します。

-   使用されたテーブル`DDL JOB ID`に従って、削除されたテーブルを回復します。

    テーブル`t`削除して別の`t`作成し、さらに新しく作成した`t`削除したとします。この場合、最初に削除した`t`復元するには、 `DDL JOB ID`を指定する方法を使用する必要があります。

    ```sql
    DROP TABLE t;
    ```

    ```sql
    ADMIN SHOW DDL JOBS 1;
    ```

    上記の 2 番目のステートメントは、テーブルの`DDL JOB ID`を検索して`t`削除するために使用されます。次の例では、 ID は`53`です。

        +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
        | JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE   | SCHEMA_STATE | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | STATE  |
        +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
        | 53     | test    |            | drop table | none         | 1         | 41       | 0         | 2019-07-10 13:23:18.277 +0800 CST | synced |
        +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+

    ```sql
    RECOVER TABLE BY JOB 53;
    ```

    このメソッドは、 `DDL JOB ID`介して削除されたテーブルを回復します。対応する DDL ジョブが`DROP TABLE`タイプでない場合は、エラーが発生します。

## 実施原則 {#implementation-principle}

テーブルを削除する場合、TiDB はテーブルメタデータのみを削除し、削除するテーブルデータ (行データとインデックスデータ) を`mysql.gc_delete_range`テーブルに書き込みます。TiDB のバックグラウンドの GC ワーカーは、GC ライフタイムを超えたキーを`mysql.gc_delete_range`テーブルから定期的に削除します。

したがって、テーブルを回復するには、GC ワーカーがテーブル データを削除する前に、テーブル メタデータを回復し、 `mysql.gc_delete_range`のテーブル内の対応する行レコードを削除するだけで済みます。テーブル メタデータを回復するには、TiDB のスナップショット読み取りを使用できます。詳細については、 [履歴データを読む](/read-historical-data.md)を参照してください。

テーブルのリカバリは、TiDB がスナップショット読み取りによってテーブル メタデータを取得し、 `CREATE TABLE`と同様のテーブル作成プロセスを実行することによって行われます。したがって、 `RECOVER TABLE`自体は本質的には一種の DDL 操作です。

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。
