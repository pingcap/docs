---
title: AUTO_RANDOM
summary: AUTO_RANDOM 属性について学習します。
---

# AUTO_RANDOM <span class="version-mark">v3.1.0 の新機能</span> {#auto-random-span-class-version-mark-new-in-v3-1-0-span}

## ユーザーシナリオ {#user-scenario}

`AUTO_RANDOM`の値はランダムかつ一意であるため、TiDBが連続したIDを割り当てることで単一storageノードに書き込みホットスポットが発生するのを回避するため、 [`AUTO_INCREMENT`](/auto-increment.md)の代わりに`AUTO_RANDOM`使用されることがよくあります。現在の`AUTO_INCREMENT`列が主キーで、型が`BIGINT`場合、 `ALTER TABLE t MODIFY COLUMN id BIGINT AUTO_RANDOM(5);`ステートメントを実行して`AUTO_INCREMENT`から`AUTO_RANDOM`に切り替えることができます。

<CustomContent platform="tidb">

TiDB で同時書き込みの多いワークロードを処理する方法の詳細については、 [高同時書き込みのベストプラクティス](/best-practices/high-concurrency-best-practices.md)参照してください。

</CustomContent>

[テーブルの作成](/sql-statements/sql-statement-create-table.md)文の`AUTO_RANDOM_BASE`パラメータは、初期増分値`auto_random`を設定するために使用されます。このオプションは内部インターフェースの一部とみなすことができます。このパラメータは無視できます。

## 基本概念 {#basic-concepts}

`AUTO_RANDOM`は、 `BIGINT`列に値を自動的に割り当てるために使用される列属性です。自動的に割り当てられる値は**ランダム**かつ**一意**です。

`AUTO_RANDOM`列目のテーブルを作成するには、以下のステートメントを使用します。3列目`AUTO_RANDOM`主キーに含まれている必要があり、 `AUTO_RANDOM`列目は主キーの最初の列です。

```sql
CREATE TABLE t (a BIGINT AUTO_RANDOM, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT PRIMARY KEY AUTO_RANDOM, b VARCHAR(255));
CREATE TABLE t (a BIGINT AUTO_RANDOM(6), b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT AUTO_RANDOM(5, 54), b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT AUTO_RANDOM(5, 54), b VARCHAR(255), PRIMARY KEY (a, b));
```

