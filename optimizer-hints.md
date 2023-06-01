---
title: Optimizer Hints
summary: Use Optimizer Hints to influence query execution plans
---

# オプティマイザーのヒント {#optimizer-hints}

TiDB は、 MySQL 5.7で導入されたコメントのような構文に基づくオプティマイザー ヒントをサポートしています。たとえば、一般的な構文の 1 つは`/*+ HINT_NAME([t1_name [, t2_name] ...]) */`です。 TiDB オプティマイザーが最適性の低いクエリ プランを選択する場合は、オプティマイザー ヒントの使用をお勧めします。

> **ノート：**
>
> 5.7.7 より前の MySQL コマンドライン クライアントは、デフォルトでオプティマイザー ヒントを削除します。これらの以前のバージョンで`Hint`構文を使用する場合は、クライアントの起動時に`--comments`オプションを追加します。例: `mysql -h 127.0.0.1 -P 4000 -uroot --comments` 。

## 構文 {#syntax}

> **ノート：**
>
> ヒントを提供したいテーブルが`USE DATABASE`で指定されたデータベースにない場合は、データベース名を明示的に指定する必要があります。例えば：
>
> ```sql
> tidb> SELECT /*+ HASH_JOIN(t2, t) */ * FROM t, test2.t2;
> Empty set, 1 warning (0.00 sec)
>
> tidb> SHOW WARNINGS;
> +---------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
> | Level   | Code | Message                                                                                                                                               |
> +---------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
> | Warning | 1815 | There are no matching table names for (t2) in optimizer hint /*+ HASH_JOIN(t2, t) */ or /*+ TIDB_HJ(t2, t) */. Maybe you can use the table alias name |
> +---------+------+-------------------------------------------------------------------------------------------------------------------------------------------------------+
> 1 row in set (0.00 sec)
>
> tidb> SELECT /*+ HASH_JOIN(test2.t2, t) */ * FROM t, test2.t2;
> Empty set (0.00 sec)
>
> tidb> SELECT /*+ READ_FROM_STORAGE(TIFLASH[test1.t1,test2.t2]) */ t1.a FROM test1.t t1, test2.t t2 WHERE t1.a = t2.a;
> Empty set (0.00 sec)
>
> ```
>
> このドキュメントの例はすべて、同じデータベース内のテーブルです。使用するテーブルが同じデータベース内にない場合は、データベース名を明示的に指定する手順を参照してください。

オプティマイザー ヒントは大文字と小文字が区別されず、SQL ステートメントの`SELECT` 、 `UPDATE` 、または`DELETE`キーワードに続く`/*+ ... */`コメント内で指定されます。オプティマイザー ヒントは現在、 `INSERT`ステートメントではサポートされていません。

ヒントはカンマで区切って複数指定できます。たとえば、次のクエリでは 3 つの異なるヒントが使用されます。

{{< copyable "" >}}

```sql
SELECT /*+ USE_INDEX(t1, idx1), HASH_AGG(), HASH_JOIN(t1) */ count(*) FROM t t1, t t2 WHERE t1.a = t2.b;
```

オプティマイザー ヒントがクエリ実行プランにどのような影響を与えるかは、 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)の出力で確認できます。

間違ったヒントや不完全なヒントによってステートメント エラーが発生することはありません。これは、ヒントがクエリ実行に対する*ヒント*(提案) セマンティクスのみを意図しているためです。同様に、ヒントが適用できない場合、TiDB は最大でも警告を返します。

> **ノート：**
>
> コメントが指定されたキーワードの後に続かない場合、それらは一般的な MySQL コメントとして扱われます。コメントは有効にならず、警告も報告されません。

