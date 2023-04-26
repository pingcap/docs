---
title: RECOVER TABLE
summary: An overview of the usage of RECOVER TABLE for the TiDB database.
---

# テーブルを回復 {#recover-table}

`RECOVER TABLE`は、 `DROP TABLE`ステートメントが実行された後、GC (ガベージ コレクション) の有効期間内に、削除されたテーブルとその上のデータを回復するために使用されます。

## 構文 {#syntax}

{{< copyable "" >}}

```sql
RECOVER TABLE table_name;
```

{{< copyable "" >}}

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

> **ノート：**
>
> -   テーブルが削除され、GC の有効期限が切れている場合、テーブルは`RECOVER TABLE`では復元できません。このシナリオで`RECOVER TABLE`を実行すると、次のようなエラーが返されます: `snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST` 。
>
> -   TiDB のバージョンが 3.0.0 以降の場合、TiDB Binlogを使用する場合は`RECOVER TABLE`を使用することはお勧めしません。
>
> -   `RECOVER TABLE`はBinlogバージョン 3.0.1 でサポートされているため、次の 3 つの状況で`RECOVER TABLE`を使用できます。
>
>     -   Binlog のバージョンは 3.0.1 以降です。
>     -   TiDB 3.0 は、上流クラスターと下流クラスターの両方で使用されます。
>     -   セカンダリ クラスタの GC ライフ タイムは、プライマリ クラスタの GC ライフ タイムよりも長くする必要があります。ただし、アップストリーム データベースとダウンストリーム データベース間のデータ レプリケーション中にレイテンシーが発生するため、ダウンストリームでのデータ リカバリが失敗する可能性があります。

<CustomContent platform="tidb">

**TiDB Binlogレプリケーション中のエラーのトラブルシューティング**

TiDB Binlogレプリケーション中に上流の TiDB で`RECOVER TABLE`使用すると、次の 3 つの状況で TiDB Binlog が中断される可能性があります。

-   ダウンストリーム データベースは`RECOVER TABLE`ステートメントをサポートしていません。エラー インスタンス: `check the manual that corresponds to your MySQL server version for the right syntax to use near 'RECOVER TABLE table_name'` 。

-   アップストリーム データベースとダウンストリーム データベースの間で GC の有効期間が一致していません。エラー インスタンス: `snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST` 。

-   アップストリーム データベースとダウンストリーム データベース間のレプリケーション中にレイテンシが発生します。エラー インスタンス: `snapshot is older than GC safe point 2019-07-10 13:45:57 +0800 CST` 。

上記の 3 つの状況では、TiDB Binlogからのデータ複製を[削除されたテーブルの完全インポート](/ecosystem-tool-user-guide.md#backup-and-restore---backup--restore-br)で再開できます。

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

    このメソッドは、最近の DDL ジョブ履歴を検索し、 `DROP TABLE`タイプの最初の DDL 操作を見つけてから、 `RECOVER TABLE`ステートメントで指定された 1 つのテーブル名と同じ名前の削除されたテーブルを回復します。

-   使用されたテーブルの`DDL JOB ID`に従って、削除されたテーブルを回復します。

    テーブル`t`削除して別の`t`を作成し、新しく作成した`t`再度削除したとします。そして、そもそも削除した`t`を復元したい場合は、 `DDL JOB ID`指定する方法を使用する必要があります。

    {{< copyable "" >}}

    ```sql
    DROP TABLE t;
    ```

    {{< copyable "" >}}

    ```sql
    ADMIN SHOW DDL JOBS 1;
    ```

    上記の 2 番目のステートメントは、テーブルの`DDL JOB ID`から削除`t`を検索するために使用されます。次の例では、ID は`53`です。

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

    このメソッドは、削除されたテーブルを`DDL JOB ID`経由で復元します。対応する DDL ジョブが`DROP TABLE`タイプでない場合、エラーが発生します。

## 実施原則 {#implementation-principle}

テーブルを削除する場合、TiDB はテーブルのメタデータのみを削除し、削除するテーブル データ (行データとインデックス データ) を`mysql.gc_delete_range`のテーブルに書き込みます。 TiDB バックグラウンドの GC ワーカーは、定期的に`mysql.gc_delete_range`テーブルから GC の有効期間を超えたキーを削除します。

したがって、テーブルを回復するには、GC ワーカーがテーブル データを削除する前に、テーブル メタデータを回復し、 `mysql.gc_delete_range`テーブル内の対応する行レコードを削除するだけで済みます。 TiDB のスナップショット読み取りを使用して、テーブル メタデータを復元できます。詳細は[履歴データの読み取り](/read-historical-data.md)を参照してください。

テーブルの復旧は、TiDB がスナップショットの読み取りによってテーブルのメタデータを取得し、次に`CREATE TABLE`と同様のテーブル作成プロセスを実行することによって行われます。したがって、 `RECOVER TABLE`自体は本質的に一種の DDL 操作です。

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。
