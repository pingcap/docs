---
title: Metadata Lock
summary: Introduce the concept, principles, and implementation details of metadata lock in TiDB.
---

# メタデータロック {#metadata-lock}

このドキュメントでは、TiDB のメタデータ ロックについて紹介します。

## コンセプト {#concept}

TiDB は、オンライン非同期スキーマ変更アルゴリズムを使用して、メタデータ オブジェクトの変更をサポートします。トランザクションが実行されると、トランザクションの開始時に対応するメタデータのスナップショットが取得されます。トランザクション中にメタデータが変更された場合、データの一貫性を確保するために、TiDB は`Information schema is changed`エラーを返し、トランザクションはコミットに失敗します。

この問題を解決するために、TiDB v6.3.0 ではオンライン DDL アルゴリズムにメタデータ ロックが導入されています。ほとんどの DML エラーを回避するために、TiDB はテーブル メタデータの変更中に DML と DDL の優先順位を調整し、古いメタデータを持つ DML がコミットされるまで DDL の実行を待機させます。

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

メタデータ ロックを有効にすると、TiDB での DDL タスクの実行にパフォーマンスに影響を与える可能性があります。影響を軽減するために、メタデータ ロックを必要としないいくつかのシナリオを以下に示します。

-   自動コミットが有効なクエリは`SELECT`
-   ステイル読み取りが有効になっています
-   一時テーブルにアクセスする

## 使用法 {#usage}

