---
title: Optimizer Hints
summary: Use Optimizer Hints to influence query execution plans
---

# オプティマイザーのヒント {#optimizer-hints}

TiDB は、 MySQL 5.7で導入されたコメントのような構文に基づくオプティマイザー ヒントをサポートします。たとえば、一般的な構文の 1 つは`/*+ HINT_NAME([t1_name [, t2_name] ...]) */`です。 TiDB オプティマイザがあまり最適でないクエリ プランを選択する場合は、オプティマイザ ヒントの使用をお勧めします。

> **ノート：**
>
> 5.7.7 より前の MySQL コマンドライン クライアントは、デフォルトでオプティマイザ ヒントを取り除きます。これらの以前のバージョンで`Hint`構文を使用する場合は、クライアントの起動時に`--comments`オプションを追加します。例: `mysql -h 127.0.0.1 -P 4000 -uroot --comments` 。

## 構文 {#syntax}

オプティマイザーのヒントは、大文字と小文字が区別されず、SQL ステートメントの`SELECT` 、 `UPDATE`または`DELETE`キーワードに続く`/*+ ... */`のコメント内で指定されます。オプティマイザーのヒントは、現在`INSERT`のステートメントではサポートされていません。

カンマ区切りで複数のヒントを指定できます。たとえば、次のクエリは 3 つの異なるヒントを使用します。

{{< copyable "" >}}

```sql
SELECT /*+ USE_INDEX(t1, idx1), HASH_AGG(), HASH_JOIN(t1) */ count(*) FROM t t1, t t2 WHERE t1.a = t2.b;
```

オプティマイザ ヒントがクエリ実行プランに与える影響は、 [`EXPLAIN`](/sql-statements/sql-statement-explain.md)と[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)の出力で確認できます。

ヒントが正しくないか不完全であっても、ステートメント エラーにはなりません。これは、ヒントがクエリ実行に対する*ヒント*(提案) セマンティックのみを持つことを意図しているためです。同様に、ヒントが適用されない場合、TiDB はせいぜい警告を返します。

> **ノート：**
>
> コメントが指定されたキーワードの後に続かない場合、それらは一般的な MySQL コメントとして扱われます。コメントは有効にならず、警告も報告されません。

