---
title: Create a Table
summary: テーブル作成における定義、ルール、ガイドラインを学びます。
---

# テーブルを作成する {#create-a-table}

このドキュメントでは、SQL ステートメントを使用してテーブルを作成する方法と、関連するベスト プラクティスを紹介します。ベスト プラクティスを説明するために、TiDB ベースの[書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションの例を示します。

## 始める前に {#before-you-start}

このドキュメントを読む前に、次のタスクが完了していることを確認してください。

-   [TiDB Cloudサーバーレスクラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md) 。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md)読んでください。
-   [データベースを作成する](/develop/dev-guide-create-database.md) 。

## テーブルとは何か {#what-is-a-table}

[テーブル](/develop/dev-guide-schema-design-overview.md#table)は、 [データベース](/develop/dev-guide-schema-design-overview.md#database)に従属する TiDB クラスター内の論理オブジェクトです。SQL ステートメントから送信されたデータを格納するために使用されます。テーブルは、行と列の形式でデータ レコードを保存します。テーブルには少なくとも 1 つの列があります。5 `n`の列を定義した場合、各データ行には`n`の列とまったく同じフィールドが含まれます。

## テーブルに名前を付ける {#name-a-table}

テーブルを作成する最初のステップは、テーブルに名前を付けることです。将来的に自分自身や同僚に大きな迷惑をかけることになるような、意味のない名前は使用しないでください。会社または組織のテーブル命名規則に従うことをお勧めします。

`CREATE TABLE`ステートメントは通常、次の形式になります。

```sql
CREATE TABLE {table_name} ( {elements} );
```

**パラメータの説明**

-   `{table_name}` : 作成するテーブルの名前。
-   `{elements}` : 列定義や主キー定義などのテーブル要素のコンマ区切りリスト。

`bookshop`データベースにユーザー情報を格納するためのテーブルを作成する必要があるとします。

まだ列が 1 つも追加されていないため、次の SQL ステートメントを実行できないことに注意してください。

```sql
CREATE TABLE `bookshop`.`users` (
);
```

## 列を定義する {#define-columns}

**列は**テーブルに従属します。各テーブルには少なくとも 1 つの列があります。列は、各行の値を単一のデータ型の小さなセルに分割することで、テーブルに構造を提供します。

カラム定義は通常、次の形式になります。

    {column_name} {data_type} {column_qualification}

**パラメータの説明**

-   `{column_name}` : 列名。
-   `{data_type}` : 列[データ型](/data-type-overview.md) 。
-   `{column_qualification}` :**列レベルの制約**や[生成された列](/generated-columns.md)句などのカラム修飾。

`users`テーブルに、一意の識別子`id` 、 `balance` 、 `nickname`などの列を追加できます。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint,
  `nickname` varchar(100),
  `balance` decimal(15,2)
);
```

上記のステートメントでは、フィールドは名前`id`とタイプ[ビッグイント](/data-type-numeric.md#bigint-type)で定義されています。これは、一意のユーザー識別子を表すために使用されます。つまり、すべてのユーザー識別子は`bigint`タイプである必要があります。

次に、長さ制限が 100 文字の[varchar](/data-type-string.md#varchar-type)型である`nickname`という名前のフィールドが定義されます。つまり、ユーザーのうち`nicknames`は`varchar`型を使用し、長さが 100 文字を超えないことを意味します。

最後に、 `balance`という名前のフィールドが追加されます。これは[小数点](/data-type-numeric.md#decimal-type)型で、**精度**は`15` 、**スケール**は`2`です。**精度は**フィールド内の合計桁数を表し、**スケールは**小数点以下の桁数を表します。たとえば、 `decimal(5,2)`精度が`5` 、スケールが`2`で、範囲が`-999.99`から`999.99`あることを意味します。 `decimal(6,1)`精度が`6` 、スケールが`1`で、範囲が`-99999.9`から`99999.9`あることを意味します。**小数点**は[固定小数点型](/data-type-numeric.md#fixed-point-types)で、数値を正確に格納するために使用できます。正確な数値が必要なシナリオ (ユーザー プロパティ関連など) では、必ず**小数点**型を使用してください。

TiDB は、 [整数型](/data-type-numeric.md#integer-types) 、 [浮動小数点型](/data-type-numeric.md#floating-point-types) 、 [固定小数点型](/data-type-numeric.md#fixed-point-types) 、 [日付と時刻の種類](/data-type-date-and-time.md) 、 [列挙型](/data-type-string.md#enum-type)など、他の多くの列データ型をサポートしています。サポートされている列[データ型](/data-type-overview.md)を参照して、データベースに保存するデータに一致する**データ型**を使用できます。

もう少し複雑にするには、 `bookshop`データの中核となる`books`テーブルを定義します。5 `books`のテーブルには、書籍の ID、タイトル、種類 (雑誌、小説、生活、芸術など)、在庫、価格、発行日などのフィールドが含まれます。

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

-   [整数](/data-type-numeric.md#integer-types) : ディスクの使用量が増えたり、パフォーマンスに影響したり (型の範囲が大きすぎる)、データ オーバーフロー (データ型の範囲が小さすぎる) したりしないように、適切なサイズの型を使用することをお勧めします。
-   [日時](/data-type-date-and-time.md) : **datetime**型は時刻値の保存に使用できます。
-   [列挙型](/data-type-string.md#enum-type) : 列挙型は、限られた値の選択を格納するために使用できます。

## 主キーを選択 {#select-primary-key}

[主キー](/constraints.md#primary-key)はテーブル内の列または列セットであり、その値によってテーブル内の行が一意に識別されます。

> **注記：**
>
> TiDB の**主キー**のデフォルト定義は、 [翻訳](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html) (MySQL の共通storageエンジン) の主キーの定義とは異なります。
>
> -   **InnoDB**の場合:**主キー**は一意であり、null ではなく、**インデックスがクラスター化されます**。
>
> -   TiDB の場合:**主キーは**一意であり、null ではありません。ただし、主キーが**クラスター化インデックス**であるとは限りません。代わりに、別のキーワード セット`CLUSTERED` `NONCLUSTERED`**主キーが****クラスター化インデックス**であるかどうかをさらに制御します。キーワードが指定されていない場合は、 [クラスター化インデックス](https://docs.pingcap.com/tidb/stable/clustered-indexes)で説明されているように、システム変数`@@global.tidb_enable_clustered_index`によって制御されます。

**主キーは**`CREATE TABLE`ステートメントで定義されます。5 [主キー制約](/constraints.md#primary-key)ステートメントでは、制約されたすべての列に NULL 以外の値のみが含まれている必要があります。

テーブルは、**主キー**なしで、または非整数の**主キー**を使用して作成できます。この場合、TiDB は**暗黙の主キー**として`_tidb_rowid`作成します。暗黙の主キー`_tidb_rowid`は単調に増加する性質のため、書き込み集中型のシナリオでは書き込みホットスポットが発生する可能性があります。したがって、書き込み集中型のアプリケーションの場合は、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)および[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)パラメータを使用してデータをシャーディングすることを検討してください。ただし、これにより読み取り増幅が発生する可能性があるため、独自のトレードオフを行う必要があります。

テーブルの**主キー**が[整数型](/data-type-numeric.md#integer-types)で`AUTO_INCREMENT`使用されている場合、 `SHARD_ROW_ID_BITS`使用してもホットスポットを回避することはできません。ホットスポットを回避する必要があり、連続した増分主キーが必要ない場合は、 `AUTO_INCREMENT`ではなく[`AUTO_RANDOM`](/auto-random.md)使用して行 ID の連続性を排除できます。

<CustomContent platform="tidb">

ホットスポットの問題の処理方法の詳細については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照してください。

</CustomContent>

[主キーを選択するためのガイドライン](#guidelines-to-follow-when-selecting-primary-key)に続いて、次の例は`users`テーブルで`AUTO_RANDOM`主キーがどのように定義されるかを示しています。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100),
  PRIMARY KEY (`id`)
);
```

