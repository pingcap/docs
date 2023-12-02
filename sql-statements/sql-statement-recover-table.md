---
title: RECOVER TABLE
summary: An overview of the usage of RECOVER TABLE for the TiDB database.
---

# テーブルを回復する {#recover-table}

`RECOVER TABLE`は、 `DROP TABLE`ステートメントの実行後、GC (ガベージ コレクション) の有効期間内に削除されたテーブルとそのデータを回復するために使用されます。

## 構文 {#syntax}

```sql
RECOVER TABLE table_name;
```

```sql
RECOVER TABLE BY JOB JOB_ID;
```

## あらすじ {#synopsis}

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
> -   テーブルが削除され、GC ライフタイムが切れた場合、テーブルを`RECOVER TABLE`で回復することはできません。このシナリオで`RECOVER TABLE`を実行すると、次のようなエラーが返されます: `snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST` 。
>
> -   TiDB バージョンが 3.0.0 以降の場合、TiDB Binlog を使用するときに`RECOVER TABLE`を使用することはお勧めできません。
>
> -   `RECOVER TABLE`はBinlogバージョン 3.0.1 でサポートされているため、次の 3 つの状況では`RECOVER TABLE`使用できます。
>
>     -   Binlogバージョンは 3.0.1 以降です。
>     -   TiDB 3.0 は、アップストリーム クラスターとダウンストリーム クラスターの両方で使用されます。
>     -   セカンダリ クラスターの GC ライフタイムは、プライマリ クラスターの GC ライフタイムよりも長くなければなりません。ただし、アップストリーム データベースとダウンストリーム データベース間のデータ レプリケーション中にレイテンシーが発生するため、ダウンストリームでデータの回復が失敗する可能性があります。

<CustomContent platform="tidb">

**TiDB Binlogレプリケーション中のエラーのトラブルシューティング**

TiDB Binlogレプリケーション中にアップストリーム TiDB で`RECOVER TABLE`使用すると、次の 3 つの状況で TiDB Binlog が中断される可能性があります。

-   ダウンストリーム データベースは`RECOVER TABLE`ステートメントをサポートしていません。エラーインスタンス: `check the manual that corresponds to your MySQL server version for the right syntax to use near 'RECOVER TABLE table_name'` 。

-   GC ライフタイムは、上流データベースと下流データベースの間で一致しません。エラーインスタンス: `snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST` 。

-   アップストリーム データベースとダウンストリーム データベース間のレプリケーション中に遅延が発生します。エラーインスタンス: `snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST` 。

上記の 3 つの状況の場合、 [削除されたテーブルの完全インポート](/ecosystem-tool-user-guide.md#backup-and-restore---backup--restore-br)を使用して TiDB Binlogからデータ レプリケーションを再開できます。

</CustomContent>

## 例 {#examples}

-   テーブル名に従って、削除されたテーブルを復元します。

    ```sql
    DROP TABLE t;
    ```

    ```sql
    RECOVER TABLE t;
    ```

    このメソッドは、最近の DDL ジョブ履歴を検索してタイプ`DROP TABLE`の最初の DDL 操作を特定し、削除されたテーブルをステートメント`RECOVER TABLE`で指定されたテーブル名と同じ名前で回復します。

-   使用されているテーブルの`DDL JOB ID`に従って、削除されたテーブルを復元します。

    テーブル`t`削除して別の`t`を作成し、さらに新しく作成した`t`削除したとします。そして、最初に削除した`t`を復元したい場合は、 `DDL JOB ID`指定する方法を使用する必要があります。

    ```sql
    DROP TABLE t;
    ```

    ```sql
    ADMIN SHOW DDL JOBS 1;
    ```

    上記の 2 番目のステートメントは、テーブルの`DDL JOB ID`検索して`t`を削除するために使用されます。次の例では、ID は`53`です。

        +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
        | JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE   | SCHEMA_STATE | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | STATE  |
        +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
        | 53     | test    |            | drop table | none         | 1         | 41       | 0         | 2019-07-10 13:23:18.277 +0800 CST | synced |
        +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+

    ```sql
    RECOVER TABLE BY JOB 53;
    ```

    このメソッドは、削除されたテーブルを`DDL JOB ID`を介して復元します。対応する DDL ジョブが`DROP TABLE`タイプでない場合、エラーが発生します。

## 実施原則 {#implementation-principle}

テーブルを削除する場合、TiDB はテーブルのメタデータのみを削除し、削除するテーブル データ (行データおよびインデックス データ) を`mysql.gc_delete_range`のテーブルに書き込みます。 TiDB バックグラウンドの GC ワーカーは、GC の有効期間を超えたキーを`mysql.gc_delete_range`テーブルから定期的に削除します。

したがって、テーブルを回復するには、GC ワーカーがテーブル データを削除する前に、テーブルのメタデータを回復し、テーブル`mysql.gc_delete_range`内の対応する行レコードを削除するだけで済みます。 TiDB のスナップショット読み取りを使用して、テーブルのメタデータを回復できます。詳細は[履歴データの読み取り](/read-historical-data.md)を参照してください。

テーブルのリカバリは、TiDB がスナップショット読み取りを通じてテーブル メタデータを取得し、その後`CREATE TABLE`と同様のテーブル作成プロセスを経ることによって行われます。したがって、 `RECOVER TABLE`自体は本質的には一種の DDL 操作です。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。
