---
title: Create a Table
summary: Learn the definitions, rules, and guidelines in table creation.
---

# テーブルを作成する {#create-a-table}

このドキュメントでは、SQL ステートメントを使用してテーブルを作成する方法と、関連するベスト プラクティスを紹介します。 TiDB ベースの[書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションの例）は、ベスト プラクティスを説明するために提供されています。

## 始める前に {#before-you-start}

このドキュメントを読む前に、次のタスクが完了していることを確認してください。

-   [TiDB サーバーレスクラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md) 。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md)を読みます。
-   [データベースを作成する](/develop/dev-guide-create-database.md) 。

## テーブルとは {#what-is-a-table}

[テーブル](/develop/dev-guide-schema-design-overview.md#table) [データベース](/develop/dev-guide-schema-design-overview.md#database)に従属する TiDB クラスター内の論理オブジェクトです。 SQL ステートメントから送信されたデータを保存するために使用されます。テーブルはデータ レコードを行と列の形式で保存します。テーブルには少なくとも 1 つの列があります。 `n`列を定義した場合、データの各行には`n`の列とまったく同じフィールドが含まれます。

## テーブルに名前を付けます {#name-a-table}

テーブルを作成する最初のステップは、テーブルに名前を付けることです。将来自分自身や同僚に多大な苦痛を与えるような意味のない名前は使用しないでください。会社または組織のテーブル命名規則に従うことをお勧めします。

`CREATE TABLE`ステートメントは通常、次の形式を取ります。

```sql
CREATE TABLE {table_name} ( {elements} );
```

**パラメータの説明**

-   `{table_name}` : 作成するテーブルの名前。
-   `{elements}` : 列定義や主キー定義などのテーブル要素のカンマ区切りリスト。

ユーザー情報をデータベース`bookshop`に保存するテーブルを作成する必要があるとします。

列が 1 つも追加されていないため、次の SQL ステートメントはまだ実行できないことに注意してください。

```sql
CREATE TABLE `bookshop`.`users` (
);
```

## 列の定義 {#define-columns}

**列は**テーブルに従属します。各テーブルには少なくとも 1 つの列があります。列は、各行の値を単一のデータ型の小さなセルに分割することにより、テーブルに構造を提供します。

カラム定義は通常、次の形式を取ります。

    {column_name} {data_type} {column_qualification}

**パラメータの説明**

-   `{column_name}` : 列名。
-   `{data_type}` : 列[データ・タイプ](/data-type-overview.md) 。
-   `{column_qualification}` :**列レベルの制約**や[生成された列](/generated-columns.md)句などのカラム修飾。

一意の識別子`id` 、 `balance` 、 `nickname`などのいくつかの列を`users`テーブルに追加できます。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint,
  `nickname` varchar(100),
  `balance` decimal(15,2)
);
```

上記のステートメントでは、フィールドは名前`id`とタイプ[ビギント](/data-type-numeric.md#bigint-type)で定義されています。これは、一意のユーザー識別子を表すために使用されます。これは、すべてのユーザー識別子が`bigint`タイプである必要があることを意味します。

次に、 `nickname`という名前のフィールドが定義されます。これはタイプ[可変長文字](/data-type-string.md#varchar-type)で、長さの制限は 100 文字です。これは、ユーザーのうち`nicknames`人が`varchar`タイプを使用しており、文字数が 100 文字以下であることを意味します。

最後に、 `balance`という名前のフィールドが追加されます。これは[10進数](/data-type-numeric.md#decimal-type)タイプで、**精度**`15`および**スケール**`2`です。**精度は**フィールド内の合計桁数を表し、**位取りは**小数点以下の桁数を表します。たとえば、 `decimal(5,2)` 、精度`5`とスケール`2`を意味し、範囲は`-999.99`から`999.99`です。 `decimal(6,1)`精度`6`とスケール`1`を意味し、範囲は`-99999.9` ～ `99999.9`です。 **10 進数**は[固定小数点型](/data-type-numeric.md#fixed-point-types)で、数値を正確に格納するために使用できます。正確な数値が必要なシナリオ (ユーザー プロパティ関連など) では、必ず**10 進数**タイプを使用してください。

TiDB は、 [整数型](/data-type-numeric.md#integer-types) 、 [浮動小数点型](/data-type-numeric.md#floating-point-types) 、 [固定小数点型](/data-type-numeric.md#fixed-point-types) 、 [日付と時刻のタイプ](/data-type-date-and-time.md) 、 [列挙型](/data-type-string.md#enum-type)など、他の多くの列データ型をサポートします。サポートされている列[データ型](/data-type-overview.md)を参照して、データベースに保存するデータに一致する**データ型を**使用できます。

もう少し複雑にするために、 `bookshop`のデータの中核となる`books`テーブルを定義できます。テーブル`books`には、本の ID、タイトル、種類 (雑誌、小説、人生、芸術など)、在庫、価格、発行日のフィールドが含まれています。

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
-   [日付時刻](/data-type-date-and-time.md) : **datetime**型を使用して時刻値を保存できます。
-   [列挙型](/data-type-string.md#enum-type) : enum 型は、限られた値の選択を保存するために使用できます。

## 主キーを選択 {#select-primary-key}

[主キー](/constraints.md#primary-key)は、値がテーブル内の行を一意に識別するテーブル内の列または列のセットです。

> **注記：**
>
> TiDB の**主キー**のデフォルト定義は、 [InnoDB](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html) (MySQL の共通storageエンジン) とは異なります。
>
> -   **InnoDB**の場合:**主キー**は一意であり、null ではなく、**インデックスはクラスター化されています**。
>
> -   TiDB では:**主キー**は一意であり、null ではありません。ただし、主キーが**クラスター化インデックス**であるとは保証されません。代わりに、別のキーワード セット`CLUSTERED` `NONCLUSTERED` 、**主キーが****クラスタード インデックス**であるかどうかをさらに制御します。キーワードが指定されていない場合は、 [クラスター化インデックス](https://docs.pingcap.com/zh/tidb/stable/clustered-indexes)で説明したように、システム変数`@@global.tidb_enable_clustered_index`によって制御されます。

**主キーは**`CREATE TABLE`ステートメントで定義されます。 [主キー制約](/constraints.md#primary-key)すべての制約された列に NULL 以外の値のみが含まれる必要があります。

テーブルは、**主キー**なしで、または非整数の**主キー**を使用して作成できます。この場合、TiDB は**暗黙的な主キー**として`_tidb_rowid`を作成します。暗黙的な主キー`_tidb_rowid`は単調増加する性質があるため、書き込みが集中するシナリオでは書き込みホットスポットが発生する可能性があります。したがって、アプリケーションが書き込み集中型である場合は、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)および[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)パラメータを使用してデータをシャーディングすることを検討してください。ただし、これにより読み取り増幅が発生する可能性があるため、独自のトレードオフを行う必要があります。

テーブルの**主キー**が[整数型](/data-type-numeric.md#integer-types)で`AUTO_INCREMENT`が使用されている場合、 `SHARD_ROW_ID_BITS`を使用してもホットスポットを回避できません。ホットスポットを回避する必要があり、連続増分主キーが必要ない場合は、 `AUTO_INCREMENT`の代わりに[`AUTO_RANDOM`](/auto-random.md)使用して行 ID の連続性を排除できます。

<CustomContent platform="tidb">

ホットスポットの問題の処理方法の詳細については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照してください。

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

TiDB は v5.0 以降[クラスター化インデックス](/clustered-indexes.md)機能をサポートしています。この機能は、主キーを含むテーブルにデータを格納する方法を制御します。これにより、特定のクエリのパフォーマンスを向上できる方法でテーブルを編成する機能が TiDB に提供されます。

この文脈での「クラスタ化」という用語は、データの保存方法の構成を指しており、連携して動作するデータベース サーバーのグループを指すものではありません。一部のデータベース管理システムでは、クラスター化インデックスをインデックス構成テーブル (IOT) と呼びます。

現在、TiDB の***主キーを含む***テーブルは次の 2 つのカテゴリに分類されています。

-   `NONCLUSTERED` : テーブルの主キーは非クラスター化インデックスです。非クラスター化インデックスを備えたテーブルでは、行データのキーは TiDB によって暗黙的に割り当てられた内部`_tidb_rowid`で構成されます。主キーは本質的に一意のインデックスであるため、非クラスター化インデックスを持つテーブルでは、行を格納するために少なくとも 2 つのキーと値のペアが必要です。
    -   `_tidb_rowid` (キー) - 行データ (値)
    -   主キーデータ（キー） - `_tidb_rowid` （値）
-   `CLUSTERED` : テーブルの主キーはクラスター化インデックスです。クラスター化インデックスを備えたテーブルでは、行データのキーはユーザーが指定した主キー データで構成されます。したがって、クラスター化インデックスを備えたテーブルでは、行を格納するために次のキーと値のペアが 1 つだけ必要になります。
    -   主キーデータ(key) - 行データ(value)

[主キーを選択](#select-primary-key)で説明したように、TiDB では**クラスター化インデックスは**キーワード`CLUSTERED`と`NONCLUSTERED`を使用して制御されます。

> **注記：**
>
> TiDB は、テーブルの`PRIMARY KEY`によるクラスタリングのみをサポートします。クラスター化インデックスが有効になっている場合、 *5*と*クラスター化インデックス*`PRIMARY KEY`用語は同じ意味で使用される場合があります。 `PRIMARY KEY`は制約 (論理プロパティ) を指し、クラスター化インデックスはデータの格納方法の物理的な実装を示します。

次の例では、 [クラスター化インデックスを選択するためのガイドライン](#guidelines-to-follow-when-selecting-clustered-index)に続いて、 `book` x `users`の`ratings`を表す`books`と`users`を関連付けたテーブルを作成します。この例では、テーブルを作成し、 `book_id`と`user_id`を使用して複合主キーを構築し、その**主キー**に**クラスター化インデックス**を作成します。

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime,
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

## 列制約を追加する {#add-column-constraints}

[主キー制約](#select-primary-key)に加えて、TiDB は[NULLではありません](/constraints.md#not-null)制約、 [固有のキー](/constraints.md#unique-key)制約、 `DEFAULT`などの他の**列制約**もサポートします。完全な制約については、ドキュメント[TiDB の制約](/constraints.md)を参照してください。

### デフォルト値を設定する {#set-default-value}

列にデフォルト値を設定するには、 `DEFAULT`制約を使用します。デフォルト値を使用すると、各列の値を指定せずにデータを挿入できます。

`DEFAULT` [サポートされている SQL関数](/functions-and-operators/functions-and-operators-overview.md)と組み合わせて使用​​すると、デフォルトの計算をアプリケーションレイヤーの外に移動できるため、アプリケーションレイヤーのリソースが節約されます。計算によって消費されたリソースは消失せず、TiDB クラスターに移動されます。通常、デフォルトの時刻でデータを挿入できます。以下は、 `ratings`テーブルにデフォルト値を設定する例です。

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

さらに、データの更新時に現在時刻もデフォルトで入力される場合は、次のステートメントを使用できます (ただし、 `ON UPDATE`後には[現在時刻に関連するステートメント](https://pingcap.github.io/sqlgram/#NowSymOptionFraction)のみを入力でき、 `DEFAULT`後には[より多くのオプション](https://pingcap.github.io/sqlgram/#DefaultValueExpr)がサポートされます)。

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

列内の値の重複を防ぐ必要がある場合は、 `UNIQUE`制約を使用できます。

たとえば、ユーザーのニックネームが一意であることを確認するには、 `users`テーブルのテーブル作成 SQL ステートメントを次のように書き換えます。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE,
  PRIMARY KEY (`id`)
);
```

