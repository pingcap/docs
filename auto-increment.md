---
title: AUTO_INCREMENT
summary: TiDB の AUTO_INCREMENT` 列属性について学習します。
---

# 自動インクリメント {#auto-increment}

このドキュメントでは、 `AUTO_INCREMENT`列属性の概念、実装原則、自動インクリメント関連の機能、制限などについて説明します。

<CustomContent platform="tidb">

> **注記：**
>
> `AUTO_INCREMENT`属性は本番環境でホットスポットを引き起こす可能性があります。詳細は[ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)参照してください。代わりに[`AUTO_RANDOM`](/auto-random.md)使用することをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> `AUTO_INCREMENT`属性は本番環境でホットスポットを引き起こす可能性があります。詳細は[ホットスポットの問題のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#handle-auto-increment-primary-key-hotspot-tables-using-auto_random)参照してください。代わりに[`AUTO_RANDOM`](/auto-random.md)使用することをお勧めします。

</CustomContent>

[`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)ステートメントの`AUTO_INCREMENT`パラメータを使用して、増分フィールドの初期値を指定することもできます。

## コンセプト {#concept}

`AUTO_INCREMENT` 、デフォルトの列値を自動的に入力するために使用される列属性です。2 `INSERT`ステートメントで`AUTO_INCREMENT`番目の列の値が指定されていない場合、システムは自動的にこの列に値を割り当てます。

パフォーマンス上の理由から、各TiDBサーバーには、 `AUTO_INCREMENT`個の数値が一括で割り当てられます（デフォルトでは3万個）。つまり、 `AUTO_INCREMENT`数値は一意であることが保証されますが、 `INSERT`ステートメントに割り当てられる値は、TiDBサーバーごとに単調なものになります。

