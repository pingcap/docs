---
title: Create a Table
summary: 表作成における定義、ルール、ガイドラインを学びましょう。
aliases: ['/ja/tidb/stable/dev-guide-create-table/','/ja/tidb/dev/dev-guide-create-table/','/ja/tidbcloud/dev-guide-create-table/']
---

# テーブルを作成する {#create-a-table}

このドキュメントでは、SQL文を使用してテーブルを作成する方法と、関連するベストプラクティスについて説明します。ベストプラクティスを説明するために、TiDBベースの[書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションの例を示します。

## 始める前に {#before-you-start}

この文書を読む前に、以下の作業が完了していることを確認してください。

-   [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md)。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md)お読みください。
-   [データベースを作成する](/develop/dev-guide-create-database.md)。

## テーブルとは何ですか {#what-is-a-table}

[テーブル](/develop/dev-guide-schema-design-overview.md#table)、TiDB の論理オブジェクトであり、 の[データベース](/develop/dev-guide-schema-design-overview.md#database)オブジェクトです。SQL ステートメントから送信されたデータを格納するために使用されます。テーブルは、行と列の形式でデータレコードを保存します。テーブルには少なくとも 1 つの列があります。 `n`列を定義した場合、各データ行には`n`列とまったく同じフィールドが含まれます。

## テーブルの名前を挙げてください {#name-a-table}

テーブルを作成する最初のステップは、テーブルに名前を付けることです。将来、自分や同僚に大きな負担をかけるような、意味のない名前は使用しないでください。会社や組織のテーブル命名規則に従うことをお勧めします。

`CREATE TABLE`ステートメントは通常、次の形式をとります。

```sql
CREATE TABLE {table_name} ( {elements} );
```

**パラメータの説明**

-   `{table_name}` : 作成するテーブルの名前。
-   `{elements}` : 列定義や主キー定義など、テーブル要素をカンマで区切ったリスト。

`bookshop`データベースにユーザー情報を保存するためのテーブルを作成する必要があるとします。

まだ列が追加されていないため、以下のSQL文は実行できないことに注意してください。

```sql
CREATE TABLE `bookshop`.`users` (
);
```

## 列を定義する {#define-columns}

**列**はテーブルの下位要素です。各テーブルには少なくとも1つの列があります。列は、各行の値を単一のデータ型の小さなセルに分割することで、テーブルに構造を与えます。

カラム定義は通常、次の形式をとります。

    {column_name} {data_type} {column_qualification}

**パラメータの説明**

-   `{column_name}` : 列名。
-   `{data_type}` : 列[データ型](/data-type-overview.md)。
-   `{column_qualification}` :**列レベルの制約**や[生成された列](/generated-columns.md)列句などのカラム修飾。

`users`テーブルに、一意の識別子`id` 、 `balance` 、 `nickname`などの列を追加できます。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint,
  `nickname` varchar(100),
  `balance` decimal(15,2)
);
```

上記の記述では、 `id`という名前とタイプ[ビギント](/data-type-numeric.md#bigint-type)を持つフィールドが定義されています。これは、一意のユーザー識別子を表すために使用されます。つまり、すべてのユーザー識別子は`bigint`タイプである必要があります。

次に、 `nickname`という名前のフィールドが定義されます。これは[varchar](/data-type-string.md#varchar-type)型で、長さの制限は 100 文字です。つまり、ユーザーの`nicknames`は`varchar`型を使用し、100 文字を超えないということです。

最後に、 `balance`という名前のフィールドが追加されます。これは[小数](/data-type-numeric.md#decimal-type)型で、**精度**は`15` 、**スケール**は`2` 。**精度は**フィールド内の桁数の合計を表し、**スケールは**小数点以下の桁数を表します。たとえば、 `decimal(5,2)`は、精度が`5` 、スケールが`2`で、範囲は`-999.99`から`999.99`となります。 `decimal(6,1)`は、精度が`6` 、スケールが`1`で、範囲が`-99999.9`から`99999.9`であることを意味します。decimal**は**[固定小数点型](/data-type-numeric.md#fixed-point-types)で、数値を正確に格納するために使用できます。正確な数値が必要なシナリオ (たとえば、ユーザー プロパティ関連) では、 **decimal**型を使用するようにしてください。

TiDB は、[整数型](/data-type-numeric.md#integer-types)、 [浮動小数点型](/data-type-numeric.md#floating-point-types)、[固定小数点型](/data-type-numeric.md#fixed-point-types)小数点型、[日付と時刻の種類](/data-type-date-and-time.md)、[列挙型](/data-type-string.md#enum-type)など、他の多くの列データ型をサポートしています。サポートされている列の[データ型](/data-type-overview.md)を参照し、データベースに保存したいデータに一致する**データ型**を使用できます。

もう少し複雑にするには、 `books`データの核となる`bookshop`テーブルを定義できます。 `books`テーブルには、書籍の ID、タイトル、種類 (雑誌、小説、ライフ、芸術など)、在庫、価格、出版日などのフィールドが含まれます。

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

このテーブルには`users`テーブルよりも多くのデータ型が含まれています。

-   [整数](/data-type-numeric.md#integer-types): ディスク使用量の過剰使用やパフォーマンスへの影響（型範囲が大きすぎる場合）またはデータオーバーフロー（データ型範囲が小さすぎる場合）を避けるため、適切なサイズの型を使用することをお勧めします。
-   :[日時](/data-type-date-and-time.md)型は**、**時間値を格納できます。
-   [列挙型](/data-type-string.md#enum-type): enum型は、限られた値の選択を格納するために使用できます。

## 主キーを選択 {#select-primary-key}

[主キー](/constraints.md#primary-key)とは、テーブル内の行を一意に識別する値を持つ、テーブル内の列または列のセットのことです。

> **注記：**
>
> TiDBにおける**プライマリキー**のデフォルト定義は、 [InnoDB](https://dev.mysql.com/doc/refman/8.0/en/innodb-storage-engine.html) （MySQLの一般的なstorageエンジン）における定義とは異なります。
>
> -   **InnoDB**では、**プライマリキー**は一意であり、nullではなく、**インデックスはクラスタ化されています**。
>
> -   TiDBでは、**プライマリキー**は一意であり、NULLであってはなりません。ただし、プライマリキーが**クラスタ化インデックス**であることは保証されていません。代わりに、別のキーワードセット`CLUSTERED` / `NONCLUSTERED`によって、**プライマリキーが****クラスタ化インデックス**であるかどうかが制御されます。キーワードが指定されていない場合は、システム変数`@@global.tidb_enable_clustered_index`によって制御されます（化を参照[クラスター化インデックス](https://docs.pingcap.com/tidb/stable/clustered-indexes)。

**主キー**は`CREATE TABLE`ステートメントで定義されます。[主キー制約](/constraints.md#primary-key)制約付き列すべてに NULL 以外の値のみが含まれることを要求します。

テーブルは**、主キー**なし、または非整数の**主キー**を使用して作成できます。この場合、TiDB は**暗黙の主キー**として`_tidb_rowid`を作成します。暗黙の主キー`_tidb_rowid`単調増加する性質を持つため、書き込み負荷の高いシナリオでは書き込みホットスポットが発生する可能性があります。したがって、アプリケーションが書き込み負荷の高い場合は、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)および[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)パラメータを使用してデータをシャーディングすることを検討してください。ただし、これにより読み取り増幅が発生する可能性があるため、トレードオフを独自に判断する必要があります。

テーブルの**主キー**が[整数型](/data-type-numeric.md#integer-types)で`AUTO_INCREMENT`が使用されている場合、 `SHARD_ROW_ID_BITS`を使用してもホットスポットを回避することはできません。ホットスポットを回避する必要があり、かつ連続的かつ増分的な主キーが必要ない場合は、 `AUTO_INCREMENT`の代わりに[`AUTO_RANDOM`](/auto-random.md)を使用して行 ID の連続性を排除できます。

TiDB セルフマネージドでホットスポットの問題を処理する方法の詳細については、[ホットスポットの問題をトラブルシューティングする](/troubleshoot-hot-spot-issues.md)。

[主キーの選択に関するガイドライン](#guidelines-to-follow-when-selecting-primary-key)に従って、次の例は、 `AUTO_RANDOM`の主キーが`users`テーブルでどのように定義されるかを示しています。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100),
  PRIMARY KEY (`id`)
);
```

