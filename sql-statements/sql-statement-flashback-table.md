---
title: FLASHBACK TABLE
summary: FLASHBACK TABLE` ステートメントを使用してテーブルを回復する方法を学習します。
---

# フラッシュバックテーブル {#flashback-table}

`FLASHBACK TABLE`構文は TiDB 4.0 以降で導入されました。3 `FLASHBACK TABLE`を使用すると、ガベージ コレクション (GC) の有効期間内に`DROP`または`TRUNCATE`操作によって削除されたテーブルとデータを復元できます。

システム変数[`tidb_gc_life_time`](/system-variables.md#tidb_gc_life_time-new-in-v50) (デフォルト: `10m0s` ) は、以前のバージョンの行の保持時間を定義します。ガベージコレクションが実行された現在の`safePoint`は、次のクエリで取得できます。

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

テーブルが削除され、GC の有効期間が過ぎた場合、 `FLASHBACK TABLE`ステートメントを使用して削除されたデータを回復することはできなくなります。それ以外の場合は、 `Can't find dropped / truncated table 't' in GC safe point 2020-03-16 16:34:52 +0800 CST`のようなエラーが返されます。

TiDB Binlog を有効にして`FLASHBACK TABLE`ステートメントを使用する場合は、次の条件と要件に注意してください。

-   ダウンストリームのセカンダリ クラスターも`FLASHBACK TABLE`サポートする必要があります。
-   セカンダリ クラスターの GC 有効期間は、プライマリ クラスターの GC 有効期間よりも長くする必要があります。
-   アップストリームとダウンストリーム間のレプリケーションの遅延により、ダウンストリームへのデータの回復が失敗する可能性もあります。
-   TiDB Binlog がテーブルを複製しているときにエラーが発生した場合は、TiDB Binlogでそのテーブルをフィルタリングし、そのテーブルのすべてのデータを手動でインポートする必要があります。

## 例 {#example}

-   `DROP`目の操作で削除されたテーブル データを回復します。

    ```sql
    DROP TABLE t;
    ```

    ```sql
    FLASHBACK TABLE t;
    ```

-   `TRUNCATE`操作で削除されたテーブル データを回復します。切り捨てられたテーブル`t`まだ存在するため、回復するテーブル`t`名前を変更する必要があります。そうしないと、テーブル`t`既に存在するため、エラーが返されます。

    ```sql
    TRUNCATE TABLE t;
    ```

    ```sql
    FLASHBACK TABLE t TO t1;
    ```

## 実施原則 {#implementation-principle}

テーブルを削除する場合、TiDB はテーブルメタデータのみを削除し、削除するテーブルデータ (行データとインデックスデータ) を`mysql.gc_delete_range`テーブルに書き込みます。TiDB のバックグラウンドにある GC ワーカーは、GC 有効期間を超えたキーを`mysql.gc_delete_range`テーブルから定期的に削除します。

したがって、テーブルをリカバリするには、GC ワーカーがテーブル データを削除する前に、テーブル メタデータをリカバリし、 `mysql.gc_delete_range`のテーブル内の対応する行レコードを削除するだけで済みます。テーブル メタデータをリカバリするには、TiDB のスナップショット読み取りを使用できます。スナップショット読み取りの詳細については、 [履歴データを読む](/read-historical-data.md)を参照してください。

`FLASHBACK TABLE t TO t1`の作業工程は以下のとおりです。

1.  TiDB は最近の DDL 履歴ジョブを検索し、テーブル`t`でタイプ`DROP TABLE`または`truncate table`の最初の DDL 操作を見つけます。TiDB が見つけられない場合は、エラーが返されます。
2.  TiDB は、DDL ジョブの開始時刻が`tikv_gc_safe_point`より前かどうかを確認します。 `tikv_gc_safe_point`より前の場合は、 `DROP`または`TRUNCATE`操作によって削除されたテーブルが GC によってクリーンアップされたことを意味し、エラーが返されます。
3.  TiDB は、DDL ジョブの開始時刻をスナップショットとして使用して、履歴データを読み取り、テーブル メタデータを読み取ります。
4.  TiDB は`mysql.gc_delete_range`の表`t`に関連する GC タスクを削除します。
5.  TiDB はテーブルのメタデータの`name` `t1`に変更し、このメタデータを使用して新しいテーブルを作成します。テーブル名のみが変更され、テーブル ID は変更されないことに注意してください。テーブル ID は、以前に削除されたテーブル`t`の ID と同じです。

上記のプロセスから、TiDB は常にテーブルのメタデータに対して操作を行い、テーブルのユーザー データは変更されていないことがわかります。復元されたテーブル`t1` 、以前に削除されたテーブル`t`と同じ ID を持つため、 `t1` `t`のユーザー データを読み取ることができます。

> **注記：**
>
> 復元されたテーブルの ID は削除されたテーブルの ID と同じであり、TiDB では既存のすべてのテーブルにグローバルに一意のテーブル ID が必要であるため、 `FLASHBACK`ステートメントを使用して同じ削除されたテーブルを複数回復元することはできません。

`FLASHBACK TABLE`操作は、TiDB がスナップショット読み取りを通じてテーブル メタデータを取得し、 `CREATE TABLE`と同様のテーブル作成プロセスを実行することによって実行されます。したがって、 `FLASHBACK TABLE`本質的には一種の DDL 操作です。

## MySQL 互換性 {#mysql-compatibility}

このステートメントは、MySQL 構文に対する TiDB 拡張です。
