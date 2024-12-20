---
title: AUTO_RANDOM
summary: AUTO_RANDOM 属性について学習します。
---

# AUTO_RANDOM <span class="version-mark">v3.1.0 の新機能</span> {#auto-random-span-class-version-mark-new-in-v3-1-0-span}

## ユーザーシナリオ {#user-scenario}

`AUTO_RANDOM`の値はランダムかつ一意であるため、TiDB が連続した ID を割り当てることによって単一のstorageノードで書き込みホットスポットが発生するのを避けるために、 [`AUTO_INCREMENT`](/auto-increment.md)の代わりに`AUTO_RANDOM`よく使用されます。現在の`AUTO_INCREMENT`列が主キーで、タイプが`BIGINT`場合、 `ALTER TABLE t MODIFY COLUMN id BIGINT AUTO_RANDOM(5);`ステートメントを実行して`AUTO_INCREMENT`から`AUTO_RANDOM`に切り替えることができます。

<CustomContent platform="tidb">

TiDB で同時書き込みの多いワークロードを処理する方法の詳細については、 [高度な同時書き込みのベストプラクティス](/best-practices/high-concurrency-best-practices.md)参照してください。

</CustomContent>

[テーブルの作成](/sql-statements/sql-statement-create-table.md)ステートメントの`AUTO_RANDOM_BASE`パラメータは、初期増分部分値`auto_random`を設定するために使用されます。このオプションは、内部インターフェイスの一部と見なすことができます。このパラメータは無視できます。

## 基本概念 {#basic-concepts}

`AUTO_RANDOM`は、 `BIGINT`列に値を自動的に割り当てるために使用される列属性です。自動的に割り当てられる値は**ランダム**かつ**一意**です。

`AUTO_RANDOM`列のテーブルを作成するには、次のステートメントを使用できます。3 列は主キーに含まれている必要があり、 `AUTO_RANDOM`列`AUTO_RANDOM`主キーの最初の列です。

```sql
CREATE TABLE t (a BIGINT AUTO_RANDOM, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b VARCHAR(255));
CREATE TABLE t (a BIGINT AUTO_RANDOM(6), b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT AUTO_RANDOM(5, 54), b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT AUTO_RANDOM(5, 54), b VARCHAR(255), PRIMARY KEY (a, b));
```

