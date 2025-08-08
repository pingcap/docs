---
title: Metadata Lock
summary: TiDB のメタデータ ロックの概念、原則、実装の詳細を紹介します。
---

# メタデータロック {#metadata-lock}

このドキュメントでは、TiDB のメタデータ ロックについて説明します。

## コンセプト {#concept}

TiDBは、オンライン非同期スキーマ変更アルゴリズムを使用して、メタデータオブジェクトの変更をサポートします。トランザクションが実行されると、トランザクション開始時の対応するメタデータスナップショットが取得されます。トランザクション中にメタデータが変更された場合、データの整合性を確保するために、TiDBはエラー`Information schema is changed`を返し、トランザクションはコミットに失敗します。

この問題を解決するため、TiDB v6.3.0ではオンラインDDLアルゴリズムにメタデータロックが導入されました。ほとんどのDMLエラーを回避するため、TiDBはテーブルメタデータの変更時にDMLとDDLの優先順位を調整し、古いメタデータを持つDMLがコミットされるまで実行中のDDLを待機させます。

## シナリオ {#scenarios}

TiDB のメタデータ ロックは、次のようなすべての DDL ステートメントに適用されます。

-   [`ADD INDEX`](/sql-statements/sql-statement-add-index.md)
-   [`ADD COLUMN`](/sql-statements/sql-statement-add-column.md)
-   [`DROP COLUMN`](/sql-statements/sql-statement-drop-column.md)
-   [`DROP INDEX`](/sql-statements/sql-statement-drop-index.md)
-   [`DROP PARTITION`](/partitioned-table.md#partition-management)
-   [`TRUNCATE TABLE`](/sql-statements/sql-statement-truncate.md)
-   [`EXCHANGE PARTITION`](/partitioned-table.md#partition-management)
-   [`CHANGE COLUMN`](/sql-statements/sql-statement-change-column.md)
-   [`MODIFY COLUMN`](/sql-statements/sql-statement-modify-column.md)

メタデータロックを有効にすると、TiDB での DDL タスク実行のパフォーマンスに若干の影響が出る可能性があります。この影響を軽減するために、メタデータロックを必要としないシナリオをいくつか以下に示します。

-   自動コミットが有効になっているクエリは`SELECT`
-   ステイル読み取りが有効になっています
-   一時テーブルにアクセスする

## 使用法 {#usage}

TiDB v6.5.0以降、メタデータロックはデフォルトで有効になります。既存のクラスタをv6.4.0以前からv6.5.0以降にアップグレードすると、TiDBはメタデータロックを自動的に有効にします。メタデータロックを無効にするには、システム変数[`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630)を`OFF`に設定します。

## インパクト {#impact}

-   DML の場合、メタデータ ロックは実行をブロックせず、デッドロックも発生しません。
-   メタデータ ロックを有効にすると、トランザクション内のメタデータ オブジェクトの情報は最初のアクセス時に決定され、その後は変更されません。
-   DDLの場合、メタデータの状態を変更すると、古いトランザクションによってDDLがブロックされる可能性があります。以下に例を示します。

    | セッション1                                                                                     | セッション2                                                     |
    | :----------------------------------------------------------------------------------------- | :--------------------------------------------------------- |
    | `CREATE TABLE t (a INT);`                                                                  |                                                            |
    | `INSERT INTO t VALUES(1);`                                                                 |                                                            |
    | `BEGIN;`                                                                                   |                                                            |
    |                                                                                            | `ALTER TABLE t ADD COLUMN b INT;`                          |
    | `SELECT * FROM t;`<br/> (テーブル`t`の現在のメタデータ バージョンを使用します。5 `(a=1, b=NULL)`返し、テーブル`t`をロックします。) |                                                            |
    |                                                                                            | `ALTER TABLE t ADD COLUMN c INT;` (セッション 1 によってブロックされています) |

    繰り返し可能読み取り分離レベルでは、トランザクションの開始からテーブルのメタデータを決定する時点までの間に、インデックスの追加や列タイプの変更など、データの変更を必要とする DDL が実行されると、DDL は次のようなエラーを返します。

    | セッション1                                                                     | セッション2                                    |
    | :------------------------------------------------------------------------- | :---------------------------------------- |
    | `CREATE TABLE t (a INT);`                                                  |                                           |
    | `INSERT INTO t VALUES(1);`                                                 |                                           |
    | `BEGIN;`                                                                   |                                           |
    |                                                                            | `ALTER TABLE t ADD INDEX idx(a);`         |
    | `SELECT * FROM t;` （インデックス`idx`使用できません）                                    |                                           |
    | `COMMIT;`                                                                  |                                           |
    | `BEGIN;`                                                                   |                                           |
    |                                                                            | `ALTER TABLE t MODIFY COLUMN a CHAR(10);` |
    | `SELECT * FROM t;` ( `ERROR 8028 (HY000): public column a has changed`を返す) |                                           |

## 可観測性 {#observability}

TiDB v6.3.0 では、現在ブロックされている DDL の情報を取得するのに役立つ`mysql.tidb_mdl_view`ビューが導入されています。

> **注記：**
>
> `mysql.tidb_mdl_view`ビューを選択するには、 [`PROCESS`権限](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process)必要です。

以下は、テーブル`t`にインデックスを追加する例です。DDL文`ALTER TABLE t ADD INDEX idx(a)`があると仮定します。

```sql
TABLE mysql.tidb_mdl_view\G
```

```
*************************** 1. row ***************************
     job_id: 118
    db_name: test
 table_name: t
      query: ALTER TABLE t ADD COLUMN c INT
 session_id: 1547698182
 start_time: 2025-03-19 09:52:36.509000
SQL_DIGESTS: ["begin","select * from `t`"]
1 row in set (0.00 sec)

```

上記の出力から、 `SESSION ID`が`1547698182`であるトランザクションが`ADD COLUMN` DDLをブロックしていることがわかります。7 `SQL_DIGEST` 、このトランザクションによって実行されたSQL文（ ``["begin","select * from `t`"]``を示しています。ブロックされたDDLの実行を継続するには、次のグローバル`KILL`文を使用して`1547698182`トランザクションを強制終了します。

```sql
mysql> KILL 1547698182;
Query OK, 0 rows affected (0.00 sec)
```

トランザクションを強制終了した後、 `mysql.tidb_mdl_view`のビューを再度選択できます。この時点では、前のトランザクションは出力に表示されません。これは、DDLがブロックされていないことを意味します。

```sql
TABLE mysql.tidb_mdl_view\G
Empty set (0.01 sec)
```

## 原則 {#principles}

### 問題の説明 {#description-of-the-issue}

TiDBにおけるDDL操作はオンラインDDLモードです。DDL文の実行中、変更対象オブジェクトのメタデータバージョンは、複数のマイナーバージョン変更を経る可能性があります。オンライン非同期メタデータ変更アルゴリズムは、隣接する2つのマイナーバージョン間の互換性のみを確立します。つまり、2つのバージョン間の操作によって、DDL変更対象のオブジェクトのデータ整合性が損なわれることはありません。

テーブルにインデックスを追加すると、DDL ステートメントの状態は次のように変わります: なし -&gt; 削除のみ、削除のみ -&gt; 書き込みのみ、書き込みのみ -&gt; 書き込み再編成、書き込み再編成 -&gt; パブリック。

次のトランザクションのコミット プロセスは、前述の制約に違反します。

| トランザクション  | トランザクションで使用されるバージョン | クラスター内の最新バージョン | バージョンの違い |
| :-------- | :------------------ | :------------- | :------- |
| トランザクション1 | なし                  | なし             | 0        |
| トランザクション2 | 削除のみ                | 削除のみ           | 0        |
| トランザクション3 | 書き込み専用              | 書き込み専用         | 0        |
| txn4      | なし                  | 書き込み専用         | 2        |
| txn5      | 書き込み再編成             | 書き込み再編成        | 0        |
| txn6      | 書き込み専用              | 書き込み再編成        | 1        |
| txn7      | 公共                  | 公共             | 0        |

上記の表では、 `txn4`コミットされたときに使用されるメタデータバージョンは、クラスター内の最新バージョンから 2 バージョン離れています。これにより、データの不整合が発生する可能性があります。

### 実装の詳細 {#implementation-details}

メタデータロックは、TiDBクラスタ内のすべてのトランザクションで使用されるメタデータのバージョン差が最大1バージョン以内であることを保証できます。この目的を達成するために、TiDBは次の2つのルールを実装しています。

-   DMLを実行すると、TiDBはDMLによってアクセスされたメタデータオブジェクト（テーブル、ビュー、対応するメタデータバージョンなど）をトランザクションコンテキストに記録します。これらのレコードは、トランザクションがコミットされるとクリーンアップされます。
-   DDL文の状態が変化すると、メタデータの最新バージョンがすべてのTiDBノードにプッシュされます。TiDBノード上でこの状態変化に関連するすべてのトランザクションで使用されるメタデータバージョンと現在のメタデータバージョンの差が2未満の場合、そのTiDBノードはメタデータオブジェクトのメタデータロックを取得したとみなされます。次の状態変化は、クラスタ内のすべてのTiDBノードがメタデータオブジェクトのメタデータロックを取得した後にのみ実行できます。
