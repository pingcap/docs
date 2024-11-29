---
title: AUTO_INCREMENT
summary: TiDB の AUTO_INCREMENT` 列属性について学習します。
---

# 自動インクリメント {#auto-increment}

このドキュメントでは、 `AUTO_INCREMENT`列属性の概念、実装原則、自動インクリメント関連の機能、制限などについて説明します。

<CustomContent platform="tidb">

> **注記：**
>
> `AUTO_INCREMENT`属性は本番環境でホットスポットを引き起こす可能性があります。詳細については[ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)参照してください。代わりに[`AUTO_RANDOM`](/auto-random.md)使用することをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> `AUTO_INCREMENT`属性は本番環境でホットスポットを引き起こす可能性があります。詳細については[ホットスポットの問題のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#handle-auto-increment-primary-key-hotspot-tables-using-auto_random)参照してください。代わりに[`AUTO_RANDOM`](/auto-random.md)使用することをお勧めします。

</CustomContent>

[`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)ステートメントの`AUTO_INCREMENT`パラメータを使用して、増分フィールドの初期値を指定することもできます。

## コンセプト {#concept}

`AUTO_INCREMENT`は、デフォルトの列値を自動的に入力するために使用される列属性です。 `INSERT`ステートメントで`AUTO_INCREMENT`列の値が指定されていない場合、システムはこの列に値を自動的に割り当てます。

パフォーマンス上の理由から、各 TiDBサーバーには`AUTO_INCREMENT`数値が値のバッチで割り当てられます (デフォルトでは 3 万)。つまり、 `AUTO_INCREMENT`数値は一意であることが保証されますが、 `INSERT`ステートメントに割り当てられる値は TiDBサーバーごとに単調になります。

