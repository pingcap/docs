---
title: Optimizer Hints
summary: Use Optimizer Hints to influence query execution plans
---

# オプティマイザーのヒント {#optimizer-hints}

TiDBは、MySQL5.7で導入されたコメントのような構文に基づくオプティマイザヒントをサポートしています。たとえば、一般的な構文の1つは`/*+ HINT_NAME([t1_name [, t2_name] ...]) */`です。 TiDBオプティマイザが最適でないクエリプランを選択する場合は、オプティマイザヒントの使用をお勧めします。

> **ノート：**
>
> 5.7.7より前のMySQLコマンドラインクライアントは、デフォルトでオプティマイザヒントを削除します。これらの以前のバージョンで`Hint`構文を使用する場合は、クライアントの起動時に`--comments`オプションを追加します。例： `mysql -h 127.0.0.1 -P 4000 -uroot --comments` 。

## 構文 {#syntax}

オプティマイザーのヒントでは大文字と小文字が区別されず、SQLステートメントの`SELECT` 、または`DELETE`キーワードに続く`/*+ ... */` `UPDATE`コメント内で指定されます。オプティマイザーヒントは現在、 `INSERT`のステートメントではサポートされていません。

複数のヒントは、コンマで区切ることで指定できます。たとえば、次のクエリは3つの異なるヒントを使用します。

{{< copyable "" >}}

```sql
SELECT /*+ USE_INDEX(t1, idx1), HASH_AGG(), HASH_JOIN(t1) */ count(*) FROM t t1, t t2 WHERE t1.a = t2.b;
```

オプティマイザヒントがクエリ実行プランにどのように影響するかは、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)と[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)の出力で確認できます。

ヒントが正しくないか不完全であっても、ステートメントエラーは発生しません。これは、ヒントは、クエリの実行に対してセマンティックな*ヒント*（提案）のみを持つことを目的としているためです。同様に、ヒントが適用できない場合、TiDBはせいぜい警告を返します。

> **ノート：**
>
> コメントが指定されたキーワードの後ろに続かない場合、それらは一般的なMySQLコメントとして扱われます。コメントは有効にならず、警告は報告されません。

