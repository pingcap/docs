---
title: RECOVER TABLE
summary: An overview of the usage of RECOVER TABLE for the TiDB database.
---

# 回復テーブル {#recover-table}

`RECOVER TABLE`は、 `DROP TABLE`ステートメントが実行された後、GC（ガベージコレクション）の有効期間内に削除されたテーブルとそのテーブル上のデータを回復するために使用されます。

## 構文 {#syntax}

{{< copyable "" >}}

```sql
RECOVER TABLE table_name
```

{{< copyable "" >}}

```sql
RECOVER TABLE BY JOB ddl_job_id
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

> **ノート：**
>
> -   テーブルが削除され、GCの有効期間が切れている場合、テーブルを`RECOVER TABLE`で回復することはできません。このシナリオで`RECOVER TABLE`を実行すると、次のようなエラーが返されます`snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST` 。
>
> -   TiDBのバージョンが3.0.0以降の場合、 Binlogを使用するときに`RECOVER TABLE`を使用することはお勧めしません。
>
> -   Binlogバージョン3.0.1では`RECOVER TABLE`がサポートされているため、次の3つの状況で`RECOVER TABLE`を使用できます。
>
>     -   Binlogのバージョンは3.0.1以降です。
>     -   TiDB 3.0は、アップストリームクラスタとダウンストリームクラスタの両方で使用されます。
>     -   セカンダリクラスタのGCライフタイムは、プライマリクラスタのGCライフタイムよりも長くする必要があります。ただし、アップストリームデータベースとダウンストリームデータベース間のデータレプリケーション中に遅延が発生するため、ダウンストリームでデータ回復が失敗する可能性があります。

<CustomContent platform="tidb">

**Binlogレプリケーション中のエラーのトラブルシューティング**

TiDB Binlogレプリケーション中にアップストリームTiDBで`RECOVER TABLE`を使用すると、次の3つの状況でBinlogが中断される可能性があります。

-   ダウンストリームデータベースは`RECOVER TABLE`ステートメントをサポートしていません。エラーインスタンス： `check the manual that corresponds to your MySQL server version for the right syntax to use near 'RECOVER TABLE table_name'` 。

-   GCの寿命は、アップストリームデータベースとダウンストリームデータベースの間で一貫していません。エラーインスタンス： `snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST` 。

-   レイテンシーは、アップストリームデータベースとダウンストリームデータベース間のレプリケーション中に発生します。エラーインスタンス： `snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST` 。

上記の3つの状況では、 Binlogからのデータレプリケーションを[削除されたテーブルの完全インポート](/ecosystem-tool-user-guide.md#backup-and-restore)で再開できます。

</CustomContent>

## 例 {#examples}

-   テーブル名に従って、削除されたテーブルを回復します。

    {{< copyable "" >}}

    ```sql
    DROP TABLE t;
    ```

    {{< copyable "" >}}

    ```sql
    RECOVER TABLE t;
    ```

    このメソッドは、最近のDDLジョブ履歴を検索し、 `DROP TABLE`タイプの最初のDDL操作を見つけてから、 `RECOVER TABLE`ステートメントで指定された1つのテーブル名と同じ名前で削除されたテーブルを回復します。

-   使用したテーブルの`DDL JOB ID`に従って、削除したテーブルを回復します。

    テーブル`t`を削除して別の`t`を作成し、新しく作成した`t`を再度削除したとします。次に、最初に削除された`t`を回復する場合は、 `DDL JOB ID`を指定するメソッドを使用する必要があります。

    {{< copyable "" >}}

    ```sql
    DROP TABLE t;
    ```

    {{< copyable "" >}}

    ```sql
    ADMIN SHOW DDL JOBS 1;
    ```

    上記の2番目のステートメントは、テーブルの`DDL JOB ID`を検索して`t`を削除するために使用されます。次の例では、IDは`53`です。

    ```
    +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
    | JOB_ID | DB_NAME | TABLE_NAME | JOB_TYPE   | SCHEMA_STATE | SCHEMA_ID | TABLE_ID | ROW_COUNT | START_TIME                        | STATE  |
    +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
    | 53     | test    |            | drop table | none         | 1         | 41       | 0         | 2019-07-10 13:23:18.277 +0800 CST | synced |
    +--------+---------+------------+------------+--------------+-----------+----------+-----------+-----------------------------------+--------+
    ```

    {{< copyable "" >}}

    ```sql
    RECOVER TABLE BY JOB 53;
    ```

    このメソッドは、 `DDL JOB ID`を介して削除されたテーブルを回復します。対応するDDLジョブが`DROP TABLE`タイプでない場合、エラーが発生します。

## 実装の原則 {#implementation-principle}

テーブルを削除する場合、TiDBはテーブルのメタデータのみを削除し、削除するテーブルデータ（行データとインデックスデータ）を`mysql.gc_delete_range`のテーブルに書き込みます。 TiDBバックグラウンドのGCワーカーは、GCの寿命を超えるキーを`mysql.gc_delete_range`のテーブルから定期的に削除します。

したがって、テーブルをリカバリするには、GCワーカーがテーブルデータを削除する前に、テーブルメタデータをリカバリし、 `mysql.gc_delete_range`のテーブルの対応する行レコードを削除するだけで済みます。 TiDBのスナップショット読み取りを使用して、テーブルのメタデータを回復できます。詳細は[履歴データを読む](/read-historical-data.md)を参照してください。

テーブルのリカバリは、TiDBがスナップショットの読み取りを通じてテーブルのメタデータを取得し、 `CREATE TABLE`と同様のテーブル作成のプロセスを実行することによって行われます。したがって、 `RECOVER TABLE`自体は、本質的に、一種のDDL操作です。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。