キーワード`AUTO_RANDOM`実行コメントで囲むことができます。詳細については[TiDB固有のコメント構文](/comment-syntax.md#tidb-specific-comment-syntax)を参照してください。

```sql
CREATE TABLE t (a bigint /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a bigint PRIMARY KEY /*T![auto_rand] AUTO_RANDOM */, b VARCHAR(255));
CREATE TABLE t (a BIGINT /*T![auto_rand] AUTO_RANDOM(6) */, b VARCHAR(255), PRIMARY KEY (a));
CREATE TABLE t (a BIGINT  /*T![auto_rand] AUTO_RANDOM(5, 54) */, b VARCHAR(255), PRIMARY KEY (a));
```

`INSERT`ステートメントを実行すると、次のようになります。

-   `AUTO_RANDOM`列目の値を明示的に指定すると、そのままテーブルに挿入されます。
-   `AUTO_RANDOM`列の値を明示的に指定しない場合は、TiDB によってランダムな値が生成され、テーブルに挿入されます。

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

-   `S`はシャードビット数です。値の範囲は`1`から`15`です。デフォルト値は`5`です。
-   `R`は自動割り当て範囲の合計長です。値の範囲は`32`から`64` 。デフォルト値は`64`です。

符号付きビットを持つ`AUTO_RANDOM`値の構造は次のとおりです。

| 符号付きビット | 予約ビット     | 破片の断片  | 自動インクリメントビット |
| ------- | --------- | ------ | ------------ |
| 1ビット    | `64-R`ビット | `S`ビット | `R-1-S`ビット   |

符号付きビットのない`AUTO_RANDOM`値の構造は次のとおりです。

| 予約ビット     | 破片の断片  | 自動インクリメントビット |
| --------- | ------ | ------------ |
| `64-R`ビット | `S`ビット | `R-S`ビット     |

-   値に符号付きビットがあるかどうかは、対応する列に`UNSIGNED`属性があるかどうかによって決まります。
-   符号ビットの長さは、属性`UNSIGNED`有無によって決まります。属性`UNSIGNED`がある場合、長さは`0`です。そうでない場合、長さは`1`です。
-   予約ビットの長さは`64-R`です。予約ビットは常に`0`です。
-   シャードビットの内容は、現在のトランザクションの開始時刻のハッシュ値を計算することで得られます。異なるシャードビット長（10など）を使用する場合は、テーブル作成時に`AUTO_RANDOM(10)`指定します。
-   自動インクリメントビットの値はstorageエンジンに格納され、順次割り当てられます。新しい値が割り当てられるたびに、値は1ずつ増加します。自動インクリメントビットは、 `AUTO_RANDOM`の値がグローバルに一意であることを保証します。自動インクリメントビットが使い果たされると、値が再び割り当てられる際にエラー`Failed to read auto-increment value from storage engine`が報告されます。
-   値の範囲：最終的に生成される値の最大ビット数 = シャードビット数 + 自動インクリメントビット数。符号付き列の範囲は`[-(2^(R-1))+1, (2^(R-1))-1]` 、符号なし列の範囲は`[0, (2^R)-1]`です。
-   `AUTO_RANDOM` `PRE_SPLIT_REGIONS`と組み合わせて使用できます。テーブルが正常に作成されると、 `PRE_SPLIT_REGIONS`テーブル内のデータを`2^(PRE_SPLIT_REGIONS)`で指定された数のリージョンに事前に分割します。

> **注記：**
>
> シャードビットの選択（ `S` ）：
>
> -   利用可能なビット数は合計64ビットであるため、シャードビット長は自動インクリメントビット長に影響します。つまり、シャードビット長が増加すると自動インクリメントビット長は減少し、逆もまた同様です。したがって、割り当てられた値のランダム性と利用可能なスペースのバランスをとる必要があります。
> -   ベストプラクティスは、シャードビットを`log(2, x)`に設定することです。ここで、 `x`現在のstorageエンジンの数です。例えば、TiDB クラスターに TiKV ノードが 16 個ある場合、シャードビットを`log(2, 16)` （つまり`4`に設定できます。すべてのリージョンが各 TiKV ノードに均等にスケジュールされると、一括書き込みの負荷が複数の TiKV ノードに均等に分散され、リソース使用率を最大化できます。
>
> 範囲の選択（ `R` ）：
>
> -   通常、アプリケーションの数値型が完全な 64 ビット整数を表現できない場合は、 `R`パラメータを設定する必要があります。
> -   例えば、JSONの数値の範囲は`[-(2^53)+1, (2^53)-1]`です。TiDBは、 `AUTO_RANDOM(5)`と定義された列にこの範囲を超える整数を簡単に割り当ててしまう可能性があり、アプリケーションがその列を読み取った際に予期しない動作を引き起こす可能性があります。このような場合、符号付き列の場合は`AUTO_RANDOM(5)` `AUTO_RANDOM(5, 54)`に、符号なし列の場合は`AUTO_RANDOM(5)` `AUTO_RANDOM(5, 53)`に置き換えることで、TiDBが列に`9007199254740991` (2^53-1) を超える整数を割り当てないようにすることができます。

`AUTO_RANDOM`列に暗黙的に割り当てられた値は`last_insert_id()`影響します。TiDB が最後に暗黙的に割り当てた ID を取得するには、 `SELECT last_insert_id ()`ステートメントを使用できます。

列番号が`AUTO_RANDOM`であるテーブルのシャードビット数を確認するには、 `SHOW CREATE TABLE`ステートメントを実行します。また、 `information_schema.tables`システムテーブルの列番号`TIDB_ROW_ID_SHARDING_INFO`で、 `PK_AUTO_RANDOM_BITS=x`のモードの値を確認することもできます`x`はシャードビット数です。

`AUTO_RANDOM`列のテーブルを作成した後、 `SHOW WARNINGS`使用して最大暗黙的割り当て時間を表示できます。

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

TiDBは、 `AUTO_INCREMENT`列と同様に、 `AUTO_RANDOM`列にも暗黙的に値を割り当てます。これらの値は、セッションレベルのシステム変数[`auto_increment_increment`](/system-variables.md#auto_increment_increment)と[`auto_increment_offset`](/system-variables.md#auto_increment_offset)によって制御されます。暗黙的に割り当てられた値の自動インクリメントビット（ID）は、式`(ID - auto_increment_offset) % auto_increment_increment == 0`に従います。

## 自動増分IDキャッシュをクリアする {#clear-the-auto-increment-id-cache}

複数のTiDBサーバーインスタンスが存在する環境で、 `AUTO_RANDOM`列目に明示的な値を持つデータを挿入すると、 `AUTO_INCREMENT`列目と同様に、IDの衝突が発生する可能性があります。明示的な挿入で使用されたID値が、TiDBが自動生成に使用する内部カウンターと競合すると、エラーが発生する可能性があります。

衝突が発生する仕組みは以下のとおりです。 `AUTO_RANDOM` IDはランダムビットと自動増分部分で構成されています。TiDBはこの自動増分部分に内部カウンタを使用します。自動増分部分がカウンタの次の値と一致するIDを明示的に挿入すると、TiDBが後で同じIDを自動生成しようとする際に、重複キーエラーが発生する可能性があります。詳細については、 [AUTO_INCREMENT 一意性](/auto-increment.md#uniqueness)参照してください。

TiDBインスタンスが1つの場合、ノードは明示的な挿入を処理する際に内部カウンターを自動的に調整し、将来の衝突を防ぐため、この問題は発生しません。一方、複数のTiDBノードがある場合、各ノードは独自のIDキャッシュを保持しており、明示的な挿入後に衝突を防ぐには、このキャッシュをクリアする必要があります。これらの未割り当てのキャッシュIDをクリアして衝突の可能性を回避するには、次の2つの方法があります。

### オプション 1: 自動的にリベースする (推奨) {#option-1-automatically-rebase-recommended}

```sql
ALTER TABLE t AUTO_RANDOM_BASE=0;
```

このステートメントは適切な基数を自動的に決定します。1 `Can't reset AUTO_INCREMENT to 0 without FORCE option, using XXX instead`ような警告メッセージが表示されますが、基数は変更さ**れる**ため、この警告は無視しても問題ありません。

> **注記：**
>
> `FORCE`キーワードを使用して`AUTO_RANDOM_BASE`から`0`設定することはできません。これを試みるとエラーが発生します。

### オプション2: 特定の基本値を手動で設定する {#option-2-manually-set-a-specific-base-value}

特定の基本値 (たとえば、 `1000` ) を設定する必要がある場合は、 `FORCE`キーワードを使用します。

```sql
ALTER TABLE t FORCE AUTO_RANDOM_BASE = 1000;
```

このアプローチは、適切な基本値を自分で決定する必要があるため、あまり便利ではありません。

> **注記：**
>
> `FORCE`使用する場合は、ゼロ以外の正の整数を指定する必要があります。

どちらのコマンドも、すべてのTiDBノードにおける後続の`AUTO_RANDOM`値生成で使用される自動インクリメントビットの開始点を変更します。すでに割り当てられているIDには影響しません。

## 制限 {#restrictions}

`AUTO_RANDOM`使用する場合は、次の制限に注意してください。

-   明示的に値を挿入するには、システム変数`@@allow_auto_random_explicit_insert`の値を`1` （デフォルトは`0` ）に設定する必要があります。データを挿入する際に、属性`AUTO_RANDOM`持つ列に明示的に値を指定することは推奨さ**れません**。そうしないと、このテーブルに自動的に割り当てられる数値が事前に使い果たされてしまう可能性があります。
-   この属性は、主キー列に**のみ**`BIGINT`型で指定してください。それ以外の場合はエラーが発生します。また、主キーの属性が`NONCLUSTERED`の場合、整数型の主キーであっても`AUTO_RANDOM`サポートされません`CLUSTERED`型の主キーの詳細については、 [クラスター化インデックス](/clustered-indexes.md)を参照してください。
-   `ALTER TABLE`使用して`AUTO_RANDOM`属性を変更することはできません (この属性の追加や削除を含む)。
-   最大値が列タイプの最大値に近い場合は、 `ALTER TABLE`を使用して`AUTO_INCREMENT`から`AUTO_RANDOM`に変更することはできません。
-   `AUTO_RANDOM`属性で指定された主キー列の列タイプを変更することはできません。
-   同じ列に同時に`AUTO_RANDOM`と`AUTO_INCREMENT`指定することはできません。
-   同じ列に`AUTO_RANDOM`と`DEFAULT` (列のデフォルト値) を同時に指定することはできません。
-   列に`AUTO_RANDOM`使用されている場合、自動生成される値が非常に大きくなる可能性があるため、列属性を`AUTO_INCREMENT`に戻すのは困難です。