現在、TiDB は範囲が異なる 2 つのカテゴリのヒントをサポートしています。ヒントの最初のカテゴリは、 [`/*+ MEMORY_QUOTA(1024 MB)*/`](#memory_quotan)など)。

ステートメント内の各クエリまたはサブクエリは異なるクエリ ブロックに対応し、各クエリ ブロックには独自の名前があります。例えば：

{{< copyable "" >}}

```sql
SELECT * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

上記のクエリ ステートメントには 3 つのクエリ ブロックがあります。最も外側の`SELECT`最初のクエリ ブロックに対応し、その名前は`sel_1`です。 2 つの`SELECT`サブクエリは 2 番目と 3 番目のクエリ ブロックに対応し、その名前はそれぞれ`sel_2`と`sel_3`です。数字の順序は、左から右に`SELECT`が現れることに基づいています。最初の`SELECT` `DELETE`または`UPDATE`に置き換えると、対応するクエリ ブロック名は`del_1`または`upd_1`になります。

## クエリブロックで有効になるヒント {#hints-that-take-effect-in-query-blocks}

このカテゴリのヒントは、 `SELECT` 、 `UPDATE` 、または`DELETE`**の**キーワードの後に続きます。ヒントの有効範囲を制御するには、ヒント内のクエリ ブロックの名前を使用します。クエリ内の各テーブルを正確に識別することで、ヒント パラメーターを明確にすることができます (テーブル名またはエイリアスが重複している場合)。ヒントでクエリ ブロックが指定されていない場合、ヒントはデフォルトで現在のブロックで有効になります。

例えば：

{{< copyable "" >}}

```sql
SELECT /*+ HASH_JOIN(@sel_1 t1@sel_1, t3) */ * FROM (SELECT t1.a, t1.b FROM t t1, t t2 WHERE t1.a = t2.a) t1, t t3 WHERE t1.b = t3.b;
```

このヒントは`sel_1`クエリ ブロックで有効になり、そのパラメータは`sel_1`の`t1`テーブルと`t3`テーブルです ( `sel_2`には`t1`テーブルも含まれます)。

上で説明したように、次の方法でヒント内のクエリ ブロックの名前を指定できます。

-   クエリ ブロック名をヒントの最初のパラメーターとして設定し、他のパラメーターとスペースで区切ります。 `QB_NAME`に加えて、このセクションにリストされているすべてのヒントには、別のオプションの隠しパラメータ`@QB_NAME`もあります。このパラメータを使用すると、このヒントの有効範囲を指定できます。
-   このテーブルがどのクエリ ブロックに属するかを明示的に指定するには、パラメーターのテーブル名に`@QB_NAME`追加します。

> **ノート：**
>
> ヒントは、ヒントが有効になるクエリ ブロックの中またはその前に配置する必要があります。ヒントがクエリ ブロックの後に置かれた場合、そのヒントは有効になりません。

### QB_NAME {#qb-name}

クエリ文が複数のネストされたクエリを含む複雑な文である場合、特定のクエリ ブロックの ID と名前が誤って識別される可能性があります。この点に関しては、ヒント`QB_NAME`が役に立ちます。

`QB_NAME`クエリブロック名を意味します。クエリ ブロックに新しい名前を指定できます。指定した`QB_NAME`と以前のデフォルト名は両方とも有効です。例えば：

{{< copyable "" >}}

```sql
SELECT /*+ QB_NAME(QB1) */ * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

このヒントは、外側`SELECT`クエリ ブロックの名前を`QB1`に指定します。これにより、クエリ ブロックに対して`QB1`とデフォルト名`sel_1`の両方が有効になります。

> **ノート：**
>
> 上記の例では、ヒントで`QB_NAME` ～ `sel_2`が指定され、元の 2 番目の`SELECT`クエリ ブロックに新しい`QB_NAME`が指定されていない場合、 `sel_2` 2 番目の`SELECT`クエリ ブロックに対して無効な名前になります。

### MERGE_JOIN(t1_name [, tl_name ...]) {#merge-join-t1-name-tl-name}

`MERGE_JOIN(t1_name [, tl_name ...])`ヒントは、指定されたテーブルに対してソート/マージ結合アルゴリズムを使用するようにオプティマイザーに指示します。一般に、このアルゴリズムはメモリ消費量は少なくなりますが、処理時間は長くなります。データ量が非常に大きい場合、またはシステムメモリが不足している場合は、このヒントを使用することをお勧めします。例えば：

{{< copyable "" >}}

```sql
select /*+ MERGE_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

> **ノート：**
>
> `TIDB_SMJ`は、TiDB 3.0.x 以前のバージョンの`MERGE_JOIN`エイリアスです。これらのバージョンのいずれかを使用している場合は、ヒントに`TIDB_SMJ(t1_name [, tl_name ...])`構文を適用する必要があります。 TiDB の新しいバージョンでは、 `TIDB_SMJ`と`MERGE_JOIN`は両方とも有効なヒント名ですが、 `MERGE_JOIN`をお勧めします。

### INL_JOIN(t1_name [, tl_name ...]) {#inl-join-t1-name-tl-name}

`INL_JOIN(t1_name [, tl_name ...])`ヒントは、指定されたテーブルに対してインデックスのネストされたループ結合アルゴリズムを使用するようにオプティマイザーに指示します。このアルゴリズムは、一部のシナリオでは消費するシステム リソースが少なくなり、処理時間が短縮される可能性がありますが、他のシナリオでは逆の結果が生じる可能性があります。外部テーブルが条件`WHERE`でフィルターされた後の結果セットが 10,000 行未満の場合は、このヒントを使用することをお勧めします。例えば：

{{< copyable "" >}}

```sql
select /*+ INL_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

`INL_JOIN()`で指定したパラメータは、クエリ プランを作成するときの内部テーブルの候補テーブルです。たとえば、 `INL_JOIN(t1)` 、TiDB がクエリ プランを作成するための内部テーブルとして`t1`使用のみを考慮することを意味します。候補テーブルに別名がある場合は、その別名を`INL_JOIN()`のパラメータとして使用する必要があります。別名がない場合は、テーブルの元の名前をパラメータとして使用します。たとえば、 `select /*+ INL_JOIN(t1) */ * from t t1, t t2 where t1.a = t2.b;`クエリでは、 `INL_JOIN()`のパラメータとして`t`ではなく、 `t`テーブルのエイリアス`t1`または`t2`を使用する必要があります。

> **ノート：**
>
> `TIDB_INLJ`は、TiDB 3.0.x 以前のバージョンの`INL_JOIN`エイリアスです。これらのバージョンのいずれかを使用している場合は、ヒントに`TIDB_INLJ(t1_name [, tl_name ...])`構文を適用する必要があります。 TiDB の新しいバージョンでは、 `TIDB_INLJ`と`INL_JOIN`は両方とも有効なヒント名ですが、 `INL_JOIN`をお勧めします。

### INL_HASH_JOIN {#inl-hash-join}

`INL_HASH_JOIN(t1_name [, tl_name])`ヒントは、インデックスのネストされたループ ハッシュ結合アルゴリズムを使用するようにオプティマイザーに指示します。このアルゴリズムを使用するための条件は、インデックスネストループ結合アルゴリズムを使用するための条件と同じです。 2 つのアルゴリズムの違いは、 `INL_JOIN`では結合された内部テーブルにハッシュ テーブルが作成されるのに対し、 `INL_HASH_JOIN`では結合された外部テーブルにハッシュ テーブルが作成されることです。 `INL_HASH_JOIN`メモリ使用量に固定制限がありますが、 `INL_JOIN`で使用されるメモリは内部テーブルで一致する行の数に依存します。

### HASH_JOIN(t1_name [, tl_name ...]) {#hash-join-t1-name-tl-name}

`HASH_JOIN(t1_name [, tl_name ...])`ヒントは、指定されたテーブルに対してハッシュ結合アルゴリズムを使用するようにオプティマイザーに指示します。このアルゴリズムを使用すると、クエリを複数のスレッドで同時に実行できるため、処理速度は向上しますが、より多くのメモリを消費します。例えば：

{{< copyable "" >}}

```sql
select /*+ HASH_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

> **ノート：**
>
> `TIDB_HJ`は、TiDB 3.0.x 以前のバージョンの`HASH_JOIN`エイリアスです。これらのバージョンのいずれかを使用している場合は、ヒントに`TIDB_HJ(t1_name [, tl_name ...])`構文を適用する必要があります。 TiDB の新しいバージョンでは、 `TIDB_HJ`と`HASH_JOIN`は両方とも有効なヒント名ですが、 `HASH_JOIN`をお勧めします。

### HASH_JOIN_BUILD(t1_name [, tl_name ...]) {#hash-join-build-t1-name-tl-name}

`HASH_JOIN_BUILD(t1_name [, tl_name ...])`ヒントは、指定されたテーブルでハッシュ結合アルゴリズムを使用し、これらのテーブルがビルド側として機能するようにオプティマイザーに指示します。このようにして、特定のテーブルを使用してハッシュ テーブルを構築できます。例えば：

```sql
SELECT /*+ HASH_JOIN_BUILD(t1) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### HASH_JOIN_PROBE(t1_name [, tl_name ...]) {#hash-join-probe-t1-name-tl-name}

`HASH_JOIN_PROBE(t1_name [, tl_name ...])`ヒントは、指定されたテーブルでハッシュ結合アルゴリズムを使用し、これらのテーブルがプローブ側として機能するようにオプティマイザーに指示します。このようにして、特定のテーブルをプローブ側としてハッシュ結合アルゴリズムを実行できます。例えば：

```sql
SELECT /*+ HASH_JOIN_PROBE(t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

### SEMI_JOIN_REWRITE() {#semi-join-rewrite}

`SEMI_JOIN_REWRITE()`ヒントは、オプティマイザに半結合クエリを通常の結合クエリに書き換えるよう指示します。現在、このヒントは`EXISTS`サブクエリに対してのみ機能します。

このヒントを使用してクエリを書き換えない場合、実行プランでハッシュ結合が選択されている場合、セミ結合クエリはサブクエリを使用してハッシュ テーブルを構築することしかできません。この場合、サブクエリの結果が外側のクエリの結果よりも大きい場合、実行速度が予想より遅くなる可能性があります。

同様に、実行プランでインデックス結合が選択されている場合、準結合クエリは駆動テーブルとして外部クエリのみを使用できます。この場合、サブクエリの結果が外側のクエリの結果よりも小さい場合、実行速度が予想より遅くなる可能性があります。

`SEMI_JOIN_REWRITE()`を使用してクエリを書き換えると、オプティマイザは選択範囲を拡張して、より適切な実行プランを選択できます。

{{< copyable "" >}}

```sql
-- Does not use SEMI_JOIN_REWRITE() to rewrite the query.
EXPLAIN SELECT * FROM t WHERE EXISTS (SELECT 1 FROM t1 WHERE t1.a = t.a);
```

```sql
+-----------------------------+---------+-----------+------------------------+---------------------------------------------------+
| id                          | estRows | task      | access object          | operator info                                     |
+-----------------------------+---------+-----------+------------------------+---------------------------------------------------+
| MergeJoin_9                 | 7992.00 | root      |                        | semi join, left key:test.t.a, right key:test.t1.a |
| ├─IndexReader_25(Build)     | 9990.00 | root      |                        | index:IndexFullScan_24                            |
| │ └─IndexFullScan_24        | 9990.00 | cop[tikv] | table:t1, index:idx(a) | keep order:true, stats:pseudo                     |
| └─IndexReader_23(Probe)     | 9990.00 | root      |                        | index:IndexFullScan_22                            |
|   └─IndexFullScan_22        | 9990.00 | cop[tikv] | table:t, index:idx(a)  | keep order:true, stats:pseudo                     |
+-----------------------------+---------+-----------+------------------------+---------------------------------------------------+
```

{{< copyable "" >}}

```sql
-- Uses SEMI_JOIN_REWRITE() to rewrite the query.
EXPLAIN SELECT * FROM t WHERE EXISTS (SELECT /*+ SEMI_JOIN_REWRITE() */ 1 FROM t1 WHERE t1.a = t.a);
```

```sql
+------------------------------+---------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------+
| id                           | estRows | task      | access object          | operator info                                                                                                 |
+------------------------------+---------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------+
| IndexJoin_16                 | 1.25    | root      |                        | inner join, inner:IndexReader_15, outer key:test.t1.a, inner key:test.t.a, equal cond:eq(test.t1.a, test.t.a) |
| ├─StreamAgg_39(Build)        | 1.00    | root      |                        | group by:test.t1.a, funcs:firstrow(test.t1.a)->test.t1.a                                                      |
| │ └─IndexReader_34           | 1.00    | root      |                        | index:IndexFullScan_33                                                                                        |
| │   └─IndexFullScan_33       | 1.00    | cop[tikv] | table:t1, index:idx(a) | keep order:true                                                                                               |
| └─IndexReader_15(Probe)      | 1.25    | root      |                        | index:Selection_14                                                                                            |
|   └─Selection_14             | 1.25    | cop[tikv] |                        | not(isnull(test.t.a))                                                                                         |
|     └─IndexRangeScan_13      | 1.25    | cop[tikv] | table:t, index:idx(a)  | range: decided by [eq(test.t.a, test.t1.a)], keep order:false, stats:pseudo                                   |
+------------------------------+---------+-----------+------------------------+---------------------------------------------------------------------------------------------------------------+
```

前の例から、ヒント`SEMI_JOIN_REWRITE()`を使用すると、TiDB は駆動テーブル`t1`に基づいて IndexJoin の実行メソッドを選択できることがわかります。

### SHUFFLE_JOIN(t1_name [, tl_name ...]) {#shuffle-join-t1-name-tl-name}

`SHUFFLE_JOIN(t1_name [, tl_name ...])`ヒントは、指定されたテーブルでシャッフル結合アルゴリズムを使用するようにオプティマイザーに指示します。このヒントは MPP モードでのみ有効です。例えば：

```sql
SELECT /*+ SHUFFLE_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

> **ノート：**
>
> -   このヒントを使用する前に、現在の TiDB クラスターがクエリでのTiFlash MPP モードの使用をサポートできることを確認してください。詳細は[TiFlash MPP モードを使用する](/tiflash/use-tiflash-mpp-mode.md)を参照してください。
> -   このヒントは、 [`HASH_JOIN_PROBE`ヒント](#hash_join_probet1_name--tl_name-)と組み合わせて使用​​して、シャッフル結合アルゴリズムのビルド側とプローブ側を制御できます。

### BROADCAST_JOIN(t1_name [, tl_name ...]) {#broadcast-join-t1-name-tl-name}

`BROADCAST_JOIN(t1_name [, tl_name ...])`ヒントは、指定されたテーブルでブロードキャスト結合アルゴリズムを使用するようにオプティマイザーに指示します。このヒントは MPP モードでのみ有効です。例えば：

```sql
SELECT /*+ BROADCAST_JOIN(t1, t2) */ * FROM t1, t2 WHERE t1.id = t2.id;
```

> **ノート：**
>
> -   このヒントを使用する前に、現在の TiDB クラスターがクエリでのTiFlash MPP モードの使用をサポートできることを確認してください。詳細は[TiFlash MPP モードを使用する](/tiflash/use-tiflash-mpp-mode.md)を参照してください。
> -   このヒントは、 [`HASH_JOIN_PROBE`ヒント](#hash_join_probet1_name--tl_name-)と組み合わせて使用して、ブロードキャスト結合アルゴリズムのビルド側とプローブ側を制御できます。

### NO_DECORRELATE() {#no-decorrelate}

`NO_DECORRELATE()`ヒントは、指定されたクエリ ブロック内の相関サブクエリの非相関化を実行しないようにオプティマイザーに指示します。このヒントは、 `EXISTS` 、 `IN` 、 `ANY` 、 `ALL` 、 `SOME`サブクエリと、相関列を含むスカラー サブクエリ (つまり、相関サブクエリ) に適用されます。

このヒントがクエリ ブロックで使用される場合、オプティマイザはサブクエリとその外側のクエリ ブロックの間の相関列の非相関化を実行しようとせず、常に適用演算子を使用してクエリを実行します。

デフォルトでは、TiDB はより高い実行効率を達成するために、相関サブクエリに対して[いくつかのシナリオ](/correlated-subquery-optimization.md#restrictions)では、非相関化により実際に実行効率が低下する可能性があります。この場合、このヒントを使用して、非相関化を実行しないようにオプティマイザに手動で指示できます。例えば：

{{< copyable "" >}}

```sql
create table t1(a int, b int);
create table t2(a int, b int, index idx(b));
```

{{< copyable "" >}}

```sql
-- Not using NO_DECORRELATE().
explain select * from t1 where t1.a < (select sum(t2.a) from t2 where t2.b = t1.b);
```

```sql
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------+
| id                               | estRows  | task      | access object | operator info                                                                                                |
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------+
| HashJoin_11                      | 9990.00  | root      |               | inner join, equal:[eq(test.t1.b, test.t2.b)], other cond:lt(cast(test.t1.a, decimal(10,0) BINARY), Column#7) |
| ├─HashAgg_23(Build)              | 7992.00  | root      |               | group by:test.t2.b, funcs:sum(Column#8)->Column#7, funcs:firstrow(test.t2.b)->test.t2.b                      |
| │ └─TableReader_24               | 7992.00  | root      |               | data:HashAgg_16                                                                                              |
| │   └─HashAgg_16                 | 7992.00  | cop[tikv] |               | group by:test.t2.b, funcs:sum(test.t2.a)->Column#8                                                           |
| │     └─Selection_22             | 9990.00  | cop[tikv] |               | not(isnull(test.t2.b))                                                                                       |
| │       └─TableFullScan_21       | 10000.00 | cop[tikv] | table:t2      | keep order:false, stats:pseudo                                                                               |
| └─TableReader_15(Probe)          | 9990.00  | root      |               | data:Selection_14                                                                                            |
|   └─Selection_14                 | 9990.00  | cop[tikv] |               | not(isnull(test.t1.b))                                                                                       |
|     └─TableFullScan_13           | 10000.00 | cop[tikv] | table:t1      | keep order:false, stats:pseudo                                                                               |
+----------------------------------+----------+-----------+---------------+--------------------------------------------------------------------------------------------------------------+
```

前述の実行計画から、オプティマイザが非相関化を自動的に実行したことがわかります。非相関実行プランには、Apply 演算子がありません。代わりに、プランにはサブクエリと外側のクエリ ブロック間の結合操作があります。相関列を含む元のフィルター条件 ( `t2.b = t1.b` ) は、通常の結合条件になります。

{{< copyable "" >}}

```sql
-- Using NO_DECORRELATE().
explain select * from t1 where t1.a < (select /*+ NO_DECORRELATE() */ sum(t2.a) from t2 where t2.b = t1.b);
```

```sql
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
| id                                       | estRows   | task      | access object          | operator info                                                                        |
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
| Projection_10                            | 10000.00  | root      |                        | test.t1.a, test.t1.b                                                                 |
| └─Apply_12                               | 10000.00  | root      |                        | CARTESIAN inner join, other cond:lt(cast(test.t1.a, decimal(10,0) BINARY), Column#7) |
|   ├─TableReader_14(Build)                | 10000.00  | root      |                        | data:TableFullScan_13                                                                |
|   │ └─TableFullScan_13                   | 10000.00  | cop[tikv] | table:t1               | keep order:false, stats:pseudo                                                       |
|   └─MaxOneRow_15(Probe)                  | 10000.00  | root      |                        |                                                                                      |
|     └─StreamAgg_20                       | 10000.00  | root      |                        | funcs:sum(Column#14)->Column#7                                                       |
|       └─Projection_45                    | 100000.00 | root      |                        | cast(test.t2.a, decimal(10,0) BINARY)->Column#14                                     |
|         └─IndexLookUp_44                 | 100000.00 | root      |                        |                                                                                      |
|           ├─IndexRangeScan_42(Build)     | 100000.00 | cop[tikv] | table:t2, index:idx(b) | range: decided by [eq(test.t2.b, test.t1.b)], keep order:false, stats:pseudo         |
|           └─TableRowIDScan_43(Probe)     | 100000.00 | cop[tikv] | table:t2               | keep order:false, stats:pseudo                                                       |
+------------------------------------------+-----------+-----------+------------------------+--------------------------------------------------------------------------------------+
```

前述の実行計画から、オプティマイザが非相関化を実行しないことがわかります。実行計画には、Apply 演算子がまだ含まれています。 `t2`テーブルにアクセスするときも、相関列を含むフィルター条件 ( `t2.b = t1.b` ) がフィルター条件となります。

### HASH_AGG() {#hash-agg}

`HASH_AGG()`ヒントは、指定されたクエリ ブロック内のすべての集計関数でハッシュ集計アルゴリズムを使用するようにオプティマイザに指示します。このアルゴリズムを使用すると、クエリを複数のスレッドで同時に実行できるため、処理速度は向上しますが、より多くのメモリを消費します。例えば：

{{< copyable "" >}}

```sql
select /*+ HASH_AGG() */ count(*) from t1, t2 where t1.a > 10 group by t1.id;
```

### STREAM_AGG() {#stream-agg}

`STREAM_AGG()`ヒントは、指定されたクエリ ブロック内のすべての集計関数でストリーム集計アルゴリズムを使用するようにオプティマイザーに指示します。一般に、このアルゴリズムはメモリ消費量は少なくなりますが、処理時間は長くなります。データ量が非常に大きい場合、またはシステムメモリが不足している場合は、このヒントを使用することをお勧めします。例えば：

{{< copyable "" >}}

```sql
select /*+ STREAM_AGG() */ count(*) from t1, t2 where t1.a > 10 group by t1.id;
```

### MPP_1PHASE_AGG() {#mpp-1phase-agg}

`MPP_1PHASE_AGG()`指定されたクエリ ブロック内のすべての集計関数に対して 1 フェーズ集計アルゴリズムを使用するようにオプティマイザに指示します。このヒントは MPP モードでのみ有効です。例えば：

```sql
SELECT /*+ MPP_1PHASE_AGG() */ COUNT(*) FROM t1, t2 WHERE t1.a > 10 GROUP BY t1.id;
```

> **ノート：**
>
> このヒントを使用する前に、現在の TiDB クラスターがクエリでのTiFlash MPP モードの使用をサポートできることを確認してください。詳細は[TiFlash MPP モードを使用する](/tiflash/use-tiflash-mpp-mode.md)を参照してください。

### MPP_2PHASE_AGG() {#mpp-2phase-agg}

`MPP_2PHASE_AGG()`指定されたクエリ ブロック内のすべての集計関数に対して 2 フェーズ集計アルゴリズムを使用するようにオプティマイザに指示します。このヒントは MPP モードでのみ有効です。例えば：

```sql
SELECT /*+ MPP_2PHASE_AGG() */ COUNT(*) FROM t1, t2 WHERE t1.a > 10 GROUP BY t1.id;
```

> **ノート：**
>
> このヒントを使用する前に、現在の TiDB クラスターがクエリでのTiFlash MPP モードの使用をサポートできることを確認してください。詳細は[TiFlash MPP モードを使用する](/tiflash/use-tiflash-mpp-mode.md)を参照してください。

### USE_INDEX(t1_name, idx1_name [, idx2_name ...]) {#use-index-t1-name-idx1-name-idx2-name}

`USE_INDEX(t1_name, idx1_name [, idx2_name ...])`ヒントは、 `t1_name`されたテーブルに対して指定されたインデックスのみを使用するようにオプティマイザーに指示します。たとえば、次のヒントを適用すると、 `select * from t t1 use index(idx1, idx2);`ステートメントを実行するのと同じ効果があります。

{{< copyable "" >}}

```sql
SELECT /*+ USE_INDEX(t1, idx1, idx2) */ * FROM t1;
```

> **ノート：**
>
> このヒントでテーブル名のみを指定し、インデックス名を指定しない場合、実行ではインデックスは考慮されず、テーブル全体がスキャンされます。

### FORCE_INDEX(t1_name, idx1_name [, idx2_name ...]) {#force-index-t1-name-idx1-name-idx2-name}

`FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])`ヒントは、指定されたインデックスのみを使用するようにオプティマイザーに指示します。

`FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])`の使い方と効果は`USE_INDEX(t1_name, idx1_name [, idx2_name ...])`と同じです。

次の 4 つのクエリは同じ効果があります。

{{< copyable "" >}}

```sql
SELECT /*+ USE_INDEX(t, idx1) */ * FROM t;
SELECT /*+ FORCE_INDEX(t, idx1) */ * FROM t;
SELECT * FROM t use index(idx1);
SELECT * FROM t force index(idx1);
```

### IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...]) {#ignore-index-t1-name-idx1-name-idx2-name}

`IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...])`ヒントは、指定された`t1_name`テーブルの指定されたインデックスを無視するようにオプティマイザに指示します。たとえば、次のヒントを適用すると、 `select * from t t1 ignore index(idx1, idx2);`ステートメントを実行するのと同じ効果があります。

{{< copyable "" >}}

```sql
select /*+ IGNORE_INDEX(t1, idx1, idx2) */ * from t t1;
```

### ORDER_INDEX(t1_name, idx1_name [, idx2_name ...]) {#order-index-t1-name-idx1-name-idx2-name}

`ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])`ヒントは、指定されたテーブルに対して指定されたインデックスのみを使用し、指定されたインデックスを順番に読み取るようにオプティマイザーに指示します。

> **警告：**
>
> このヒントにより、SQL ステートメントが失敗する可能性があります。最初にテストすることをお勧めします。テスト中にエラーが発生した場合は、ヒントを削除します。テストが正常に実行された場合は、引き続き使用できます。

このヒントは通常、次のシナリオに適用されます。

```sql
CREATE TABLE t(a INT, b INT, key(a), key(b));
EXPLAIN SELECT /*+ ORDER_INDEX(t, a) */ a FROM t ORDER BY a LIMIT 10;
```

```sql
+----------------------------+---------+-----------+---------------------+-------------------------------+
| id                         | estRows | task      | access object       | operator info                 |
+----------------------------+---------+-----------+---------------------+-------------------------------+
| Limit_10                   | 10.00   | root      |                     | offset:0, count:10            |
| └─IndexReader_14           | 10.00   | root      |                     | index:Limit_13                |
|   └─Limit_13               | 10.00   | cop[tikv] |                     | offset:0, count:10            |
|     └─IndexFullScan_12     | 10.00   | cop[tikv] | table:t, index:a(a) | keep order:true, stats:pseudo |
+----------------------------+---------+-----------+---------------------+-------------------------------+
```

オプティマイザーは、このクエリに対して 2 種類のプラン ( `Limit + IndexScan(keep order: true)`と`TopN + IndexScan(keep order: false)`を生成します。 `ORDER_INDEX`ヒントが使用される場合、オプティマイザはインデックスを順番に読み取る最初のプランを選択します。

> **ノート：**
>
> -   クエリ自体がインデックスを順番に読み取る必要がない場合 (つまり、ヒントがなければ、オプティマイザはどのような状況でもインデックスを順番に読み取るプランを生成しません)、ヒント`ORDER_INDEX`を使用すると、エラー`Can't find a proper physical plan for this query`発生します。 。この場合、対応する`ORDER_INDEX`ヒントを削除する必要があります。
> -   パーティションテーブルのインデックスは順番に読み取ることができないため、パーティションテーブルとその関連インデックスに対して`ORDER_INDEX`ヒントを使用しないでください。