## クラスター化されているかどうか {#clustered-or-not}

TiDB は、バージョン 5.0 以降、 [クラスター化インデックス](/clustered-indexes.md)機能をサポートしています。この機能は、主キーを含むテーブルにデータを格納する方法を制御します。この機能により、TiDB は特定のクエリのパフォーマンスを向上できる方法でテーブルを整理できるようになります。

この文脈における「クラスター化」という用語は、連携して動作するデータベース サーバーのグループではなく、データの格納方法の構成を指します。一部のデータベース管理システムでは、クラスター化インデックスをインデックス構成テーブル (IOT) と呼びます。

現在、TiDB 内の***主キーを含む***テーブルは次の 2 つのカテゴリに分類されます。

-   `NONCLUSTERED` : テーブルの主キーは非クラスター化インデックスです。非クラスター化インデックスを持つテーブルでは、行データのキーは TiDB によって暗黙的に割り当てられた内部`_tidb_rowid`で構成されます。主キーは本質的に一意のインデックスであるため、非クラスター化インデックスを持つテーブルでは行を格納するために少なくとも 2 つのキーと値のペアが必要です。
    -   `_tidb_rowid` (キー) - 行データ (値)
    -   主キーデータ（キー） - `_tidb_rowid` （値）
-   `CLUSTERED` : テーブルの主キーはクラスター化インデックスです。クラスター化インデックスを持つテーブルでは、行データのキーはユーザーが指定した主キー データで構成されます。したがって、クラスター化インデックスを持つテーブルでは、行を格納するために 1 つのキーと値のペアのみが必要です。
    -   主キーデータ（キー） - 行データ（値）

