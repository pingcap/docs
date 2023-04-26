---
title: AUTO_INCREMENT
summary: Learn the `AUTO_INCREMENT` column attribute of TiDB.
---

# 自動増加 {#auto-increment}

このドキュメントでは、 `AUTO_INCREMENT`列属性について、その概念、実装の原則、自動インクリメント関連の機能、および制限事項を含めて紹介します。

<CustomContent platform="tidb">

> **ノート：**
>
> `AUTO_INCREMENT`属性は、本番環境でホットスポットを引き起こす可能性があります。詳細は[ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)参照してください。代わりに[`AUTO_RANDOM`](/auto-random.md)を使用することをお勧めします。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> `AUTO_INCREMENT`属性は、本番環境でホットスポットを引き起こす可能性があります。詳細は[ホットスポットの問題のトラブルシューティング](https://docs.pingcap.com/tidb/stable/troubleshoot-hot-spot-issues#handle-auto-increment-primary-key-hotspot-tables-using-auto_random)参照してください。代わりに[`AUTO_RANDOM`](/auto-random.md)を使用することをお勧めします。

</CustomContent>

## コンセプト {#concept}

`AUTO_INCREMENT`は、デフォルトの列値を自動的に入力するために使用される列属性です。 `INSERT`ステートメントで`AUTO_INCREMENT`列の値が指定されていない場合、システムは自動的にこの列に値を割り当てます。

パフォーマンス上の理由から、値のバッチで`AUTO_INCREMENT`の数値 (デフォルトでは 30,000) が各 TiDBサーバーに割り当てられます。これは、 `AUTO_INCREMENT`数値が一意であることが保証されている一方で、 `INSERT`のステートメントに割り当てられた値は、TiDBサーバーごとに単調にしかならないことを意味します。

> **ノート：**
>
> すべての TiDB サーバーで`AUTO_INCREMENT`数字を単調にしたい場合で、TiDB のバージョンが v6.5.0 以降の場合は、 [MySQL 互換モード](#mysql-compatibility-mode)を有効にすることをお勧めします。

以下は`AUTO_INCREMENT`の基本的な例です。

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

さらに、 `AUTO_INCREMENT` 、列の値を明示的に指定する`INSERT`ステートメントもサポートします。そのような場合、TiDB は明示的に指定された値を格納します。

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

上記の使い方は、MySQL の`AUTO_INCREMENT`と同じです。ただし、暗黙的に割り当てられる特定の値に関しては、TiDB は MySQL と大きく異なります。

## 実施原則 {#implementation-principles}

TiDB は、次の方法で`AUTO_INCREMENT`暗黙的な代入を実装します。

自動インクリメント列ごとに、割り当てられた最大 ID を記録するために、グローバルに表示されるキーと値のペアが使用されます。分散環境では、ノード間の通信にいくらかのオーバーヘッドがあります。したがって、書き込み増幅の問題を回避するために、各 TiDB ノードは、ID を割り当てるときにキャッシュとして連続する ID のバッチに適用し、最初のバッチが割り当てられた後に次の ID のバッチに適用します。そのため、毎回 ID を割り当てる際に、TiDB ノードは ID 用のstorageノードに適用されません。例えば：

```sql
CREATE TABLE t(id int UNIQUE KEY AUTO_INCREMENT, c int);
```

クラスター内に 2 つの TiDB インスタンス`A`と`B`があるとします。それぞれ`A`と`B`の`t`テーブルで`INSERT`ステートメントを実行すると、次のようになります。

```sql
INSERT INTO t (c) VALUES (1)
```

インスタンス`A` `[1,30000]`の自動インクリメント ID をキャッシュし、インスタンス`B`は`[30001,60000]`の自動インクリメント ID をキャッシュする場合があります。実行される`INSERT`ステートメントでは、各インスタンスのこれらのキャッシュされた ID がデフォルト値として`AUTO_INCREMENT`列に割り当てられます。

## 基本的な機能 {#basic-features}

### 独自性 {#uniqueness}

> **警告：**
>
> クラスターに複数の TiDB インスタンスがあり、テーブル スキーマに自動インクリメント ID が含まれている場合は、明示的な挿入と暗黙的な割り当てを同時に使用しないことをお勧めします。つまり、自動インクリメント列のデフォルト値とカスタム値。そうしないと、暗黙的に割り当てられた値の一意性が損なわれる可能性があります。

上記の例では、次の操作を順番に実行します。

1.  クライアントはステートメント`INSERT INTO t VALUES (2, 1)`をインスタンス`B`に挿入し、インスタンス 3 は`id`を`2`に設定します。ステートメントは正常に実行されます。

2.  クライアントはステートメント`INSERT INTO t (c) (1)`をインスタンス`A`に送信します。このステートメントでは値`id`指定されていないため、ID は`A`によって割り当てられます。現在、 `A` `[1, 30000]`の ID をキャッシュしているため、自動インクリメント ID の値として`2`割り当て、ローカル カウンターを`1`増やします。このとき、ID が`2`のデータはすでにデータベースに存在するため、 `Duplicated Error`エラーが返されます。

### 単調性 {#monotonicity}

TiDB は、サーバーごとに`AUTO_INCREMENT`値が単調 (常に増加) であることを保証します。 1 ～ 3 の連続した`AUTO_INCREMENT`値が生成される次の例を考えてみましょう。

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

単調性は、連続性と同じ保証ではありません。次の例を検討してください。

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

この例では、 `3`の値`AUTO_INCREMENT`が`INSERT INTO t (a) VALUES ('A'), ('C') ON DUPLICATE KEY UPDATE cnt = cnt + 1;`のキー`A`の`INSERT`に割り当てられますが、この`INSERT`ステートメントに重複キー`A`含まれているため、使用されることはありません。これにより、シーケンスが連続しないギャップが生じます。 MySQL とは異なりますが、この動作は正当であると見なされます。 MySQL では、トランザクションの中止やロールバックなど、他のシナリオでもシーケンスにギャップがあります。

## AUTO_ID_CACHE {#auto-id-cache}

`INSERT`操作が別の TiDBサーバーに対して実行されると、 `AUTO_INCREMENT`シーケンスが劇的に*ジャンプする*ように見えることがあります。これは、各サーバーが独自の`AUTO_INCREMENT`の値のキャッシュを持っていることが原因です。

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

最初の TiDBサーバーに対する新しい`INSERT`操作により、 `AUTO_INCREMENT`の値`4`が生成されます。これは、最初の TiDBサーバーの`AUTO_INCREMENT`キャッシュに割り当て用のスペースがまだ残っているためです。この場合、値`4`が`2000001`の値の後に挿入されるため、値のシーケンスはグローバルに単調であると見なすことはできません。

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

`AUTO_INCREMENT`キャッシュは、TiDBサーバーの再起動後は保持されません。最初の TiDBサーバーが再起動された後、次の`INSERT`ステートメントが実行されます。

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

TiDBサーバーの再起動の頻度が高いと、 `AUTO_INCREMENT`値が枯渇する可能性があります。上記の例では、最初の TiDBサーバーのキャッシュにはまだ値`[5-30000]`の空きがあります。これらの値は失われ、再割り当てされません。

`AUTO_INCREMENT`値が連続していることに依存することはお勧めしません。 TiDBサーバーに値`[2000001-2030000]`のキャッシュがある次の例を考えてみましょう。値`2029998`手動で挿入すると、新しいキャッシュ範囲が取得されるときの動作を確認できます。

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

値`2030000`が挿入された後、次の値は`2060001`です。この一連のジャンプは、別の TiDBサーバーが`[2030001-2060000]`の中間キャッシュ範囲を取得したためです。複数の TiDB サーバーがデプロイされている場合、キャッシュ要求がインターリーブされるため、 `AUTO_INCREMENT`シーケンスにギャップが生じます。

### キャッシュサイズの制御 {#cache-size-control}

以前のバージョンの TiDB では、自動インクリメント ID のキャッシュ サイズはユーザーに対して透過的でした。 v3.0.14、v3.1.2、および v4.0.rc-2 から、TiDB は`AUTO_ID_CACHE`テーブル オプションを導入して、ユーザーが自動インクリメント ID を割り当てるためのキャッシュ サイズを設定できるようにしました。

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

この時点で、この列の自動インクリメント キャッシュを無効にして、暗黙的な挿入をやり直すと、結果は次のようになります。

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

再割り当てされた値は`101`です。これは、自動インクリメント ID を割り当てるためのキャッシュのサイズが`100`であることを示しています。

さらに、バッチ`INSERT`ステートメント内の連続する ID の長さが`AUTO_ID_CACHE`を超える場合、TiDB はそれに応じてキャッシュ サイズを増やし、ステートメントを適切に挿入できるようにします。

### 自動インクリメント ステップ サイズとオフセット {#auto-increment-step-size-and-offset}

v3.0.9 および v4.0.0-rc.1 以降、MySQL の動作と同様に、自動インクリメント列に暗黙的に割り当てられる値は、 `@@auto_increment_increment`および`@@auto_increment_offset`セッション変数によって制御されます。

自動インクリメント列に暗黙的に割り当てられる値 (ID) は、次の式を満たします。

`(ID - auto_increment_offset) % auto_increment_increment == 0`

## MySQL 互換モード {#mysql-compatibility-mode}

TiDB v6.4.0 では、集中自動インクリメント ID 割り当てサービスが導入されています。各リクエストでは、TiDB インスタンスにデータをキャッシュする代わりに、このサービスから自動インクリメント ID が割り当てられます。

現在、集中割り当てサービスは TiDB プロセスにあり、DDL 所有者のように機能します。 1 つの TiDB インスタンスがプライマリ ノードとして ID を割り当て、他の TiDB インスタンスはセカンダリ ノードとして機能します。高可用性を確保するために、プライマリ インスタンスに障害が発生すると、TiDB は自動フェイルオーバーを開始します。

MySQL 互換モードを使用するには、テーブルの作成時に`AUTO_ID_CACHE`から`1`を設定できます。

```sql
CREATE TABLE t(a int AUTO_INCREMENT key) AUTO_ID_CACHE 1;
```

> **ノート：**
>
> TiDB では、 `AUTO_ID_CACHE`から`1`に設定すると、TiDB が ID をキャッシュしないことを意味します。ただし、実装は TiDB のバージョンによって異なります。
>
> -   TiDB v6.4.0 より前では、ID を割り当てるには TiKV トランザクションが要求ごとに`AUTO_INCREMENT`値を保持する必要があるため、 `AUTO_ID_CACHE`から`1`に設定するとパフォーマンスが低下します。
> -   TiDB v6.4.0 以降、集中割り当てサービスが導入されたため、 `AUTO_INCREMENT`値の変更は TiDB プロセスでのインメモリ操作にすぎないため、より高速になりました。

MySQL 互換モードを有効にすると、割り当てられた ID は**一意**で<strong>単調に増加し</strong>、動作は MySQL とほぼ同じになります。 TiDB インスタンス間でアクセスしても、ID は単調に保たれます。一元化されたサービスのプライマリ インスタンスがクラッシュした場合にのみ、いくつかの ID が連続していない可能性があります。これは、ID の一意性を確保するために、フェールオーバー中にプライマリ インスタンスによって割り当てられたはずの一部の ID がセカンダリ インスタンスによって破棄されるためです。

## 制限 {#restrictions}

現在、TiDB で使用する場合、 `AUTO_INCREMENT`には次の制限があります。

-   これは、主キーの最初の列またはインデックスの最初の列で定義する必要があります。
-   `INTEGER` 、 `FLOAT` 、または`DOUBLE`型の列で定義する必要があります。
-   `DEFAULT`列の値と同じ列には指定できません。
-   `ALTER TABLE`を使用して`AUTO_INCREMENT`属性を追加することはできません。
-   `ALTER TABLE`を使用して`AUTO_INCREMENT`属性を削除できます。ただし、v2.1.18 および v3.0.4 以降、TiDB はセッション変数`@@tidb_allow_remove_auto_inc`を使用して、 `ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`を使用して列の`AUTO_INCREMENT`属性を削除できるかどうかを制御します。デフォルトでは、 `ALTER TABLE MODIFY`または`ALTER TABLE CHANGE`を使用して`AUTO_INCREMENT`属性を削除することはできません。
-   `ALTER TABLE`の場合、 `FORCE`オプションを使用して`AUTO_INCREMENT`値をより小さい値に設定する必要があります。
-   `AUTO_INCREMENT`を`MAX(<auto_increment_column>)`より小さい値に設定すると、既存の値がスキップされないため、重複キーが発生します。