### NO_ORDER_INDEX(t1_name, idx1_name [, idx2_name ...]) {#no-order-index-t1-name-idx1-name-idx2-name}

`NO_ORDER_INDEX(t1_name, idx1_name [, idx2_name ...])`ヒントは、指定されたテーブルに対して指定されたインデックスのみを使用し、指定されたインデックスを順番に読み取らないようにオプティマイザーに指示します。このヒントは通常、次のシナリオに適用されます。

次の例は、クエリ ステートメントの効果が`SELECT * FROM t t1 use index(idx1, idx2);`と同等であることを示しています。

```sql
CREATE TABLE t(a INT, b INT, key(a), key(b));
EXPLAIN SELECT /*+ NO_ORDER_INDEX(t, a) */ a FROM t ORDER BY a LIMIT 10;
```

```sql
+----------------------------+----------+-----------+---------------------+--------------------------------+
| id                         | estRows  | task      | access object       | operator info                  |
+----------------------------+----------+-----------+---------------------+--------------------------------+
| TopN_7                     | 10.00    | root      |                     | test.t.a, offset:0, count:10   |
| └─IndexReader_14           | 10.00    | root      |                     | index:TopN_13                  |
|   └─TopN_13                | 10.00    | cop[tikv] |                     | test.t.a, offset:0, count:10   |
|     └─IndexFullScan_12     | 10000.00 | cop[tikv] | table:t, index:a(a) | keep order:false, stats:pseudo |
+----------------------------+----------+-----------+---------------------+--------------------------------+
```

