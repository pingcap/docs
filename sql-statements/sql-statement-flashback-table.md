---
title: FLASHBACK TABLE
summary: Learn how to recover tables using the `FLASHBACK TABLE` statement.
---

# フラッシュバック テーブル {#flashback-table}

`FLASHBACK TABLE`構文は TiDB 4.0 以降で導入されました。 `FLASHBACK TABLE`ステートメントを使用して、ガベージ コレクション (GC) の有効期間内に`DROP`または`TRUNCATE`操作によって削除されたテーブルとデータを復元できます。

システム変数[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) (デフォルト: `10m0s` ) は、以前のバージョンの行の保持時間を定義します。ガベージコレクションが実行された現在の`safePoint`の場所は、次のクエリで取得できます。

{{< copyable "" >}}

```sql
SELECT * FROM mysql.tidb WHERE variable_name = 'tikv_gc_safe_point';
```

`tikv_gc_safe_point`回の後に`DROP`つか`TRUNCATE`のステートメントでテーブルが削除されている限り、 `FLASHBACK TABLE`ステートメントを使用してテーブルを復元できます。

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

テーブルが削除され、GC の有効期間が過ぎた場合、 `FLASHBACK TABLE`ステートメントを使用して削除されたデータを回復することはできなくなります。そうしないと、 `Can't find dropped / truncated table 't' in GC safe point 2020-03-16 16:34:52 +0800 CST`のようなエラーが返されます。

TiDB Binlog を有効にして`FLASHBACK TABLE`ステートメントを使用する場合は、次の条件と要件に注意してください。

-   下流の二次クラスターも`FLASHBACK TABLE`をサポートする必要があります。
-   セカンダリ クラスタの GC ライフタイムは、プライマリ クラスタの GC ライフタイムよりも長くする必要があります。
-   アップストリームとダウンストリーム間のレプリケーションの遅延により、ダウンストリームへのデータの回復が失敗することもあります。
-   TiDB Binlogがテーブルを複製しているときにエラーが発生した場合は、TiDB Binlogでそのテーブルをフィルタリングし、そのテーブルのすべてのデータを手動でインポートする必要があります。

## 例 {#example}

-   `DROP`回の操作で削除されたテーブル データを復元します。

    {{< copyable "" >}}

    ```sql
    DROP TABLE t;
    ```

    {{< copyable "" >}}

    ```sql
    FLASHBACK TABLE t;
    ```

-   `TRUNCATE`回の操作で落としたテーブルデータを復旧します。切り捨てられたテーブル`t`まだ存在するため、テーブル`t`名前を変更して復元する必要があります。そうしないと、テーブル`t`が既に存在するため、エラーが返されます。

    {{< copyable "" >}}

    ```sql
    TRUNCATE TABLE t;
    ```

    {{< copyable "" >}}

    ```sql
    FLASHBACK TABLE t TO t1;
    ```

## 実施原則 {#implementation-principle}

テーブルを削除する場合、TiDB はテーブルのメタデータのみを削除し、削除するテーブル データ (行データとインデックス データ) を`mysql.gc_delete_range`のテーブルに書き込みます。 TiDB バックグラウンドの GC ワーカーは、GC の有効期間を超えたキーを`mysql.gc_delete_range`テーブルから定期的に削除します。

したがって、テーブルを回復するには、GC ワーカーがテーブル データを削除する前に、テーブル メタデータを回復し、 `mysql.gc_delete_range`テーブル内の対応する行レコードを削除するだけで済みます。 TiDB のスナップショット読み取りを使用して、テーブル メタデータを復元できます。スナップショットの読み込みの詳細については、 [履歴データの読み取り](/read-historical-data.md)を参照してください。

以下は`FLASHBACK TABLE t TO t1`の作業プロセスです。

1.  TiDB は最近の DDL 履歴ジョブを検索し、テーブル`t`で`DROP TABLE`または`truncate table`タイプの最初の DDL 操作を見つけます。 TiDB が検索に失敗すると、エラーが返されます。
2.  TiDB は、DDL ジョブの開始時刻が`tikv_gc_safe_point`より前かどうかを確認します。 `tikv_gc_safe_point`より前の場合は、 `DROP`または`TRUNCATE`操作で削除されたテーブルが GC によってクリーンアップされ、エラーが返されたことを意味します。
3.  TiDB は、DDL ジョブの開始時刻をスナップショットとして使用して、履歴データとテーブル メタデータを読み取ります。
4.  TiDB は`mysql.gc_delete_range`の表`t`に関連する GC タスクを削除します。
5.  TiDB はテーブルのメタデータの`name` `t1`に変更し、このメタデータを使用して新しいテーブルを作成します。テーブル名のみが変更され、テーブル ID は変更されないことに注意してください。テーブル ID は、以前にドロップされたテーブルの ID と同じです`t` 。

上記のプロセスから、TiDB は常にテーブルのメタデータで動作し、テーブルのユーザー データは変更されていないことがわかります。復元されたテーブル`t1`は、以前に削除されたテーブル`t`と同じ ID を持つため、 `t1` `t`のユーザー データを読み取ることができます。

> **ノート：**
>
> `FLASHBACK`ステートメントを使用して削除された同じテーブルを複数回復元することはできません。これは、復元されたテーブルの ID が削除されたテーブルの ID と同じであり、TiDB ではすべての既存のテーブルがグローバルに一意のテーブル ID を持つ必要があるためです。

`FLASHBACK TABLE`操作は、TiDB がスナップショットの読み取りによってテーブル メタデータを取得し、 `CREATE TABLE`と同様のテーブル作成プロセスを実行することによって行われます。したがって、 `FLASHBACK TABLE`は本質的に一種の DDL 操作です。

## MySQL の互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。
