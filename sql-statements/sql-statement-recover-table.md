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
> -   テーブルが削除され、GC の有効期間が過ぎた場合、 `RECOVER TABLE`ではテーブルを回復できません。このシナリオで`RECOVER TABLE`実行すると、 `snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST`のようなエラーが返されます。
>
> -   TiDB バージョンが 3.0.0 以降の場合、TiDB Binlogを使用するときは`RECOVER TABLE`使用することはお勧めしません。
>
> -   `RECOVER TABLE`はBinlogバージョン 3.0.1 でサポートされているため、次の 3 つの状況では`RECOVER TABLE`使用できます。
>
>     -   Binlogのバージョンは3.0.1以降です。
>     -   TiDB 3.0 は、アップストリーム クラスターとダウンストリーム クラスターの両方で使用されます。
>     -   セカンダリ クラスターの GC ライフタイムは、プライマリ クラスターの GC ライフタイムよりも長くする必要があります。ただし、上流データベースと下流データベース間のデータ レプリケーション中にレイテンシーが発生するため、下流でのデータ回復が失敗する可能性があります。

<CustomContent platform="tidb">

**TiDB Binlogレプリケーション中のエラーのトラブルシューティング**

TiDB Binlogレプリケーション中にアップストリーム TiDB で`RECOVER TABLE`使用すると、次の 3 つの状況で TiDB Binlogが中断される可能性があります。

-   ダウンストリーム データベースは`RECOVER TABLE`ステートメントをサポートしていません。エラー インスタンス: `check the manual that corresponds to your MySQL server version for the right syntax to use near 'RECOVER TABLE table_name'` 。

-   GC の有効期間は、アップストリーム データベースとダウンストリーム データベース間で一貫していません。エラー インスタンス: `snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST` 。

-   アップストリーム データベースとダウンストリーム データベース間のレプリケーション中に遅延が発生します。エラー インスタンス: `snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST` 。

上記の 3 つの状況では、 [削除されたテーブルの完全インポート](/ecosystem-tool-user-guide.md#backup-and-restore---backup--restore-br)使用して TiDB Binlogからのデータ レプリケーションを再開できます。

</CustomContent>

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
