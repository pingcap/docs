---
title: Create a Table
summary: Learn the definitions, rules, and guidelines in table creation.
---

# テーブルを作成する {#create-a-table}

このドキュメントでは、SQL ステートメントを使用してテーブルを作成する方法と、関連するベスト プラクティスを紹介します。ベスト プラクティスを説明するために、TiDB ベースのアプリケーション[書店](/develop/dev-guide-bookshop-schema-design.md)の例を示します。

## 始める前に {#before-you-start}

このドキュメントを読む前に、次のタスクが完了していることを確認してください。

-   [TiDB Cloud(Serverless Tier) で TiDBクラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md) .
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md)を読んでください。
-   [データベースを作成する](/develop/dev-guide-create-database.md) .

## テーブルとは {#what-is-a-table}

[テーブル](/develop/dev-guide-schema-design-overview.md#table) [データベース](/develop/dev-guide-schema-design-overview.md#database)に従属する TiDB クラスター内の論理オブジェクトです。 SQL ステートメントから送信されたデータを格納するために使用されます。テーブルは、行と列の形式でデータ レコードを保存します。テーブルには少なくとも 1 つの列があります。 `n`列を定義した場合、データの各行には`n`の列とまったく同じフィールドがあります。

## テーブルに名前を付ける {#name-a-table}

テーブルを作成するための最初のステップは、テーブルに名前を付けることです。将来、自分自身や同僚に大きな苦痛を与えるような意味のない名前は使用しないでください。会社または組織のテーブル命名規則に従うことをお勧めします。

`CREATE TABLE`ステートメントは通常、次の形式を取ります。

```sql
CREATE TABLE {table_name} ( {elements} );
```

**パラメータの説明**

-   `{table_name}` : 作成するテーブルの名前。
-   `{elements}` : 列定義や主キー定義などのテーブル要素のコンマ区切りリスト。

`bookshop`データベースにユーザー情報を格納するためのテーブルを作成する必要があるとします。

列が 1 つも追加されていないため、次の SQL ステートメントはまだ実行できないことに注意してください。

```sql
CREATE TABLE `bookshop`.`users` (
);
```

## 列を定義する {#define-columns}

**列は**テーブルに従属しています。各テーブルには少なくとも 1 つの列があります。列は、各行の値を 1 つのデータ型の小さなセルに分割することで、テーブルに構造を提供します。

カラムの定義は通常、次の形式を取ります。

```
{column_name} {data_type} {column_qualification}
```

**パラメータの説明**

-   `{column_name}` : 列名。
-   `{data_type}` : 列[データ・タイプ](/data-type-overview.md) 。
-   `{column_qualification}` :**列レベルの制約**や[生成された列 (実験的機能)](/generated-columns.md)句などのカラムの修飾。

一意の識別子`id` 、 `balance` 、および`nickname`など、いくつかの列を`users`テーブルに追加できます。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint,
  `nickname` varchar(100),
  `balance` decimal(15,2)
);
```

上記のステートメントでは、フィールドは名前`id`とタイプ[bigint](/data-type-numeric.md#bigint-type)で定義されています。これは、一意のユーザー識別子を表すために使用されます。これは、すべてのユーザー ID が`bigint`型である必要があることを意味します。

次に、 `nickname`という名前のフィールドが定義されます。これは[varchar](/data-type-string.md#varchar-type)型で、長さ制限は 100 文字です。これは、 `nicknames`のユーザーが`varchar`タイプを使用し、100 文字以内であることを意味します。

最後に、**精度**が`15`で<strong>位取り</strong>が`2`の[小数](/data-type-numeric.md#decimal-type)型である`balance`という名前のフィールドが追加されます。<strong>精度は</strong>フィールド内の合計桁数を表し、<strong>スケールは</strong>小数点以下の桁数を表します。たとえば、 `decimal(5,2)` 、精度が`5`でスケールが`2`で、範囲が`-999.99`から`999.99`であることを意味します。 `decimal(6,1)`精度`6`とスケール`1`を意味し、範囲は`-99999.9`から`99999.9`です。 <strong>decimal</strong>は[固定小数点型](/data-type-numeric.md#fixed-point-types)で、数値を正確に格納するために使用できます。正確な数値が必要なシナリオ (ユーザー プロパティ関連など) では、必ず<strong>decimal</strong>型を使用してください。

TiDB は、 [整数型](/data-type-numeric.md#integer-types) 、 [浮動小数点型](/data-type-numeric.md#floating-point-types) 、 [固定小数点型](/data-type-numeric.md#fixed-point-types) 、 [日付と時刻の種類](/data-type-date-and-time.md) 、および[列挙型](/data-type-string.md#enum-type)を含む、他の多くの列データ型をサポートしています。サポートされている列[データ型](/data-type-overview.md)を参照して、データベースに保存するデータに一致する**データ型を**使用できます。

もう少し複雑にするために、 `bookshop`のデータのコアとなる`books`テーブルを定義できます。 `books`テーブルには、書籍の ID、タイトル、種類 (雑誌、小説、人生、芸術など)、在庫、価格、出版日のフィールドが含まれています。

```sql
CREATE TABLE `bookshop`.`books` (
  `id` bigint NOT NULL,
  `title` varchar(100),
  `type` enum('Magazine', 'Novel', 'Life', 'Arts', 'Comics', 'Education & Reference', 'Humanities & Social Sciences', 'Science & Technology', 'Kids', 'Sports'),
  `published_at` datetime,
  `stock` int,
  `price` decimal(15,2)
);
```

このテーブルには、 `users`テーブルよりも多くのデータ型が含まれています。

-   [整数](/data-type-numeric.md#integer-types) : ディスクの使用量が多すぎたり、パフォーマンスへの影響 (型の範囲が大きすぎる) やデータのオーバーフロー (データ型の範囲が小さすぎる) を避けるために、適切なサイズの型を使用することをお勧めします。
-   [日付時刻](/data-type-date-and-time.md) : **datetime**型を使用して時刻値を格納できます。
-   [列挙](/data-type-string.md#enum-type) : 列挙型を使用して、限定された値の選択を格納できます。

## 主キーを選択 {#select-primary-key}

[主キー](/constraints.md#primary-key)は、テーブル内の行を一意に識別する値を持つテーブル内の列または列のセットです。

> **ノート：**
>
> TiDB の**主キー**のデフォルト定義は、 [InnoDB](https://mariadb.com/kb/en/innodb/) (MySQL の共通storageエンジン) とは異なります。
>
> -   **InnoDB**の場合:<strong>主キーは</strong>一意であり、null ではなく、<strong>インデックスがクラスター化されています</strong>。
>
> -   TiDB の場合:**主キーは**一意であり、null ではありません。ただし、主キーが<strong>クラスター化インデックス</strong>であるとは限りません。代わりに、別の一連のキーワード`CLUSTERED` `NONCLUSTERED`追加で<strong>主キーが</strong><strong>クラスター化インデックス</strong>かどうかを制御します。キーワードが指定されていない場合は、 [クラスター化インデックス](https://docs.pingcap.com/zh/tidb/stable/clustered-indexes)で説明されているように、システム変数`@@global.tidb_enable_clustered_index`によって制御されます。

**主キーは**`CREATE TABLE`ステートメントで定義されています。 [主キー制約](/constraints.md#primary-key) 、すべての制約された列に非 NULL 値のみが含まれている必要があります。

テーブルは、**主キー**なしで作成することも、整数以外の<strong>主キー</strong>を使用して作成することもできます。この場合、TiDB は<strong>暗黙の主キー</strong>として`_tidb_rowid`を作成します。暗黙的な主キー`_tidb_rowid` 、単調に増加する性質があるため、書き込みが集中するシナリオでは書き込みホットスポットが発生する可能性があります。したがって、アプリケーションが書き込み集中型の場合は、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)および[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)パラメーターを使用してデータをシャーディングすることを検討してください。ただし、これは読み取り増幅につながる可能性があるため、独自のトレードオフを行う必要があります。

テーブルの**主キー**が[整数型](/data-type-numeric.md#integer-types)で`AUTO_INCREMENT`が使用されている場合、ホットスポットは`SHARD_ROW_ID_BITS`を使用しても回避できません。ホットスポットを回避する必要があり、継続的な増分主キーが必要ない場合は、 `AUTO_INCREMENT`の代わりに[`AUTO_RANDOM`](/auto-random.md)使用して行 ID の連続性を排除できます。

<CustomContent platform="tidb">

ホットスポットの問題を処理する方法の詳細については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照してください。

</CustomContent>

[主キーを選択するためのガイドライン](#guidelines-to-follow-when-selecting-primary-key)に続いて、次の例は`AUTO_RANDOM`主キーが`users`テーブルでどのように定義されるかを示しています。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100),
  PRIMARY KEY (`id`)
);
```