現在、TiDB は、スコープが異なる 2 つのカテゴリのヒントをサポートしています。ヒントの最初のカテゴリは、 [`/*+ HASH_AGG() */`](#hash_agg)などのクエリ ブロックのスコープで有効になります。ヒントの 2 番目のカテゴリは、 [`/*+ MEMORY_QUOTA(1024 MB)*/`](#memory_quotan)などのクエリ全体で有効です。

ステートメント内の各クエリまたはサブクエリは、異なるクエリ ブロックに対応し、各クエリ ブロックには独自の名前があります。例えば：

{{< copyable "" >}}

```sql
SELECT * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

上記のクエリ ステートメントには 3 つのクエリ ブロックがあります。最も外側の`SELECT`は、名前が`sel_1`である最初のクエリ ブロックに対応します。 2 つの`SELECT`サブクエリは、2 番目と 3 番目のクエリ ブロックに対応し、その名前はそれぞれ`sel_2`と`sel_3`です。数字の並びは、左から右に`SELECT`のように並んでいます。最初の`SELECT`を`DELETE`または`UPDATE`に置き換えると、対応するクエリ ブロック名は`del_1`または`upd_1`になります。

## クエリ ブロックで有効になるヒント {#hints-that-take-effect-in-query-blocks}

このカテゴリのヒントは、 `SELECT` 、**または**`DELETE` `UPDATE`のキーワードの後ろに続くことができます。ヒントの有効範囲を制御するには、ヒントでクエリ ブロックの名前を使用します。クエリ内の各テーブルを正確に識別することで、ヒント パラメーターを明確にすることができます (テーブル名またはエイリアスが重複している場合)。ヒントでクエリ ブロックが指定されていない場合、ヒントは既定で現在のブロックで有効になります。

例えば：

{{< copyable "" >}}

```sql
SELECT /*+ HASH_JOIN(@sel_1 t1@sel_1, t3) */ * FROM (SELECT t1.a, t1.b FROM t t1, t t2 WHERE t1.a = t2.a) t1, t t3 WHERE t1.b = t3.b;
```

このヒントは`sel_1`クエリ ブロックで有効になり、そのパラメーターは`sel_1`の`t1`と`t3`のテーブルです ( `sel_2`には`t1`のテーブルも含まれます)。

上記のように、次の方法でヒントにクエリ ブロックの名前を指定できます。

-   ヒントの最初のパラメーターとしてクエリ ブロック名を設定し、他のパラメーターとはスペースで区切ります。 `QB_NAME`に加えて、このセクションにリストされているすべてのヒントには、別のオプションの隠しパラメーター`@QB_NAME`もあります。このパラメーターを使用して、このヒントの有効範囲を指定できます。
-   パラメーターのテーブル名に`@QB_NAME`を追加して、このテーブルが属するクエリ ブロックを明示的に指定します。

> **ノート：**
>
> ヒントは、ヒントが有効になるクエリ ブロックの中または前に配置する必要があります。クエリ ブロックの後にヒントを配置すると、有効になりません。

### QB_NAME {#qb-name}

クエリ ステートメントが複数のネストされたクエリを含む複雑なステートメントである場合、特定のクエリ ブロックの ID と名前が誤って識別される可能性があります。ヒント`QB_NAME`は、この点で私たちを助けることができます。

`QB_NAME`はクエリ ブロック名を意味します。クエリ ブロックに新しい名前を指定できます。指定された`QB_NAME`と以前のデフォルト名はどちらも有効です。例えば：

{{< copyable "" >}}

```sql
SELECT /*+ QB_NAME(QB1) */ * FROM (SELECT * FROM t) t1, (SELECT * FROM t) t2;
```

このヒントは、外側の`SELECT`クエリ ブロックの名前を`QB1`に指定します。これにより、クエリ ブロックに対して`QB1`と既定の名前`sel_1`の両方が有効になります。

> **ノート：**
>
> 上記の例で、ヒントが`QB_NAME`から`sel_2`を指定し、元の 2 番目の`SELECT`クエリ ブロックに新しい`QB_NAME`を指定しない場合、 `sel_2`は 2 番目の`SELECT`クエリ ブロックの無効な名前になります。

### MERGE_JOIN(t1_name [, tl_name ...]) {#merge-join-t1-name-tl-name}

`MERGE_JOIN(t1_name [, tl_name ...])`ヒントは、指定されたテーブルに対してソートマージ結合アルゴリズムを使用するようオプティマイザに指示します。一般に、このアルゴリズムはメモリの消費量は少なくなりますが、処理時間は長くなります。データ ボリュームが非常に大きい場合、またはシステム メモリが不足している場合は、このヒントを使用することをお勧めします。例えば：

{{< copyable "" >}}

```sql
select /*+ MERGE_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

> **ノート：**
>
> `TIDB_SMJ`は、TiDB 3.0.x 以前のバージョンでは`MERGE_JOIN`のエイリアスです。これらのバージョンのいずれかを使用している場合は、ヒントに`TIDB_SMJ(t1_name [, tl_name ...])`構文を適用する必要があります。それ以降のバージョンの TiDB では、 `TIDB_SMJ`と`MERGE_JOIN`の両方がヒントの有効な名前ですが、 `MERGE_JOIN`をお勧めします。

### INL_JOIN(t1_name [, tl_name ...]) {#inl-join-t1-name-tl-name}

`INL_JOIN(t1_name [, tl_name ...])`ヒントは、指定されたテーブルに対してインデックス ネスト ループ結合アルゴリズムを使用するようオプティマイザに指示します。このアルゴリズムは、一部のシナリオでは消費するシステム リソースが少なく、処理時間が短くなる可能性があり、他のシナリオでは逆の結果になる可能性があります。外部テーブルが`WHERE`条件でフィルター処理された後の結果セットが 10,000 行未満の場合は、このヒントを使用することをお勧めします。例えば：

{{< copyable "" >}}

```sql
select /*+ INL_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

`INL_JOIN()`で指定したパラメーターは、クエリ プランを作成するときの内部テーブルの候補テーブルです。たとえば、 `INL_JOIN(t1)`は、TiDB が`t1`のみを内部テーブルとして使用してクエリ プランを作成することを考慮することを意味します。候補テーブルにエイリアスがある場合は、エイリアスを`INL_JOIN()`のパラメーターとして使用する必要があります。エイリアスがない場合は、テーブルの元の名前をパラメーターとして使用します。たとえば、 `select /*+ INL_JOIN(t1) */ * from t t1, t t2 where t1.a = t2.b;`クエリでは、 `INL_JOIN()`のパラメーターとして`t`ではなく、 `t`テーブルのエイリアス`t1`または`t2`を使用する必要があります。

> **ノート：**
>
> `TIDB_INLJ`は、TiDB 3.0.x 以前のバージョンでは`INL_JOIN`のエイリアスです。これらのバージョンのいずれかを使用している場合は、ヒントに`TIDB_INLJ(t1_name [, tl_name ...])`構文を適用する必要があります。それ以降のバージョンの TiDB では、 `TIDB_INLJ`と`INL_JOIN`の両方がヒントの有効な名前ですが、 `INL_JOIN`をお勧めします。

### INL_HASH_JOIN {#inl-hash-join}

`INL_HASH_JOIN(t1_name [, tl_name])`ヒントは、インデックスのネストされたループ ハッシュ結合アルゴリズムを使用するようオプティマイザに指示します。このアルゴリズムを使用するための条件は、インデクス ネスト ループ ジョイン アルゴリズムを使用するための条件と同じです。 2 つのアルゴリズムの違いは、 `INL_JOIN`は結合された内部テーブルにハッシュ テーブルを作成するのに対し、 `INL_HASH_JOIN`は結合された外部テーブルにハッシュ テーブルを作成することです。 `INL_HASH_JOIN`ではメモリ使用量に一定の制限がありますが、 `INL_JOIN`で使用されるメモリは内部テーブルで一致する行の数に依存します。

### HASH_JOIN(t1_name [, tl_name ...]) {#hash-join-t1-name-tl-name}

`HASH_JOIN(t1_name [, tl_name ...])`ヒントは、指定されたテーブルに対してハッシュ結合アルゴリズムを使用するようオプティマイザに指示します。このアルゴリズムを使用すると、クエリを複数のスレッドで同時に実行できます。これにより、処理速度は向上しますが、より多くのメモリを消費します。例えば：

{{< copyable "" >}}

```sql
select /*+ HASH_JOIN(t1, t2) */ * from t1, t2 where t1.id = t2.id;
```

> **ノート：**
>
> `TIDB_HJ`は、TiDB 3.0.x 以前のバージョンでは`HASH_JOIN`のエイリアスです。これらのバージョンのいずれかを使用している場合は、ヒントに`TIDB_HJ(t1_name [, tl_name ...])`構文を適用する必要があります。それ以降のバージョンの TiDB では、 `TIDB_HJ`と`HASH_JOIN`の両方がヒントの有効な名前ですが、 `HASH_JOIN`をお勧めします。

### HASH_AGG() {#hash-agg}

`HASH_AGG()`ヒントは、指定されたクエリ ブロックのすべての集計関数でハッシュ集計アルゴリズムを使用するようオプティマイザに指示します。このアルゴリズムを使用すると、クエリを複数のスレッドで同時に実行できます。これにより、処理速度は向上しますが、より多くのメモリを消費します。例えば：

{{< copyable "" >}}

```sql
select /*+ HASH_AGG() */ count(*) from t1, t2 where t1.a > 10 group by t1.id;
```

### STREAM_AGG() {#stream-agg}

`STREAM_AGG()`ヒントは、指定されたクエリ ブロックのすべての集計関数でストリーム集計アルゴリズムを使用するようオプティマイザに指示します。一般に、このアルゴリズムはメモリの消費量は少なくなりますが、処理時間は長くなります。データ ボリュームが非常に大きい場合、またはシステム メモリが不足している場合は、このヒントを使用することをお勧めします。例えば：

{{< copyable "" >}}

```sql
select /*+ STREAM_AGG() */ count(*) from t1, t2 where t1.a > 10 group by t1.id;
```

### USE_INDEX(t1_name, idx1_name [, idx2_name ...]) {#use-index-t1-name-idx1-name-idx2-name}

`USE_INDEX(t1_name, idx1_name [, idx2_name ...])`ヒントは、指定された`t1_name`テーブルに対して指定されたインデックスのみを使用するようにオプティマイザに指示します。たとえば、次のヒントを適用すると、 `select * from t t1 use index(idx1, idx2);`ステートメントを実行した場合と同じ効果があります。

{{< copyable "" >}}

```sql
SELECT /*+ USE_INDEX(t1, idx1, idx2) */ * FROM t1;
```

> **ノート：**
>
> このヒントでテーブル名のみを指定し、インデックス名を指定しない場合、実行ではインデックスは考慮されず、テーブル全体がスキャンされます。

### FORCE_INDEX(t1_name, idx1_name [, idx2_name ...]) {#force-index-t1-name-idx1-name-idx2-name}

`FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])`ヒントは、指定されたインデックスのみを使用するようにオプティマイザに指示します。

`FORCE_INDEX(t1_name, idx1_name [, idx2_name ...])`の使い方と効果は`USE_INDEX(t1_name, idx1_name [, idx2_name ...])`の使い方と効果と同じです。

次の 4 つのクエリは同じ効果があります。

{{< copyable "" >}}

```sql
SELECT /*+ USE_INDEX(t, idx1) */ * FROM t;
SELECT /*+ FORCE_INDEX(t, idx1) */ * FROM t;
SELECT * FROM t use index(idx1);
SELECT * FROM t force index(idx1);
```

### IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...]) {#ignore-index-t1-name-idx1-name-idx2-name}

`IGNORE_INDEX(t1_name, idx1_name [, idx2_name ...])`ヒントは、指定された`t1_name`テーブルの指定されたインデックスを無視するようにオプティマイザに指示します。たとえば、次のヒントを適用すると、 `select * from t t1 ignore index(idx1, idx2);`ステートメントを実行した場合と同じ効果があります。

{{< copyable "" >}}

```sql
select /*+ IGNORE_INDEX(t1, idx1, idx2) */ * from t t1;
```

### AGG_TO_COP() {#agg-to-cop}

`AGG_TO_COP()`ヒントは、指定されたクエリ ブロックの集計操作をコプロセッサにプッシュ ダウンするようオプティマイザに指示します。オプティマイザがプッシュダウンに適した集計関数をプッシュダウンしない場合は、このヒントを使用することをお勧めします。例えば：

{{< copyable "" >}}

```sql
select /*+ AGG_TO_COP() */ sum(t1.a) from t t1;
```

### LIMIT_TO_COP() {#limit-to-cop}

`LIMIT_TO_COP()`ヒントは、指定されたクエリ ブロック内の`Limit`および`TopN`演算子をコプロセッサにプッシュ ダウンするようオプティマイザに指示します。オプティマイザーがそのような操作を実行しない場合は、このヒントを使用することをお勧めします。例えば：

{{< copyable "" >}}

```sql
SELECT /*+ LIMIT_TO_COP() */ * FROM t WHERE a = 1 AND b > 10 ORDER BY c LIMIT 1;
```

### READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]]) {#read-from-storage-tiflash-t1-name-tl-name-tikv-t2-name-tl-name}

`READ_FROM_STORAGE(TIFLASH[t1_name [, tl_name ...]], TIKV[t2_name [, tl_name ...]])`ヒントは、特定のストレージ エンジンから特定のテーブルを読み取るようにオプティマイザに指示します。現在、このヒントは`TIKV`と`TIFLASH`の 2 つのストレージ エンジン パラメーターをサポートしています。テーブルにエイリアスがある場合は、エイリアスを`READ_FROM_STORAGE()`のパラメーターとして使用します。テーブルにエイリアスがない場合は、テーブルの元の名前をパラメーターとして使用します。例えば：

{{< copyable "" >}}

```sql
select /*+ READ_FROM_STORAGE(TIFLASH[t1], TIKV[t2]) */ t1.a from t t1, t t2 where t1.a = t2.a;
```

> **ノート：**
>
> オプティマイザで別のスキーマのテーブルを使用する場合は、スキーマ名を明示的に指定する必要があります。例えば：
>
> ```sql
> SELECT /*+ READ_FROM_STORAGE(TIFLASH[test1.t1,test2.t2]) */ t1.a FROM test1.t t1, test2.t t2 WHERE t1.a = t2.a;
> ```

### USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...]) {#use-index-merge-t1-name-idx1-name-idx2-name}

`USE_INDEX_MERGE(t1_name, idx1_name [, idx2_name ...])`ヒントは、インデックス マージ メソッドを使用して特定のテーブルにアクセスするようオプティマイザに指示します。指定されたインデックスのリストはオプションのパラメーターです。リストを明示的に指定すると、TiDB はリストからインデックスを選択してインデックス マージを構築します。インデックスのリストを指定しない場合、TiDB は利用可能なすべてのインデックスからインデックスを選択して、インデックス マージを構築します。例えば：

{{< copyable "" >}}

```sql
SELECT /*+ USE_INDEX_MERGE(t1, idx_a, idx_b, idx_c) */ * FROM t1 WHERE t1.a > 10 OR t1.b > 10;
```

同じテーブルに対して複数の`USE_INDEX_MERGE`ヒントが作成されると、オプティマイザは、これらのヒントで指定されたインデックス セットの和集合からインデックスを選択しようとします。

> **ノート：**
>
> `USE_INDEX_MERGE`のパラメーターは、列名ではなくインデックス名を参照します。主キーのインデックス名は`primary`です。

このヒントは、次のような厳密な条件で有効になります。

-   クエリが全テーブル スキャンに加えて単一インデックス スキャンを選択できる場合、オプティマイザはインデックス マージを選択しません。

### LEADING(t1_name [, tl_name ...]) {#leading-t1-name-tl-name}

`LEADING(t1_name [, tl_name ...])`ヒントは、実行計画を生成するときに、ヒントで指定されたテーブル名の順序に従って複数テーブルの結合の順序を決定することをオプティマイザに通知します。例えば：

{{< copyable "" >}}

```sql
SELECT /*+ LEADING(t1, t2) */ * FROM t1, t2, t3 WHERE t1.id = t2.id and t2.id = t3.id;
```

複数テーブルの結合を伴う上記のクエリでは、結合の順序は、 `LEADING()`ヒントで指定されたテーブル名の順序によって決定されます。オプティマイザーは、最初に`t1`と`t2`を結合し、次に結果を`t3`と結合します。このヒントは[`STRAIGHT_JOIN`](#straight_join)よりも一般的です。

`LEADING`ヒントは、次の状況では有効になりません。

-   複数の`LEADING`ヒントが指定されています。
-   `LEADING`ヒントで指定されたテーブル名が存在しません。
-   `LEADING`のヒントに重複したテーブル名が指定されています。
-   オプティマイザーは、 `LEADING`ヒントで指定された順序に従って結合操作を実行できません。
-   `straight_join()`ヒントは既に存在します。
-   クエリに外部結合が含まれています。
-   `MERGE_JOIN` 、 `INL_JOIN` 、 `INL_HASH_JOIN` 、および`HASH_JOIN`ヒントのいずれかが同時に使用されます。

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

## クエリ全体で有効なヒント {#hints-that-take-effect-in-the-whole-query}

このカテゴリのヒントは、**最初の**`SELECT` 、 `UPDATE` 、または`DELETE`キーワードの後ろにのみ続くことができます。これは、このクエリの実行時に指定されたシステム変数の値を変更することと同じです。ヒントの優先度は、既存のシステム変数の優先度よりも高くなります。

> **ノート：**
>
> このカテゴリのヒントには、オプションの隠し変数`@QB_NAME`もありますが、変数を指定した場合でも、ヒントはクエリ全体で有効になります。

### NO_INDEX_MERGE() {#no-index-merge}

`NO_INDEX_MERGE()`ヒントは、オプティマイザのインデックス マージ機能を無効にします。

たとえば、次のクエリはインデックス マージを使用しません。

{{< copyable "" >}}

```sql
select /*+ NO_INDEX_MERGE() */ * from t where t.a > 0 or t.b > 0;
```

このヒントに加えて、システム変数`tidb_enable_index_merge`を設定すると、この機能を有効にするかどうかも制御されます。

> **ノート：**
>
> -   `NO_INDEX_MERGE`は`USE_INDEX_MERGE`より優先度が高くなります。両方のヒントを使用する場合、 `USE_INDEX_MERGE`は有効になりません。
> -   サブクエリの場合、サブクエリの最も外側のレベルに配置された場合にのみ`NO_INDEX_MERGE`が有効になります。

### USE_TOJA(ブール値) {#use-toja-boolean-value}

`boolean_value`パラメータは`TRUE`または`FALSE`です。 `USE_TOJA(TRUE)`ヒントにより、オプティマイザーは`in`条件 (サブクエリを含む) を結合および集計操作に変換できます。比較すると、 `USE_TOJA(FALSE)`ヒントはこの機能を無効にします。

たとえば、次のクエリは、 `in (select t2.a from t2) subq`を対応する結合操作と集計操作に変換します。

{{< copyable "" >}}

```sql
select /*+ USE_TOJA(TRUE) */ t1.a, t1.b from t1 where t1.a in (select t2.a from t2) subq;
```

このヒントに加えて、システム変数`tidb_opt_insubq_to_join_and_agg`を設定すると、この機能を有効にするかどうかも制御されます。

### MAX_EXECUTION_TIME(N) {#max-execution-time-n}

`MAX_EXECUTION_TIME(N)`ヒントは、サーバーがステートメントを終了する前にステートメントの実行が許可される時間に制限`N` (ミリ秒単位のタイムアウト値) を設定します。次のヒントで、 `MAX_EXECUTION_TIME(1000)`はタイムアウトが 1000 ミリ秒 (つまり、1 秒) であることを意味します。

{{< copyable "" >}}

```sql
select /*+ MAX_EXECUTION_TIME(1000) */ * from t1 inner join t2 where t1.id = t2.id;
```

このヒントに加えて、 `global.max_execution_time`システム変数はステートメントの実行時間を制限することもできます。

### MEMORY_QUOTA(N) {#memory-quota-n}

`MEMORY_QUOTA(N)`ヒントは、ステートメントが使用できるメモリ量に制限`N` (MB または GB 単位のしきい値) を設定します。ステートメントのメモリ使用量がこの制限を超えると、TiDB はステートメントの制限を超えた動作に基づいてログ メッセージを生成するか、単に終了します。

次のヒントの`MEMORY_QUOTA(1024 MB)`は、メモリ使用量が 1024 MB に制限されていることを意味します。

{{< copyable "" >}}

```sql
select /*+ MEMORY_QUOTA(1024 MB) */ * from t;
```

このヒントに加えて、 [`tidb_mem_quota_query`](/system-variables.md#tidb_mem_quota_query)システム変数は、ステートメントのメモリ使用量を制限することもできます。

### READ_CONSISTENT_REPLICA() {#read-consistent-replica}

`READ_CONSISTENT_REPLICA()`ヒントは、TiKV フォロワー ノードから一貫したデータを読み取る機能を有効にします。例えば：

{{< copyable "" >}}

```sql
select /*+ READ_CONSISTENT_REPLICA() */ * from t;
```

このヒントに加えて、 `tidb_replica_read`環境変数を`'follower'`または`'leader'`に設定すると、この機能を有効にするかどうかも制御されます。

### IGNORE_PLAN_CACHE() {#ignore-plan-cache}

`IGNORE_PLAN_CACHE()`ヒントは、現在の`prepare`ステートメントを処理するときに Plan Cache を使用しないようにオプティマイザーに通知します。

このヒントは、 [準備計画キャッシュ](/sql-prepared-plan-cache.md)が有効になっている場合に、特定のタイプのクエリのプラン キャッシュを一時的に無効にするために使用されます。

次の例では、 `prepare`ステートメントの実行時に Plan Cache が強制的に無効にされます。

{{< copyable "" >}}

```sql
prepare stmt from 'select  /*+ IGNORE_PLAN_CACHE() */ * from t where t.id = ?';
```

### STRAIGHT_JOIN() {#straight-join}

`STRAIGHT_JOIN()`ヒントは、結合計画を生成するときに`FROM`句のテーブル名の順序でテーブルを結合することをオプティマイザに思い出させます。

{{< copyable "" >}}

```sql
SELECT /*+ STRAIGHT_JOIN() */ * FROM t t1, t t2 WHERE t1.a = t2.a;
```

> **ノート：**
>
> -   `STRAIGHT_JOIN`は`LEADING`よりも優先度が高くなります。両方のヒントを使用する場合、 `LEADING`は有効になりません。
> -   `STRAIGHT_JOIN`ヒントよりも一般的な`LEADING`ヒントを使用することをお勧めします。

### NTH_PLAN(N) {#nth-plan-n}

`NTH_PLAN(N)`のヒントは、オプティマイザが物理的な最適化中に見つかった`N`番目の物理的な計画を選択することを思い出させます。 `N`は正の整数でなければなりません。

指定された`N`が物理最適化の検索範囲を超えている場合、TiDB は警告を返し、このヒントを無視する戦略に基づいて最適な物理計画を選択します。

このヒントは、カスケード プランナーが有効になっている場合は有効になりません。

次の例では、オプティマイザーは、物理的な最適化中に見つかった 3 番目の物理的な計画を選択するように強制されます。

{{< copyable "" >}}

```sql
SELECT /*+ NTH_PLAN(3) */ count(*) from t where a > 5;
```

> **ノート：**
>
> `NTH_PLAN(N)`は主にテスト用であり、以降のバージョンでは互換性が保証されていません。このヒント**は注意して**使用してください。