## クラスター化されているか否か {#clustered-or-not}

TiDB は v5.0 以降、[クラスター化インデックス](/clustered-indexes.md)機能をサポートしています。この機能は、主キーを含むテーブルにデータを格納する方法を制御します。これにより、特定のクエリのパフォーマンスを向上できる方法でテーブルを編成する機能が TiDB に提供されます。

この文脈における「クラスタ化」という用語は、データの格納方法の構成を指し、連携して動作するデータベースサーバーのグループを指すものではありません。一部のデータベース管理システムでは、クラスタ化されたインデックステーブルをインデックス構成テーブル（IOT）と呼んでいます。

現在、TiDBの***主キーを含む***テーブルは、以下の2つのカテゴリに分類されます。

-   `NONCLUSTERED` : テーブルの主キーは非クラスター化インデックスです。非クラスター化インデックスを持つテーブルでは、行データのキーは、TiDB によって暗黙的に割り当てられる内部`_tidb_rowid`で構成されます。主キーは基本的に一意のインデックスであるため、非クラスター化インデックスを持つテーブルでは、行を格納するために少なくとも 2 つのキーと値のペアが必要です。それらは次のとおりです。
    -   `_tidb_rowid` （キー） - 行データ（値）
    -   主キーデータ（キー） - `_tidb_rowid` （値）