## クラスター化されているかどうか {#clustered-or-not}

TiDB は v5.0 以降、 [クラスター化インデックス](/clustered-indexes.md)機能をサポートしています。この機能は、主キーを含むテーブルにデータを格納する方法を制御します。特定のクエリのパフォーマンスを向上させる方法でテーブルを編成する機能を TiDB に提供します。

このコンテキストでのクラスター化という用語は、データがどのように格納されるかの編成を指し、連携して動作するデータベース サーバーのグループではありません。一部のデータベース管理システムでは、クラスター化インデックスをインデックス構成テーブル (IOT) と呼んでいます。

現在、TiDB の***主キーを含む***テーブルは、次の 2 つのカテゴリに分類されます。

-   `NONCLUSTERED` : テーブルの主キーは非クラスター化インデックスです。非クラスター化インデックスを持つテーブルでは、行データのキーは、TiDB によって暗黙的に割り当てられた内部`_tidb_rowid`で構成されます。主キーは基本的に一意のインデックスであるため、非クラスター化インデックスを含むテーブルには、行を格納するために少なくとも 2 つのキーと値のペアが必要です。
    -   `_tidb_rowid` (キー) - 行データ (値)
    -   主キー データ (キー) - `_tidb_rowid` (値)
-   `CLUSTERED` : テーブルの主キーはクラスター化インデックスです。クラスタ化インデックスを持つテーブルでは、行データのキーは、ユーザーが指定した主キー データで構成されます。したがって、クラスター化されたインデックスを持つテーブルでは、行を格納するために必要なキーと値のペアは 1 つだけです。
    -   主キーデータ（キー） - 行データ（値）

