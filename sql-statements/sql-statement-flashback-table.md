---
title: FLASHBACK TABLE
summary: Learn how to recover tables using the `FLASHBACK TABLE` statement.
---

# フラッシュバックテーブル {#flashback-table}

`FLASHBACK TABLE`構文は TiDB 4.0 以降に導入されました。 `FLASHBACK TABLE`ステートメントを使用すると、ガベージ コレクション (GC) の存続期間内に`DROP`または`TRUNCATE`操作によって削除されたテーブルとデータを復元できます。

システム変数[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) (デフォルト: `10m0s` ) は、以前のバージョンの行の保持時間を定義します。ガベージコレクションが実行された現在の`safePoint`の場所は、次のクエリで取得できます。

```sql
SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
```

`tikv_gc_safe_point`回の経過後に`DROP`または`TRUNCATE`ステートメントによってテーブルが削除された限り、 `FLASHBACK TABLE`ステートメントを使用してテーブルを復元できます。

## 構文 {#syntax}

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

テーブルが削除され、GC 有効期間が経過した場合、 `FLASHBACK TABLE`ステートメントを使用して削除されたデータを回復することはできなくなります。それ以外の場合は、 `Can't find dropped / truncated table 't' in GC safe point 2020-03-16 16:34:52 +0800 CST`のようなエラーが返されます。

TiDB Binlog を有効にして`FLASHBACK TABLE`ステートメントを使用する場合は、次の条件と要件に注意してください。

-   ダウンストリームのセカンダリ クラスターも`FLASHBACK TABLE`をサポートする必要があります。
-   セカンダリ クラスターの GC ライフタイムは、プライマリ クラスターの GC ライフタイムよりも長くする必要があります。
-   アップストリームとダウンストリーム間のレプリケーションの遅延により、ダウンストリームへのデータの回復に失敗する可能性もあります。
-   TiDB Binlogがテーブルを複製しているときにエラーが発生した場合は、TiDB Binlogでそのテーブルをフィルタリングし、そのテーブルのすべてのデータを手動でインポートする必要があります。

## 例 {#example}

-   `DROP`の操作によって削除されたテーブル データを復元します。

    ```sql
    DROP TABLE t;
    ```

    ```sql
    FLASHBACK TABLE t;
    ```

-   `TRUNCATE`の操作で削除されたテーブル データを回復します。切り詰められたテーブル`t`はまだ存在するため、リカバリするテーブル`t`の名前を変更する必要があります。そうしないと、テーブル`t`がすでに存在するため、エラーが返されます。

    ```sql
    TRUNCATE TABLE t;
    ```

    ```sql
    FLASHBACK TABLE t TO t1;
    ```

## 実施原則 {#implementation-principle}

テーブルを削除する場合、TiDB はテーブルのメタデータのみを削除し、削除するテーブル データ (行データおよびインデックス データ) を`mysql.gc_delete_range`のテーブルに書き込みます。 TiDB バックグラウンドの GC ワーカーは、GC の有効期間を超えたキーを`mysql.gc_delete_range`テーブルから定期的に削除します。

したがって、テーブルを回復するには、GC ワーカーがテーブル データを削除する前に、テーブルのメタデータを回復し、テーブル`mysql.gc_delete_range`内の対応する行レコードを削除するだけで済みます。 TiDB のスナップショット読み取りを使用して、テーブルのメタデータを回復できます。スナップショットリードの詳細については、 [履歴データの読み取り](/read-historical-data.md)を参照してください。

`FLASHBACK TABLE t TO t1`の作業工程は以下の通りです。

1.  TiDB は、最近の DDL 履歴ジョブを検索し、テーブル`t`でタイプ`DROP TABLE`またはタイプ`truncate table`の最初の DDL 操作を見つけます。 TiDB が見つからない場合は、エラーが返されます。
2.  TiDB は、DDL ジョブの開始時刻が`tikv_gc_safe_point`より前であるかどうかをチェックします。 `tikv_gc_safe_point`より前の場合は、 `DROP`または`TRUNCATE`操作によって削除されたテーブルが GC によってクリーンアップされ、エラーが返されたことを意味します。
3.  TiDB は、DDL ジョブの開始時間をスナップショットとして使用して、履歴データを読み取り、テーブルのメタデータを読み取ります。
4.  TiDB は、 `mysql.gc_delete_range`のテーブル`t`に関連する GC タスクを削除します。
5.  TiDB は、テーブルのメタデータの`name` `t1`に変更し、このメタデータを使用して新しいテーブルを作成します。テーブル名のみが変更され、テーブル ID は変更されないことに注意してください。テーブル ID は、以前に削除されたテーブル`t`の ID と同じです。

上記のプロセスから、TiDB は常にテーブルのメタデータに対して動作し、テーブルのユーザー データは決して変更されていないことがわかります。復元されたテーブル`t1`は、以前に削除されたテーブル`t`と同じ ID を持っているため、 `t1` `t`のユーザー データを読み取ることができます。

> **注記：**
>
> 復元されたテーブルの ID は削除されたテーブルの ID と同じであり、TiDB ではすべての既存のテーブルがグローバルに一意のテーブル ID を持つ必要があるため、 `FLASHBACK`ステートメントを使用して同じ削除されたテーブルを複数回復元することはできません。

`FLASHBACK TABLE`操作は、TiDB がスナップショット読み取りを通じてテーブル メタデータを取得し、その後`CREATE TABLE`と同様のテーブル作成プロセスを経ることによって実行されます。したがって、 `FLASHBACK TABLE`は本質的には一種の DDL 操作です。

## MySQLの互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張機能です。
