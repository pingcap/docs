---
title: AUTO_INCREMENT
summary: Learn the `AUTO_INCREMENT` column attribute of TiDB.
---

# 自動増加 {#auto-increment}

このドキュメントでは、 `AUTO_INCREMENT`列の属性を紹介します。これには、その概念、実装の原則、自動インクリメント関連の機能、および制限が含まれます。

## 概念 {#concept}

`AUTO_INCREMENT`は、デフォルトの列値を自動的に入力するために使用される列属性です。 `INSERT`ステートメントで`AUTO_INCREMENT`列の値が指定されていない場合、システムはこの列に値を自動的に割り当てます。

パフォーマンス上の理由から、 `AUTO_INCREMENT`の数値が値のバッチ（デフォルトでは3万）で各TiDBサーバーに割り当てられます。つまり、 `AUTO_INCREMENT`の数値は一意であることが保証されていますが、 `INSERT`のステートメントに割り当てられた値は、TiDBサーバーごとに単調になります。

以下は`AUTO_INCREMENT`の基本的な例です：

{{< copyable "" >}}

```sql
CREATE TABLE t(id int PRIMARY KEY AUTO_INCREMENT, c int);
```

{{< copyable "" >}}

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

さらに、 `AUTO_INCREMENT`は、列の値を明示的に指定する`INSERT`のステートメントもサポートします。このような場合、TiDBは明示的に指定された値を格納します。

{{< copyable "" >}}

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

上記の使用法は、MySQLの`AUTO_INCREMENT`の使用法と同じです。ただし、暗黙的に割り当てられる特定の値に関しては、TiDBはMySQLとは大きく異なります。

## 実装の原則 {#implementation-principles}

TiDBは、次の方法で`AUTO_INCREMENT`の暗黙的な割り当てを実装します。

自動インクリメント列ごとに、グローバルに表示されるキーと値のペアを使用して、割り当てられた最大IDを記録します。分散環境では、ノード間の通信にいくらかのオーバーヘッドがあります。したがって、ライトアンプリフィケーションの問題を回避するために、各TiDBノードはIDを割り当てるときにキャッシュとして連続するIDのバッチを適用し、最初のバッチが割り当てられた後にIDの次のバッチを適用します。したがって、TiDBノードは、毎回IDを割り当てるときにIDのストレージノードに適用されません。例えば：

```sql
CREATE TABLE t(id int UNIQUE KEY AUTO_INCREMENT, c int);
```

クラスタに2つのTiDBインスタンス`A`と`B`があると仮定します。それぞれ`A`と`B`の`t`テーブルで`INSERT`ステートメントを実行する場合：

```sql
INSERT INTO t (c) VALUES (1)
```

インスタンス`A`は`[1,30000]`の自動インクリメントIDをキャッシュし、インスタンス`B`は`[30001,60000]`の自動インクリメントIDをキャッシュする場合があります。実行される`INSERT`のステートメントでは、各インスタンスのこれらのキャッシュされたIDがデフォルト値として`AUTO_INCREMENT`列に割り当てられます。

## 基本的な機能 {#basic-features}

### 独自性 {#uniqueness}

> **警告：**
>
> クラスタに複数のTiDBインスタンスがある場合、テーブルスキーマに自動インクリメントIDが含まれている場合は、明示的な挿入と暗黙的な割り当てを同時に使用しないことをお勧めします。つまり、自動インクリメント列とカスタムのデフォルト値を使用します。値。そうしないと、暗黙的に割り当てられた値の一意性が損なわれる可能性があります。

上記の例では、次の操作を順番に実行します。

1.  クライアントは、ステートメント`INSERT INTO t VALUES (2, 1)`をインスタンス`B`に挿入します。これにより、 `id`が`2`に設定されます。ステートメントは正常に実行されました。

2.  クライアントはステートメント`INSERT INTO t (c) (1)`をインスタンス`A`に送信します。このステートメントは`id`の値を指定しないため、IDは`A`によって割り当てられます。現在、 `A`は`[1, 30000]`のIDをキャッシュしているため、自動インクリメントIDの値として`2`を割り当て、ローカルカウンターを`1`増加させる可能性があります。このとき、IDが`2`のデータはデータベースに既に存在するため、 `Duplicated Error`エラーが返されます。

### 単調性 {#monotonicity}

TiDBは、サーバーごとに`AUTO_INCREMENT`の値が単調（常に増加）であることを保証します。 1〜3の連続する`AUTO_INCREMENT`の値が生成される次の例を考えてみます。

{{< copyable "" >}}

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

単調性は、連続と同じ保証ではありません。次の例を考えてみましょう。

{{< copyable "" >}}

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

この例では、 `3`の`AUTO_INCREMENT`値が`INSERT INTO t (a) VALUES ('A'), ('C') ON DUPLICATE KEY UPDATE cnt = cnt + 1;`のキー`A`の`INSERT`に割り当てられていますが、この`INSERT`ステートメントに重複するキー`A`が含まれているため、使用されません。これにより、シーケンスが連続しないギャップが発生します。この動作は、MySQLとは異なりますが、合法と見なされます。 MySQLは、トランザクションが中止されてロールバックされるなど、他のシナリオでもシーケンスにギャップがあります。

## AUTO_ID_CACHE {#auto-id-cache}