[主キーを選択](#select-primary-key)で説明したように、**クラスター化インデックスは**キーワード`CLUSTERED`と`NONCLUSTERED`を使用して TiDB で制御されます。

> **ノート：**
>
> TiDB は、テーブルの`PRIMARY KEY`によるクラスタリングのみをサポートします。クラスター化インデックスを有効にすると、 *5*と<em>クラスター化インデックスという</em>用語が同じ意味で使用される`PRIMARY KEY`があります。 `PRIMARY KEY`は制約 (論理プロパティ) を参照し、クラスター化インデックスはデータの格納方法の物理的な実装を記述します。

[クラスタ化インデックスを選択するためのガイドライン](#guidelines-to-follow-when-selecting-clustered-index)に続いて、次の例では、 `books`と`users`の間の関連付けを持つテーブルを作成します。これは、 `book` x `users`の`ratings`を表します。この例では、テーブルを作成し、 `book_id`と`user_id`を使用して複合主キーを作成し、その**主キー**に<strong>クラスター化インデックス</strong>を作成します。

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime,
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

## 列の制約を追加する {#add-column-constraints}

[主キー制約](#select-primary-key)に加えて、TiDB は[ヌルではない](/constraints.md#not-null)制約、 [ユニークキー](/constraints.md#unique-key)制約、および`DEFAULT`などの他の**列制約**もサポートしています。完全な制約については、 [TiDB の制約](/constraints.md)ドキュメントを参照してください。

### デフォルト値を設定 {#set-default-value}

列にデフォルト値を設定するには、 `DEFAULT`制約を使用します。デフォルト値を使用すると、各列の値を指定せずにデータを挿入できます。

`DEFAULT`と[サポートされている SQL関数](/functions-and-operators/functions-and-operators-overview.md)を一緒に使用して、デフォルトの計算をアプリケーションレイヤーの外に移動し、アプリケーションレイヤーのリソースを節約できます。計算によって消費されたリソースは消えず、TiDB クラスターに移動されます。通常、デフォルトの時間でデータを挿入できます。以下は、 `ratings`テーブルにデフォルト値を設定する例です。

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

さらに、データの更新時にデフォルトで現在時刻も入力される場合は、次のステートメントを使用できます (ただし、 `ON UPDATE`後に入力できるのは[現在時刻関連のステートメント](https://pingcap.github.io/sqlgram/#NowSymOptionFraction)のみであり、 `DEFAULT`の後には[より多くのオプション](https://pingcap.github.io/sqlgram/#DefaultValueExpr)がサポートされています)。

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

### 値の重複を防ぐ {#prevent-duplicate-values}

列で値が重複しないようにする必要がある場合は、 `UNIQUE`制約を使用できます。

たとえば、ユーザーのニックネームが一意であることを確認するには、次のように`users`テーブルのテーブル作成 SQL ステートメントを書き直すことができます。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE,
  PRIMARY KEY (`id`)
);
```

同じ`nickname`を`users`テーブルに挿入しようとすると、エラーが返されます。

### null 値を防ぐ {#prevent-null-values}

列の null 値を防ぐ必要がある場合は、 `NOT NULL`制約を使用できます。

例として、ユーザーのニックネームを取り上げます。ニックネームが固有であるだけでなく、ヌルでもないことを確認するには、 `users`表を作成するための SQL ステートメントを次のように書き直すことができます。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE NOT NULL,
  PRIMARY KEY (`id`)
);
```

## HTAP 機能を使用する {#use-htap-capabilities}

<CustomContent platform="tidb">

> **ノート：**
>
> このガイドに記載されている手順は、テスト環境でのクイック スタート***専用***です。本番環境については、 [HTAP を調べる](/explore-htap.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **ノート：**
>
> このガイドに記載されている手順は、***クイック***スタート専用です。詳細については、 [TiFlashで HTAPクラスタを使用する](/tiflash/tiflash-overview.md)を参照してください。

</CustomContent>

`bookshop`アプリケーションを使用して`ratings`テーブルで OLAP 分析を実行するとします。たとえば、**書籍の評価が評価の時間と有意な相関関係があるかどうかを**クエリするために、ユーザーの書籍の評価が客観的かどうか。次に、 `ratings`テーブル全体の`score`と`rated_at`フィールドを照会する必要があります。この操作は、OLTP のみのデータベースではリソースを集中的に使用します。または、ETL またはその他のデータ同期ツールを使用して、分析のために OLTP データベースから専用の OLAP データベースにデータをエクスポートすることもできます。

このシナリオでは、OLTP と OLAP の両方のシナリオをサポートする**HTAP (Hybrid Transactional and Analytical Processing)**データベースである TiDB が、理想的なワンストップ データベース ソリューションです。

### 列ベースのデータを複製する {#replicate-column-based-data}

<CustomContent platform="tidb">

現在、TiDB は**TiFlash**と<strong>TiSpark の</strong>2 つのデータ分析エンジンをサポートしています。大規模なデータ シナリオ (100 T) では、 <strong>TiFlash MPP が</strong>HTAP の主要なソリューションとして推奨され、 <strong>TiSpark が</strong>補完的なソリューションとして推奨されます。

TiDB HTAP機能の詳細については、次のドキュメントを参照してください: [TiDB HTAPのクイック スタート ガイド](/quick-start-with-htap.md)および[HTAP を調べる](/explore-htap.md) 。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB HTAP機能の詳細については、 [TiDB CloudHTAP クイック スタート](/tidb-cloud/tidb-cloud-htap-quickstart.md)および[TiFlashで HTAPクラスタを使用する](/tiflash/tiflash-overview.md)を参照してください。

</CustomContent>

この例では、 `bookshop`データベースのデータ分析エンジンとして[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)が選択されています。

TiFlash は、展開後にデータを自動的に複製しません。したがって、レプリケートするテーブルを手動で指定する必要があります。

```sql
ALTER TABLE {table_name} SET TIFLASH REPLICA {count};
```

**パラメータの説明**

-   `{table_name}` : テーブル名。
-   `{count}` : レプリケートされたレプリカの数。 0 の場合、複製されたレプリカは削除されます。

その後、 **TiFlash は**テーブルを複製します。クエリが実行されると、TiDB はコストの最適化に基づいて、クエリに対して TiKV (行ベース) またはTiFlash (列ベース) を自動的に選択します。または、クエリで<strong>TiFlash</strong>レプリカを使用するかどうかを手動で指定することもできます。指定方法については、 [TiDB を使用してTiFlashレプリカを読み取る](/tiflash/use-tidb-to-read-tiflash.md)を参照してください。

### HTAP 機能の使用例 {#an-example-of-using-htap-capabilities}

`ratings`テーブルは、 TiFlashの`1`レプリカを開きます。

```sql
ALTER TABLE `bookshop`.`ratings` SET TIFLASH REPLICA 1;
```

> **ノート：**
>
> クラスターに**TiFlash**ノードが含まれていない場合、この SQL ステートメントはエラーを報告します: `1105 - the tiflash replica count: 1 should be less than the total tiflash server count: 0` 。 [TiDB Cloud(Serverless Tier) で TiDBクラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-serverless-tier-cluster)を使用して、 <strong>TiFlash</strong>を含むServerless Tierクラスターを作成できます。

次に、次のクエリを実行できます。

```sql
SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)ステートメントを実行して、このステートメントが**TiFlash**を使用しているかどうかを確認することもできます。

```sql
EXPLAIN ANALYZE SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

実行結果:

```sql
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
| id                          | estRows   | actRows | task         | access object | execution info                                                                                                                                                                                                                                                                                                                                                       | operator info                                                                                                                                  | memory   | disk |
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
| Projection_4                | 299821.99 | 24      | root         |               | time:60.8ms, loops:6, Concurrency:5                                                                                                                                                                                                                                                                                                                                  | hour(cast(bookshop.ratings.rated_at, time))->Column#6, Column#5                                                                                | 17.7 KB  | N/A  |
| └─HashAgg_5                 | 299821.99 | 24      | root         |               | time:60.7ms, loops:6, partial_worker:{wall_time:60.660079ms, concurrency:5, task_num:293, tot_wait:262.536669ms, tot_exec:40.171833ms, tot_time:302.827753ms, max:60.636886ms, p95:60.636886ms}, final_worker:{wall_time:60.701437ms, concurrency:5, task_num:25, tot_wait:303.114278ms, tot_exec:176.564µs, tot_time:303.297475ms, max:60.69326ms, p95:60.69326ms}  | group by:Column#10, funcs:avg(Column#8)->Column#5, funcs:firstrow(Column#9)->bookshop.ratings.rated_at                                         | 714.0 KB | N/A  |
|   └─Projection_15           | 300000.00 | 300000  | root         |               | time:58.5ms, loops:294, Concurrency:5                                                                                                                                                                                                                                                                                                                                | cast(bookshop.ratings.score, decimal(8,4) BINARY)->Column#8, bookshop.ratings.rated_at, hour(cast(bookshop.ratings.rated_at, time))->Column#10 | 366.2 KB | N/A  |
|     └─TableReader_10        | 300000.00 | 300000  | root         |               | time:43.5ms, loops:294, cop_task: {num: 1, max: 43.1ms, proc_keys: 0, rpc_num: 1, rpc_time: 43ms, copr_cache_hit_ratio: 0.00}                                                                                                                                                                                                                                        | data:TableFullScan_9                                                                                                                           | 4.58 MB  | N/A  |
|       └─TableFullScan_9     | 300000.00 | 300000  | cop[tiflash] | table:ratings | tiflash_task:{time:5.98ms, loops:8, threads:1}, tiflash_scan:{dtfile:{total_scanned_packs:45, total_skipped_packs:1, total_scanned_rows:368640, total_skipped_rows:8192, total_rs_index_load_time: 1ms, total_read_time: 1ms},total_create_snapshot_time:1ms}                                                                                                        | keep order:false                                                                                                                               | N/A      | N/A  |
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
```

フィールド`cop[tiflash]`が表示される場合、タスクが処理のために**TiFlash**に送信されることを意味します。

## <code>CREATE TABLE</code>ステートメントを実行する {#execute-the-code-create-table-code-statement}

上記のルールに従ってすべてのテーブルを作成すると、 [データベースの初期化](/develop/dev-guide-bookshop-schema-design.md#database-initialization-script-dbinitsql)のスクリプトは次のようになります。テーブル情報を詳しく見る必要がある場合は、 [表の説明](/develop/dev-guide-bookshop-schema-design.md#description-of-the-tables)を参照してください。

データベース初期化スクリプトに`init.sql`という名前を付けて保存するには、次のステートメントを実行してデータベースを初期化します。

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    < init.sql
```

`bookshop`データベースの下にあるすべてのテーブルを表示するには、 [`SHOW TABLES`](/sql-statements/sql-statement-show-tables.md#show-full-tables)ステートメントを使用します。

```sql
SHOW TABLES IN `bookshop`;
```

実行結果:

```
+--------------------+
| Tables_in_bookshop |
+--------------------+
| authors            |
| book_authors       |
| books              |
| orders             |
| ratings            |
| users              |
+--------------------+
```

## 表を作成する際に従うべきガイドライン {#guidelines-to-follow-when-creating-a-table}

このセクションでは、テーブルを作成する際に従う必要があるガイドラインを示します。

### テーブルに名前を付ける際に従うべきガイドライン {#guidelines-to-follow-when-naming-a-table}

-   **完全修飾された**テーブル名 (たとえば、 `CREATE TABLE {database_name}. {table_name}` ) を使用します。データベース名を指定しない場合、TiDB は<strong>SQL セッション</strong>で現在のデータベースを使用します。 SQL セッションでデータベースを指定するために`USE {databasename};`使用しない場合、TiDB はエラーを返します。
-   意味のあるテーブル名を使用してください。たとえば、ユーザー テーブルを作成する必要がある場合は、名前`user` 、 `t_user` 、 `users`を使用するか、会社または組織の命名規則に従うことができます。会社または組織に命名規則がない場合は、 [テーブルの命名規則](/develop/dev-guide-object-naming-guidelines.md#table-naming-convention)を参照できます。 `t1` 、 `table1`などのテーブル名は使用しないでください。
-   複数の単語はアンダースコアで区切ります。名前は 32 文字以内にすることをお勧めします。
-   異なるビジネス モジュールのテーブル用に別の`DATABASE`を作成し、それに応じてコメントを追加します。

### 列を定義する際に従うべきガイドライン {#guidelines-to-follow-when-defining-columns}

-   列でサポートされている[データ型](/data-type-overview.md)を確認し、データ型の制限に従ってデータを整理します。列に格納する予定のデータに適したタイプを選択します。
-   主キーを選択するための[従うべきガイドライン](#guidelines-to-follow-when-selecting-primary-key)を確認し、主キー列を使用するかどうかを決定します。
-   クラスター化インデックスを選択するための[従うべきガイドライン](#guidelines-to-follow-when-selecting-clustered-index)確認し、**クラスター化インデックスを**指定するかどうかを決定します。
-   [列の制約を追加する](#add-column-constraints)を確認し、列に制約を追加するかどうかを決定します。
-   意味のある列名を使用してください。会社または組織のテーブル命名規則に従うことをお勧めします。会社または組織に対応する命名規則がない場合は、 [列の命名規則](/develop/dev-guide-object-naming-guidelines.md#column-naming-convention)を参照してください。

### 主キーを選択する際に従うべきガイドライン {#guidelines-to-follow-when-selecting-primary-key}

-   テーブル内に**主キー**または<strong>一意のインデックス</strong>を定義します。
-   **主キー**として意味のある<strong>列</strong>を選択するようにしてください。
-   パフォーマンス上の理由から、幅の広いテーブルを格納しないようにしてください。テーブル フィールドの数が`60`を超え、1 行の合計データ サイズが`64K`を超えることはお勧めしません。データ長が多すぎるフィールドを別のテーブルに分割することをお勧めします。
-   複雑なデータ型を使用することはお勧めしません。
-   フィールドを結合するには、データ型が一貫していることを確認し、暗黙的な変換を避けてください。
-   単一の単調なデータ列に**主キー**を定義することは避けてください。単一のモノトニック データ列 (たとえば、 `AUTO_INCREMENT`属性を持つ列) を使用して<strong>主キー</strong>を定義すると、書き込みパフォーマンスに影響を与える可能性があります。可能であれば、主キーの連続属性と増分属性を破棄する`AUTO_INCREMENT`の代わりに`AUTO_RANDOM`使用してください。
-   書き込みが集中するシナリオで単一のモノトニック データ列にインデックスを作成する必要がある場合は、このモノトニック データ列を**主キー**として定義する代わりに、 `AUTO_RANDOM`使用してそのテーブルの<strong>主キーを</strong>作成するか、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)と[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)を使用できます。破片へ`_tidb_rowid` 。

### クラスター化インデックスを選択する際に従うべきガイドライン {#guidelines-to-follow-when-selecting-clustered-index}

-   **クラスター化インデックス**を作成するには、 [主キーを選択するためのガイドライン](#guidelines-to-follow-when-selecting-primary-key)に従ってください。

-   クラスター化されていないインデックスを含むテーブルと比較して、クラスター化されたインデックスを含むテーブルは、次のシナリオでより優れたパフォーマンスとスループットの利点を提供します。
    -   データが挿入されると、クラスター化インデックスは、ネットワークからのインデックス データの 1 回の書き込みを減らします。
    -   同等の条件を持つクエリに主キーのみが含まれる場合、クラスター化インデックスは、ネットワークからのインデックス データの 1 回の読み取りを減らします。
    -   範囲条件を含むクエリに主キーのみが含まれる場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。
    -   同等または範囲条件を含むクエリに主キー プレフィックスのみが含まれる場合、クラスター化インデックスは、ネットワークからのインデックス データの複数回の読み取りを減らします。

-   一方、クラスター化インデックスを含むテーブルには、次の問題がある場合があります。
    -   近い値を持つ多数の主キーを挿入すると、書き込みホットスポットの問題が発生する可能性があります。 [主キーを選択する際に従うべきガイドライン](#guidelines-to-follow-when-selecting-primary-key)に従ってください。
    -   主キーのデータ型が 64 ビットより大きい場合、特に複数のセカンダリ インデックスがある場合、テーブル データはより多くのstorage領域を占有します。

-   [クラスタ化インデックスを使用するかどうかのデフォルトの動作](/clustered-indexes.md#create-a-table-with-clustered-indexes)を制御するには、システム変数`@@global.tidb_enable_clustered_index`と構成`alter-primary-key`を使用する代わりに、クラスター化インデックスを使用するかどうかを明示的に指定できます。

### <code>CREATE TABLE</code>ステートメントを実行する際に従うべきガイドライン {#guidelines-to-follow-when-executing-the-code-create-table-code-statement}

-   クライアント側のDriverまたは ORM を使用してデータベース スキーマの変更を実行することはお勧めしません。 [MySQL クライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)使用するか、GUI クライアントを使用してデータベース スキーマの変更を実行することをお勧めします。このドキュメントでは、 **MySQL クライアントを**使用して SQL ファイルを渡し、ほとんどのシナリオでデータベース スキーマの変更を実行します。
-   SQL 開発に従ってください[テーブルの作成と削除の仕様](/develop/dev-guide-sql-development-specification.md#create-and-delete-tables) 。 build 文と delete 文をビジネス アプリケーション内にラップして、判断ロジックを追加することをお勧めします。

## もう一歩 {#one-more-step}

このドキュメントで作成されたすべてのテーブルにセカンダリ インデックスが含まれているわけではないことに注意してください。副次索引を追加するためのガイドについては、 [セカンダリ インデックスの作成](/develop/dev-guide-create-secondary-indexes.md)を参照してください。