キーワード`AUTO_RANDOM`実行可能コメントで囲むことができます。詳細については[TiDB固有のコメント構文](/comment-syntax.md#tidb-specific-comment-syntax)を参照してください。

```sql
CREATE TABLE t (a bigint /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a bigint PRIMARY KEY /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255));
CREATE TABLE t (a BIGINT /*T![auto_rand] AUTO_RANDOM(6) */, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT  /*T![auto_rand] AUTO_RANDOM(5, 54) */, b VARCHAR(255), PRIMARY KEY (a));
```

`INSERT`ステートメントを実行すると、次のようになります。

-   `AUTO_RANDOM`列目の値を明示的に指定すると、そのままテーブルに挿入されます。
-   `AUTO_RANDOM`列の値を明示的に指定しない場合、TiDB はランダムな値を生成し、それをテーブルに挿入します。

```sql
tidb> CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b VARCHAR(255)) /*T! PRE_SPLIT_REGIONS=2 */ ;
Query OK, 0 rows affected, 1 warning (0.01 sec)

tidb> INSERT INTO t(a, b) VALUES (1, 'string');
Query OK, 1 row affected (0.00 sec)

tidb> SELECT * FROM t;
+---+--------+
| a | b      |
+---+--------+
| 1 | string |
+---+--------+
1 row in set (0.01 sec)

tidb> INSERT INTO t(b) VALUES ('string2');
Query OK, 1 row affected (0.00 sec)

tidb> INSERT INTO t(b) VALUES ('string3');
Query OK, 1 row affected (0.00 sec)

tidb> SELECT * FROM t;
+---------------------+---------+
| a                   | b       |
+---------------------+---------+
|                   1 | string  |
| 1152921504606846978 | string2 |
| 4899916394579099651 | string3 |
+---------------------+---------+
3 rows in set (0.00 sec)

tidb> SHOW CREATE TABLE t;
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| Table | Create Table                                                                                                                                                                                                                                                    |
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
| t     | CREATE TABLE `t` (
  `a` bigint NOT NULL /*T![auto_rand] AUTO_RANDOM(5) */,
  `b` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`a`) /*T![clustered_index] CLUSTERED */
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin /*T! PRE_SPLIT_REGIONS=2 */ |
+-------+-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
1 row in set (0.00 sec)

tidb> SHOW TABLE t REGIONS;
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
| REGION_ID | START_KEY                   | END_KEY                     | LEADER_ID | LEADER_STORE_ID | PEERS               | SCATTERING | WRITTEN_BYTES | READ_BYTES | APPROXIMATE_SIZE(MB) | APPROXIMATE_KEYS | SCHEDULING_CONSTRAINTS | SCHEDULING_STATE |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
|     62798 | t_158_                      | t_158_r_2305843009213693952 |     62810 |              28 | 62811, 62812, 62810 |          0 |           151 |          0 |                    1 |                0 |                        |                  |
|     62802 | t_158_r_2305843009213693952 | t_158_r_4611686018427387904 |     62803 |               1 | 62803, 62804, 62805 |          0 |            39 |          0 |                    1 |                0 |                        |                  |
|     62806 | t_158_r_4611686018427387904 | t_158_r_6917529027641081856 |     62813 |               4 | 62813, 62814, 62815 |          0 |           160 |          0 |                    1 |                0 |                        |                  |
|      9289 | t_158_r_6917529027641081856 | 78000000                    |     48268 |               1 | 48268, 58951, 62791 |          0 |         10628 |      43639 |                    2 |             7999 |                        |                  |
+-----------+-----------------------------+-----------------------------+-----------+-----------------+---------------------+------------+---------------+------------+----------------------+------------------+------------------------+------------------+
4 rows in set (0.00 sec)
```

TiDB によって自動的に割り当てられる`AUTO_RANDOM(S, R)`列の値の合計は 64 ビットです。

-   `S`はシャードビットの数です。値の範囲は`1`から`15`です。デフォルト値は`5`です。
-   `R`は自動割り当て範囲の合計長です。値の範囲は`32`から`64` 。デフォルト値は`64`です。

符号付きビットを持つ`AUTO_RANDOM`値の構造は次のとおりです。

| 符号付きビット | 予約ビット     | 破片の断片  | 自動増分ビット    |
| ------- | --------- | ------ | ---------- |
| 1ビット    | `64-R`ビット | `S`ビット | `R-1-S`ビット |

符号付きビットのない`AUTO_RANDOM`値の構造は次のとおりです。

| 予約ビット     | 破片の断片  | 自動増分ビット  |
| --------- | ------ | -------- |
| `64-R`ビット | `S`ビット | `R-S`ビット |

-   値に符号付きビットがあるかどうかは、対応する列に`UNSIGNED`属性があるかどうかによって決まります。
-   符号ビットの長さは、 `UNSIGNED`属性の存在によって決まります。 `UNSIGNED`属性がある場合、長さは`0`です。それ以外の場合、長さは`1`です。
-   予約ビットの長さは`64-R`です。予約ビットは常に`0`です。
-   シャード ビットの内容は、現在のトランザクションの開始時刻のハッシュ値を計算することによって取得されます。異なる長さのシャード ビット (10 など) を使用するには、テーブルの作成時に`AUTO_RANDOM(10)`指定します。
-   自動増分ビットの値はstorageエンジンに格納され、順番に割り当てられます。新しい値が割り当てられるたびに、値は 1 ずつ増加します。自動増分ビットにより、 `AUTO_RANDOM`の値がグローバルに一意であることが保証されます。自動増分ビットが使い果たされると、値が再度割り当てられるときにエラー`Failed to read auto-increment value from storage engine`が報告されます。
-   値の範囲: 最終的に生成される値の最大ビット数 = シャード ビット + 自動増分ビット。符号付き列の範囲は`[-(2^(R-1))+1, (2^(R-1))-1]`で、符号なし列の範囲は`[0, (2^R)-1]`です。
-   `AUTO_RANDOM` `PRE_SPLIT_REGIONS`と一緒に使用できます。テーブルが正常に作成されると、 `PRE_SPLIT_REGIONS`テーブル内のデータを`2^(PRE_SPLIT_REGIONS)`で指定された数のリージョンに事前に分割します。

> **注記：**
>
> シャードビットの選択（ `S` ）：
>
> -   使用可能なビットは合計 64 ビットあるため、シャード ビットの長さは自動インクリメント ビットの長さに影響します。つまり、シャード ビットの長さが長くなると、自動インクリメント ビットの長さは短くなり、逆もまた同様です。したがって、割り当てられた値のランダム性と使用可能なスペースのバランスを取る必要があります。
> -   ベストプラクティスは、シャードビットを`log(2, x)`に設定することです。ここで、 `x`現在のstorageエンジンの数です。たとえば、TiDB クラスターに 16 個の TiKV ノードがある場合、シャードビットを`log(2, 16)` (つまり`4`に設定できます。すべての領域が各 TiKV ノードに均等にスケジュールされた後、一括書き込みの負荷を異なる TiKV ノードに均一に分散して、リソースの使用率を最大化できます。
>
> 範囲の選択（ `R` ）：
>
> -   通常、アプリケーションの数値型が完全な 64 ビット整数を表現できない場合は、 `R`パラメータを設定する必要があります。
> -   たとえば、JSON の数値の範囲は`[-(2^53)+1, (2^53)-1]`です。TiDB は、 `AUTO_RANDOM(5)`として定義された列にこの範囲を超える整数を簡単に割り当てることができ、アプリケーションが列を読み取るときに予期しない動作が発生します。このような場合、符号付き列の場合は`AUTO_RANDOM(5)` `AUTO_RANDOM(5, 54)`に置き換え、符号なし列の場合は`AUTO_RANDOM(5)`を`AUTO_RANDOM(5, 53)`に置き換えて、TiDB が列に`9007199254740991` (2^53-1) を超える整数を割り当てないようにすることができます。

`AUTO_RANDOM`列に暗黙的に割り当てられた値は`last_insert_id()`影響します。TiDB が最後に暗黙的に割り当てる ID を取得するには、 `SELECT last_insert_id ()`ステートメントを使用できます。

`AUTO_RANDOM`列のテーブルのシャード ビット数を表示するには、 `SHOW CREATE TABLE`ステートメントを実行します。また、 `information_schema.tables`システム テーブルの`TIDB_ROW_ID_SHARDING_INFO`列で`PK_AUTO_RANDOM_BITS=x`モードの値を確認することもできます。11 `x`シャード ビットの数です。

`AUTO_RANDOM`列のテーブルを作成した後、 `SHOW WARNINGS`使用して暗黙的な割り当ての最大回数を表示できます。

```sql
CREATE TABLE t (a BIGINT AUTO_RANDOM, b VARCHAR(255), PRIMARY KEY (a));
SHOW WARNINGS;
```

出力は次のようになります。

```sql
+-------+------+---------------------------------------------------------+
| Level | Code | Message                                                 |
+-------+------+---------------------------------------------------------+
| Note  | 1105 | Available implicit allocation times: 288230376151711743 |
+-------+------+---------------------------------------------------------+
1 row in set (0.00 sec)
```

## IDの暗黙的な割り当てルール {#implicit-allocation-rules-of-ids}

TiDB は、 `AUTO_INCREMENT`列と同様に`AUTO_RANDOM`列に値を暗黙的に割り当てます。これらは、セッション レベルのシステム変数[`auto_increment_increment`](/system-variables.md#auto_increment_increment)および[`auto_increment_offset`](/system-variables.md#auto_increment_offset)によっても制御されます。暗黙的に割り当てられた値の自動増分ビット (ID) は、式`(ID - auto_increment_offset) % auto_increment_increment == 0`に従います。

## 制限 {#restrictions}

`AUTO_RANDOM`使用する場合は、次の制限に注意してください。

-   明示的に値を挿入するには、 `@@allow_auto_random_explicit_insert`システム変数の値を`1` (既定では`0` ) に設定する必要があります。データを挿入するときに、 `AUTO_RANDOM`属性を持つ列に値を明示的に指定することはお勧めし**ません**。そうしないと、このテーブルに自動的に割り当てられる数値が事前に使い果たされる可能性があります。
-   この属性は主キー列に`BIGINT`型のみ**に**指定してください。指定しない場合はエラーが発生します。また、主キーの属性が`NONCLUSTERED`の場合、整数主キーであっても`AUTO_RANDOM`はサポートされません。 `CLUSTERED`型の主キーの詳細については[クラスター化インデックス](/clustered-indexes.md)を参照してください。
-   `ALTER TABLE`使用して`AUTO_RANDOM`属性を変更することはできません (この属性の追加や削除を含む)。
-   最大値が列タイプの最大値に近い場合は、 `ALTER TABLE`使用して`AUTO_INCREMENT`から`AUTO_RANDOM`に変更することはできません。
-   `AUTO_RANDOM`属性で指定された主キー列の列タイプを変更することはできません。
-   同じ列に`AUTO_RANDOM`と`AUTO_INCREMENT`同時に指定することはできません。
-   同じ列に`AUTO_RANDOM`と`DEFAULT` (列のデフォルト値) を同時に指定することはできません。
-   列に`AUTO_RANDOM`使用されている場合、自動生成された値が非常に大きくなる可能性があるため、列属性を`AUTO_INCREMENT`に戻すことは困難です。