`users`テーブルに同じ`nickname`挿入しようとすると、エラーが返されます。

### NULL値を防ぐ {#prevent-null-values}

列に NULL 値が含まれないようにする必要がある場合は、 `NOT NULL`制約を使用できます。

ユーザーのニックネームを例に挙げます。ニックネームが一意であるだけでなく、NULL でないことを確認するには、 `users`テーブルを作成する SQL ステートメントを次のように書き換えます。

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

> **注記：**
>
> このガイドに記載されている手順は、テスト環境でのクイック スタート***のみ***を目的としています。本番環境については、 [HTAP を探索する](/explore-htap.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このガイドに記載されている手順は、クイックスタート***のみ***を目的としています。詳細な手順については、 [TiFlashで HTAPクラスタを使用する](/tiflash/tiflash-overview.md)を参照してください。

</CustomContent>

たとえば**、本の評価が評価の時間と有意な相関関係があるかどうかを**クエリするために、 `bookshop`アプリケーションを使用して`ratings`テーブルに対して OLAP 分析を実行するとします。つまり、本のユーザーの評価が評価されたかどうかを分析します。客観的かどうか。次に、 `ratings`テーブル全体の`score`と`rated_at`フィールドをクエリする必要があります。この操作は、OLTP 専用データベースの場合、リソースを大量に消費します。または、ETL またはその他のデータ同期ツールを使用して、分析のために OLTP データベースから専用の OLAP データベースにデータをエクスポートすることもできます。

このシナリオでは、OLTP シナリオと OLAP シナリオの両方をサポートする**HTAP (ハイブリッド トランザクションおよび分析処理)**データベースである TiDB が、理想的なワンストップ データベース ソリューションです。

### 列ベースのデータをレプリケートする {#replicate-column-based-data}

<CustomContent platform="tidb">

現在、TiDB は、 **TiFlash**と**TiSpark という**2 つのデータ分析エンジンをサポートしています。大規模データ シナリオ (100 T) の場合、 **TiFlash MPP が**HTAP の主要ソリューションとして推奨され、 **TiSpark が**補完ソリューションとして推奨されます。

TiDB HTAP機能の詳細については、ドキュメント[TiDB HTAPのクイック スタート ガイド](/quick-start-with-htap.md)および[HTAP を探索する](/explore-htap.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB HTAP機能の詳細については、 [TiDB CloudHTAP クイック スタート](/tidb-cloud/tidb-cloud-htap-quickstart.md)および[TiFlashで HTAPクラスタを使用する](/tiflash/tiflash-overview.md)を参照してください。

</CustomContent>

この例では、データベース`bookshop`データ分析エンジンとして[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)が選択されています。

TiFlash は、展開後にデータを自動的に複製しません。したがって、レプリケートするテーブルを手動で指定する必要があります。

```sql
ALTER TABLE {table_name} SET TIFLASH REPLICA {count};
```

**パラメータの説明**

-   `{table_name}` : テーブル名。
-   `{count}` : 複製されたレプリカの数。 0 の場合、複製されたレプリカは削除されます。

**TiFlash は**テーブルを複製します。クエリが実行されると、TiDB はコストの最適化に基づいてクエリに対して TiKV (行ベース) またはTiFlash (列ベース) を自動的に選択します。あるいは、クエリで**TiFlash**レプリカを使用するかどうかを手動で指定できます。指定方法については[TiDB を使用してTiFlashレプリカを読み取る](/tiflash/use-tidb-to-read-tiflash.md)を参照してください。

### HTAP 機能の使用例 {#an-example-of-using-htap-capabilities}

`ratings`テーブルはTiFlashの`1`レプリカを開きます。

```sql
ALTER TABLE `bookshop`.`ratings` SET TIFLASH REPLICA 1;
```

> **注記：**
>
> クラスターに**TiFlash**ノードが含まれていない場合、この SQL ステートメントはエラー`1105 - the tiflash replica count: 1 should be less than the total tiflash server count: 0`を報告します。 [TiDB サーバーレスクラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-serverless-cluster)を使用すると、 **TiFlash**を含む TiDB サーバーレス クラスターを作成できます。

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

フィールド`cop[tiflash]`が表示される場合は、タスクが処理のために**TiFlash**に送信されることを意味します。

## <code>CREATE TABLE</code>ステートメントを実行します {#execute-the-code-create-table-code-statement}

上記のルールに従ってすべてのテーブルを作成した後、 [データベースの初期化](/develop/dev-guide-bookshop-schema-design.md#database-initialization-script-dbinitsql)のスクリプトは次のようになります。テーブル情報を詳しく見たい場合は[テーブルの説明](/develop/dev-guide-bookshop-schema-design.md#description-of-the-tables)を参照してください。

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

## テーブルを作成するときに従うべきガイドライン {#guidelines-to-follow-when-creating-a-table}

このセクションでは、テーブルを作成するときに従う必要があるガイドラインを示します。

### テーブルに名前を付けるときに従うべきガイドライン {#guidelines-to-follow-when-naming-a-table}

-   **完全修飾**テーブル名 (たとえば、 `CREATE TABLE {database_name}. {table_name}` ) を使用します。データベース名を指定しない場合、TiDB は**SQL セッション**で現在のデータベースを使用します。 SQL セッションでデータベースを指定するために`USE {databasename};`使用しない場合、TiDB はエラーを返します。
-   意味のあるテーブル名を使用してください。たとえば、ユーザー テーブルを作成する必要がある場合は、 `user` 、 `t_user` 、 `users`という名前を使用するか、会社または組織の命名規則に従うことができます。会社や組織に命名規則がない場合は、 [テーブルの命名規則](/develop/dev-guide-object-naming-guidelines.md#table-naming-convention)を参照してください。 `t1` 、 `table1`などのテーブル名は使用しないでください。
-   複数の単語はアンダースコアで区切られ、名前は 32 文字以下にすることをお勧めします。
-   さまざまなビジネス モジュールのテーブルに対して個別の`DATABASE`を作成し、それに応じてコメントを追加します。

### 列を定義するときに従うべきガイドライン {#guidelines-to-follow-when-defining-columns}

-   列でサポートされる[データ型](/data-type-overview.md)確認し、データ型の制限に従ってデータを整理します。列に保存する予定のデータに適切なタイプを選択します。
-   主キー選択の[従うべきガイドライン](#guidelines-to-follow-when-selecting-primary-key)にチェックを入れ、主キー列を使用するかどうかを決定します。
-   クラスター化インデックスの選択の[従うべきガイドライン](#guidelines-to-follow-when-selecting-clustered-index)にチェックを入れ、**クラスター化インデックスを**指定するかどうかを決定します。
-   [列制約の追加](#add-column-constraints)にチェックを入れ、列に制約を追加するかどうかを決定します。
-   意味のある列名を使用してください。会社または組織のテーブル命名規則に従うことをお勧めします。会社または組織に対応する命名規則がない場合は、 [列の命名規則](/develop/dev-guide-object-naming-guidelines.md#column-naming-convention)を参照してください。

### 主キーを選択する際に従うべきガイドライン {#guidelines-to-follow-when-selecting-primary-key}

-   テーブル内に**主キー**または**一意のインデックス**を定義します。
-   意味のある**列を****主キー**として選択するようにしてください。
-   パフォーマンス上の理由から、非常に幅の広いテーブルを保存しないようにしてください。テーブル フィールドの数が`60`超え、単一行の合計データ サイズが`64K`を超えることはお勧めできません。データ長が長すぎるフィールドを別のテーブルに分割することをお勧めします。
-   複雑なデータ型を使用することはお勧めできません。
-   結合するフィールドについては、データ型が一貫していることを確認し、暗黙的な変換を避けてください。
-   単一の単調データ列に**主キー**を定義することは避けてください。単一の単調データ列 (たとえば、 `AUTO_INCREMENT`属性を持つ列) を使用して**主キー**を定義すると、書き込みパフォーマンスに影響を与える可能性があります。可能であれば、 `AUTO_INCREMENT`の代わりに`AUTO_RANDOM`使用してください。これにより、主キーの継続的および増分属性が破棄されます。
-   書き込みが集中するシナリオで単一の単調データ列にインデックスを作成する必要がある場合は、この単調データ列を**主キー**として定義する代わりに、 `AUTO_RANDOM`使用してそのテーブルの**主キー**を作成するか、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)と[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)を使用できます。シャードへ`_tidb_rowid` 。

### クラスター化インデックスを選択する際に従うべきガイドライン {#guidelines-to-follow-when-selecting-clustered-index}

-   [主キーを選択するためのガイドライン](#guidelines-to-follow-when-selecting-primary-key)に従って**クラスター化インデックス**を構築します。

-   非クラスター化インデックスを含むテーブルと比較して、クラスター化インデックスを含むテーブルは、次のシナリオでパフォーマンスとスループットの利点が大きくなります。
    -   データが挿入されると、クラスター化インデックスにより、ネットワークからのインデックス データの書き込みが 1 回削減されます。
    -   同等の条件を持つクエリに主キーのみが含まれる場合、クラスター化インデックスにより、ネットワークからのインデックス データの読み取りが 1 回削減されます。
    -   範囲条件を含むクエリに主キーのみが含まれる場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。
    -   同等条件または範囲条件を含むクエリに主キー プレフィックスのみが含まれる場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。

-   一方、クラスター化インデックスを含むテーブルには次の問題が発生する可能性があります。
    -   近い値を持つ主キーを多数挿入すると、書き込みホットスポットの問題が発生する可能性があります。 [主キーを選択するときに従うべきガイドライン](#guidelines-to-follow-when-selecting-primary-key)に従ってください。
    -   主キーのデータ型が 64 ビットより大きい場合、特に複数のセカンダリ インデックスがある場合、テーブル データはより多くのstorage領域を占有します。

-   [クラスター化インデックスを使用するかどうかのデフォルトの動作](/clustered-indexes.md#create-a-table-with-clustered-indexes)を制御するには、システム変数`@@global.tidb_enable_clustered_index`と構成`alter-primary-key`を使用する代わりに、クラスター化インデックスを使用するかどうかを明示的に指定できます。

### <code>CREATE TABLE</code>ステートメントを実行するときに従うべきガイドライン {#guidelines-to-follow-when-executing-the-code-create-table-code-statement}

-   データベース スキーマの変更を実行するためにクライアント側のDriverまたは ORM を使用することはお勧めできません。データベース スキーマの変更を実行するには、 [MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)使用するか、GUI クライアントを使用することをお勧めします。このドキュメントでは、 **MySQL クライアントを**使用して SQL ファイルを渡し、ほとんどのシナリオでデータベース スキーマの変更を実行します。
-   SQL 開発[テーブルの作成と削除の仕様](/develop/dev-guide-sql-development-specification.md#create-and-delete-tables)に従ってください。ビジネスアプリケーション内にbuild文とdelete文をラップして判定ロジックを追加することを推奨します。

## もう一歩 {#one-more-step}

このドキュメントで作成されたすべてのテーブルにはセカンダリ インデックスが含まれていないことに注意してください。セカンダリ インデックスを追加するガイドについては、 [セカンダリインデックスの作成](/develop/dev-guide-create-secondary-indexes.md)を参照してください。