> **注記：**
>
> すべての TiDB サーバーで`AUTO_INCREMENT`数値を単調にしたい場合、および TiDB バージョンが v6.5.0 以降である場合は、 [MySQL互換モード](#mysql-compatibility-mode)を有効にすることをお勧めします。

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

さらに、 `AUTO_INCREMENT`列の値を明示的に指定する`INSERT`のステートメントもサポートしています。このような場合、TiDB は明示的に指定された値を保存します。

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

上記の使用方法は、MySQL の`AUTO_INCREMENT`と同じです。ただし、暗黙的に割り当てられる特定の値に関しては、TiDB は MySQL とは大きく異なります。

## 実施原則 {#implementation-principles}

TiDB は`AUTO_INCREMENT`暗黙的な割り当てを次のように実装します。

各自動増分列では、割り当てられた最大 ID を記録するために、グローバルに表示されるキーと値のペアが使用されます。分散環境では、ノード間の通信にオーバーヘッドが伴います。したがって、書き込み増幅の問題を回避するために、各 TiDB ノードは、ID を割り当てるときに連続する ID のバッチをキャッシュとして適用し、最初のバッチが割り当てられた後に次の ID のバッチを適用します。したがって、TiDB ノードは、ID を割り当てるたびにstorageノードに ID を適用しません。例:

```sql
CREATE TABLE t(id int UNIQUE KEY AUTO_INCREMENT, c int);
```

クラスター内に`A`と`B` 2 つの TiDB インスタンスがあるとします。 `A`と`B`でそれぞれ`t`テーブルに対して`INSERT`ステートメントを実行すると、次のようになります。

```sql
INSERT INTO t (c) VALUES (1)
```

インスタンス`A` `[1,30000]`の自動インクリメント ID をキャッシュし、インスタンス`B`は`[30001,60000]`の自動インクリメント ID をキャッシュする可能性があります。実行される`INSERT`のステートメントでは、各インスタンスのこれらのキャッシュされた ID がデフォルト値として`AUTO_INCREMENT`列に割り当てられます。

## 基本機能 {#basic-features}

### ユニークさ {#uniqueness}

> **警告：**
>
> クラスターに複数の TiDB インスタンスがあり、テーブル スキーマに自動インクリメント ID が含まれている場合は、明示的な挿入と暗黙的な割り当てを同時に使用しないことをお勧めします。つまり、自動インクリメント列のデフォルト値とカスタム値を使用します。そうしないと、暗黙的に割り当てられた値の一意性が損なわれる可能性があります。

上記の例では、次の操作を順番に実行します。

1.  クライアントはインスタンス`B`にステートメント`INSERT INTO t VALUES (2, 1)`を挿入し、 `id`を`2`に設定します。ステートメントは正常に実行されます。

2.  クライアントはインスタンス`A`にステートメント`INSERT INTO t (c) (1)`送信します。このステートメントでは`id`の値が指定されていないため、ID は`A`によって割り当てられます。現在、 `A` `[1, 30000]`の ID をキャッシュしているため、自動インクリメント ID の値として`2`割り当て、ローカル カウンターを`1`増加させる可能性があります。この時点で、ID が`2`のデータがすでにデータベースに存在するため、 `Duplicated Error`エラーが返されます。

### 単調性 {#monotonicity}

TiDB は、サーバーごとに`AUTO_INCREMENT`値が単調 (常に増加) であることを保証します。1 ～ 3 の連続した`AUTO_INCREMENT`の値が生成される次の例を考えてみましょう。

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

単調性は連続性と同じ保証ではありません。次の例を考えてみましょう。

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

この例では、 `INSERT INTO t (a) VALUES ('A'), ('C') ON DUPLICATE KEY UPDATE cnt = cnt + 1;`のキー`A`の`INSERT`に`3`の`AUTO_INCREMENT`の値が割り当てられていますが、この`INSERT`ステートメントには重複キー`A`含まれているため、使用されることはありません。これにより、シーケンスが連続しないギャップが発生します。この動作は、MySQL とは異なりますが、合法であると見なされます。MySQL では、トランザクションが中止されロールバックされるなどの他のシナリオでもシーケンスにギャップが発生します。

## 自動IDキャッシュ {#auto-id-cache}

異なる TiDBサーバーに対して`INSERT`操作を実行すると、 `AUTO_INCREMENT`シーケンスが大幅に*ジャンプする*ように見える場合があります。これは、各サーバーが独自の`AUTO_INCREMENT`値のキャッシュを持っているために発生します。

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

初期 TiDBサーバーに対する新しい`INSERT`操作により、 `AUTO_INCREMENT`の値`4`生成されます。これは、初期 TiDBサーバーの`AUTO_INCREMENT`キャッシュに割り当て用のスペースがまだ残っているためです。この場合、 `4`の値が`2000001`の値の後に挿入されるため、値のシーケンスはグローバルに単調であるとは見なされません。

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

`AUTO_INCREMENT`キャッシュは TiDBサーバーの再起動後は保持されません。最初の TiDBサーバーが再起動された後、次の`INSERT`ステートメントが実行されます。

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

TiDBサーバーの再起動率が高いと、 `AUTO_INCREMENT`の値が枯渇する可能性があります。上記の例では、最初の TiDBサーバーのキャッシュにはまだ`[5-30000]`値が空いています。これらの値は失われ、再割り当てされません。

`AUTO_INCREMENT`値が連続していることに依存することは推奨されません。TiDBサーバーに値`[2000001-2030000]`のキャッシュがある次の例を考えてみましょう。値`2029998`手動で挿入すると、新しいキャッシュ範囲が取得されるときの動作を確認できます。

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

値`2030000`が挿入された後、次の値は`2060001`です。このシーケンスのジャンプは、別の TiDBサーバーが中間キャッシュ範囲`[2030001-2060000]`を取得するためです。複数の TiDB サーバーが展開されている場合、キャッシュ要求がインターリーブされるため、 `AUTO_INCREMENT`シーケンスにギャップが生じます。

### キャッシュサイズの制御 {#cache-size-control}

以前のバージョンの TiDB では、自動インクリメント ID のキャッシュ サイズはユーザーにとって透過的でした。v3.0.14、v3.1.2、v4.0.rc-2 以降、TiDB では`AUTO_ID_CACHE`テーブル オプションが導入され、ユーザーが自動インクリメント ID を割り当てるためのキャッシュ サイズを設定できるようになりました。

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
  `a` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`a`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin AUTO_INCREMENT=101 /*T![auto_id_cache] AUTO_ID_CACHE=100 */ |
+-------+------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)
```

この時点で TiDB を再起動すると、自動増分 ID キャッシュは失われ、新しい挿入操作では、以前にキャッシュされた範囲を超えたより高い値から ID が割り当てられます。

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

新しく割り当てられた値は`101`です。これは、自動インクリメント ID を割り当てるためのキャッシュのサイズが`100`であることを示しています。

さらに、バッチ`INSERT`ステートメント内の連続 ID の長さが`AUTO_ID_CACHE`を超えると、TiDB はそれに応じてキャッシュ サイズを増やし、ステートメントがデータを適切に挿入できるようにします。

### 自動増分IDキャッシュをクリアする {#clear-the-auto-increment-id-cache}

シナリオによっては、データの一貫性を確保するために自動増分 ID キャッシュをクリアする必要がある場合があります。例:

<CustomContent platform="tidb">

-   [データ移行 (DM)](/dm/dm-overview.md)使用した増分レプリケーションのシナリオでは、レプリケーションが完了すると、ダウンストリーム TiDB へのデータ書き込みが DM からアプリケーションの書き込み操作に切り替わります。一方、自動インクリメント列の ID 書き込みモードは、通常、明示的な挿入から暗黙的な割り当てに切り替わります。

</CustomContent>
<CustomContent platform="tidb-cloud">

-   [データ移行](/tidb-cloud/migrate-incremental-data-from-mysql-using-data-migration.md)機能を使用した増分レプリケーションのシナリオでは、レプリケーションが完了すると、ダウンストリーム TiDB へのデータ書き込みが DM からアプリケーションの書き込み操作に切り替わります。一方、自動増分列の ID 書き込みモードは通常、明示的な挿入から暗黙的な割り当てに切り替わります。

</CustomContent>

-   アプリケーションで明示的な ID の挿入と暗黙的な ID の割り当ての両方を行う場合は、自動増分 ID キャッシュをクリアして、将来暗黙的に割り当てられた ID と以前に明示的に挿入された ID の競合を回避する必要があります。競合が発生すると、主キーの競合エラーが発生する可能性があります。詳細については、 [ユニークさ](/auto-increment.md#uniqueness)参照してください。

クラスター内のすべての TiDB ノードの自動インクリメント ID キャッシュをクリアするには、 `ALTER TABLE`ステートメントを`AUTO_INCREMENT = 0`で実行します。例:

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

v3.0.9 および v4.0.0-rc.1 以降では、MySQL の動作と同様に、自動インクリメント列に暗黙的に割り当てられる値は、セッション変数`@@auto_increment_increment`および`@@auto_increment_offset`によって制御されます。

自動インクリメント列に暗黙的に割り当てられる値 (ID) は、次の式を満たします。

`(ID - auto_increment_offset) % auto_increment_increment == 0`

## MySQL互換モード {#mysql-compatibility-mode}

TiDB v6.4.0 では、集中型の自動増分 ID 割り当てサービスが導入されています。各リクエストでは、TiDB インスタンスにデータをキャッシュする代わりに、このサービスから自動増分 ID が割り当てられます。

現在、集中割り当てサービスは TiDB プロセス内にあり、DDL 所有者のように機能します。1 つの TiDB インスタンスがプライマリ ノードとして ID を割り当て、他の TiDB インスタンスはセカンダリ ノードとして機能します。高可用性を確保するために、プライマリ インスタンスに障害が発生すると、TiDB は自動フェイルオーバーを開始します。

MySQL 互換モードを使用するには、テーブルを作成するときに`AUTO_ID_CACHE`から`1`設定します。

```sql
CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 1;
```

> **注記：**
>
> TiDB では、 `AUTO_ID_CACHE`から`1`に設定すると、TiDB は ID をキャッシュしなくなります。ただし、実装は TiDB のバージョンによって異なります。
>
> -   TiDB v6.4.0 より前では、ID を割り当てるには、各リクエストに対して`AUTO_INCREMENT`値を保持する TiKV トランザクションが必要であったため、 `AUTO_ID_CACHE`から`1`に設定するとパフォーマンスが低下します。
> -   TiDB v6.4.0 以降では、集中割り当てサービスが導入されているため、 `AUTO_INCREMENT`値の変更は TiDB プロセス内のメモリ内操作のみになるため、より高速になります。
> -   `AUTO_ID_CACHE`を`0`に設定すると、TiDB はデフォルトのキャッシュ サイズ`30000`を使用します。

MySQL 互換モードを有効にすると、割り当てられた ID は**一意**かつ**単調増加し**、動作は MySQL とほぼ同じになります。TiDB インスタンス間でアクセスしても、ID は単調増加を維持します。集中自動増分 ID 割り当てサービスのプライマリ インスタンスが終了した場合 (たとえば、TiDB ノードの再起動中) またはクラッシュした場合のみ、連続しない ID が存在する可能性があります。これは、セカンダリ インスタンスがフェイルオーバー中にプライマリ インスタンスによって割り当てられた一部の ID を破棄して、ID の一意性を確保するためです。

## 制限 {#restrictions}

現在、 `AUTO_INCREMENT` TiDB で使用する場合、次の制限があります。

-   TiDB v6.6.0 以前のバージョンの場合、定義された列は主キーまたはインデックス プレフィックスのいずれかである必要があります。
-   `INTEGER` 、 `FLOAT` 、または`DOUBLE`タイプの列に定義する必要があります。
-   `DEFAULT`列目の値と同じ列には指定できません。
-   `ALTER TABLE` 、属性`AUTO_INCREMENT`を持つ列を追加または変更するために使用することはできません。これには、属性`AUTO_INCREMENT`を既存の列に追加するために`ALTER TABLE ... MODIFY/CHANGE COLUMN`使用することや、属性`AUTO_INCREMENT`を持つ列を追加するために`ALTER TABLE ... ADD COLUMN`使用することも含まれます。
-   `ALTER TABLE` `AUTO_INCREMENT`属性を削除するために使用できます。ただし、v2.1.18 および v3.0.4 以降では、TiDB はセッション変数`@@tidb_allow_remove_auto_inc`使用して、列の`AUTO_INCREMENT`属性を削除するために`ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`使用できるかどうかを制御します。デフォルトでは、 `ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`使用して`AUTO_INCREMENT`属性を削除することはできません。
-   `ALTER TABLE`では、 `AUTO_INCREMENT`値を小さい値に設定するために`FORCE`オプションが必要です。
-   `AUTO_INCREMENT`を`MAX(<auto_increment_column>)`より小さい値に設定すると、既存の値がスキップされないため、キーが重複することになります。