> **注記：**
>
> すべての TiDB サーバーで`AUTO_INCREMENT`数値を単調にしたい場合、TiDB バージョンが v6.5.0 以降であれば、 [MySQL互換モード](#mysql-compatibility-mode)有効にすることをお勧めします。

以下は`AUTO_INCREMENT`の基本的な例です。

```sql
CREATE TABLE t(id int PRIMARY KEY AUTO_INCREMENT, c int);
```

```sql
INSERT INTO t(c) VALUES (1);
INSERT INTO t(c) VALUES (2);
INSERT INTO t(c) VALUES (3), (4), (5);
```

```sql
mysql> SELECT * FROM t;
+----+---+
| id | c |
+----+---+
| 1  | 1 |
| 2  | 2 |
| 3  | 3 |
| 4  | 4 |
| 5  | 5 |
+----+---+
5 rows in set (0.01 sec)
```

さらに、 `AUTO_INCREMENT`列の値を明示的に指定する`INSERT`ステートメントもサポートしています。これらの場合、TiDB は明示的に指定された値を保存します。

```sql
INSERT INTO t(id, c) VALUES (6, 6);
```

```sql
mysql> SELECT * FROM t;
+----+---+
| id | c |
+----+---+
| 1  | 1 |
| 2  | 2 |
| 3  | 3 |
| 4  | 4 |
| 5  | 5 |
| 6  | 6 |
+----+---+
6 rows in set (0.01 sec)
```

上記の使用法はMySQLの`AUTO_INCREMENT`と同じです。ただし、暗黙的に割り当てられる具体的な値に関しては、TiDBはMySQLとは大きく異なります。

## 実施原則 {#implementation-principles}

TiDB は`AUTO_INCREMENT`暗黙的な割り当てを次のように実装します。

各自動インクリメント列には、割り当てられたIDの最大値を記録するために、グローバルに参照可能なキーと値のペアが使用されます。分散環境では、ノード間の通信にはオーバーヘッドが伴います。そのため、ライトアンプリフィケーションの問題を回避するために、各TiDBノードはIDを割り当てる際に、連続するIDのバッチをキャッシュとして適用し、最初のバッチが割り当てられた後、次のIDのバッチを適用します。したがって、TiDBノードはIDを割り当てるたびに、storageノードにIDを要求しません。例：

```sql
CREATE TABLE t(id int UNIQUE KEY AUTO_INCREMENT, c int);
```

クラスター内に2つのTiDBインスタンス（ `A`と`B`があるとします。7テーブルに対してそれぞれ`t`と`B` `A` `INSERT`ステートメントを実行すると、次のようになります。

```sql
INSERT INTO t (c) VALUES (1)
```

インスタンス`A` `[1,30000]`の自動インクリメント ID をキャッシュし、インスタンス`B` `[30001,60000]`の自動インクリメント ID をキャッシュしている可能性があります。実行される`INSERT`ステートメントでは、各インスタンスのキャッシュされた ID が`AUTO_INCREMENT`番目の列にデフォルト値として割り当てられます。

## 基本機能 {#basic-features}

### ユニークさ {#uniqueness}

> **警告：**
>
> クラスタに複数のTiDBインスタンスがあり、テーブルスキーマに自動インクリメントIDが含まれている場合、明示的な挿入と暗黙的な割り当て（自動インクリメント列のデフォルト値とカスタム値の使用）を同時に使用しないことを推奨します。そうしないと、暗黙的に割り当てられた値の一意性が損なわれる可能性があります。

上記の例では、次の操作を順番に実行します。

1.  クライアントはインスタンス`B`にステートメント`INSERT INTO t VALUES (2, 1)`を挿入し、 `id`を`2`に設定します。ステートメントは正常に実行されます。

2.  クライアントはインスタンス`A`にステートメント`INSERT INTO t (c) (1)`送信します。このステートメントでは`id`の値が指定されていないため、ID は`A`に割り当てられます。現在、 `A` `[1, 30000]`のIDをキャッシュしているため、自動インクリメントIDの値として`2`割り当て、ローカルカウンタを`1`増加させる可能性があります。このとき、ID `2`のデータが既にデータベースに存在するため、 `Duplicated Error`エラーが返されます。

### 単調性 {#monotonicity}

TiDBは、サーバーごとに`AUTO_INCREMENT`値が単調増加（常に増加）であることを保証します。1から3までの連続した`AUTO_INCREMENT`値が生成される次の例を考えてみましょう。

```sql
CREATE TABLE t (a int PRIMARY KEY AUTO_INCREMENT, b timestamp NOT NULL DEFAULT NOW());
INSERT INTO t (a) VALUES (NULL), (NULL), (NULL);
SELECT * FROM t;
```

```sql
Query OK, 0 rows affected (0.11 sec)

Query OK, 3 rows affected (0.02 sec)
Records: 3  Duplicates: 0  Warnings: 0

+---+---------------------+
| a | b                   |
+---+---------------------+
| 1 | 2020-09-09 20:38:22 |
| 2 | 2020-09-09 20:38:22 |
| 3 | 2020-09-09 20:38:22 |
+---+---------------------+
3 rows in set (0.00 sec)
```

単調性と連続性は必ずしも同じではありません。次の例を考えてみましょう。

```sql
CREATE TABLE t (id INT NOT NULL PRIMARY KEY auto_increment, a VARCHAR(10), cnt INT NOT NULL DEFAULT 1, UNIQUE KEY (a));
INSERT INTO t (a) VALUES ('A'), ('B');
SELECT * FROM t;
INSERT INTO t (a) VALUES ('A'), ('C') ON DUPLICATE KEY UPDATE cnt = cnt + 1;
SELECT * FROM t;
```

```sql
Query OK, 0 rows affected (0.00 sec)

Query OK, 2 rows affected (0.00 sec)
Records: 2  Duplicates: 0  Warnings: 0

+----+------+-----+
| id | a    | cnt |
+----+------+-----+
|  1 | A    |   1 |
|  2 | B    |   1 |
+----+------+-----+
2 rows in set (0.00 sec)

Query OK, 3 rows affected (0.00 sec)
Records: 2  Duplicates: 1  Warnings: 0

+----+------+-----+
| id | a    | cnt |
+----+------+-----+
|  1 | A    |   2 |
|  2 | B    |   1 |
|  4 | C    |   1 |
+----+------+-----+
3 rows in set (0.00 sec)
```

この例では、 `INSERT INTO t (a) VALUES ('A'), ('C') ON DUPLICATE KEY UPDATE cnt = cnt + 1;`のキー`A`の`INSERT`に値`3`の`AUTO_INCREMENT`が割り当てられていますが、この`INSERT`文には重複キー`A`が含まれているため、実際には使用されません。これにより、シーケンスが連続しないギャップが発生します。この動作はMySQLとは異なりますが、有効とみなされます。MySQLでは、トランザクションが中止されてロールバックされるなどの他のシナリオでも、シーケンスにギャップが発生します。

## 自動IDキャッシュ {#auto-id-cache}

異なるTiDBサーバーに対して`INSERT`操作を実行すると、 `AUTO_INCREMENT`番目のシーケンスが大幅に*ジャンプする*ように見える場合があります。これは、各サーバーが`AUTO_INCREMENT`の値のキャッシュを独自に持っているためです。

```sql
CREATE TABLE t (a int PRIMARY KEY AUTO_INCREMENT, b timestamp NOT NULL DEFAULT NOW());
INSERT INTO t (a) VALUES (NULL), (NULL), (NULL);
INSERT INTO t (a) VALUES (NULL);
SELECT * FROM t;
```

```sql
Query OK, 1 row affected (0.03 sec)

+---------+---------------------+
| a       | b                   |
+---------+---------------------+
|       1 | 2020-09-09 20:38:22 |
|       2 | 2020-09-09 20:38:22 |
|       3 | 2020-09-09 20:38:22 |
| 2000001 | 2020-09-09 20:43:43 |
+---------+---------------------+
4 rows in set (0.00 sec)
```

初期TiDBサーバーに対する新たな`INSERT`操作は、 `AUTO_INCREMENT`の値`4`生成します。これは、初期TiDBサーバーの`AUTO_INCREMENT`キャッシュにまだ割り当て用のスペースが残っているためです。この場合、 `4`の値が`2000001`の後に挿入されるため、値のシーケンスはグローバルに単調であるとは考えられません。

```sql
mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.01 sec)

mysql> SELECT * FROM t ORDER BY b;
+---------+---------------------+
| a       | b                   |
+---------+---------------------+
|       1 | 2020-09-09 20:38:22 |
|       2 | 2020-09-09 20:38:22 |
|       3 | 2020-09-09 20:38:22 |
| 2000001 | 2020-09-09 20:43:43 |
|       4 | 2020-09-09 20:44:43 |
+---------+---------------------+
5 rows in set (0.00 sec)
```

`AUTO_INCREMENT`キャッシュはTiDBサーバーの再起動後には保持されません。最初のTiDBサーバーの再起動後、以下の`INSERT`文が実行されます。

```sql
mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.01 sec)

mysql> SELECT * FROM t ORDER BY b;
+---------+---------------------+
| a       | b                   |
+---------+---------------------+
|       1 | 2020-09-09 20:38:22 |
|       2 | 2020-09-09 20:38:22 |
|       3 | 2020-09-09 20:38:22 |
| 2000001 | 2020-09-09 20:43:43 |
|       4 | 2020-09-09 20:44:43 |
| 2030001 | 2020-09-09 20:54:11 |
+---------+---------------------+
6 rows in set (0.00 sec)
```

TiDBサーバーの再起動頻度が高いと、 `AUTO_INCREMENT`の値が枯渇する可能性があります。上記の例では、初期TiDBサーバーのキャッシュにはまだ`[5-30000]`空き値があります。これらの値は失われ、再割り当てされません。

`AUTO_INCREMENT`値が連続しているという前提に頼るのは推奨されません。次の例では、TiDBサーバーに`[2000001-2030000]`値のキャッシュがあります。手動で`2029998`値を挿入すると、新しいキャッシュ範囲が取得される際の動作を確認できます。

```sql
mysql> INSERT INTO t (a) VALUES (2029998);
Query OK, 1 row affected (0.01 sec)

mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.01 sec)

mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.00 sec)

mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.02 sec)

mysql> INSERT INTO t (a) VALUES (NULL);
Query OK, 1 row affected (0.01 sec)

mysql> SELECT * FROM t ORDER BY b;
+---------+---------------------+
| a       | b                   |
+---------+---------------------+
|       1 | 2020-09-09 20:38:22 |
|       2 | 2020-09-09 20:38:22 |
|       3 | 2020-09-09 20:38:22 |
| 2000001 | 2020-09-09 20:43:43 |
|       4 | 2020-09-09 20:44:43 |
| 2030001 | 2020-09-09 20:54:11 |
| 2029998 | 2020-09-09 21:08:11 |
| 2029999 | 2020-09-09 21:08:11 |
| 2030000 | 2020-09-09 21:08:11 |
| 2060001 | 2020-09-09 21:08:11 |
| 2060002 | 2020-09-09 21:08:11 |
+---------+---------------------+
11 rows in set (0.00 sec)
```

値`2030000`が挿入された後、次の値は`2060001`です。このシーケンスのジャンプは、別の TiDBサーバーが中間キャッシュ範囲`[2030001-2060000]`取得しているためです。複数の TiDB サーバーが展開されている場合、キャッシュ要求がインターリーブされるため、 `AUTO_INCREMENT`シーケンスにギャップが生じます。

### キャッシュサイズの制御 {#cache-size-control}

TiDBの以前のバージョンでは、自動インクリメントIDのキャッシュサイズはユーザーにとって透過的でした。v3.0.14、v3.1.2、v4.0.rc-2以降、TiDBは`AUTO_ID_CACHE`テーブルオプションを導入し、ユーザーが自動インクリメントIDを割り当てるためのキャッシュサイズを設定できるようになりました。

```sql
CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 100;
Query OK, 0 rows affected (0.02 sec)

INSERT INTO t values();
Query OK, 1 row affected (0.00 sec)

SELECT * FROM t;
+---+
| a |
+---+
| 1 |
+---+
1 row in set (0.01 sec)

SHOW CREATE TABLE t;
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                                             |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` int NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`a`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=101 /*T![auto_id_cache] AUTO_ID_CACHE=100 */ |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

この時点で TiDB を再起動すると、自動増分 ID キャッシュは失われ、新しい挿入操作では、以前にキャッシュされた範囲を超えた高い値から始まる ID が割り当てられます。

```sql
INSERT INTO t VALUES();
Query OK, 1 row affected (0.00 sec)

SELECT * FROM t;
+-----+
| a   |
+-----+
|   1 |
| 101 |
+-----+
2 rows in set (0.01 sec)
```

新しく割り当てられた値は`101` 。これは、自動インクリメントIDを割り当てるためのキャッシュのサイズが`100`であることを示しています。

さらに、バッチ`INSERT`ステートメント内の連続 ID の長さが`AUTO_ID_CACHE`を超えると、TiDB はそれに応じてキャッシュ サイズを増やし、ステートメントがデータを適切に挿入できるようにします。

### 自動増分IDキャッシュをクリアする {#clear-the-auto-increment-id-cache}

場合によっては、データの一貫性を確保するために、自動増分IDキャッシュをクリアする必要がある場合があります。例：

<CustomContent platform="tidb">

-   [データ移行（DM）](/dm/dm-overview.md)使用した増分レプリケーションのシナリオでは、レプリケーションが完了すると、下流の TiDB へのデータ書き込みは DM からアプリケーションの書き込み操作に切り替わります。同時に、自動インクリメント列の ID 書き込みモードは通常、明示的な挿入から暗黙的な割り当てに切り替わります。
-   TiDB Lightningはデータのインポートを完了すると、自動増分IDキャッシュを自動的にクリアします。しかし、TiCDCは増分データ同期後にキャッシュを自動的にクリアしません。そのため、TiCDCを停止した後、フェイルオーバーを実行する前に、下流クラスタの自動増分IDキャッシュを手動でクリアする必要があります。

</CustomContent>
<CustomContent platform="tidb-cloud">

-   [データ移行](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)機能を使用した増分レプリケーションのシナリオでは、レプリケーションが完了すると、下流 TiDB へのデータ書き込みは DM からアプリケーションの書き込み操作に切り替わります。同時に、自動インクリメント列の ID 書き込みモードは通常、明示的な挿入から暗黙的な割り当てに切り替わります。
-   TiDB Lightningはデータのインポートを完了すると、自動増分IDキャッシュを自動的にクリアします。しかし、TiCDCは増分データ同期後にキャッシュを自動的にクリアしません。そのため、TiCDCを停止した後、フェイルオーバーを実行する前に、下流クラスタの自動増分IDキャッシュを手動でクリアする必要があります。

</CustomContent>

-   アプリケーションで明示的なIDの挿入と暗黙的なIDの割り当ての両方を行う場合、将来暗黙的に割り当てられたIDと以前に明示的に挿入されたIDとの競合を回避するために、自動インクリメントIDキャッシュをクリアする必要があります。競合が発生すると、主キーの競合エラーが発生する可能性があります。詳細については、 [ユニークさ](/auto-increment.md#uniqueness)参照してください。

クラスター内のすべてのTiDBノードの自動インクリメントIDキャッシュをクリアするには、 `ALTER TABLE`ステートメントを`AUTO_INCREMENT = 0`とともに実行します。例:

```sql
CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 100;
Query OK, 0 rows affected (0.02 sec)

INSERT INTO t VALUES();
Query OK, 1 row affected (0.02 sec)

INSERT INTO t VALUES(50);
Query OK, 1 row affected (0.00 sec)

SELECT * FROM t;
+----+
| a  |
+----+
|  1 |
| 50 |
+----+
2 rows in set (0.01 sec)
```

```sql
ALTER TABLE t AUTO_INCREMENT = 0;
Query OK, 0 rows affected, 1 warning (0.07 sec)

SHOW WARNINGS;
+---------+------+-------------------------------------------------------------------------+
| Level   | Code | Message                                                                 |
+---------+------+-------------------------------------------------------------------------+
| Warning | 1105 | Can't reset AUTO_INCREMENT to 0 without FORCE option, using 101 instead |
+---------+------+-------------------------------------------------------------------------+
1 row in set (0.01 sec)

INSERT INTO t VALUES();
Query OK, 1 row affected (0.02 sec)

SELECT * FROM t;
+-----+
| a   |
+-----+
|   1 |
|  50 |
| 101 |
+-----+
3 rows in set (0.01 sec)
```

### 自動増分ステップサイズとオフセット {#auto-increment-step-size-and-offset}

v3.0.9 および v4.0.0-rc.1 以降では、MySQL の動作と同様に、自動インクリメント列に暗黙的に割り当てられる値は、 `@@auto_increment_increment`および`@@auto_increment_offset`セッション変数によって制御されます。

自動インクリメント列に暗黙的に割り当てられる値 (ID) は、次の式を満たします。

`(ID - auto_increment_offset) % auto_increment_increment == 0`

## MySQL互換モード {#mysql-compatibility-mode}

TiDBは、MySQL互換の自動インクリメント列モードを提供し、IDが厳密に増加し、ギャップが最小限に抑えられることを保証します。このモードを有効にするには、テーブル作成時に`AUTO_ID_CACHE`を`1`に設定します。

```sql
CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 1;
```

`AUTO_ID_CACHE` `1`に設定すると、すべての TiDB インスタンスにわたって ID が厳密に増加し、各 ID が一意であることが保証され、デフォルトのキャッシュ モード (キャッシュされた値が 30000 の`AUTO_ID_CACHE 0` ) と比較して ID 間のギャップが最小限に抑えられます。

たとえば、 `AUTO_ID_CACHE 1`の場合、次のようなシーケンスが表示されます。

```sql
INSERT INTO t VALUES (); -- Returns ID 1
INSERT INTO t VALUES (); -- Returns ID 2
INSERT INTO t VALUES (); -- Returns ID 3
-- After failover
INSERT INTO t VALUES (); -- Might return ID 5
```

対照的に、デフォルトのキャッシュ（ `AUTO_ID_CACHE 0` ）では、より大きなギャップが発生する可能性があります。

```sql
INSERT INTO t VALUES (); -- Returns ID 1
INSERT INTO t VALUES (); -- Returns ID 2
-- New TiDB instance allocates next batch
INSERT INTO t VALUES (); -- Returns ID 30001
```

IDは常に増加し、 `AUTO_ID_CACHE 0`のような大きなギャップは発生しませんが、以下のシナリオでは、シーケンスに小さなギャップが発生する可能性があります。これらのギャップは、IDの一意性と厳密に増加する性質の両方を維持するために必要です。

-   プライマリインスタンスが終了またはクラッシュした場合のフェイルオーバー中

    MySQL互換モードを有効にすると、割り当てられたIDは**一意かつ****単調増加**となり、動作はMySQLとほぼ同じになります。複数のTiDBインスタンスにまたがってアクセスする場合でも、IDの単調性は維持されます。ただし、集中型サービスのプライマリインスタンスがクラッシュした場合、一部のIDが連続しなくなる可能性があります。これは、セカンダリインスタンスがフェイルオーバー時にプライマリインスタンスによって割り当てられた一部のIDを破棄することで、IDの一意性を確保するためです。

-   TiDBノードのローリングアップグレード中

-   通常の同時トランザクション中（MySQLと同様）

> **注記：**
>
> `AUTO_ID_CACHE 1`の動作とパフォーマンスは、TiDB のバージョンごとに進化しています。
>
> -   v6.4.0 より前では、各 ID 割り当てに TiKV トランザクションが必要であり、パフォーマンスに影響します。
> -   v6.4.0 では、TiDB は、ID 割り当てをメモリ内操作として実行する集中割り当てサービスを導入し、パフォーマンスを大幅に向上させました。
> -   v8.1.0以降、TiDBはプライマリノード終了時の自動的な`forceRebase`操作を削除し、再起動を高速化します。これによりフェイルオーバー時に非連続のIDが追加される可能性がありますが、多くのテーブルで`AUTO_ID_CACHE 1`使用されている場合に書き込みブロックが発生するのを防ぎます。

## 制限 {#restrictions}

現在、 `AUTO_INCREMENT` TiDB で使用する場合、次の制限があります。

-   TiDB v6.6.0 以前のバージョンの場合、定義された列は主キーまたはインデックス プレフィックスのいずれかである必要があります。
-   `INTEGER` 、 `FLOAT` 、または`DOUBLE`タイプの列に定義する必要があります。
-   `DEFAULT`列目の値と同じ列には指定できません。
-   `ALTER TABLE` 、属性`AUTO_INCREMENT`を持つ列を追加または変更するために使用できません。これには、属性`AUTO_INCREMENT`既存の列に追加するために`ALTER TABLE ... MODIFY/CHANGE COLUMN`使用することや、属性`AUTO_INCREMENT`を持つ列を追加するために`ALTER TABLE ... ADD COLUMN`使用することも含まれます。
-   `ALTER TABLE` `AUTO_INCREMENT`属性を削除するために使用できます。ただし、v2.1.18 および v3.0.4 以降、TiDB はセッション変数`@@tidb_allow_remove_auto_inc`使用して、列の`AUTO_INCREMENT`の属性を削除するために`ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`使用できるかどうかを制御します。デフォルトでは、 `ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`使用して`AUTO_INCREMENT`番目の属性を削除することはできません。
-   `ALTER TABLE` 、 `AUTO_INCREMENT`値を小さい値に設定するには`FORCE`オプションが必要です。
-   `AUTO_INCREMENT` `MAX(<auto_increment_column>)`より小さい値に設定すると、既存の値がスキップされないため、キーが重複することになります。