別のTiDBサーバーに対して`INSERT`の操作を実行すると、 `AUTO_INCREMENT`のシーケンスが劇的に*ジャンプ*するように見える場合があります。これは、各サーバーが`AUTO_INCREMENT`の値の独自のキャッシュを持っているという事実が原因です。

{{< copyable "" >}}

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

最初のTiDBサーバーに対する新しい`INSERT`操作は、 `4`の`AUTO_INCREMENT`値を生成します。これは、最初のTiDBサーバーの`AUTO_INCREMENT`キャッシュに、割り当て用のスペースがまだ残っているためです。この場合、値のシーケンスはグローバルに単調であると見なすことはできません。これは、値`4`が値`2000001`の後に挿入されるためです。

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

`AUTO_INCREMENT`のキャッシュは、TiDBサーバーの再起動後も保持されません。次の`INSERT`のステートメントは、最初のTiDBサーバーが再起動された後に実行されます。

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

TiDBサーバーの再起動率が高いと、 `AUTO_INCREMENT`の値が使い果たされる可能性があります。上記の例では、最初のTiDBサーバーのキャッシュに値`[5-30000]`が残っています。これらの値は失われ、再割り当てされません。

`AUTO_INCREMENT`の値が連続していることに依存することはお勧めしません。次の例を考えてみましょう。ここでは、TiDBサーバーに値`[2000001-2030000]`のキャッシュがあります。値`2029998`を手動で挿入すると、新しいキャッシュ範囲が取得されたときの動作を確認できます。

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

値`2030000`が挿入された後、次の値は`2060001`です。このシーケンスのジャンプは、別のTiDBサーバーが`[2030001-2060000]`の中間キャッシュ範囲を取得しているためです。複数のTiDBサーバーが展開されている場合、キャッシュ要求がインターリーブされるため、 `AUTO_INCREMENT`のシーケンスにギャップが生じます。

### キャッシュサイズ制御 {#cache-size-control}

以前のバージョンのTiDBでは、自動インクリメントIDのキャッシュサイズはユーザーに対して透過的でした。 v3.0.14、v3.1.2、およびv4.0.rc-2以降、TiDBは、ユーザーが自動インクリメントIDを割り当てるためのキャッシュサイズを設定できるようにする`AUTO_ID_CACHE`テーブルオプションを導入しました。

```sql
mysql> CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 100;
Query OK, 0 rows affected (0.02 sec)

mysql> INSERT INTO t values();
Query OK, 1 row affected (0.00 sec)
Records: 1  Duplicates: 0  Warnings: 0

mysql> SELECT * FROM t;
+---+
| a |
+---+
| 1 |
+---+
1 row in set (0.01 sec)
```

このとき、この列の自動インクリメントキャッシュを無効にして暗黙の挿入をやり直すと、結果は次のようになります。

```sql
mysql> DELETE FROM t;
Query OK, 1 row affected (0.01 sec)

mysql> RENAME TABLE t to t1;
Query OK, 0 rows affected (0.01 sec)

mysql> INSERT INTO t1 values()
Query OK, 1 row affected (0.00 sec)

mysql> SELECT * FROM t;
+-----+
| a   |
+-----+
| 101 |
+-----+
1 row in set (0.00 sec)
```

再割り当てされた値は`101`です。これは、自動インクリメントIDを割り当てるためのキャッシュのサイズが`100`であることを示しています。

さらに、バッチ`INSERT`ステートメントの連続するIDの長さが`AUTO_ID_CACHE`の長さを超えると、TiDBはそれに応じてキャッシュサイズを増やし、ステートメントを正しく挿入できるようにします。

### ステップサイズとオフセットの自動インクリメント {#auto-increment-step-size-and-offset}

v3.0.9およびv4.0.0-rc.1以降、MySQLの動作と同様に、自動インクリメント列に暗黙的に割り当てられる値は、 `@@auto_increment_increment`および`@@auto_increment_offset`セッション変数によって制御されます。

自動インクリメント列に暗黙的に割り当てられた値（ID）は、次の式を満たします。

`(ID - auto_increment_offset) % auto_increment_increment == 0`

## 制限 {#restrictions}

現在、TiDBで使用する場合、 `AUTO_INCREMENT`には次の制限があります。

-   主キーの最初の列またはインデックスの最初の列で定義する必要があります。
-   `INTEGER` 、または`FLOAT`タイプの列で定義する必要があり`DOUBLE` 。
-   `DEFAULT`列の値と同じ列に指定することはできません。
-   `ALTER TABLE`を使用して`AUTO_INCREMENT`属性を追加することはできません。
-   `ALTER TABLE`は、 `AUTO_INCREMENT`属性を削除するために使用できます。ただし、v2.1.18およびv3.0.4以降、TiDBはセッション変数`@@tidb_allow_remove_auto_inc`を使用して、列の`AUTO_INCREMENT`属性を削除するために`ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`を使用できるかどうかを制御します。デフォルトでは、 `ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`を使用して`AUTO_INCREMENT`属性を削除することはできません。
-   `ALTER TABLE`には、 `AUTO_INCREMENT`の値を小さい値に設定するための`FORCE`のオプションが必要です。
-   `AUTO_INCREMENT`を`MAX(<auto_increment_column>)`より小さい値に設定すると、既存の値がスキップされないため、キーが重複します。