-   `CLUSTERED` : テーブルの主キーはクラスタ化インデックスです。クラスタ化インデックスを持つテーブルでは、行データのキーはユーザーが指定した主キーデータで構成されます。したがって、クラスタ化インデックスを持つテーブルでは、行を格納するために必要なキーと値のペアは1つだけです。それは次のとおりです。
    -   主キーデータ（キー） - 行データ（値）

[プライマリキーを選択](#select-primary-key)で説明されているように、**クラスター化インデックス**は TiDB でキーワード`CLUSTERED`および`NONCLUSTERED`を使用して制御されます。

> **注記：**
>
> TiDB は、テーブルの`PRIMARY KEY`によるクラスタリングのみをサポートしています。クラスタ化インデックスが有効になっている場合、 *{* `PRIMARY KEY`と*クラスタ化インデックス*という用語は同じ意味で使用されることがあります。 `PRIMARY KEY`は制約 (論理プロパティ) を指し、クラスタ化インデックスはデータの格納方法の物理的な実装を表します。

[クラスター化インデックスを選択するためのガイドライン](#guidelines-to-follow-when-selecting-clustered-index)ためのガイドラインに従って、次の例では、 `books`と`users` } の間の関連付けを持つテーブルを作成します。これは、 `ratings` `book`を表します。 `users` .この例では、テーブルを作成し、 `book_id`と`user_id`を使用して複合主キーを構築し、その**主キー**に**クラスター化インデックス**を作成します。

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

[主キー制約](#select-primary-key)に加えて、TiDB は[NULL不可](/constraints.md#not-null)制約、[ユニークキー](/constraints.md#unique-key)制約、および`DEFAULT`などの他の**列制約**もサポートします。完全な制約については、 [TiDBの制約](/constraints.md)ドキュメントを参照してください。

### デフォルト値を設定する {#set-default-value}

列にデフォルト値を設定するには、 `DEFAULT`制約を使用します。デフォルト値を使用すると、各列の値を指定せずにデータを挿入できます。

`DEFAULT` [サポートされているSQL関数](/functions-and-operators/functions-and-operators-overview.md)と組み合わせて使用​​できます。これにより、デフォルト値の計算をアプリケーションレイヤーから外すことで、アプリケーションレイヤーのリソースを節約できます。計算によって消費されたリソースは消滅せず、データベースによって処理されます。通常、デフォルト値を使用してデータを挿入できます。以下は`ratings`テーブルにデフォルト値を設定する例です。

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

さらに、データ更新時に現在時刻もデフォルトで入力される場合は、以下のステートメントを使用できます（ただし、 `ON UPDATE`の後には、現在時刻に関連する式のみを入力できます）。

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

さまざまなデータ型のデフォルト値の詳細については、[デフォルト値](/data-type-default-values.md)参照してください。

### 重複値を防止する {#prevent-duplicate-values}

列内の重複値を防止する必要がある場合は、 `UNIQUE`制約を使用できます。

例えば、ユーザーのニックネームが一意であることを確認するには、 `users`テーブルのテーブル作成 SQL ステートメントを次のように書き換えることができます。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE,
  PRIMARY KEY (`id`)
);
```

`nickname`を`users`テーブルに挿入しようとすると、エラーが返されます。

### null値を防止する {#prevent-null-values}

列にヌル値が含まれるのを防ぐ必要がある場合は、 `NOT NULL`制約を使用できます。

ユーザーのニックネームを例にとってみましょう。ニックネームが一意であるだけでなく、null でないことを確認するには、 `users`テーブルを作成するための SQL ステートメントを次のように書き換えることができます。

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE NOT NULL,
  PRIMARY KEY (`id`)
);
```

## HTAP機能を使用する {#use-htap-capabilities}

> **注記：**
>
> このセクションで説明する手順は、クイック スタートとテスト***のみ***を目的としています。 TiDB での HTAP の使用法の詳細については、 [HTAPを探索する](/explore-htap.md)参照してください。

`ratings`アプリケーションを使用して`bookshop`テーブルに対して OLAP 分析を実行したいとします。たとえば、**書籍の評価と評価のタイミングに有意な相関関係があるかどうかを**クエリし、ユーザーによる書籍の評価が客観的かどうかを分析したいとします。この場合`score`フィールドと`rated_at` `ratings` } フィールドをクエリする必要があります。この操作は、OLTP 専用データベースではリソースを大量に消費します。または、ETL やその他のデータ同期ツールを使用して、OLTP データベースから専用の OLAP データベースにデータをエクスポートして分析することもできます。

このシナリオでは、OLTPとOLAPの両方のシナリオをサポートする**HTAP（ハイブリッド・トランザクション・アンド・アナリティカル・プロセッシング）**データベースであるTiDBが、理想的なワンストップデータベースソリューションとなります。

TiDBでは、オンライン・トランザクション処理（OLTP）には行ベースのstorageエンジンである[ティクヴ](/tikv-overview.md)、オンライン分析処理（OLAP）には列指向storageエンジンである[TiFlash](/tiflash/tiflash-overview.md)を使用できます。設定後、 TiFlashはRaft Learnerコンセンサスアルゴリズムに従ってTiKVからリアルタイムでデータを複製し、TiKVとTiFlash間のデータの一貫性を厳密に確保します。

### 列ベースのデータを複製する {#replicate-column-based-data}

TiFlashはデプロイ後にデータを自動的に複製しません。そのため、複製するテーブルを手動で指定する必要があります。

```sql
ALTER TABLE {table_name} SET TIFLASH REPLICA {count};
```

**パラメータの説明**

-   `{table_name}` : テーブル名。
-   `{count}` : 複製されたレプリカの数。0 の場合、複製されたレプリカは削除されます。

**TiFlash は**テーブルを複製します。クエリが実行されると、TiDB はコストの最適化に基づいてクエリに対して TiKV (行ベース) またはTiFlash (列ベース) を自動的に選択します。あるいは、クエリで**TiFlash**レプリカを使用するかどうかを手動で指定できます。指定方法については、 [TiDBを使用してTiFlashレプリカを読み取ります](/tiflash/use-tidb-to-read-tiflash.md)参照してください。

### HTAP機能の使用例 {#an-example-of-using-htap-capabilities}

`ratings`テーブルは、 TiFlashの`1`レプリカを開きます。

```sql
ALTER TABLE `bookshop`.`ratings` SET TIFLASH REPLICA 1;
```

> **注記：**
>
> クラスターに**TiFlash**ノードが含まれていない場合、この SQL ステートメントはエラー`1105 - the tiflash replica count: 1 should be less than the total tiflash server count: 0`を報告します。 [TiDB Cloud Starterインスタンスを作成する](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-starter-instance)を使用して、 **TiFlash**を含むTiDB Cloud Starterインスタンスを作成できます。

次に、以下のクエリを実行できます。

```sql
SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

また、 [`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)ステートメントを実行して、このステートメントが**TiFlash**を使用しているかどうかを確認することもできます。

```sql
EXPLAIN ANALYZE SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

実行結果：

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

フィールド`cop[tiflash]`が表示された場合、タスクが処理のために**TiFlash**に送信されることを意味します。

## <code>CREATE TABLE</code>文を実行します。 {#execute-the-code-create-table-code-statement}

上記のルールに従ってすべてのテーブルを作成した後、データベース[データベースの初期化](/develop/dev-guide-bookshop-schema-design.md#database-initialization-script-dbinitsql)スクリプトは次のようになります。テーブル情報を詳しく見たい場合は、 [表の説明](/develop/dev-guide-bookshop-schema-design.md#description-of-the-tables)を参照してください。

データベース初期化スクリプトに`init.sql`という名前を付けて保存するには、次のステートメントを実行してデータベースを初期化します。

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    < init.sql
```

`bookshop`データベース配下のすべてのテーブルを表示するには、 [`SHOW TABLES`](/sql-statements/sql-statement-show-tables.md#show-full-tables)ステートメントを使用します。

```sql
SHOW TABLES IN `bookshop`;
```

実行結果：

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

このセクションでは、テーブルを作成する際に従うべきガイドラインを示します。

### テーブル名を付ける際のガイドライン {#guidelines-to-follow-when-naming-a-table}

-   **完全修飾**テーブル名（例： `CREATE TABLE {database_name}. {table_name}` ）を使用してください。データベース名を指定しない場合、TiDB は**SQL セッション**で現在使用されているデータベースを使用します。SQL セッションでデータベースを指定する際に`USE {databasename};`を使用しない場合、TiDB はエラーを返します。
-   意味のあるテーブル名を使用してください。たとえば、ユーザー テーブルを作成する必要がある場合は、 `user` 、 `t_user` 、 `users`のような名前を使用するか、会社または組織の命名規則に従ってください。会社または組織に命名規則がない場合は、 [テーブル命名規則](/develop/dev-guide-object-naming-guidelines.md#table-naming-convention)を参照してください。 `t1` 、 `table1`のようなテーブル名は使用しないでください。
-   複数の単語はアンダースコアで区切られ、名前は32文字以内にすることをお勧めします。
-   異なるビジネスモジュールのテーブル用に個別の`DATABASE`を作成し、それに応じてコメントを追加してください。

### 列を定義する際に従うべきガイドライン {#guidelines-to-follow-when-defining-columns}

-   列のサポート[データ型](/data-type-overview.md)を確認し、データ型の制約に従ってデータを整理してください。列に格納するデータに適した型を選択してください。
-   主キーの選択に関する[従うべきガイドライン](#guidelines-to-follow-when-selecting-primary-key)を確認し、主キー列を使用するかどうかを決定します。
-   クラスタ化インデックスを選択するための[従うべきガイドライン](#guidelines-to-follow-when-selecting-clustered-index)ガイドラインを確認し、**クラスタ化インデックス**を指定するかどうかを決定してください。
-   [列制約を追加する](#add-column-constraints)チェックし、列に制約を追加するかどうかを決定します。
-   意味のある列名を使用してください。会社または組織のテーブル命名規則に従うことをお勧めします。会社または組織に対応する命名規則がない場合は、 [列名の命名規則](/develop/dev-guide-object-naming-guidelines.md#column-naming-convention)を参照してください。

### 主キーを選択する際に従うべきガイドライン {#guidelines-to-follow-when-selecting-primary-key}

-   テーブル内に**主キー**または**一意インデックス**を定義します。
-   意味のある**列を****主キー**として選択するようにしてください。
-   パフォーマンス上の理由から、幅の広いテーブルを保存することは避けてください。テーブルフィールドの数が`60`を超え、1行のデータの合計サイズが`64K`超えることは推奨されません。データ長が長すぎるフィールドは、別のテーブルに分割することをお勧めします。
-   複雑なデータ型を使用することは推奨されません。
-   結合するフィールドについては、データ型が一致していることを確認し、暗黙的な型変換を避けてください。
-   単一の単調データ列に**主キー**を定義することは避けてください。単一の単調データ列（たとえば、 `AUTO_INCREMENT`属性を持つ列）を使用して**主キー**を定義すると、書き込みパフォーマンスに影響が出る可能性があります。可能であれば、 `AUTO_RANDOM`ではなく`AUTO_INCREMENT` }を使用してください。これにより、主キーの連続性および増分属性が破棄されます。
-   書き込み集中シナリオで単一の単調データ列にインデックスを作成する必要がある場合は、この単調データ列を**主キー**として定義する代わりに、 `AUTO_RANDOM`を使用してそのテーブルの**主キー**を作成するか、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)と[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)を使用して`_tidb_rowid`をシャーディングすることができます。

### クラスター化インデックスを選択する際に従うべきガイドライン {#guidelines-to-follow-when-selecting-clustered-index}

-   **クラスター化インデックス**を構築するには、 [主キーの選択に関するガイドライン](#guidelines-to-follow-when-selecting-primary-key)に従ってください。

-   クラスター化インデックスを持たないテーブルと比較して、クラスター化インデックスを持つテーブルは、以下のシナリオにおいて、より優れたパフォーマンスとスループットのメリットを提供します。
    -   データが挿入される際、クラスタ化インデックスによって、ネットワークからのインデックスデータの書き込み回数が1回削減されます。
    -   同等の条件を持つクエリが主キーのみに関係する場合、クラスタ化インデックスによってネットワークからのインデックスデータの読み取り回数が1回削減されます。
    -   範囲条件を含むクエリが主キーのみに関係する場合、クラスタ化インデックスはネットワークからのインデックスデータの読み取り回数を削減します。
    -   同等条件または範囲条件を含むクエリが主キーのプレフィックスのみに関係する場合、クラスタ化インデックスはネットワークからのインデックスデータの複数回の読み取りを削減します。

-   一方、クラスター化インデックスを持つテーブルには、次のような問題が発生する可能性があります。
    -   近い値を持つ主キーを多数挿入すると、書き込みホットスポットの問題が発生する可能性があります。 [主キーを選択する際に従うべきガイドライン](#guidelines-to-follow-when-selecting-primary-key)てください。
    -   主キーのデータ型が64ビットより大きい場合、特にセカンダリインデックスが複数存在する場合は、テーブルデータがより多くのstorage容量を消費します。

-   [クラスター化インデックスを使用するかどうかのデフォルトの動作](/clustered-indexes.md#create-a-table-with-clustered-indexes)を制御するには、システム変数`@@global.tidb_enable_clustered_index`と構成`alter-primary-key` } を使用する代わりに、クラスター化インデックスを使用するかどうかを明示的に指定できます。

### <code>CREATE TABLE</code>文を実行する際に従うべきガイドライン {#guidelines-to-follow-when-executing-the-code-create-table-code-statement}

-   データベーススキーマの変更にクライアント側のDriverやORMを使用することは推奨されません。データベーススキーマの変更には[MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)またはGUIクライアントを使用することをお勧めします。このドキュメントでは、ほとんどのシナリオでSQLファイルを渡してデータベーススキーマを変更するために**MySQLクライアント**を使用します。
-   SQL 開発[テーブルの作成と削除に関する仕様](/develop/dev-guide-sql-development-specification.md#create-and-delete-tables)従ってください。ビジネスアプリケーション内にbuild文とdelete文をラップして判定ロジックを追加することを推奨します。

## あと一歩 {#one-more-step}

このドキュメントで作成されたすべてのテーブルにはセカンダリ インデックスが含まれていないことに注意してください。セカンダリ インデックスを追加するガイドについては、 [セカンダリインデックスの作成](/develop/dev-guide-create-secondary-indexes.md)を参照してください。

## お困りですか？ {#need-help}

-   [不和](https://discord.gg/DQZ2dy3cuc?utm_source=doc)or [スラック](https://slack.tidb.io/invite?team=tidb-community&#x26;channel=everyone&#x26;ref=pingcap-docs)コミュニティに質問してください。
-   [TiDB Cloudのサポートチケットを送信してください](https://tidb.support.pingcap.com/servicedesk/customer/portals)
-   [TiDB Self-Managedのサポートチケットを送信してください](/support.md)