v6.5.0 以降、TiDB はデフォルトでメタデータ ロックを有効にします。既存のクラスターを v6.4.0 以前から v6.5.0 以降にアップグレードすると、TiDB はメタデータ ロックを自動的に有効にします。メタデータのロックを無効にするには、システム変数[`tidb_enable_metadata_lock`](/system-variables.md#tidb_enable_metadata_lock-new-in-v630) ～ `OFF`を設定します。

## インパクト {#impact}

-   DML の場合、メタデータ ロックはその実行をブロックせず、デッドロックも引き起こしません。
-   メタデータ ロックが有効な場合、トランザクション内のメタデータ オブジェクトの情報は最初のアクセス時に決定され、それ以降は変更されません。
-   DDL の場合、メタデータの状態を変更すると、古いトランザクションによって DDL がブロックされる可能性があります。以下は例です。

    | セッション1                                                                                           | セッション2                                                    |
    | :----------------------------------------------------------------------------------------------- | :-------------------------------------------------------- |
    | `CREATE TABLE t (a INT);`                                                                        |                                                           |
    | `INSERT INTO t VALUES(1);`                                                                       |                                                           |
    | `BEGIN;`                                                                                         |                                                           |
    |                                                                                                  | `ALTER TABLE t ADD COLUMN b INT;`                         |
    | `SELECT * FROM t;`<br/> ( table `t`の現在のメタデータ バージョンを使用します。 `(a=1, b=NULL)`を返し、 table `t`をロックします。) |                                                           |
    |                                                                                                  | `ALTER TABLE t ADD COLUMN c INT;` (セッション 1 によってブロックされました) |

    反復可能な読み取り分離レベルでは、トランザクションの開始からテーブルのメタデータを決定する時点まで、インデックスの追加や列の型の変更など、データ変更を必要とする DDL が実行されると、DDL は次のようなエラーを返します。 :

    | セッション1                                                               | セッション2                                    |
    | :------------------------------------------------------------------- | :---------------------------------------- |
    | `CREATE TABLE t (a INT);`                                            |                                           |
    | `INSERT INTO t VALUES(1);`                                           |                                           |
    | `BEGIN;`                                                             |                                           |
    |                                                                      | `ALTER TABLE t ADD INDEX idx(a);`         |
    | `SELECT * FROM t;` (インデックス`idx`は使用できません)                             |                                           |
    | `COMMIT;`                                                            |                                           |
    | `BEGIN;`                                                             |                                           |
    |                                                                      | `ALTER TABLE t MODIFY COLUMN a CHAR(10);` |
    | `SELECT * FROM t;` ( `Error 8028: Information schema is changed`を返す) |                                           |

## 可観測性 {#observability}

TiDB v6.3.0 では、現在ブロックされている DDL の情報を取得するのに役立つ`mysql.tidb_mdl_view`ビューが導入されています。

> **注記：**
>
> `mysql.tidb_mdl_view`ビューを選択するには、 [`PROCESS`権限](https://dev.mysql.com/doc/refman/8.0/en/privileges-provided.html#priv_process)が必要です。

以下では、例としてテーブル`t`にインデックスを追加します。 DDL ステートメント`ALTER TABLE t ADD INDEX idx(a)`あるとします。

```sql
SELECT * FROM mysql.tidb_mdl_view\G
*************************** 1. row ***************************
    JOB_ID: 141
   DB_NAME: test
TABLE_NAME: t
     QUERY: ALTER TABLE t ADD INDEX idx(a)
SESSION ID: 2199023255957
  TxnStart: 08-30 16:35:41.313(435643624013955072)
SQL_DIGESTS: ["begin","select * from `t`"]
1 row in set (0.02 sec)
```

前述の出力から、 `SESSION ID`が`2199023255957`トランザクションが`ADD INDEX` DDL をブロックしていることがわかります。 `SQL_DIGEST`このトランザクション ( ``["begin","select * from `t`"]``によって実行される SQL ステートメントを示しています。ブロックされた DDL の実行を継続するには、次のグローバル`KILL`ステートメントを使用して`2199023255957`トランザクションを強制終了します。

```sql
mysql> KILL 2199023255957;
Query OK, 0 rows affected (0.00 sec)
```

トランザクションを強制終了した後、再度`mysql.tidb_mdl_view`ビューを選択できます。現時点では、前のトランザクションは出力に表示されません。これは、DDL がブロックされていないことを意味します。

```sql
SELECT * FROM mysql.tidb_mdl_view\G
Empty set (0.01 sec)
```

## 原則 {#principles}

### この件についての説明 {#description-of-the-issue}

TiDB での DDL 操作はオンライン DDL モードです。 DDL ステートメントの実行中、変更対象の定義済みオブジェクトのメタデータ バージョンには、複数のマイナー バージョン変更が加えられる可能性があります。オンライン非同期メタデータ変更アルゴリズムは、2 つの隣接するマイナー バージョンに互換性があることのみを確立します。つまり、2 つのバージョン間の操作によって、DDL が変更するオブジェクトのデータの一貫性が損なわれることはありません。

テーブルにインデックスを追加すると、DDL ステートメントの状態は次のように変化します: なし -&gt; 削除のみ、削除のみ -&gt; 書き込みのみ、書き込みのみ -&gt; 書き込み Reorg、書き込み Reorg -&gt; パブリック。

次のトランザクションのコミット プロセスは、前述の制約に違反します。

| トランザクション | トランザクションで使用されるバージョン | クラスター内の最新バージョン | バージョンの違い |
| :------- | :------------------ | :------------- | :------- |
| txn1     | なし                  | なし             | 0        |
| txn2     | 削除のみ                | 削除のみ           | 0        |
| txn3     | 書き込み専用              | 書き込み専用         | 0        |
| txn4     | なし                  | 書き込み専用         | 2        |
| txn5     | WriteReorg          | WriteReorg     | 0        |
| txn6     | 書き込み専用              | WriteReorg     | 1        |
| txn7     | 公共                  | 公共             | 0        |

上の表では、 `txn4`がコミットされたときに使用されるメタデータのバージョンは、クラスター内の最新バージョンとは 2 つのバージョンが異なります。これにより、データの不整合が発生する可能性があります。

### 実装の詳細 {#implementation-details}

メタデータ ロックは、TiDB クラスター内のすべてのトランザクションで使用されるメタデータ バージョンが最大 1 バージョン異なることを保証します。この目標を達成するために、TiDB は次の 2 つのルールを実装します。

-   DML を実行すると、TiDB は、トランザクション コンテキストで DML によってアクセスされたメタデータ オブジェクト (テーブル、ビュー、対応するメタデータ バージョンなど) を記録します。これらのレコードは、トランザクションがコミットされるときにクリーンアップされます。
-   DDL ステートメントの状態が変更されると、最新バージョンのメタデータがすべての TiDB ノードにプッシュされます。 TiDB ノード上のこの状態変更に関連するすべてのトランザクションで使用されるメタデータ バージョンと現在のメタデータ バージョンの差が 2 未満である場合、TiDB ノードはメタデータ オブジェクトのメタデータ ロックを取得すると見なされます。次の状態変更は、クラスター内のすべての TiDB ノードがメタデータ オブジェクトのメタデータ ロックを取得した後にのみ実行できます。
