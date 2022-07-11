---
title: Create a Table
summary: Learn the definitions, rules, and guidelines in table creation.
---

# テーブルを作成する {#create-a-table}

このドキュメントでは、SQLステートメントと関連するベストプラクティスを使用してテーブルを作成する方法を紹介します。ベストプラクティスを説明するために、TiDBベースの[書店](/develop/dev-guide-bookshop-schema-design.md)アプリケーションの例が提供されています。

## 始める前に {#before-you-start}

このドキュメントを読む前に、次のタスクが完了していることを確認してください。

-   [TiDB CloudでTiDBクラスターを構築する（DevTier）](/develop/dev-guide-build-cluster-in-cloud.md) 。
-   [スキーマ設計の概要](/develop/dev-guide-schema-design-overview.md)を読んでください。
-   [データベースを作成する](/develop/dev-guide-create-database.md) 。

## テーブルとは {#what-is-a-table}

[テーブル](/develop/dev-guide-schema-design-overview.md#table)は、 [データベース](/develop/dev-guide-schema-design-overview.md#database)に従属するTiDBクラスタの論理オブジェクトです。 SQLステートメントから送信されたデータを格納するために使用されます。テーブルは、データレコードを行と列の形式で保存します。テーブルには少なくとも1つの列があります。 `n`列を定義した場合、データの各行には`n`列とまったく同じフィールドがあります。

## テーブルに名前を付ける {#name-a-table}

テーブルを作成するための最初のステップは、テーブルに名前を付けることです。将来、自分自身や同僚に大きな苦痛を与えるような意味のない名前を使用しないでください。会社または組織のテーブル命名規則に従うことをお勧めします。

`CREATE TABLE`ステートメントは通常、次の形式を取ります。

{{< copyable "" >}}

```sql
CREATE TABLE {table_name} ( {elements} );
```

**パラメータの説明**

-   `{table_name}` ：作成するテーブルの名前。
-   `{elements}` ：列定義や主キー定義などのテーブル要素のコンマ区切りリスト。

`bookshop`のデータベースにユーザー情報を格納するためのテーブルを作成する必要があるとします。

単一の列が追加されていないため、次のSQLステートメントはまだ実行できないことに注意してください。

{{< copyable "" >}}

```sql
CREATE TABLE `bookshop`.`users` (
);
```

## 列を定義する {#define-columns}

**列**はテーブルに従属します。各テーブルには少なくとも1つの列があります。列は、各行の値を単一のデータ型の小さなセルに分割することにより、テーブルに構造を提供します。

カラム定義は通常、次の形式を取ります。

```
{column_name} {data_type} {column_qualification}
```

**パラメータの説明**

-   `{column_name}` ：列名。
-   `{data_type}` ：列[データ・タイプ](/basic-features.md#data-types-functions-and-operators) 。
-   `{column_qualification}` ：カラム**レベルの制約**や[生成された列（実験的特徴）](/generated-columns.md)の句などの列の資格。

`nickname`の識別子`id`など、いくつかの列を`users`テーブルに追加でき`balance` 。

{{< copyable "" >}}

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint,
  `nickname` varchar(100),
  `balance` decimal(15,2)
);
```

上記のステートメントでは、フィールドは名前`id`とタイプ[bigint](/data-type-numeric.md#bigint-type)で定義されています。これは、一意のユーザー識別子を表すために使用されます。これは、すべてのユーザーIDが`bigint`タイプでなければならないことを意味します。

次に、長さ制限が100文字の[varchar](/data-type-string.md#varchar-type)タイプの`nickname`という名前のフィールドが定義されます。これは、ユーザーの`nicknames`人が`varchar`タイプを使用し、100文字以下であることを意味します。

最後に、 `balance`という名前のフィールドが追加されます。これは[10進数](/data-type-numeric.md#decimal-type)タイプで、**精度**は`15` 、<strong>スケール</strong>は`2`です。 <strong>Precision</strong>はフィールドの合計桁数を表し、 <strong>scale</strong>は小数点以下の桁数を表します。たとえば、 `decimal(5,2)`は、精度が`5` 、スケールが`2`を意味し、範囲は`-999.99` `999.99` 。 `decimal(6,1)`は、精度が`6` 、スケールが`1`で、範囲が`-99999.9`であることを`99999.9`します。<strong>小数</strong>は[固定小数点タイプ](/data-type-numeric.md#fixed-point-types)で、数値を正確に格納するために使用できます。正確な数値が必要なシナリオ（たとえば、ユーザープロパティ関連）では、必ず<strong>10進</strong>型を使用してください。

[浮動小数点型](/data-type-numeric.md#floating-point-types)は、 [整数型](/data-type-numeric.md#integer-types) 、および[固定小数点タイプ](/data-type-numeric.md#fixed-point-types)を含む他の多くの列データ型を[列挙型](/data-type-string.md#enum-type)し[日付と時刻のタイプ](/data-type-date-and-time.md) 。サポートされている列[データ型](/basic-features.md#data-types-functions-and-operators)を参照して、データベースに保存するデータと一致する**データ型**を使用できます。

もう少し複雑にするために、 `bookshop`のデータのコアとなる`books`のテーブルを定義できます。 `books`の表には、本のID、タイトル、タイプ（たとえば、雑誌、小説、生活、芸術）、株価、価格、および発行日のフィールドが含まれています。

{{< copyable "" >}}

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

このテーブルには、 `users`のテーブルよりも多くのデータ型が含まれています。

-   [int](/data-type-numeric.md#integer-types) ：ディスクを使いすぎたり、パフォーマンス（タイプ範囲が大きすぎる）やデータオーバーフロー（データタイプ範囲が小さすぎる）に影響を与えたりしないように、適切なサイズのタイプを使用することをお勧めします。
-   [日付時刻](/data-type-date-and-time.md) ：**日時**タイプを使用して時刻値を格納できます。
-   [列挙型](/data-type-string.md#enum-type) ：列挙型を使用して、限られた値の選択を格納できます。

## 主キーを選択します {#select-primary-key}

[主キー](/constraints.md#primary-key)は、テーブル内の1つの列または列のセットであり、その値はテーブル内の行を一意に識別します。

> **ノート：**
>
> TiDBの**主キー**のデフォルト定義は、 [InnoDB](https://mariadb.com/kb/en/innodb/) （MySQLの一般的なストレージエンジン）の定義とは異なります。
>
> -   **InnoDB**の場合：<strong>主キー</strong>は一意であり、nullではなく、<strong>インデックスがクラスター化</strong>されています。
>
> -   TiDBの場合：**主キー**は一意であり、nullではありません。ただし、主キーが<strong>クラスター化インデックス</strong>であるとは限りません。代わりに、キーワード`NONCLUSTERED`の別のセットが、<strong>主キー</strong>が<strong>クラスター化インデックス</strong>であるかどうかをさらに制御し`CLUSTERED` 。キーワードが指定されていない場合は、 [クラスタ化インデックス](https://docs.pingcap.com/zh/tidb/stable/clustered-indexes)で説明されているように、システム変数`@@global.tidb_enable_clustered_index`によって制御されます。

**主キー**は`CREATE TABLE`ステートメントで定義されています。 [主キーの制約](/constraints.md#primary-key)では、すべての制約付き列にNULL以外の値のみが含まれている必要があります。

テーブルは、**主キー**なしで、または非整数の<strong>主キー</strong>を使用して作成できます。この場合、TiDBは<strong>暗黙の主キー</strong>として`_tidb_rowid`を作成します。暗黙の主キー`_tidb_rowid`は、その単調に増加する性質のため、書き込みが集中するシナリオで書き込みホットスポットを引き起こす可能性があります。したがって、アプリケーションが書き込みを多用する場合は、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)および[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)パラメーターを使用してデータをシャーディングすることを検討してください。ただし、これは読み取りの増幅につながる可能性があるため、独自のトレードオフを行う必要があります。

テーブルの**主キー**が[整数型](/data-type-numeric.md#integer-types)であり、 `AUTO_INCREMENT`が使用されている場合、 `SHARD_ROW_ID_BITS`を使用してホットスポットを回避することはできません。ホットスポットを回避する必要があり、連続的で増分的な主キーが必要ない場合は、 `AUTO_INCREMENT`ではなく[`AUTO_RANDOM`](/auto-random.md)を使用して、行IDの連続性を排除できます。

ホットスポットの問題を処理する方法の詳細については、 [ホットスポットの問題のトラブルシューティング](/troubleshoot-hot-spot-issues.md)を参照してください。

[主キーを選択するためのガイドライン](#guidelines-to-follow-when-selecting-primary-key)に続いて、次の例は、 `users`テーブルで`AUTO_RANDOM`主キーがどのように定義されているかを示しています。

{{< copyable "" >}}

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100),
  PRIMARY KEY (`id`)
);
```

## クラスター化されているかどうか {#clustered-or-not}

TiDBは、v5.0以降の[クラスター化されたインデックス](/clustered-indexes.md)つの機能をサポートしています。この機能は、主キーを含むテーブルにデータを格納する方法を制御します。これにより、TiDBは、特定のクエリのパフォーマンスを向上させる方法でテーブルを整理することができます。

このコンテキストでのクラスター化という用語は、データがどのように格納されるかを表すものであり、データベースサーバーのグループが連携して動作するものではありません。一部のデータベース管理システムでは、クラスター化インデックスをインデックス編成テーブル（IOT）と呼んでいます。

現在、TiDBの***主キーを含む***テーブルは、次の2つのカテゴリに分類されます。

-   `NONCLUSTERED` ：テーブルの主キーは非クラスター化インデックスです。非クラスター化インデックスを持つテーブルでは、行データのキーは、TiDBによって暗黙的に割り当てられた内部`_tidb_rowid`で構成されます。主キーは本質的に一意のインデックスであるため、非クラスター化インデックスを持つテーブルには、行を格納するために少なくとも2つのキーと値のペアが必要です。
    -   `_tidb_rowid` （キー）-行データ（値）
    -   主キーデータ（キー） `_tidb_rowid` （値）
-   `CLUSTERED` ：テーブルの主キーはクラスター化インデックスです。クラスタ化インデックスを持つテーブルでは、行データのキーは、ユーザーが指定した主キーデータで構成されます。したがって、クラスター化インデックスを持つテーブルは、行を格納するために1つのキーと値のペアのみを必要とします。
    -   主キーデータ（キー）-行データ（値）

[主キーを選択します](#select-primary-key)で説明したように、**クラスター化インデックス**は、キーワード`CLUSTERED`および`NONCLUSTERED`を使用してTiDBで制御されます。

> **ノート：**
>
> TiDBは、テーブルの`PRIMARY KEY`によるクラスタリングのみをサポートします。クラスター化インデックスを有効にすると*、* `PRIMARY KEY`という用語と<em>クラスター化インデックス</em>は同じ意味で使用される場合があります。 `PRIMARY KEY`は制約（論理プロパティ）を示し、クラスター化されたインデックスはデータの格納方法の物理的な実装を示します。

[クラスタ化インデックスを選択するためのガイドライン](#guidelines-to-follow-when-selecting-clustered-index)に続いて、次の例では、 `books`と`users`の間の関連付けを持つテーブルを作成します。これは、 `book`の`ratings`を`users`ます。この例では、テーブルを作成し、 `book_id`と`user_id`を使用して複合主キーを作成し、その**主キー**に<strong>クラスター化インデックス</strong>を作成します。

{{< copyable "" >}}

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

[主キーの制約](#select-primary-key)に加えて、TiDBは、 [NULLではありません](/constraints.md#not-null)制約、 [ユニークキー](/constraints.md#unique-key)制約、 `DEFAULT`などの他の**列制約**もサポートします。完全な制約については、 [TiDBの制約](/constraints.md)のドキュメントを参照してください。

### デフォルト値を設定する {#set-default-value}

列にデフォルト値を設定するには、 `DEFAULT`制約を使用します。デフォルト値では、各列に値を指定せずにデータを挿入できます。

`DEFAULT`と[サポートされているSQL関数](/basic-features.md#data-types-functions-and-operators)を併用して、デフォルトの計算をアプリケーション層の外に移動し、アプリケーション層のリソースを節約できます。計算によって消費されたリソースは消えず、TiDBクラスタに移動されます。通常、デフォルトの時刻でデータを挿入できます。以下は、 `ratings`テーブルのデフォルト値の設定の例です。

{{< copyable "" >}}

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

さらに、データの更新時にデフォルトで現在時刻も入力される場合は、次のステートメントを使用できます（ただし、 `ON UPDATE`の後には[現在の時間に関連するステートメント](https://pingcap.github.io/sqlgram/#NowSymOptionFraction)のみを入力でき、 `DEFAULT`の後には[より多くのオプション](https://pingcap.github.io/sqlgram/#DefaultValueExpr)がサポートされます）。

{{< copyable "" >}}

```sql
CREATE TABLE `bookshop`.`ratings` (
  `book_id` bigint,
  `user_id` bigint,
  `score` tinyint,
  `rated_at` datetime DEFAULT NOW() ON UPDATE NOW(),
  PRIMARY KEY (`book_id`,`user_id`) CLUSTERED
);
```

### 重複する値を防ぐ {#prevent-duplicate-values}

列の値の重複を防ぐ必要がある場合は、 `UNIQUE`制約を使用できます。

たとえば、ユーザーのニックネームが一意であることを確認するには、次のように`users`のテーブルのテーブル作成SQLステートメントを書き直すことができます。

{{< copyable "" >}}

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE,
  PRIMARY KEY (`id`)
);
```

同じ`nickname`を`users`テーブルに挿入しようとすると、エラーが返されます。

### null値を防ぐ {#prevent-null-values}

列のnull値を防ぐ必要がある場合は、 `NOT NULL`制約を使用できます。

例としてユーザーのニックネームを取り上げます。ニックネームが一意であるだけでなくnullでもないことを確認するには、次のように`users`テーブルを作成するためのSQLステートメントを書き直します。

{{< copyable "" >}}

```sql
CREATE TABLE `bookshop`.`users` (
  `id` bigint AUTO_RANDOM,
  `balance` decimal(15,2),
  `nickname` varchar(100) UNIQUE NOT NULL,
  PRIMARY KEY (`id`)
);
```

## HTAP機能を使用する {#use-htap-capabilities}

> **ノート：**
>
> このガイドに記載されている手順は、テスト環境でのクイックスタート***のみ***を目的としています。実稼働環境については、 [HTAPを探索する](/explore-htap.md)を参照してください。

たとえば、 `bookshop`のアプリケーションを使用して`ratings`のテーブルに対してOLAP分析を実行**し、本の評価が評価の時間と有意な相関関係があるかどうか**を照会するとします。これは、ユーザーの本の評価を分析することです。客観的かどうか。次に、 `ratings`個のテーブル全体の`score`個と`rated_at`のフィールドを照会する必要があります。この操作は、OLTPのみのデータベースではリソースを大量に消費します。または、ETLまたはその他のデータ同期ツールを使用して、分析のためにOLTPデータベースから専用のOLAPデータベースにデータをエクスポートすることもできます。

このシナリオでは、OLTPシナリオとOLAPシナリオの両方をサポートする**HTAP（Hybrid Transactional and Analytical Processing）**データベースであるTiDBは、理想的なワンストップデータベースソリューションです。

### 列ベースのデータを複製する {#replicate-column-based-data}

現在、TiDBは**TiFlash**と<strong>TiSpark</strong>の2つのデータ分析エンジンをサポートしています。大規模なデータシナリオ（100 T）の場合、HTAPの主要なソリューションとして<strong>TiFlash MPP</strong>を推奨し、補完的なソリューションとして<strong>TiSpark</strong>を推奨します。 TiDB HTAP機能の詳細については、次のドキュメントを参照してください： [TiDB HTAPのクイックスタートガイド](/quick-start-with-htap.md)および[HTAPを探索する](/explore-htap.md) 。

この例では、 `bookshop`のデータベースのデータ分析エンジンとして[TiFlash](https://docs.pingcap.com/tidb/stable/tiflash-overview)が選択されています。

TiFlashは、展開後にデータを自動的に複製しません。したがって、複製するテーブルを手動で指定する必要があります。

{{< copyable "" >}}

```sql
ALTER TABLE {table_name} SET TIFLASH REPLICA {count};
```

**パラメータの説明**

-   `{table_name}` ：テーブル名。
-   `{count}` ：複製されたレプリカの数。 0の場合、複製されたレプリカは削除されます。

その後、 **TiFlash**はテーブルを複製します。クエリが実行されると、TiDBはコストの最適化に基づいてクエリにTiKV（行ベース）またはTiFlash（列ベース）を自動的に選択します。または、クエリで<strong>TiFlash</strong>レプリカを使用するかどうかを手動で指定することもできます。指定方法については、 [TiDBを使用してTiFlashレプリカを読み取る](/tiflash/use-tidb-to-read-tiflash.md)を参照してください。

### HTAP機能の使用例 {#an-example-of-using-htap-capabilities}

`ratings`のテーブルは、TiFlashの`1`のレプリカを開きます。

{{< copyable "" >}}

```sql
ALTER TABLE `bookshop`.`ratings` SET TIFLASH REPLICA 1;
```

> **ノート：**
>
> クラスタに**TiFlash**ノードが含まれていない場合、このSQLステートメントはエラーを報告します： `1105 - the tiflash replica count: 1 should be less than the total tiflash server count: 0` 。 [TiDB CloudでTiDBクラスターを構築する（DevTier）](/develop/dev-guide-build-cluster-in-cloud.md#step-1-create-a-free-cluster)を使用して、 <strong>TiFlash</strong>を含む無料のクラスタを作成できます。

次に、次のクエリを実行できます。

{{< copyable "" >}}

```sql
SELECT HOUR(`rated_at`), AVG(`score`) FROM `bookshop`.`ratings` GROUP BY HOUR(`rated_at`);
```

[`EXPLAIN ANALYZE`](/sql-statements/sql-statement-explain-analyze.md)ステートメントを実行して、このステートメントが**TiFlash**を使用しているかどうかを確認することもできます。

{{< copyable "" >}}

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
|       └─TableFullScan_9     | 300000.00 | 300000  | cop[tiflash] | table:ratings | tiflash_task:{time:5.98ms, loops:8, threads:1}                                                                                                                                                                                                                                                                                                                       | keep order:false                                                                                                                               | N/A      | N/A  |
+-----------------------------+-----------+---------+--------------+---------------+----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------------------------------------------------------+----------+------+
```

フィールド`cop[tiflash]`が表示されている場合は、タスクが処理のために**TiFlash**に送信されていることを意味します。

## <code>CREATE TABLE</code>ステートメントを実行します {#execute-the-code-create-table-code-statement}

上記のルールに従ってすべてのテーブルを作成すると、 [データベースの初期化](/develop/dev-guide-bookshop-schema-design.md#database-initialization-script-dbinitsql)のスクリプトは次のようになります。表の詳細を確認する必要がある場合は、 [テーブルの説明](/develop/dev-guide-bookshop-schema-design.md#description-of-the-tables)を参照してください。

データベース初期化スクリプト`init.sql`に名前を付けて保存するには、次のステートメントを実行してデータベースを初期化します。

{{< copyable "" >}}

```shell
mysql
    -u root \
    -h {host} \
    -P {port} \
    -p {password} \
    < init.sql
```

`bookshop`データベースの下にあるすべてのテーブルを表示するには、 [`SHOW TABLES`](/sql-statements/sql-statement-show-tables.md#show-full-tables)ステートメントを使用します。

{{< copyable "" >}}

```sql
SHOW TABLES IN `bookshop`;
```

実行結果：

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

## テーブルを作成するときに従うべきガイドライン {#guidelines-to-follow-when-creating-a-table}

このセクションでは、テーブルを作成するときに従う必要のあるガイドラインを示します。

### テーブルに名前を付けるときに従うべきガイドライン {#guidelines-to-follow-when-naming-a-table}

-   **完全修飾**テーブル名（たとえば、 `CREATE TABLE {database_name}. {table_name}` ）を使用します。データベース名を指定しない場合、TiDBは<strong>SQLセッション</strong>で現在のデータベースを使用します。 SQLセッションでデータベースを指定するために`USE {databasename};`を使用しない場合、TiDBはエラーを返します。
-   意味のあるテーブル名を使用してください。たとえば、ユーザーテーブルを作成する必要がある場合は、 `user`の`users`を使用するか、会社または組織の命名規則に従うことができ`t_user` 。会社または組織に命名規則がない場合は、 [テーブルの命名規則](/develop/dev-guide-object-naming-guidelines.md#table-naming-convention)を参照できます。 `t1`などのテーブル`table1`は使用しないでください。
-   複数の単語はアンダースコアで区切られます。名前は32文字以内にすることをお勧めします。
-   異なるビジネスモジュールのテーブル用に個別の`DATABASE`を作成し、それに応じてコメントを追加します。

### 列を定義するときに従うべきガイドライン {#guidelines-to-follow-when-defining-columns}

-   列でサポートされている[データ型](/basic-features.md#data-types-functions-and-operators)を確認し、データ型の制限に従ってデータを整理します。列に保存する予定のデータに適切なタイプを選択します。
-   主キーを選択するための[従うべきガイドライン](#guidelines-to-follow-when-selecting-primary-key)をチェックし、主キー列を使用するかどうかを決定します。
-   クラスタ化インデックスを選択するための[従うべきガイドライン](#guidelines-to-follow-when-selecting-clustered-index)をチェックし、クラスタ化**インデックス**を指定するかどうかを決定します。
-   [列制約の追加](#add-column-constraints)をチェックして、列に制約を追加するかどうかを決定します。
-   意味のある列名を使用してください。会社または組織のテーブル命名規則に従うことをお勧めします。会社または組織に対応する命名規則がない場合は、 [列の命名規則](/develop/dev-guide-object-naming-guidelines.md#column-naming-convention)を参照してください。

### 主キーを選択する際に従うべきガイドライン {#guidelines-to-follow-when-selecting-primary-key}

-   テーブル内で**主キー**または<strong>一意のインデックス</strong>を定義します。
-   **主キー**として意味のある<strong>列</strong>を選択してみてください。
-   パフォーマンス上の理由から、幅の広いテーブルの保存は避けてください。テーブルフィールドの数が`60`を超え、単一行の合計データサイズが`64K`を超えることはお勧めしません。データ長が長すぎるフィールドを別のテーブルに分割することをお勧めします。
-   複雑なデータ型を使用することはお勧めしません。
-   結合するフィールドについては、データ型に一貫性があることを確認し、暗黙的な変換を避けてください。
-   単一の単調なデータ列に**主キー**を定義することは避けてください。単一の単調データ列（たとえば、 `AUTO_INCREMENT`属性を持つ列）を使用して<strong>主キー</strong>を定義する場合、書き込みパフォーマンスに影響を与える可能性があります。可能であれば、 `AUTO_INCREMENT`の代わりに`AUTO_RANDOM`を使用してください。これにより、主キーの連続属性と増分属性が破棄されます。
-   書き込みが集中するシナリオで単一の単調データ列にインデックスを作成する必要がある場合は、この単調データ列を**主キー**として定義する代わりに、 `AUTO_RANDOM`を使用してそのテーブルの<strong>主キー</strong>を作成するか、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)と[`PRE_SPLIT_REGIONS`](/sql-statements/sql-statement-split-region.md#pre_split_regions)を使用できます。 `_tidb_rowid`をシャーディングします。

### クラスタ化インデックスを選択する際に従うべきガイドライン {#guidelines-to-follow-when-selecting-clustered-index}

-   [主キーを選択するためのガイドライン](#guidelines-to-follow-when-selecting-primary-key)に従って、**クラスター化インデックス**を作成します。

-   非クラスター化インデックスを持つテーブルと比較して、クラスター化インデックスを持つテーブルは、次のシナリオでパフォーマンスとスループットの利点が向上します。
    -   データが挿入されると、クラスター化されたインデックスにより、ネットワークからのインデックスデータの書き込みが1回減ります。
    -   同等の条件を持つクエリに主キーのみが含まれる場合、クラスター化インデックスは、ネットワークからのインデックスデータの読み取りを1回減らします。
    -   範囲条件を含むクエリに主キーのみが含まれる場合、クラスター化インデックスは、ネットワークからのインデックスデータの複数の読み取りを減らします。
    -   同等または範囲の条件を持つクエリに主キープレフィックスのみが含まれる場合、クラスター化インデックスは、ネットワークからのインデックスデータの複数の読み取りを削減します。

-   一方、クラスター化インデックスを持つテーブルには、次の問題がある可能性があります。
    -   近い値を持つ多数の主キーを挿入すると、書き込みホットスポットの問題が発生する可能性があります。 [主キーを選択するときに従うべきガイドライン](#guidelines-to-follow-when-selecting-primary-key)に従ってください。
    -   主キーのデータ型が64ビットより大きい場合、特に複数のセカンダリインデックスがある場合、テーブルデータはより多くのストレージスペースを占有します。

-   [クラスタ化インデックスを使用するかどうかのデフォルトの動作](/clustered-indexes.md#create-a-table-with-clustered-indexes)を制御するには、システム変数`@@global.tidb_enable_clustered_index`と構成`alter-primary-key`を使用する代わりに、クラスター化インデックスを使用するかどうかを明示的に指定できます。

### <code>CREATE TABLE</code>ステートメントを実行するときに従うべきガイドライン {#guidelines-to-follow-when-executing-the-code-create-table-code-statement}

-   データベーススキーマの変更を実行するためにクライアント側のDriverまたはORMを使用することはお勧めしません。 [MySQLクライアント](https://dev.mysql.com/doc/refman/8.0/en/mysql.html)を使用するか、GUIクライアントを使用してデータベーススキーマの変更を実行することをお勧めします。このドキュメントでは、 **MySQLクライアント**を使用してSQLファイルを渡し、ほとんどのシナリオでデータベーススキーマの変更を実行します。
-   SQL開発[テーブルの作成と削除の仕様](/develop/dev-guide-sql-development-specification.md#create-and-delete-tables)に従ってください。判断ロジックを追加するために、ビジネスアプリケーション内でビルドステートメントと削除ステートメントをラップすることをお勧めします。

## もう1つのステップ {#one-more-step}

このドキュメントで作成されたすべてのテーブルには、セカンダリインデックスが含まれていないことに注意してください。セカンダリインデックスを追加するためのガイドについては、 [セカンダリインデックスの作成](/develop/dev-guide-create-secondary-indexes.md)を参照してください。