[主キーを選択](#select-primary-key)で説明したように、**クラスター化インデックスは**TiDB ではキーワード`CLUSTERED`と`NONCLUSTERED`使用して制御されます。

> **注記：**
>
> TiDB は、テーブルの`PRIMARY KEY`によるクラスタリングのみをサポートします。クラスター化インデックスが`PRIMARY KEY`*と**クラスター化インデックス*という用語は同じ意味で使用できます。 `PRIMARY KEY`制約 (論理プロパティ) を指し、クラスター化インデックスはデータの格納方法の物理的な実装を表します。

[クラスター化インデックスを選択するためのガイドライン](#guidelines-to-follow-when-selecting-clustered-index)に続いて、次の例では、 `book` × `users`の`ratings`を表す`books`と`users`の関連付けを持つテーブルを作成します。 この例では、テーブルを作成し、 `book_id`と`user_id`使用して複合主キーを構築し、その**主キー**に**クラスター化インデックス**を作成します。

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

[主キー制約](#select-primary-key)に加えて、 TiDB は[NULLではない](/constraints.md#not-null)制約、 [ユニークキー](/constraints.md#unique-key)制約、 `DEFAULT`などの他の**列制約**もサポートしています。 完全な制約については、 [TiDB制約](/constraints.md)ドキュメントを参照してください。

### デフォルト値を設定する {#set-default-value}

列にデフォルト値を設定するには、 `DEFAULT`制約を使用します。デフォルト値を使用すると、各列に値を指定せずにデータを挿入できます。

`DEFAULT`と[サポートされているSQL関数](/functions-and-operators/functions-and-operators-overview.md)併用すると、デフォルトの計算をアプリケーションレイヤーの外に移動できるため、アプリケーションレイヤーのリソースを節約できます。計算で消費されたリソースは消えず、TiDB クラスターに移動されます。通常、デフォルトの時間でデータを挿入できます。次の例は、 `ratings`テーブルでデフォルト値を設定する例です。

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

さらに、データの更新時に現在の時刻もデフォルトで入力される場合は、次のステートメントを使用できます (ただし、 `ON UPDATE`後には現在の時刻に関連する式のみを入力できます)。

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

さまざまなデータ型のデフォルト値の詳細については、 [デフォルト値](/data-type-default-values.md)参照してください。

### 重複した値を防ぐ {#prevent-duplicate-values}

列内の値の重複を防ぐ必要がある場合は、 `UNIQUE`制約を使用できます。

たとえば、ユーザーのニックネームが一意であることを確認するには、 `users`のテーブルのテーブル作成 SQL ステートメントを次のように書き換えます。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE,
  PRIMARY KEY (`id`)
);
```

同じ`nickname` `users`テーブルに挿入しようとすると、エラーが返されます。

### NULL値を防ぐ {#prevent-null-values}

列に null 値が含まれるのを防ぐ必要がある場合は、 `NOT NULL`制約を使用できます。

ユーザーのニックネームを例に挙げます。ニックネームが一意であるだけでなく、null でないことを確認するには、 `users`テーブルを作成するための SQL ステートメントを次のように書き換えます。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE NOT NULL,
  PRIMARY KEY (`id`)
);
```

## HTAP機能を使用する {#use-htap-capabilities}

<CustomContent platform="tidb">

> **注記：**
>
> このガイドで説明されている手順は、テスト環境での迅速な開始のみを***目的と***しています。本番環境の場合は、 [HTAPを探索する](/explore-htap.md)を参照してください。

</CustomContent>

<CustomContent platform="tidb-cloud">

> **注記：**
>
> このガイドで説明されている手順は、クイック スタートのみを***目的***としています。詳細な手順については、 [TiFlashでHTAPクラスタを使用する](/tiflash/tiflash-overview.md)を参照してください。

</CustomContent>

たとえば、 `bookshop`アプリケーションを使用して`ratings`テーブルで OLAP 分析を実行し**、本の評価が評価の時間と有意な相関関係があるかどうかを**照会するとします。これは、本に対するユーザーの評価が客観的かどうかを分析するためです。次に、 `ratings`テーブル全体の`score`フィールドと`rated_at`フィールドを照会する必要があります。この操作は、OLTP のみのデータベースではリソースを大量に消費します。または、ETL またはその他のデータ同期ツールを使用して、OLTP データベースから分析専用の OLAP データベースにデータをエクスポートすることもできます。

このシナリオでは、OLTP と OLAP の両方のシナリオをサポートする**HTAP (ハイブリッド トランザクションおよび分析処理)**データベースである TiDB が、理想的なワンストップ データベース ソリューションです。

### 列ベースのデータを複製する {#replicate-column-based-data}

<CustomContent platform="tidb">

現在、TiDB は**TiFlash**と**TiSpark の**2 つのデータ分析エンジンをサポートしています。大規模データ シナリオ (100 T) の場合、HTAP のプライマリ ソリューションとして**TiFlash MPP**を推奨し、補完ソリューションとして**TiSpark を**推奨します。

TiDB HTAP機能の詳細については、次のドキュメントを参照してください: [TiDB HTAPクイック スタート ガイド](/quick-start-with-htap.md)および[HTAPを探索する](/explore-htap.md) 。

</CustomContent>

<CustomContent platform="tidb-cloud">

TiDB HTAP機能の詳細については、 [TiDB Cloud HTAP クイックスタート](/tidb-cloud/tidb-cloud-htap-quickstart.md)および[TiFlashでHTAPクラスタを使用する](/tiflash/tiflash-overview.md)参照してください。

</CustomContent>

この例では、 `bookshop`データベースのデータ分析エンジンとして[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)選択されています。

TiFlash はデプロイメント後にデータを自動的に複製しません。そのため、複製するテーブルを手動で指定する必要があります。

```sql
ALTER TABLE {table_name} SET TIFLASH REPLICA {count};
```

**パラメータの説明**

-   `{table_name}` : テーブル名。
-   `{count}` : 複製されたレプリカの数。0 の場合、複製されたレプリカは削除されます。

その後、 **TiFlash は**テーブルを複製します。クエリが実行されると、TiDB はコスト最適化に基づいてクエリに対して TiKV (行ベース) またはTiFlash (列ベース) を自動的に選択します。または、クエリで**TiFlash**レプリカを使用するかどうかを手動で指定することもできます。指定方法については、 [TiDBを使用してTiFlashレプリカを読み取る](/tiflash/use-tidb-to-read-tiflash.md)を参照してください。

### HTAP機能の使用例 {#an-example-of-using-htap-capabilities}

`ratings`テーブルはTiFlashの`1`のレプリカを開きます。

```sql
ALTER TABLE `bookshop`.`ratings` SET TIFLASH REPLICA 1;
```

> **注記：**
>
> クラスターに**TiFlash**ノードが含まれていない場合、この SQL ステートメントはエラーを報告します: `1105 - the tiflash replica count: 1 should be less than the total tiflash server count: 0` 。 [TiDB Cloudサーバーレスクラスタを構築する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-tidb-cloud-serverless-cluster)使用して、 **TiFlash を**含むTiDB Cloud Serverless クラスターを作成できます。

次に、次のクエリを実行します。

```sql
SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)ステートメントを実行して、このステートメントが**TiFlash を**使用しているかどうかを確認することもできます。

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

フィールド`cop[tiflash]`が表示された場合、タスクは処理のために**TiFlash**に送信されることを意味します。

## <code>CREATE TABLE</code>ステートメントを実行する {#execute-the-code-create-table-code-statement}

上記のルールに従ってすべてのテーブルを作成すると、スクリプト[データベースの初期化](/develop/dev-guide-bookshop-schema-design.md#database-initialization-script-dbinitsql)は次のようになります。テーブル情報を詳しく確認する必要がある場合は、 [表の説明](/develop/dev-guide-bookshop-schema-design.md#description-of-the-tables)を参照してください。

データベース初期化スクリプト`init.sql`に名前を付けて保存するには、次のステートメントを実行してデータベースを初期化します。

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

## テーブルを作成する際に従うべきガイドライン {#guidelines-to-follow-when-creating-a-table}

このセクションでは、テーブルを作成するときに従う必要があるガイドラインを示します。

### テーブルに名前を付けるときに従うべきガイドライン {#guidelines-to-follow-when-naming-a-table}

-   **完全修飾**テーブル名 (例: `CREATE TABLE {database_name}. {table_name}` ) を使用します。データベース名を指定しない場合、TiDB は**SQL セッション**の現在のデータベースを使用します。SQL セッションでデータベースを指定するために`USE {databasename};`使用しない場合、TiDB はエラーを返します。
-   意味のあるテーブル名を使用してください。たとえば、ユーザー テーブルを作成する必要がある場合は、 `user` 、 `t_user` 、 `users`の名前を使用するか、会社または組織の命名規則に従うことができます。会社または組織に命名規則がない場合は、 [テーブル命名規則](/develop/dev-guide-object-naming-guidelines.md#table-naming-convention)を参照してください。 `t1` 、 `table1`などのテーブル名は使用しないでください。
-   複数の単語はアンダースコアで区切られ、名前は 32 文字以内にすることをお勧めします。
-   異なるビジネス モジュールのテーブルごとに個別の`DATABASE`作成し、それに応じてコメントを追加します。

### 列を定義する際に従うべきガイドライン {#guidelines-to-follow-when-defining-columns}

-   列でサポートされている[データ型](/data-type-overview.md)を確認し、データ型の制限に従ってデータを整理します。列に格納する予定のデータに適した型を選択します。
-   主キーを選択するための[従うべきガイドライン](#guidelines-to-follow-when-selecting-primary-key)を確認し、主キー列を使用するかどうかを決定します。
-   クラスター化インデックスを選択するための[従うべきガイドライン](#guidelines-to-follow-when-selecting-clustered-index)を確認し、**クラスター化インデックス**を指定するかどうかを決定します。
-   [列制約の追加](#add-column-constraints)チェックし、列に制約を追加するかどうかを決定します。
-   意味のある列名を使用してください。会社または組織のテーブル命名規則に従うことをお勧めします。会社または組織に対応する命名規則がない場合は、 [列の命名規則](/develop/dev-guide-object-naming-guidelines.md#column-naming-convention)を参照してください。

### 主キーを選択する際のガイドライン {#guidelines-to-follow-when-selecting-primary-key}

-   テーブル内に**主キー**または**一意のインデックス**を定義します。
-   意味のある**列を****主キー**として選択するようにしてください。
-   パフォーマンス上の理由から、非常に幅の広いテーブルを保存しないようにしてください。テーブル フィールドの数が`60`を超え、単一行の合計データ サイズが`64K`超えることは推奨されません。データ長が長すぎるフィールドは別のテーブルに分割することをお勧めします。
-   複雑なデータ型の使用はお勧めしません。
-   結合するフィールドについては、データ型が一貫していることを確認し、暗黙的な変換を回避してください。
-   単一の単調なデータ列に**主キー**を定義しないでください。単一の単調なデータ列 (たとえば、 `AUTO_INCREMENT`属性を持つ列) を使用して**主キー**を定義すると、書き込みパフォーマンスに影響する可能性があります。可能であれば、主キーの連続および増分属性を破棄する`AUTO_INCREMENT`ではなく`AUTO_RANDOM`使用してください。
-   書き込み集中型のシナリオで単一の単調なデータ列にインデックスを作成する必要がある場合は、この単調なデータ列を**主キー**として定義する代わりに、 `AUTO_RANDOM`使用してそのテーブルの**主キー**を作成するか、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)と[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)使用して`_tidb_rowid`シャード化することができます。

### クラスター化インデックスを選択する際のガイドライン {#guidelines-to-follow-when-selecting-clustered-index}

-   **クラスター化インデックス**を構築するには、 [主キーを選択するためのガイドライン](#guidelines-to-follow-when-selecting-primary-key)に従ってください。

-   非クラスター化インデックスを持つテーブルと比較すると、クラスター化インデックスを持つテーブルでは、次のシナリオでパフォーマンスとスループットの利点が大きくなります。
    -   データが挿入されると、クラスター化インデックスにより、ネットワークからのインデックス データの書き込みが 1 回削減されます。
    -   同等の条件を持つクエリに主キーのみが関係する場合、クラスター化インデックスにより、ネットワークからのインデックス データの読み取りが 1 回削減されます。
    -   範囲条件を持つクエリに主キーのみが関係する場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。
    -   同等条件または範囲条件を持つクエリに主キー プレフィックスのみが関係する場合、クラスター化インデックスにより、ネットワークからのインデックス データの複数回の読み取りが削減されます。

-   一方、クラスター化インデックスを持つテーブルでは、次のような問題が発生する可能性があります。
    -   近い値を持つ主キーを多数挿入すると、書き込みホットスポットの問題が発生する可能性があります。 [主キーを選択する際のガイドライン](#guidelines-to-follow-when-selecting-primary-key)に従ってください。
    -   主キーのデータ型が 64 ビットより大きい場合、特に複数のセカンダリ インデックスがある場合、テーブル データはより多くのstorage領域を占有します。

-   [クラスター化インデックスを使用するかどうかのデフォルトの動作](/clustered-indexes.md#create-a-table-with-clustered-indexes)を制御するには、システム変数`@@global.tidb_enable_clustered_index`と構成`alter-primary-key`を使用する代わりに、クラスター化インデックスを使用するかどうかを明示的に指定できます。

### <code>CREATE TABLE</code>ステートメントを実行する際に従うべきガイドライン {#guidelines-to-follow-when-executing-the-code-create-table-code-statement}

-   データベース スキーマの変更を実行するためにクライアント側のDriverまたは ORM を使用することは推奨されません。データベース スキーマの変更を実行するには、 [MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)使用するか、GUI クライアントを使用することをお勧めします。このドキュメントでは、ほとんどのシナリオでデータベース スキーマの変更を実行するために、 **MySQL クライアント**を使用して SQL ファイルを渡します。
-   SQL 開発[テーブルの作成と削除の仕様](/develop/dev-guide-sql-development-specification.md#create-and-delete-tables)に従います。判断ロジックを追加するには、ビジネス アプリケーション内で build ステートメントと delete ステートメントをラップすることをお勧めします。

## もう一歩 {#one-more-step}

このドキュメントで作成されたすべてのテーブルにはセカンダリ インデックスが含まれていないことに注意してください。セカンダリ インデックスを追加するガイドについては、 [セカンダリインデックスの作成](/develop/dev-guide-create-secondary-indexes.md)を参照してください。

## ヘルプが必要ですか? {#need-help}

<CustomContent platform="tidb">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](/support.md)について質問します。

</CustomContent>

<CustomContent platform="tidb-cloud">

[TiDB コミュニティ](https://ask.pingcap.com/) 、または[サポートチケットを作成する](https://support.pingcap.com/)について質問します。

</CustomContent>