現在、TiDBは、スコープが異なる2つのカテゴリのヒントをサポートしています。ヒントの最初のカテゴリは、 [`/*+ HASH_AGG() */`](#hash_agg)などのクエリブロックのスコープで有効になります。ヒントの2番目のカテゴリは、 [`/*+ MEMORY_QUOTA(1024 MB)*/`](#memory_quotan)などのクエリ全体で有効になります。

ステートメント内の各クエリまたはサブクエリは、異なるクエリブロックに対応し、各クエリブロックには独自の名前があります。例えば：

{{< copyable "" >}}

```sql
SELECT * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

上記のクエリステートメントには3つのクエリブロックがあります。最も外側の`SELECT`は、名前が`sel_1`の最初のクエリブロックに対応します。 2つの`SELECT`つのサブクエリは、2番目と3番目のクエリブロックに対応します。名前はそれぞれ`sel_2`と`sel_3`です。番号の順序は、左から右への`SELECT`の出現に基づいています。最初の`SELECT`を`DELETE`または`UPDATE`に置き換えると、対応するクエリブロック名は`del_1`または`upd_1`になります。

## クエリブロックで有効になるヒント {#hints-that-take-effect-in-query-blocks}

このカテゴリのヒントは、 `SELECT` 、**または**`DELETE` `UPDATE`のキーワードの後ろに続けることができます。ヒントの有効範囲を制御するには、ヒントでクエリブロックの名前を使用します。クエリ内の各テーブルを正確に識別することで、ヒントパラメータを明確にすることができます（テーブル名またはエイリアスが重複している場合）。ヒントにクエリブロックが指定されていない場合、ヒントはデフォルトで現在のブロックで有効になります。

例えば：

{{< copyable "" >}}

```sql
SELECT /*+ HASH_JOIN(@sel_1 t1@sel_1, t3) */ * FROM (SELECT t1.a, t1.b FROM t t1, t t2 WHERE t1.a = t2.a) t1, t t3 WHERE t1.b = t3.b;
```

このヒントは`sel_1`のクエリブロックで有効になり、そのパラメータは`sel_1`の`t1`と`t3`のテーブルです（ `sel_2`には`t1`のテーブルも含まれます）。

上記のように、次の方法でヒントにクエリブロックの名前を指定できます。

-   ヒントの最初のパラメーターとしてクエリブロック名を設定し、他のパラメーターとはスペースで区切ります。 `QB_NAME`に加えて、このセクションにリストされているすべてのヒントには、別のオプションの非表示パラメーター`@QB_NAME`もあります。このパラメーターを使用することにより、このヒントの有効な範囲を指定できます。
-   パラメータのテーブル名に`@QB_NAME`を追加して、このテーブルが属するクエリブロックを明示的に指定します。

> **ノート：**
>
> ヒントを有効にするクエリブロックの中または前にヒントを配置する必要があります。ヒントがクエリブロックの後に置かれている場合、それは有効になりません。

### QB_NAME {#qb-name}

クエリステートメントが複数のネストされたクエリを含む複雑なステートメントである場合、特定のクエリブロックのIDと名前が誤って識別される可能性があります。ヒント`QB_NAME`は、この点で役立ちます。

`QB_NAME`はクエリブロック名を意味します。クエリブロックに新しい名前を指定できます。指定された`QB_NAME`と以前のデフォルト名は両方とも有効です。例えば：

{{< copyable "" >}}

```sql
SELECT /*+ QB_NAME(QB1) */ * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

このヒントは、外側の`SELECT`クエリブロックの名前を`QB1`に指定します。これにより、 `QB1`とデフォルト名`sel_1`の両方がクエリブロックに対して有効になります。

> **ノート：**
>
> 上記の例で、ヒントが`QB_NAME`から`sel_2`を指定し、元の2番目の`SELECT`クエリブロックに新しい`QB_NAME`を指定しない場合、 `sel_2`は2番目の`SELECT`クエリブロックの無効な名前になります。

### MERGE_JOIN（t1_name [、tl_name ...]） {#merge-join-t1-name-tl-name}

`MERGE_JOIN(t1_name [, tl_name ...])`ヒントは、オプティマイザに、指定されたテーブルに対してソート-マージ結合アルゴリズムを使用するように指示します。一般に、このアルゴリズムはより少ないメモリを消費しますが、より長い処理時間を要します。データ量が非常に多い場合やシステムメモリが不足している場合は、このヒントを使用することをお勧めします。例えば：

{{< copyable "" >}}

```sql
select /*+ MERGE_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

> **ノート：**
>
> `TIDB_SMJ`は、TiDB3.0.x以前のバージョンの`MERGE_JOIN`のエイリアスです。これらのバージョンのいずれかを使用している場合は、ヒントに`TIDB_SMJ(t1_name [, tl_name ...])`の構文を適用する必要があります。それ以降のバージョンのTiDBでは、 `TIDB_SMJ`と`MERGE_JOIN`の両方がヒントの有効な名前ですが、 `MERGE_JOIN`をお勧めします。

### INL_JOIN（t1_name [、tl_name ...]） {#inl-join-t1-name-tl-name}

`INL_JOIN(t1_name [, tl_name ...])`ヒントは、指定されたテーブルにインデックスネストループ結合アルゴリズムを使用するようにオプティマイザに指示します。このアルゴリズムは、一部のシナリオではシステムリソースの消費量が少なく、処理時間が短くなる可能性があり、他のシナリオでは逆の結果をもたらす可能性があります。外側のテーブルが`WHERE`条件でフィルタリングされた後、結果セットが10,000行未満の場合は、このヒントを使用することをお勧めします。例えば：

{{< copyable "" >}}

```sql
select /*+ INL_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

`INL_JOIN()`で指定されたパラメーターは、クエリプランを作成するときの内部テーブルの候補テーブルです。たとえば、 `INL_JOIN(t1)`は、TiDBがクエリプランを作成するための内部テーブルとして`t1`の使用のみを考慮することを意味します。候補テーブルにエイリアスがある場合は、 `INL_JOIN()`のパラメータとしてエイリアスを使用する必要があります。エイリアスがない場合は、テーブルの元の名前をパラメータとして使用します。たとえば、 `select /*+ INL_JOIN(t1) */ * from t t1, t t2 where t1.a = t2.b;`クエリでは、 `INL_JOIN()`のパラメータとして`t`ではなく`t`テーブルのエイリアス`t1`または`t2`を使用する必要があります。

> **ノート：**
>
> `TIDB_INLJ`は、TiDB3.0.x以前のバージョンの`INL_JOIN`のエイリアスです。これらのバージョンのいずれかを使用している場合は、ヒントに`TIDB_INLJ(t1_name [, tl_name ...])`の構文を適用する必要があります。それ以降のバージョンのTiDBでは、 `TIDB_INLJ`と`INL_JOIN`の両方がヒントの有効な名前ですが、 `INL_JOIN`をお勧めします。

### INL_HASH_JOIN {#inl-hash-join}

`INL_HASH_JOIN(t1_name [, tl_name])`ヒントは、オプティマイザにインデックスネストループハッシュ結合アルゴリズムを使用するように指示します。このアルゴリズムを使用するための条件は、インデックスネストループ結合アルゴリズムを使用するための条件と同じです。 2つのアルゴリズムの違いは、 `INL_JOIN`は結合された内部テーブルにハッシュテーブルを作成しますが、 `INL_HASH_JOIN`は結合された外部テーブルにハッシュテーブルを作成することです。 `INL_HASH_JOIN`にはメモリ使用量の固定制限がありますが、 `INL_JOIN`で使用されるメモリは、内部テーブルで一致する行数によって異なります。

### HASH_JOIN（t1_name [、tl_name ...]） {#hash-join-t1-name-tl-name}

`HASH_JOIN(t1_name [, tl_name ...])`ヒントは、指定されたテーブルにハッシュ結合アルゴリズムを使用するようにオプティマイザーに指示します。このアルゴリズムを使用すると、クエリを複数のスレッドと同時に実行できます。これにより、処理速度は向上しますが、より多くのメモリを消費します。例えば：

{{< copyable "" >}}

```sql
select /*+ HASH_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

> **ノート：**
>
> `TIDB_HJ`は、TiDB3.0.x以前のバージョンの`HASH_JOIN`のエイリアスです。これらのバージョンのいずれかを使用している場合は、ヒントに`TIDB_HJ(t1_name [, tl_name ...])`の構文を適用する必要があります。それ以降のバージョンのTiDBでは、 `TIDB_HJ`と`HASH_JOIN`の両方がヒントの有効な名前ですが、 `HASH_JOIN`をお勧めします。

### HASH_AGG（） {#hash-agg}

`HASH_AGG()`ヒントは、指定されたクエリブロック内のすべての集計関数でハッシュ集計アルゴリズムを使用するようにオプティマイザに指示します。このアルゴリズムを使用すると、クエリを複数のスレッドと同時に実行できます。これにより、処理速度は向上しますが、より多くのメモリを消費します。例えば：

{{< copyable "" >}}

```sql
select /*+ HASH_AGG() */ count(*) from t1, t2 where t1.a > 10 group by t1.id;
```

### STREAM_AGG（） {#stream-agg}

`STREAM_AGG()`ヒントは、指定されたクエリブロック内のすべての集計関数でストリーム集計アルゴリズムを使用するようにオプティマイザに指示します。一般に、このアルゴリズムはより少ないメモリを消費しますが、より長い処理時間を要します。データ量が非常に多い場合やシステムメモリが不足している場合は、このヒントを使用することをお勧めします。例えば：

{{< copyable "" >}}

```sql
select /*+ STREAM_AGG() */ count(*) from t1, t2 where t1.a > 10 group by t1.id;
```

### USE_INDEX（t1_name、idx1_name [、idx2_name ...]） {#use-index-t1-name-idx1-name-idx2-name}

`USE_INDEX(t1_name, idx1_name [, idx2_name ...])`ヒントは、指定された`t1_name`のテーブルに対して指定されたインデックスのみを使用するようにオプティマイザに指示します。たとえば、次のヒントを適用すると、 `select * from t t1 use index(idx1, idx2);`ステートメントを実行するのと同じ効果があります。

{{< copyable "" >}}

```sql
SELECT /*+ USE_INDEX(t1, idx1, idx2) */ * FROM t1;
```

> **ノート：**
>
> このヒントでテーブル名のみを指定し、インデックス名は指定しない場合、実行ではインデックスは考慮されず、テーブル全体がスキャンされます。

### FORCE_INDEX（t1_name、idx1_name [、idx2_name ...]） {#force-index-t1-name-idx1-name-idx2-name}

`FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])`ヒントは、指定されたインデックスのみを使用するようにオプティマイザに指示します。

`FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])`の使用法と効果は、 `USE_INDEX(t1_name, idx1_name [, idx2_name ...])`の使用法と効果と同じです。

次の4つのクエリは同じ効果があります。

{{< copyable "" >}}

```sql
SELECT /*+ USE_INDEX(t, idx1) */ * FROM t;
SELECT /*+ FORCE_INDEX(t, idx1) */ * FROM t;
SELECT * FROM t use index(idx1);
SELECT * FROM t force index(idx1);
```

### IGNORE_INDEX（t1_name、idx1_name [、idx2_name ...]） {#ignore-index-t1-name-idx1-name-idx2-name}

`IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...])`ヒントは、指定された`t1_name`テーブルの指定されたインデックスを無視するようにオプティマイザーに指示します。たとえば、次のヒントを適用すると、 `select * from t t1 ignore index(idx1, idx2);`ステートメントを実行するのと同じ効果があります。

{{< copyable "" >}}

```sql
select /*+ IGNORE_INDEX(t1, idx1, idx2) */ * from t t1;
```

### AGG_TO_COP（） {#agg-to-cop}

`AGG_TO_COP()`ヒントは、指定されたクエリ・ブロック内の集約操作をコプロセッサーにプッシュダウンするようにオプティマイザーに指示します。オプティマイザがプッシュダウンに適した集計関数をプッシュダウンしない場合は、このヒントを使用することをお勧めします。例えば：

{{< copyable "" >}}

```sql
select /*+ AGG_TO_COP() */ sum(t1.a) from t t1;
```

### LIMIT_TO_COP（） {#limit-to-cop}

`LIMIT_TO_COP()`ヒントは、オプティマイザーに、指定された照会ブロック内の`Limit`および`TopN`の演算子をコプロセッサーにプッシュダウンするように指示します。オプティマイザがそのような操作を実行しない場合は、このヒントを使用することをお勧めします。例えば：

{{< copyable "" >}}

```sql
SELECT /*+ LIMIT_TO_COP() */ * FROM t WHERE a = 1 AND b > 10 ORDER BY c LIMIT 1;
```

### READ_FROM_STORAGE（TIFLASH [t1_name [、tl_name ...]]、TIKV [t2_name [、tl_name ...]]） {#read-from-storage-tiflash-t1-name-tl-name-tikv-t2-name-tl-name}

`READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]])`ヒントは、オプティマイザに特定のストレージエンジンから特定のテーブルを読み取るように指示します。現在、このヒントは2つのストレージエンジンパラメータ（ `TIKV`と`TIFLASH` ）をサポートしています。テーブルにエイリアスがある場合は、エイリアスを`READ_FROM_STORAGE()`のパラメータとして使用します。テーブルにエイリアスがない場合は、テーブルの元の名前をパラメータとして使用します。例えば：

{{< copyable "" >}}

```sql
select /*+ READ_FROM_STORAGE(TIFLASH[t1], TIKV[t2]) */ t1.a from t t1, t t2 where t1.a = t2.a;
```

> **ノート：**
>
> オプティマイザで別のスキーマのテーブルを使用する場合は、スキーマ名を明示的に指定する必要があります。例えば：
>
> {{< copyable "" >}}
>
> ```sql
> SELECT /*+ READ_FROM_STORAGE(TIFLASH[test1.t1,test2.t2]) */ t1.a FROM test1.t t1, test2.t t2 WHERE t1.a = t2.a;
> ```

### USE_INDEX_MERGE（t1_name、idx1_name [、idx2_name ...]） {#use-index-merge-t1-name-idx1-name-idx2-name}

`USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...])`ヒントは、オプティマイザにインデックスマージメソッドを使用して特定のテーブルにアクセスするように指示します。指定されたインデックスのリストはオプションのパラメータです。リストを明示的に指定すると、TiDBはリストからインデックスを選択してインデックスマージを構築します。インデックスのリストを指定しない場合、TiDBは使用可能なすべてのインデックスからインデックスを選択してインデックスマージを構築します。例えば：

{{< copyable "" >}}

```sql
SELECT /*+ USE_INDEX_MERGE(t1, idx_a, idx_b, idx_c) */ * FROM t1 WHERE t1.a > 10 OR t1.b > 10;
```

同じテーブルに対して複数の`USE_INDEX_MERGE`ヒントが作成されると、オプティマイザは、これらのヒントで指定されたインデックスセットの和集合からインデックスを選択しようとします。

> **ノート：**
>
> `USE_INDEX_MERGE`のパラメーターは、列名ではなく、索引名を参照します。主キーのインデックス名は`primary`です。

このヒントは、次のような厳しい条件で有効になります。

-   クエリが全表スキャンに加えて単一のインデックススキャンを選択できる場合、オプティマイザはインデックスマージを選択しません。

### LEADING（t1_name [、tl_name ...]） {#leading-t1-name-tl-name}

`LEADING(t1_name [, tl_name ...])`ヒントは、実行プランを生成するときに、ヒントで指定されたテーブル名の順序に従ってマルチテーブル結合の順序を決定することをオプティマイザに通知します。例えば：

{{< copyable "" >}}

```sql
SELECT /*+ LEADING(t1, t2) */ * FROM t1, t2, t3 WHERE t1.id = t2.id and t2.id = t3.id;
```

マルチテーブル結合を使用する上記のクエリでは、結合の順序は、 `LEADING()`ヒントで指定されたテーブル名の順序によって決定されます。オプティマイザーは最初に`t1`と`t2`を結合し、次に結果を`t3`で結合します。このヒントは[`STRAIGHT_JOIN`](#straight_join)よりも一般的です。

`LEADING`のヒントは、次の状況では有効になりません。

-   複数の`LEADING`ヒントが指定されています。
-   `LEADING`ヒントで指定されたテーブル名が存在しません。
-   重複したテーブル名が`LEADING`ヒントで指定されています。
-   オプティマイザは、 `LEADING`ヒントで指定された順序に従って結合操作を実行できません。
-   `straight_join()`のヒントはすでに存在します。
-   クエリには外部結合が含まれています。
-   `MERGE_JOIN` 、および`INL_JOIN`のヒントの`HASH_JOIN`かが同時に使用され`INL_HASH_JOIN` 。

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

## クエリ全体で有効になるヒント {#hints-that-take-effect-in-the-whole-query}

このカテゴリのヒントは、**最初の**`SELECT` 、または`UPDATE`キーワードの後ろにのみ続くことができ`DELETE` 。これは、このクエリの実行時に指定されたシステム変数の値を変更することと同じです。ヒントの優先度は、既存のシステム変数の優先度よりも高くなっています。

> **ノート：**
>
> このカテゴリのヒントには、オプションの非表示変数`@QB_NAME`もありますが、変数を指定した場合でも、ヒントはクエリ全体で有効になります。

### NO_INDEX_MERGE（） {#no-index-merge}

`NO_INDEX_MERGE()`ヒントは、オプティマイザのインデックスマージ機能を無効にします。

たとえば、次のクエリはインデックスマージを使用しません。

{{< copyable "" >}}

```sql
select /*+ NO_INDEX_MERGE() */ * from t where t.a > 0 or t.b > 0;
```

このヒントに加えて、 `tidb_enable_index_merge`システム変数を設定すると、この機能を有効にするかどうかも制御されます。

> **ノート：**
>
> -   `NO_INDEX_MERGE`は`USE_INDEX_MERGE`よりも優先度が高くなります。両方のヒントを使用すると、 `USE_INDEX_MERGE`は有効になりません。
> -   サブクエリの場合、 `NO_INDEX_MERGE`は、サブクエリの最も外側のレベルに配置されている場合にのみ有効になります。

### USE_TOJA（boolean_value） {#use-toja-boolean-value}

`boolean_value`パラメーターは`TRUE`または`FALSE`にすることができます。 `USE_TOJA(TRUE)`ヒントを使用すると、オプティマイザは`in`条件（サブクエリを含む）を結合および集計操作に変換できます。比較すると、 `USE_TOJA(FALSE)`ヒントはこの機能を無効にします。

たとえば、次のクエリは`in (select t2.a from t2) subq`を対応する結合および集計操作に変換します。

{{< copyable "" >}}

```sql
select /*+ USE_TOJA(TRUE) */ t1.a, t1.b from t1 where t1.a in (select t2.a from t2) subq;
```

このヒントに加えて、 `tidb_opt_insubq_to_join_and_agg`システム変数を設定すると、この機能を有効にするかどうかも制御されます。

### MAX_EXECUTION_TIME（N） {#max-execution-time-n}

`MAX_EXECUTION_TIME(N)`ヒントは、サーバーがステートメントを終了する前にステートメントの実行が許可される期間に制限`N` （ミリ秒単位のタイムアウト値）を設定します。次のヒントで、 `MAX_EXECUTION_TIME(1000)`は、タイムアウトが1000ミリ秒（つまり、1秒）であることを意味します。

{{< copyable "" >}}

```sql
select /*+ MAX_EXECUTION_TIME(1000) */ * from t1 inner join t2 where t1.id = t2.id;
```

このヒントに加えて、 `global.max_execution_time`システム変数はステートメントの実行時間を制限することもできます。

### MEMORY_QUOTA（N） {#memory-quota-n}

`MEMORY_QUOTA(N)`のヒントでは、ステートメントで使用できるメモリの量に制限`N` （MBまたはGB単位のしきい値）が設定されます。ステートメントのメモリ使用量がこの制限を超えると、TiDBはステートメントの制限を超えた動作に基づいてログメッセージを生成するか、単に終了します。

次のヒントで、 `MEMORY_QUOTA(1024 MB)`は、メモリ使用量が1024MBに制限されていることを意味します。

{{< copyable "" >}}

```sql
select /*+ MEMORY_QUOTA(1024 MB) */ * from t;
```

このヒントに加えて、 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)システム変数はステートメントのメモリ使用量を制限することもできます。

### READ_CONSISTENT_REPLICA（） {#read-consistent-replica}

`READ_CONSISTENT_REPLICA()`ヒントは、TiKVフォロワーノードから一貫性のあるデータを読み取る機能を有効にします。例えば：

{{< copyable "" >}}

```sql
select /*+ READ_CONSISTENT_REPLICA() */ * from t;
```

このヒントに加えて、 `tidb_replica_read`環境変数を`'follower'`または`'leader'`に設定すると、この機能を有効にするかどうかも制御されます。

### IGNORE_PLAN_CACHE（） {#ignore-plan-cache}

`IGNORE_PLAN_CACHE()`のヒントは、現在の`prepare`のステートメントを処理するときにプランキャッシュを使用しないようにオプティマイザーに通知します。

このヒントは、 [準備-計画-キャッシュ](/sql-prepared-plan-cache.md)が有効になっている場合に、特定のタイプのクエリのプランキャッシュを一時的に無効にするために使用されます。

次の例では、 `prepare`ステートメントを実行すると、プランキャッシュが強制的に無効になります。

{{< copyable "" >}}

```sql
prepare stmt from 'select  /*+ IGNORE_PLAN_CACHE() */ * from t where t.id = ?';
```

### STRAIGHT_JOIN（） {#straight-join}

`STRAIGHT_JOIN()`ヒントは、結合プランを生成するときに、オプティマイザーが`FROM`節のテーブル名の順序でテーブルを結合することを通知します。

{{< copyable "" >}}

```sql
SELECT /*+ STRAIGHT_JOIN() */ * FROM t t1, t t2 WHERE t1.a = t2.a;
```

> **ノート：**
>
> -   `STRAIGHT_JOIN`は`LEADING`よりも優先されます。両方のヒントを使用すると、 `LEADING`は有効になりません。
> -   `STRAIGHT_JOIN`ヒントよりも一般的な`LEADING`ヒントを使用することをお勧めします。

### NTH_PLAN（N） {#nth-plan-n}

`NTH_PLAN(N)`のヒントは、物理最適化中に見つかった`N`番目の物理計画を選択するようにオプティマイザーに通知します。 `N`は正の整数でなければなりません。

指定された`N`が物理最適化の検索範囲を超えている場合、TiDBは警告を返し、このヒントを無視する戦略に基づいて最適な物理計画を選択します。

このヒントは、カスケードプランナーが有効になっている場合は有効になりません。

次の例では、オプティマイザーは、物理最適化中に検出された3番目の物理計画を選択するように強制されます。

{{< copyable "" >}}

```sql
SELECT /*+ NTH_PLAN(3) */ count(*) from t where a > 5;
```

> **ノート：**
>
> `NTH_PLAN(N)`は主にテストに使用され、それ以降のバージョンでは互換性が保証されません。このヒント**は注意して**使用してください。
