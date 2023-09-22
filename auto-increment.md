---
title: AUTO_INCREMENT
summary: Learn the `AUTO_INCREMENT` column attribute of TiDB.
---

# 自動増加 {#auto-increment}

このドキュメントでは、 `AUTO_INCREMENT`列属性について、その概念、実装原則、自動インクリメント関連の機能、および制限事項を含めて紹介します。

<CustomContent platform="tidb">

> **注記：**
>
> `AUTO_INCREMENT`属性は、本番環境でホットスポットを引き起こす可能性があります。詳細は[ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)参照してください。代わりに[`AUTO_RANDOM`](/auto-random.md)を使用することをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> `AUTO_INCREMENT`属性は、本番環境でホットスポットを引き起こす可能性があります。詳細は[ホットスポットの問題のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#handle-auto-increment-primary-key-hotspot-tables-using-auto_random)参照してください。代わりに[`AUTO_RANDOM`](/auto-random.md)を使用することをお勧めします。

</CustomContent>

[`CREATE TABLE`](/sql-statements/sql-statement-create-table.md)ステートメントの`AUTO_INCREMENT`パラメータを使用して、増分フィールドの初期値を指定することもできます。

## コンセプト {#concept}

`AUTO_INCREMENT`は、デフォルトの列値を自動的に入力するために使用される列属性です。 `INSERT`ステートメントで`AUTO_INCREMENT`列の値が指定されていない場合、システムは自動的にこの列に値を割り当てます。

パフォーマンス上の理由から、値のバッチ (デフォルトでは 30,000) で`AUTO_INCREMENT`番号が各 TiDBサーバーに割り当てられます。これは、 `AUTO_INCREMENT`数値が一意であることが保証されている一方で、 `INSERT`のステートメントに割り当てられた値は、TiDBサーバーごとに単調であることを意味します。

> **注記：**
>
> すべての TiDB サーバーで`AUTO_INCREMENT`数値を単調にしたい場合、および TiDB バージョンが v6.5.0 以降の場合は、 [MySQL互換モード](#mysql-compatibility-mode)を有効にすることをお勧めします。

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

さらに、 `AUTO_INCREMENT`列値を明示的に指定する`INSERT`ステートメントもサポートします。このような場合、TiDB は明示的に指定された値を保存します。

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

上記の使い方はMySQLの`AUTO_INCREMENT`と同じです。ただし、暗黙的に割り当てられる特定の値という点では、TiDB は MySQL とは大きく異なります。

## 実装原則 {#implementation-principles}

TiDB は、次の方法で`AUTO_INCREMENT`暗黙的な割り当てを実装します。

自動インクリメント列ごとに、グローバルに表示されるキーと値のペアを使用して、割り当てられた最大 ID が記録されます。分散環境では、ノード間の通信にある程度のオーバーヘッドが発生します。したがって、書き込み増幅の問題を回避するために、各 TiDB ノードは ID を割り当てるときに連続する ID のバッチをキャッシュとして適用し、最初のバッチが割り当てられた後、次の ID のバッチを適用します。したがって、TiDB ノードは、毎回 ID を割り当てるときに、ID のstorageノードに適用されません。例えば：

```sql
CREATE TABLE t(id int UNIQUE KEY AUTO_INCREMENT, c int);
```

クラスター内に 2 つの TiDB インスタンス`A`と`B`あると仮定します。 `A`と`B`の`t`テーブルに対して`INSERT`ステートメントをそれぞれ実行すると、次のようになります。

```sql
INSERT INTO t (c) VALUES (1)
```

インスタンス`A` `[1,30000]`の自動インクリメント ID をキャッシュし、インスタンス`B` `[30001,60000]`の自動インクリメント ID をキャッシュします。実行される`INSERT`ステートメントでは、各インスタンスのこれらのキャッシュされた ID がデフォルト値として`AUTO_INCREMENT`列に割り当てられます。

## 基本的な機能 {#basic-features}

### 独自性 {#uniqueness}

> **警告：**
>
> クラスターに複数の TiDB インスタンスがあり、テーブル スキーマに自動インクリメント ID が含まれている場合は、明示的な挿入と暗黙的な割り当てを同時に使用しないことをお勧めします。つまり、自動インクリメント列のデフォルト値とカスタムの割り当てを使用します。価値観。そうしないと、暗黙的に割り当てられた値の一意性が損なわれる可能性があります。

上の例では、次の操作を順番に実行します。

1.  クライアントはステートメント`INSERT INTO t VALUES (2, 1)`をインスタンス`B`に挿入し、これにより`id`が`2`に設定されます。ステートメントは正常に実行されました。

2.  クライアントはステートメント`INSERT INTO t (c) (1)`をインスタンス`A`に送信します。このステートメントでは値`id`指定されていないため、ID は`A`によって割り当てられます。現時点では、 `A` `[1, 30000]`の ID をキャッシュしているため、自動インクリメント ID の値として`2`割り当て、ローカル カウンタを`1`だけ増加させる可能性があります。このとき、データベースにはすでにIDが`2`データが存在するため、 `Duplicated Error`エラーが返されます。

### 単調性 {#monotonicity}

TiDB は、サーバーごとに`AUTO_INCREMENT`値が単調 (常に増加) であることを保証します。 1 ～ 3 の連続する`AUTO_INCREMENT`値が生成される次の例を考えてみましょう。

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

この例では、値`AUTO_INCREMENT`の`3`が`INSERT INTO t (a) VALUES ('A'), ('C') ON DUPLICATE KEY UPDATE cnt = cnt + 1;`のキー`A`の`INSERT`に割り当てられますが、この`INSERT`ステートメントには重複キー`A`が含まれているため、使用されません。これにより、シーケンスが不連続になるギャップが生じます。この動作は、MySQL とは異なりますが、合法とみなされます。 MySQL では、トランザクションの中止やロールバックなど、他のシナリオでもシーケンスにギャップが発生します。

## AUTO_ID_CACHE {#auto-id-cache}

`INSERT`操作が別の TiDBサーバーに対して実行されると、 `AUTO_INCREMENT`シーケンスが大幅に*ジャンプしている*ように見える場合があります。これは、各サーバーが`AUTO_INCREMENT`値の独自のキャッシュを持っていることが原因で発生します。

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

最初の TiDBサーバーに対する新しい`INSERT`操作により、 `AUTO_INCREMENT`の値`4`が生成されます。これは、初期 TiDBサーバーの`AUTO_INCREMENT`キャッシュに割り当て用のスペースがまだ残っているためです。この場合、値`4`が値`2000001`の後に挿入されるため、値のシーケンスは全体的に単調であるとは見なされません。

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

`AUTO_INCREMENT`キャッシュは、TiDBサーバーが再起動されると保持されません。次の`INSERT`ステートメントは、最初の TiDBサーバーが再起動された後に実行されます。

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

TiDBサーバーの再起動の頻度が高いと、 `AUTO_INCREMENT`値が枯渇する可能性があります。上記の例では、最初の TiDBサーバーのキャッシュにはまだ空き値`[5-30000]`あります。これらの値は失われ、再割り当てされません。

`AUTO_INCREMENT`値が連続していることに依存することはお勧めできません。 TiDBサーバーに値`[2000001-2030000]`のキャッシュがある次の例を考えてみましょう。値`2029998`手動で挿入すると、新しいキャッシュ範囲が取得されるときの動作を確認できます。

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

値`2030000`が挿入されると、次の値は`2060001`になります。このシーケンスのジャンプは、別の TiDBサーバーが中間キャッシュ範囲`[2030001-2060000]`を取得したためです。複数の TiDB サーバーがデプロイされている場合、キャッシュ リクエストがインターリーブされるため、 `AUTO_INCREMENT`シーケンスにギャップが生じます。

### キャッシュサイズの制御 {#cache-size-control}

TiDB の以前のバージョンでは、自動インクリメント ID のキャッシュ サイズはユーザーに対して透過的でした。 v3.0.14、v3.1.2、および v4.0.rc-2 以降、TiDB には`AUTO_ID_CACHE`テーブル オプションが導入され、ユーザーが自動インクリメント ID を割り当てるためのキャッシュ サイズを設定できるようになりました。

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

このとき、この列の自動インクリメント キャッシュを無効にして暗黙的な挿入をやり直すと、結果は次のようになります。

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

再割り当てされた値は`101`です。これは、オートインクリメント ID を割り当てるためのキャッシュのサイズが`100`であることを示しています。

さらに、バッチ`INSERT`ステートメント内の連続 ID の長さが`AUTO_ID_CACHE`の長さを超える場合、TiDB はステートメントを適切に挿入できるように、それに応じてキャッシュ サイズを増やします。

### 自動インクリメントステップサイズとオフセット {#auto-increment-step-size-and-offset}

v3.0.9 および v4.0.0-rc.1 以降、MySQL の動作と同様に、自動インクリメント カラムに暗黙的に割り当てられる値は、セッション変数`@@auto_increment_increment`および`@@auto_increment_offset`によって制御されます。

自動インクリメント列に暗黙的に割り当てられる値 (ID) は、次の方程式を満たします。

`(ID - auto_increment_offset) % auto_increment_increment == 0`

## MySQL互換モード {#mysql-compatibility-mode}

TiDB v6.4.0 では、一元的な自動インクリメント ID 割り当てサービスが導入されています。各リクエストでは、TiDB インスタンスにデータをキャッシュする代わりに、このサービスから自動インクリメント ID が割り当てられます。

現在、集中割り当てサービスは TiDB プロセス内にあり、DDL 所有者のように機能します。 1 つの TiDB インスタンスはプライマリ ノードとして ID を割り当て、他の TiDB インスタンスはセカンダリ ノードとして機能します。高可用性を確保するために、プライマリ インスタンスに障害が発生すると、TiDB は自動フェイルオーバーを開始します。

MySQL 互換モードを使用するには、テーブルの作成時に`AUTO_ID_CACHE` ～ `1`を設定します。

```sql
CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 1;
```

> **注記：**
>
> TiDB では、 `AUTO_ID_CACHE`から`1`に設定すると、TiDB が ID をキャッシュしなくなることを意味します。ただし、実装は TiDB のバージョンによって異なります。
>
> -   TiDB v6.4.0 より前では、ID を割り当てるには TiKV トランザクションがリクエストごとに`AUTO_INCREMENT`値を保持する必要があるため、 `AUTO_ID_CACHE`から`1`に設定するとパフォーマンスが低下します。
> -   TiDB v6.4.0 以降、集中割り当てサービスが導入されているため、値`AUTO_INCREMENT`の変更は TiDB プロセス内のメモリ内操作のみであるため、より高速になっています。
> -   `AUTO_ID_CACHE`から`0`に設定すると、TiDB はデフォルトのキャッシュ サイズ`30000`を使用することを意味します。

MySQL 互換モードを有効にすると、割り当てられた ID は**一意で****単調増加し**、動作は MySQL とほぼ同じになります。 TiDB インスタンスをまたいでアクセスした場合でも、ID は単調に保たれます。集中サービスのプライマリ インスタンスがクラッシュした場合にのみ、連続しない ID がいくつか存在する可能性があります。これは、ID の一意性を確保するために、フェールオーバー中にセカンダリ インスタンスがプライマリ インスタンスによって割り当てられたはずの一部の ID を破棄するためです。

## 制限 {#restrictions}

現在、 `AUTO_INCREMENT` TiDB で使用する場合、次の制限があります。

-   TiDB v6.6.0 以前のバージョンの場合、定義された列は主キーまたはインデックス接頭辞のいずれかである必要があります。
-   `INTEGER` 、 `FLOAT` 、または`DOUBLE`タイプの列に定義する必要があります。
-   `DEFAULT`列の値と同じ列には指定できません。
-   `ALTER TABLE`を使用して`AUTO_INCREMENT`属性の列を追加または変更することはできません。これには、 `ALTER TABLE ... MODIFY/CHANGE COLUMN`を使用して`AUTO_INCREMENT`属性を既存の列に追加することや、 `ALTER TABLE ... ADD COLUMN`を使用して`AUTO_INCREMENT`属性の列を追加することも含まれます。
-   `ALTER TABLE`を使用すると、 `AUTO_INCREMENT`属性を削除できます。ただし、v2.1.18 および v3.0.4 以降、TiDB はセッション変数`@@tidb_allow_remove_auto_inc`を使用して、列の`AUTO_INCREMENT`属性を削除するために`ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`を使用できるかどうかを制御します。デフォルトでは、 `ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`を使用して`AUTO_INCREMENT`属性を削除することはできません。
-   `ALTER TABLE`は、 `AUTO_INCREMENT`値をより小さい値に設定するための`FORCE`オプションが必要です。
-   `AUTO_INCREMENT`を`MAX(<auto_increment_column>)`より小さい値に設定すると、既存の値がスキップされないため、キーが重複します。
