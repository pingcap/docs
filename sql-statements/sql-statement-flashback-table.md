---
title: FLASHBACK TABLE
summary: Learn how to recover tables using the `FLASHBACK TABLE` statement.
---

# フラッシュバックテーブル {#flashback-table}

`FLASHBACK TABLE`構文は、TiDB4.0以降に導入されました。 `FLASHBACK TABLE`ステートメントを使用して、ガベージコレクション（GC）の有効期間内に`DROP`または`TRUNCATE`操作によってドロップされたテーブルとデータを復元できます。

システム変数[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) （デフォルト： `10m0s` ）は、以前のバージョンの行の保持時間を定義します。ガラベージ収集が実行された現在の`safePoint`は、次のクエリで取得できます。

{{< copyable "" >}}

```sql
SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
```

`tikv_gc_safe_point`回後にテーブルが`DROP`または`TRUNCATE`ステートメントドロップされる限り、 `FLASHBACK TABLE`ステートメントを使用してテーブルを復元できます。

## 構文 {#syntax}

{{< copyable "" >}}

```sql
FLASHBACK TABLE table_name [TO other_table_name]
```

## あらすじ {#synopsis}

```ebnf+diagram
FlashbackTableStmt ::=
    'FLASHBACK' 'TABLE' TableName FlashbackToNewName

TableName ::=
    Identifier ( '.' Identifier )?

FlashbackToNewName ::=
    ( 'TO' Identifier )?
```

## ノート {#notes}

テーブルがドロップされ、GCの有効期間が過ぎた場合、 `FLASHBACK TABLE`ステートメントを使用してドロップされたデータを回復することはできなくなります。そうしないと、 `Can't find dropped / truncated table 't' in GC safe point 2020-03-16 16:34:52 +0800 CST`のようなエラーが返されます。

TiDB Binlogを有効にして、 `FLASHBACK TABLE`ステートメントを使用するときは、次の条件と要件に注意してください。

-   ダウンストリームセカンダリクラスタも`FLASHBACK TABLE`をサポートする必要があります。
-   セカンダリクラスタのGCライフタイムは、プライマリクラスタのGCライフタイムより長くする必要があります。
-   アップストリームとダウンストリーム間のレプリケーションの遅延も、ダウンストリームへのデータの回復に失敗する原因となる可能性があります。
-   TiDB Binlogがテーブルを複製しているときにエラーが発生した場合は、TiDB Binlogでそのテーブルをフィルタリングし、そのテーブルのすべてのデータを手動でインポートする必要があります。

## 例 {#example}

-   `DROP`の操作でドロップされたテーブルデータを回復します。

    {{< copyable "" >}}

    ```sql
    DROP TABLE t;
    ```

    {{< copyable "" >}}

    ```sql
    FLASHBACK TABLE t;
    ```

-   `TRUNCATE`の操作で削除されたテーブルデータを回復します。切り捨てられたテーブル`t`はまだ存在するため、回復するにはテーブル`t`の名前を変更する必要があります。そうしないと、テーブル`t`がすでに存在するため、エラーが返されます。

    {{< copyable "" >}}

    ```sql
    TRUNCATE TABLE t;
    ```

    {{< copyable "" >}}

    ```sql
    FLASHBACK TABLE t TO t1;
    ```

## 実装の原則 {#implementation-principle}

テーブルを削除する場合、TiDBはテーブルのメタデータのみを削除し、削除するテーブルデータ（行データとインデックスデータ）を`mysql.gc_delete_range`のテーブルに書き込みます。 TiDBバックグラウンドのGCワーカーは、GCの有効期間を超えるキーを`mysql.gc_delete_range`のテーブルから定期的に削除します。

したがって、テーブルをリカバリするには、GCワーカーがテーブルデータを削除する前に、テーブルメタデータをリカバリし、 `mysql.gc_delete_range`のテーブルの対応する行レコードを削除するだけで済みます。 TiDBのスナップショット読み取りを使用して、テーブルのメタデータを回復できます。読み取りスナップショットの詳細については、 [履歴データを読む](/read-historical-data.md)を参照してください。

以下は`FLASHBACK TABLE t TO t1`の作業プロセスです：

1.  TiDBは、最近のDDL履歴ジョブを検索し、表`t`で`DROP TABLE`または`truncate table`タイプの最初のDDL操作を見つけます。 TiDBが1つを見つけられなかった場合、エラーが返されます。
2.  TiDBは、DDLジョブの開始時刻が`tikv_gc_safe_point`より前かどうかをチェックします。 `tikv_gc_safe_point`より前の場合は、 `DROP`または`TRUNCATE`の操作で削除されたテーブルがGCによってクリーンアップされ、エラーが返されたことを意味します。
3.  TiDBは、DDLジョブの開始時刻をスナップショットとして使用して、履歴データを読み取り、テーブルのメタデータを読み取ります。
4.  TiDBは、 `mysql.gc_delete_range`の表`t`に関連するGCタスクを削除します。
5.  TiDBは、テーブルのメタデータの`name`を`t1`に変更し、このメタデータを使用して新しいテーブルを作成します。テーブル名のみが変更され、テーブルIDは変更されないことに注意してください。テーブルIDは、前にドロップしたテーブル`t`のIDと同じです。

上記のプロセスから、TiDBは常にテーブルのメタデータを操作し、テーブルのユーザーデータは変更されていないことがわかります。復元されたテーブル`t1`は以前に削除されたテーブル`t`と同じIDを持っているため、 `t1`は`t`のユーザーデータを読み取ることができます。

> **ノート：**
>
> 復元されたテーブルのIDは削除されたテーブルのIDと同じであり、TiDBでは既存のすべてのテーブルにグローバルに一意のテーブルIDが必要であるため、 `FLASHBACK`のステートメントを使用して同じ削除済みテーブルを複数回復元することはできません。

`FLASHBACK TABLE`の操作は、TiDBがスナップショットの読み取りを通じてテーブルのメタデータを取得し、 `CREATE TABLE`と同様のテーブル作成のプロセスを実行することによって実行されます。したがって、 `FLASHBACK TABLE`は本質的に一種のDDL操作です。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL構文のTiDB拡張です。