`ORDER_INDEX`ヒントの例と同様に、オプティマイザーはこのクエリに対して`Limit + IndexScan(keep order: true)`と`TopN + IndexScan(keep order: false)`の 2 種類のプランを生成します。 `NO_ORDER_INDEX`ヒントが使用される場合、オプティマイザは後者のプランを選択して、インデックスを順不同で読み取ります。

### AGG_TO_COP() {#agg-to-cop}

`AGG_TO_COP()`ヒントは、指定されたクエリ ブロック内の集計演算をコプロセッサにプッシュダウンするようにオプティマイザーに指示します。オプティマイザがプッシュダウンに適した集計関数をプッシュダウンしない場合は、このヒントを使用することをお勧めします。例えば：

{{< copyable "" >}}

```sql
select /*+ AGG_TO_COP() */ sum(t1.a) from t t1;
```

### LIMIT_TO_COP() {#limit-to-cop}

`LIMIT_TO_COP()`ヒントは、指定されたクエリ ブロック内の`Limit`および`TopN`演算子をコプロセッサにプッシュダウンするようにオプティマイザに指示します。オプティマイザがそのような操作を実行しない場合は、このヒントを使用することをお勧めします。例えば：

{{< copyable "" >}}

```sql
SELECT /*+ LIMIT_TO_COP() */ * FROM t WHERE a = 1 AND b > 10 ORDER BY c LIMIT 1;
```

### READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]]) {#read-from-storage-tiflash-t1-name-tl-name-tikv-t2-name-tl-name}

`READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]])`ヒントは、特定のstorageエンジンから特定のテーブルを読み取るようにオプティマイザーに指示します。現在、このヒントは 2 つのstorageエンジン パラメーター ( `TIKV`と`TIFLASH`をサポートしています。テーブルに別名がある場合は、その別名を`READ_FROM_STORAGE()`のパラメータとして使用します。テーブルに別名がない場合は、テーブルの元の名前をパラメータとして使用します。例えば：

{{< copyable "" >}}

```sql
select /*+ READ_FROM_STORAGE(TIFLASH[t1], TIKV[t2]) */ t1.a from t t1, t t2 where t1.a = t2.a;
```

### USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...]) {#use-index-merge-t1-name-idx1-name-idx2-name}

`USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...])`ヒントは、インデックス マージ メソッドを使用して特定のテーブルにアクセスするようにオプティマイザに指示します。インデクス結合には、交差型と共用体型の 2 種類があります。詳細は[インデックス マージを使用した Explain ステートメント](/explain-index-merge.md)を参照してください。

インデックスのリストを明示的に指定すると、TiDB はリストからインデックスを選択してインデックス マージを構築します。インデックスのリストを指定しない場合、TiDB は使用可能なすべてのインデックスからインデックスを選択してインデックス マージを構築します。

交差タイプのインデックス マージの場合、指定されたインデックスのリストはヒント内の必須パラメーターです。 Union タイプのインデックス マージの場合、指定されたインデックスのリストはヒント内のオプションのパラメーターです。次の例を参照してください。

{{< copyable "" >}}

```sql
SELECT /*+ USE_INDEX_MERGE(t1, idx_a, idx_b, idx_c) */ * FROM t1 WHERE t1.a > 10 OR t1.b > 10;
```

同じテーブルに対して複数の`USE_INDEX_MERGE`ヒントが作成されると、オプティマイザは、これらのヒントで指定されたインデックス セットの和集合からインデックスを選択しようとします。

> **ノート：**
>
> `USE_INDEX_MERGE`のパラメータは、列名ではなくインデックス名を参照します。主キーのインデックス名は`primary`です。

### LEADING(t1_name [, tl_name ...]) {#leading-t1-name-tl-name}

`LEADING(t1_name [, tl_name ...])`ヒントは、実行プランを生成するときに、ヒントで指定されたテーブル名の順序に従って複数テーブルの結合の順序を決定することをオプティマイザに思い出させます。例えば：

{{< copyable "" >}}

```sql
SELECT /*+ LEADING(t1, t2) */ * FROM t1, t2, t3 WHERE t1.id = t2.id and t2.id = t3.id;
```

複数テーブル結合を使用した上記のクエリでは、結合の順序は`LEADING()`ヒントで指定されたテーブル名の順序によって決まります。オプティマイザはまず`t1`と`t2`を結合し、次にその結果を`t3`と結合します。このヒントは[`STRAIGHT_JOIN`](#straight_join)よりも一般的です。

`LEADING`ヒントは、次の状況では有効になりません。

-   `LEADING`ヒントが複数指定されています。
-   `LEADING`ヒントで指定されたテーブル名は存在しません。
-   `LEADING`ヒントに重複したテーブル名が指定されています。
-   オプティマイザは、 `LEADING`ヒントで指定された順序に従って結合操作を実行できません。
-   `straight_join()`ヒントはすでに存在します。
-   クエリには、デカルト積を伴う外部結合が含まれています。
-   `MERGE_JOIN` 、 `INL_JOIN` 、 `INL_HASH_JOIN` 、 `HASH_JOIN`のヒントのいずれかが同時に使用されます。

上記の状況では、警告が生成されます。

```sql
-- Multiple `LEADING` hints are specified.
SELECT /*+ LEADING(t1, t2) LEADING(t3) */ * FROM t1, t2, t3 WHERE t1.id = t2.id and t2.id = t3.id;

-- To learn why the `LEADING` hint fails to take effect, execute `show warnings`.
SHOW WARNINGS;
```

```sql
+---------+------+-------------------------------------------------------------------------------------------------------------------+
| Level   | Code | Message                                                                                                           |
+---------+------+-------------------------------------------------------------------------------------------------------------------+
| Warning | 1815 | We can only use one leading hint at most, when multiple leading hints are used, all leading hints will be invalid |
+---------+------+-------------------------------------------------------------------------------------------------------------------+
```

> **ノート：**
>
> クエリ ステートメントに外部結合が含まれる場合、ヒントでは結合順序を交換できるテーブルのみを指定できます。結合順序を入れ替えることができないテーブルがヒント内にある場合、ヒントは無効になります。たとえば、 `SELECT * FROM t1 LEFT JOIN (t2 JOIN t3 JOIN t4) ON t1.a = t2.a;`で、 `t2` 、 `t3` 、および`t4`テーブルの結合順序を制御する場合、 `LEADING`ヒントに`t1`を指定することはできません。

### マージ（） {#merge}

共通テーブル式 (CTE) を含むクエリで`MERGE()`ヒントを使用すると、サブクエリの実体化が無効になり、サブクエリが CTE にインライン展開される可能性があります。このヒントは、非再帰的 CTE にのみ適用されます。一部のシナリオでは、 `MERGE()`を使用すると、一時スペースを割り当てるデフォルトの動作よりも高い実行効率が得られます。たとえば、クエリ条件をプッシュダウンするか、CTE クエリをネストします。

```sql
-- Uses the hint to push down the predicate of the outer query.
WITH CTE AS (SELECT /*+ MERGE() */ * FROM tc WHERE tc.a < 60) SELECT * FROM CTE WHERE CTE.a < 18;

-- Uses the hint in a nested CTE query to expand a CTE inline into the outer query.
WITH CTE1 AS (SELECT * FROM t1), CTE2 AS (WITH CTE3 AS (SELECT /*+ MERGE() */ * FROM t2), CTE4 AS (SELECT * FROM t3) SELECT * FROM CTE3, CTE4) SELECT * FROM CTE1, CTE2;
```

> **ノート：**
>
> `MERGE()`は、単純な CTE クエリにのみ適用されます。以下の場合には適用されません。
>
> -   [再帰的 CTE](https://docs.pingcap.com/tidb/stable/dev-guide-use-common-table-expression#recursive-cte)
> -   集約演算子、ウィンドウ関数、 `DISTINCT`など、展開できないインラインを含むサブクエリ。
>
> CTE 参照の数が多すぎると、クエリのパフォーマンスがデフォルトの実体化動作よりも低下する可能性があります。

## グローバルに有効なヒント {#hints-that-take-effect-globally}

グローバル ヒントは[ビュー](/views.md)で機能します。グローバル ヒントとして指定すると、クエリで定義されたヒントがビュー内で有効になります。グローバル ヒントを指定するには、まず`QB_NAME`ヒントを使用してクエリ ブロック名を定義し、次に`ViewName@QueryBlockName`の形式でターゲット ヒントを追加します。

### ステップ 1: <code>QB_NAME</code>ヒントを使用してビューのクエリ ブロック名を定義する {#step-1-define-the-query-block-name-of-the-view-using-the-code-qb-name-code-hint}

[クエリブロック](#qb_name)の定義と同じですが、構文は`QB_NAME(QB)`から`QB_NAME(QB, ViewName@QueryBlockName [.ViewName@QueryBlockName .ViewName@QueryBlockName ...])`に拡張されています。

> **ノート：**
>
> `@QueryBlockName`とその直後の`.ViewName@QueryBlockName`間には空白があります。それ以外の場合、 `.ViewName@QueryBlockName` `QueryBlockName`の一部として扱われます。たとえば、 `QB_NAME(v2_1, v2@SEL_1 .@SEL_1)`は有効ですが、 `QB_NAME(v2_1, v2@SEL_1.@SEL_1)`正しく解析できません。

-   単一のビューを持ち、サブクエリを持たない単純なステートメントの場合、次の例では、ビュー`v`の最初のクエリ ブロック名を指定します。

    ```sql
    SELECT /* Comment: The name of the current query block is the default @SEL_1 */ * FROM v;
    ```

    ビュー`v`の場合、クエリ ステートメントから始まるリスト ( `ViewName@QueryBlockName [.ViewName@QueryBlockName .ViewName@QueryBlockName ...]` ) の最初のビュー名は`v@SEL_1`です。ビュー`v`の最初のクエリ ブロックは、 `QB_NAME(v_1, v@SEL_1 .@SEL_1)`として宣言することも、 `@SEL_1`を省略して単に`QB_NAME(v_1, v)`として記述することもできます。

    ```sql
    CREATE VIEW v AS SELECT /* Comment: The name of the current query block is the default @SEL_1 */ * FROM t;

    -- Specifies the global hint
    SELECT /*+ QB_NAME(v_1, v) USE_INDEX(t@v_1, idx) */ * FROM v;
    ```

-   ネストされたビューとサブクエリを含む複雑なステートメントの場合、次の例では、ビュー`v1`と`v2`の 2 つのクエリ ブロックのそれぞれの名前を指定します。

    ```sql
    SELECT /* Comment: The name of the current query block is the default @SEL_1 */ * FROM v2 JOIN (
        SELECT /* Comment: The name of the current query block is the default @SEL_2 */ * FROM v2) vv;
    ```

    最初のビュー`v2`の場合、最初のクエリ ステートメントから始まるリスト内の最初のビュー名は`v2@SEL_1`です。 2 番目のビュー`v2`の場合、最初のビュー名は`v2@SEL_2`です。次の例では、最初のビュー`v2`のみを考慮しています。

    ビュー`v2`の最初のクエリ ブロックは`QB_NAME(v2_1, v2@SEL_1 .@SEL_1)`として宣言でき、ビュー`v2`の 2 番目のクエリ ブロックは`QB_NAME(v2_2, v2@SEL_1 .@SEL_2)`として宣言できます。

    ```sql
    CREATE VIEW v2 AS
        SELECT * FROM t JOIN /* Comment: For view v2, the name of the current query block is the default @SEL_1. So, the current query block view list is v2@SEL_1 .@SEL_1 */
        (
            SELECT COUNT(*) FROM t1 JOIN v1 /* Comment: For view v2, the name of the current query block is the default @SEL_2. So, the current query block view list is v2@SEL_1 .@SEL_2 */
        ) tt;
    ```

    ビュー`v1`の場合、前のステートメントから始まるリスト内の最初のビュー名は`v2@SEL_1 .v1@SEL_2`です。ビュー`v1`の最初のクエリ ブロックは`QB_NAME(v1_1, v2@SEL_1 .v1@SEL_2 .@SEL_1)`として宣言でき、ビュー`v1`の 2 番目のクエリ ブロックは`QB_NAME(v1_2, v2@SEL_1 .v1@SEL_2 .@SEL_2)`として宣言できます。

    ```sql
    CREATE VIEW v1 AS SELECT * FROM t JOIN /* Comment: For view `v1`, the name of the current query block is the default @SEL_1. So, the current query block view list is v2@SEL_1 .@SEL_2 .v1@SEL_1 */
        (
            SELECT COUNT(*) FROM t1 JOIN t2 /* Comment: For view `v1`, the name of the current query block is the default @SEL_2. So, the current query block view list is v2@SEL_1 .@SEL_2 .v1@SEL_2 */
        ) tt;
    ```

> **ノート：**
>
> -   ビューでグローバル ヒントを使用するには、ビュー内で対応する`QB_NAME`ヒントを定義する必要があります。そうしないと、グローバル ヒントが有効になりません。
>
> -   ヒントを使用してビュー内の複数のテーブル名を指定する場合、同じヒントに表示されるテーブル名が同じビューの同じクエリ ブロック内にあることを確認する必要があります。
>
> -   最も外側のクエリ ブロックのビューで`QB_NAME`ヒントを定義すると、次のようになります。
>
>     -   `QB_NAME`のビュー リストの最初の項目については、 `@SEL_`が明示的に宣言されていない場合、デフォルトは`QB_NAME`が定義されているクエリ ブロックの位置と一致します。つまり、クエリ`SELECT /*+ QB_NAME(qb1, v2) */ * FROM v2 JOIN (SELECT /*+ QB_NAME(qb2, v2) */ * FROM v2) vv;`は`SELECT /*+ QB_NAME(qb1, v2@SEL_1) */ * FROM v2 JOIN (SELECT /*+ QB_NAME(qb2, v2@SEL_2) */ * FROM v2) vv;`と同等です。
>     -   `QB_NAME`のビューリストの先頭項目以外の項目は、 `@SEL_1`のみ省略可能です。つまり、現在のビューの最初のクエリ ブロックで`@SEL_1`が宣言されている場合、 `@SEL_1`省略できます。それ以外の場合、 `@SEL_`省略できません。前述の例の場合:
>
>         -   ビュー`v2`の最初のクエリ ブロックは`QB_NAME(v2_1, v2)`として宣言できます。
>         -   ビュー`v2`の 2 番目のクエリ ブロックは`QB_NAME(v2_2, v2.@SEL_2)`として宣言できます。
>         -   ビュー`v1`の最初のクエリ ブロックは`QB_NAME(v1_1, v2.v1@SEL_2)`として宣言できます。
>         -   ビュー`v1`の 2 番目のクエリ ブロックは`QB_NAME(v1_2, v2.v1@SEL_2 .@SEL_2)`として宣言できます。

### ステップ 2: ターゲット ヒントを追加する {#step-2-add-the-target-hints}

ビューのクエリ ブロックに`QB_NAME`ヒントを定義した後、必要な[クエリブロックで有効になるヒント](#hints-that-take-effect-in-query-blocks) `ViewName@QueryBlockName`の形式で追加して、ビュー内で有効にすることができます。例えば：

-   ビュー`v2`の最初のクエリ ブロックに`MERGE_JOIN()`ヒントを指定します。

    ```sql
    SELECT /*+ QB_NAME(v2_1, v2) merge_join(t@v2_1) */ * FROM v2;
    ```

-   ビュー`v2`の 2 番目のクエリ ブロックにヒント`MERGE_JOIN()`と`STREAM_AGG()`を指定します。

    ```sql
    SELECT /*+ QB_NAME(v2_2, v2.@SEL_2) merge_join(t1@v2_2) stream_agg(@v2_2) */ * FROM v2;
    ```

-   ビュー`v1`の最初のクエリ ブロックに`HASH_JOIN()`ヒントを指定します。

    ```sql
    SELECT /*+ QB_NAME(v1_1, v2.v1@SEL_2) hash_join(t@v1_1) */ * FROM v2;
    ```

-   ビュー`v1`の 2 番目のクエリ ブロックにヒント`HASH_JOIN()`と`HASH_AGG()`を指定します。

    ```sql
    SELECT /*+ QB_NAME(v1_2, v2.v1@SEL_2 .@SEL_2) hash_join(t1@v1_2) hash_agg(@v1_2) */ * FROM v2;
    ```

## クエリ全体で有効なヒント {#hints-that-take-effect-in-the-whole-query}

このカテゴリのヒントは、**最初の**`SELECT` 、 `UPDATE` 、または`DELETE`キーワードの後に​​のみ続きます。これは、このクエリの実行時に指定されたシステム変数の値を変更するのと同じです。ヒントの優先順位は、既​​存のシステム変数の優先順位よりも高くなります。

> **ノート：**
>
> このカテゴリのヒントにはオプションの隠し変数`@QB_NAME`もありますが、変数を指定した場合でも、ヒントはクエリ全体で有効になります。

### NO_INDEX_MERGE() {#no-index-merge}

`NO_INDEX_MERGE()`ヒントは、オプティマイザのインデックス マージ機能を無効にします。

たとえば、次のクエリではインデックス マージが使用されません。

{{< copyable "" >}}

```sql
select /*+ NO_INDEX_MERGE() */ * from t where t.a > 0 or t.b > 0;
```

このヒントに加えて、 `tidb_enable_index_merge`システム変数を設定すると、この機能を有効にするかどうかも制御されます。

> **ノート：**
>
> -   `NO_INDEX_MERGE` `USE_INDEX_MERGE`よりも高い優先順位を持ちます。両方のヒントを使用した場合、 `USE_INDEX_MERGE`有効になりません。
> -   サブクエリの場合、 `NO_INDEX_MERGE`サブクエリの最も外側のレベルに配置された場合にのみ有効になります。

### USE_TOJA(ブール値) {#use-toja-boolean-value}

`boolean_value`パラメータには`TRUE`または`FALSE`を指定できます。 `USE_TOJA(TRUE)`ヒントにより、オプティマイザは`in`条件 (サブクエリを含む) を結合および集計操作に変換できるようになります。比較的、 `USE_TOJA(FALSE)`ヒントはこの機能を無効にします。

たとえば、次のクエリは`in (select t2.a from t2) subq`を対応する結合および集計操作に変換します。

{{< copyable "" >}}

```sql
select /*+ USE_TOJA(TRUE) */ t1.a, t1.b from t1 where t1.a in (select t2.a from t2) subq;
```

このヒントに加えて、 `tidb_opt_insubq_to_join_and_agg`システム変数を設定すると、この機能を有効にするかどうかも制御されます。

### MAX_EXECUTION_TIME(N) {#max-execution-time-n}

`MAX_EXECUTION_TIME(N)`ヒントは、サーバーがステートメントを終了するまでにステートメントの実行が許可される時間に制限`N` (ミリ秒単位のタイムアウト値) を設けます。次のヒントでは、 `MAX_EXECUTION_TIME(1000)`タイムアウトが 1000 ミリ秒 (つまり 1 秒) であることを意味します。

{{< copyable "" >}}

```sql
select /*+ MAX_EXECUTION_TIME(1000) */ * from t1 inner join t2 where t1.id = t2.id;
```

このヒントに加えて、 `global.max_execution_time`システム変数によってステートメントの実行時間を制限することもできます。

### MEMORY_QUOTA(N) {#memory-quota-n}

`MEMORY_QUOTA(N)`ヒントは、ステートメントが使用できるメモリ量に制限`N` (MB または GB 単位のしきい値) を設定します。ステートメントのメモリ使用量がこの制限を超えると、TiDB はステートメントの制限超過動作に基づいてログ メッセージを生成するか、ステートメントを終了します。

次のヒントでは、 `MEMORY_QUOTA(1024 MB)`メモリ使用量が 1024 MB に制限されていることを意味します。

{{< copyable "" >}}

```sql
select /*+ MEMORY_QUOTA(1024 MB) */ * from t;
```

このヒントに加えて、 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)システム変数もステートメントのメモリ使用量を制限できます。

### READ_CONSISTENT_REPLICA() {#read-consistent-replica}

`READ_CONSISTENT_REPLICA()`ヒントにより、TiKV フォロワー ノードから一貫したデータを読み取る機能が有効になります。例えば：

{{< copyable "" >}}

```sql
select /*+ READ_CONSISTENT_REPLICA() */ * from t;
```

このヒントに加えて、環境変数`tidb_replica_read`を`'follower'`または`'leader'`に設定すると、この機能を有効にするかどうかも制御されます。

### IGNORE_PLAN_CACHE() {#ignore-plan-cache}

`IGNORE_PLAN_CACHE()`ヒントは、現在の`prepare`ステートメントを処理するときにプラン キャッシュを使用しないようにオプティマイザに通知します。

このヒントは、 [準備プランキャッシュ](/sql-prepared-plan-cache.md)が有効な場合に、特定の種類のクエリに対してプラン キャッシュを一時的に無効にするために使用されます。

次の例では、 `prepare`ステートメントの実行時にプラン キャッシュが強制的に無効になります。

{{< copyable "" >}}

```sql
prepare stmt from 'select  /*+ IGNORE_PLAN_CACHE() */ * from t where t.id = ?';
```

### STRAIGHT_JOIN() {#straight-join}

`STRAIGHT_JOIN()`ヒントは、結合計画を生成するときに、オプティマイザに`FROM`句のテーブル名の順序でテーブルを結合するように指示します。

{{< copyable "" >}}

```sql
SELECT /*+ STRAIGHT_JOIN() */ * FROM t t1, t t2 WHERE t1.a = t2.a;
```

> **ノート：**
>
> -   `STRAIGHT_JOIN`は`LEADING`よりも優先されます。両方のヒントを使用した場合、 `LEADING`有効になりません。
> -   `STRAIGHT_JOIN`ヒントよりも一般的な`LEADING`ヒントを使用することをお勧めします。

### NTH_PLAN(N) {#nth-plan-n}

`NTH_PLAN(N)`ヒントは、物理最適化中に見つかった`N`番目の物理プランを選択するようにオプティマイザーに思い出させます。 `N`正の整数でなければなりません。

指定された`N`が物理最適化の検索範囲を超えている場合、TiDB は警告を返し、このヒントを無視する戦略に基づいて最適な物理プランを選択します。

このヒントは、カスケード プランナーが有効になっている場合には有効になりません。

次の例では、オプティマイザは物理的な最適化中に見つかった 3 番目の物理プランを選択するように強制されます。

{{< copyable "" >}}

```sql
SELECT /*+ NTH_PLAN(3) */ count(*) from t where a > 5;
```

> **ノート：**
>
> `NTH_PLAN(N)`は主にテスト用に使用されており、それ以降のバージョンでの互換性は保証されません。このヒントは**注意して**使用してください。

### RESOURCE_GROUP(リソースグループ名) {#resource-group-resource-group-name}

`RESOURCE_GROUP(resource_group_name)`はリソースを分離するために[リソース制御](/tidb-resource-control.md)に使用されます。このヒントは、指定されたリソース グループを使用して現在のステートメントを一時的に実行します。指定されたリソース グループが存在しない場合、このヒントは無視されます。

例：

```sql
SELECT /*+ RESOURCE_GROUP(rg1) */ * FROM t limit 10;
```
