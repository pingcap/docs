---
title: Best Practices for High-Concurrency Writes
summary: このドキュメントでは、TiDBにおける高同時書き込みワークロードの処理に関するベストプラクティスを紹介します。データ分散、ホットスポット発生事例、そして複雑なホットスポット問題に関する課題と解決策を解説します。また、パフォーマンスを最適化するためのパラメータ設定についても解説します。
aliases: ['/ja/tidb/stable/high-concurrency-best-practices/','/ja/tidb/dev/high-concurrency-best-practices/']
---

# 高同時書き込みのベストプラクティス {#best-practices-for-high-concurrency-writes}

このドキュメントでは、TiDB で同時実行性の高い書き込み負荷の高いワークロードを処理するためのベスト プラクティスについて説明します。これは、アプリケーション開発を容易にするのに役立ちます。

## 対象読者 {#target-audience}

このドキュメントは、読者がTiDBの基礎を理解していることを前提としています。まず、TiDBの基礎を解説した以下の3つのブログ記事と、 [TiDB ベストプラクティス](https://www.pingcap.com/blog/tidb-best-practice/)読みいただくことをお勧めします。

-   [データストレージ](https://www.pingcap.com/blog/tidb-internal-data-storage/)
-   [コンピューティング](https://www.pingcap.com/blog/tidb-internal-computing/)
-   [スケジュール](https://www.pingcap.com/blog/tidb-internal-scheduling/)

## 同時書き込みの多いシナリオ {#highly-concurrent-write-intensive-scenario}

高度な同時書き込みシナリオは、決済や清算などのアプリケーションでバッチタスクを実行する際によく発生します。このシナリオには、次のような特徴があります。

-   膨大な量のデータ
-   履歴データを短時間でデータベースにインポートする必要性
-   短時間でデータベースから膨大な量のデータを読み取る必要がある

これらの機能は TiDB に次のような課題をもたらします。

-   書き込み容量または読み取り容量は線形に拡張可能である必要があります。
-   大量のデータが同時に書き込まれてもデータベースのパフォーマンスは安定しており、低下しません。

分散データベースでは、すべてのノードの能力を最大限に活用し、単一のノードがボトルネックにならないようにすることが重要です。

## TiDBにおけるデータ分散の原則 {#data-distribution-principles-in-tidb}

上記の課題に対処するには、TiDBのデータセグメンテーションとスケジューリングの原理から始める必要があります。詳細については[スケジュール](https://www.pingcap.com/blog/tidb-internal-scheduling/)を参照してください。

TiDBはデータをリージョンに分割します。リージョンはそれぞれ、デフォルトで96MBのサイズ制限を持つデータ範囲を表します。各リージョンには複数のレプリカがあり、レプリカの各グループはRaftグループと呼ばれます。RaftRaftでは、リージョンLeaderがデータ範囲内の読み取りおよび書き込みタスク（TiDBは[フォロワー読み取り](/follower-read.md)サポート）を実行します。リージョンLeaderは、Placement Driver （PD）コンポーネントによって自動的に異なる物理ノードにスケジュールされ、読み取りおよび書き込みの負荷を均等に分散します。

![TiDB Data Overview](/media/best-practices/tidb-data-overview.png)

理論上、アプリケーションに書き込みホットスポットがない場合、TiDBはそのアーキテクチャの特性により、読み取りおよび書き込み容量を線形に拡張できるだけでなく、分散リソースを最大限に活用できます。この観点から、TiDBは特に、同時実行性が高く、書き込みが集中するシナリオに適しています。

しかし、実際の状況は理論上の想定とは異なることがよくあります。

> **注記：**
>
> アプリケーションに書き込みホットスポットがないということは、書き込みシナリオに`AUTO_INCREMENT`主キーまたは単調に増加するインデックスがないことを意味します。

## ホットスポットケース {#hotspot-case}

ホットスポットがどのように生成されるかを、以下のケースで説明します。以下の表を例に挙げます。

```sql
CREATE TABLE IF NOT EXISTS TEST_HOTSPOT(
      id         BIGINT PRIMARY KEY,
      age        INT,
      user_name  VARCHAR(32),
      email      VARCHAR(128)
)
```

このテーブルは構造が単純です。主キーの`id`以外に、セカンダリインデックスは存在しません。このテーブルにデータを書き込むには、次のステートメントを実行してください。3 `id`乱数として離散的に生成されます。

```sql
SET SESSION cte_max_recursion_depth = 1000000;
INSERT INTO TEST_HOTSPOT
SELECT
  n,                                       -- ID
  RAND()*80,                               -- Number between 0 and 80
  CONCAT('user-',n),
  CONCAT(
    CHAR(65 + (RAND() * 25) USING ascii),  -- Number between 65 and 65+25, converted to a character, A-Z
    '-user-',
    n,
    '@example.com'
  )
FROM
  (WITH RECURSIVE nr(n) AS 
    (SELECT 1                              -- Start CTE at 1
      UNION ALL SELECT n + 1               -- increase n with 1 every loop
      FROM nr WHERE n < 1000000            -- stop loop at 1_000_000 
    ) SELECT n FROM nr
  ) a;
```

負荷は、上記のステートメントを短時間に集中的に実行することによって発生します。

理論上、上記の操作はTiDBのベストプラクティスに準拠しているように見え、アプリケーションにホットスポットは発生しません。十分なマシン数があれば、TiDBの分散処理能力を最大限に活用できます。これが本当にベストプラクティスに準拠しているかどうかを検証するために、以下の実験的環境でテストを実施しました。

クラスタトポロジーには、TiDBノード2台、PDノード3台、TiKVノード6台が配置されています。このテストはベンチマークではなく原理説明を目的としているため、QPSパフォーマンスは無視してください。

![QPS1](/media/best-practices/QPS1.png)

クライアントは短時間で「集中的な」書き込みリクエストを開始し、TiDBは3K QPSの書き込みを受信しました。理論上、負荷は6つのTiKVノードに均等に分散されるはずです。しかし、各TiKVノードのCPU使用率から判断すると、負荷分散は不均一です。1 `tikv-3`ノードが書き込みのホットスポットとなっています。

![QPS2](/media/best-practices/QPS2.png)

![QPS3](/media/best-practices/QPS3.png)

[RaftストアCPU](/grafana-tikv-dashboard.md)はスレッド`raftstore`のCPU使用率で、通常は書き込み負荷を表します。このシナリオでは、 `tikv-3`がこのRaftグループのLeader、 `tikv-0`と`tikv-1`フォロワーです。他のノードの負荷はほぼ空です。

PD の監視メトリックでも、ホットスポットが発生したことが確認されています。

![QPS4](/media/best-practices/QPS4.png)

## ホットスポットの原因 {#hotspot-causes}

上記のテストでは、ベストプラクティスで期待される理想的なパフォーマンスを達成できていません。これは、TiDBに新しく作成された各テーブルのデータを保存するために、デフォルトで1つのリージョンのみが分割され、以下のデータ範囲が保持されるためです。

    [CommonPrefix + TableID, CommonPrefix + TableID + 1)

短期間のうちに、同じリージョンに大量のデータが継続的に書き込まれます。

![TiKV Region Split](/media/best-practices/tikv-Region-split.png)

上の図は、リージョン分割プロセスを示しています。データがTiKVに継続的に書き込まれると、TiKVはリージョンを複数のリージョンに分割します。リーダー選出は、分割対象のリージョンLeaderが配置されている元のストアで開始されるため、新しく分割された2つのリージョンのリーダーは同じストアに残っている可能性があります。この分割プロセスは、新しく分割されたリージョン2とリージョン3でも発生する可能性があります。このように、書き込み負荷はTiKVノード1に集中します。

継続的な書き込みプロセス中、ノード1でホットスポットが発生していることを検出すると、PDは集中しているリーダーノードを他のノードに均等に分散させます。TiKVノードの数がリージョンレプリカの数よりも多い場合、TiKVはこれらのリージョンをアイドルノードに移行しようとします。書き込みプロセス中のこれらの2つの操作は、PDの監視メトリクスにも反映されます。

![QPS5](/media/best-practices/QPS5.png)

一定期間の連続書き込みの後、PDはTiKVクラスタ全体の負荷が均等に分散される状態を自動的にスケジュールします。その時点で、クラスタ全体の容量を最大限に活用できるようになります。

ほとんどの場合、ホットスポットが発生する上記のプロセスは正常であり、これはデータベースのリージョンウォームアップフェーズです。ただし、同時書き込みが集中するシナリオでは、このフェーズを回避する必要があります。

## ホットスポットソリューション {#hotspot-solution}

理論上期待される理想的なパフォーマンスを実現するには、リージョンを必要な数のリージョンに直接分割し、これらのリージョンをクラスター内の他のノードに事前にスケジュールすることで、ウォームアップ フェーズをスキップできます。

v3.0.x、v2.1.13以降のバージョンでは、TiDBは[分割リージョン](/sql-statements/sql-statement-split-region.md)と呼ばれる新機能をサポートしています。この新機能は、以下の新しい構文を提供します。

```sql
SPLIT TABLE table_name [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
```

```sql
SPLIT TABLE table_name [INDEX index_name] BY (value_list) [, (value_list)]
```

しかし、TiDBはこの事前分割操作を自動的に実行しません。その理由は、TiDB内のデータ分散に関係しています。

![Table Region Range](/media/best-practices/table-Region-range.png)

上の図から、行のキーのエンコーディング規則によれば、 `rowID`のみが可変部分となります。TiDB では、 `rowID`は`Int64`整数です。ただし、リージョン分割も実際の状況に基づいて行う必要があるため、 `Int64`整数範囲を必要な数の範囲に均等に分割し、それらを異なるノードに分散させる必要はないかもしれません。

`rowID`への書き込みが完全に離散的であれば、上記の方法ではホットスポットは発生しません。行IDまたはインデックスが固定範囲またはプレフィックスを持つ場合（例えば、 `[2000w, 5000w)`の範囲にデータを離散的に挿入する場合）、ホットスポットも発生しません。ただし、上記の方法でリージョンを分割した場合、開始時に同じリージョンにデータが書き込まれる可能性があります。

TiDBは汎用的な用途向けのデータベースであり、データ分布について想定していません。そのため、最初はテーブルのデータを格納するために1つのリージョンのみを使用し、実際のデータが挿入された後は、データ分布に応じてリージョンを自動的に分割します。

このような状況とホットスポット問題を回避する必要性を踏まえ、TiDBは`Split Region`構文を使用して、同時書き込みが集中するシナリオでパフォーマンスを最適化します。上記のケースに基づいて、 `Split Region`構文を使用してリージョンを分散させ、負荷分散を観察してみましょう。

テストで書き込まれるデータは正の範囲内で完全に離散的であるため、次のステートメントを使用して、テーブルを`minInt64`から`maxInt64`範囲内の 128 個の領域に事前に分割できます。

```sql
SPLIT TABLE TEST_HOTSPOT BETWEEN (0) AND (9223372036854775807) REGIONS 128;
```

事前分割操作の後、 `SHOW TABLE test_hotspot REGIONS;`のステートメントを実行して、 リージョン scattering の状態を確認します。3 `SCATTERING`の列の値がすべて`0`であれば、スケジューリングは成功です。

次のSQL文を使用して、リージョンリーダーの分布を確認することもできます。1 `table_name`実際のテーブル名に置き換えてください。

```sql
SELECT
    p.STORE_ID,
    COUNT(s.REGION_ID) PEER_COUNT
FROM
    INFORMATION_SCHEMA.TIKV_REGION_STATUS s
    JOIN INFORMATION_SCHEMA.TIKV_REGION_PEERS p ON s.REGION_ID = p.REGION_ID
WHERE
    TABLE_NAME = 'table_name'
    AND p.is_leader = 1
GROUP BY
    p.STORE_ID
ORDER BY
    PEER_COUNT DESC;
```

次に、書き込みロードを再度操作します。

![QPS6](/media/best-practices/QPS6.png)

![QPS7](/media/best-practices/QPS7.png)

![QPS8](/media/best-practices/QPS8.png)

明らかなホットスポットの問題は解決されたことがわかります。

この場合、テーブルは単純です。他のケースでは、インデックスのホットスポット問題も考慮する必要があるかもしれません。インデックスリージョンを事前に分割する方法の詳細については、 [分割リージョン](/sql-statements/sql-statement-split-region.md)を参照してください。

## 複雑なホットスポットの問題 {#complex-hotspot-problems}

**問題1:**

テーブルに主キーがない場合、または主キーが`Int`型ではなく、ランダムに分散された主キーIDを生成したくない場合、TiDBは暗黙的に`_tidb_rowid`列目を行IDとして提供します。一般的に、 `SHARD_ROW_ID_BITS`番目のパラメータを使用しない場合、 `_tidb_rowid`番目の列の値も単調に増加するため、ホットスポットが発生する可能性があります。詳細は[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)を参照してください。

このような状況でホットスポット問題を回避するには、テーブルを作成する際に`SHARD_ROW_ID_BITS`と`PRE_SPLIT_REGIONS`使用できます。 `PRE_SPLIT_REGIONS`の詳細については、 [分割前のリージョン](/sql-statements/sql-statement-split-region.md#pre_split_regions)を参照してください。

`SHARD_ROW_ID_BITS` 、 `_tidb_rowid`列目に生成された行 ID をランダムに散布するために使用されます。4 `PRE_SPLIT_REGIONS` 、テーブルの作成後にリージョンを事前に分割するために使用されます。

> **注記：**
>
> `PRE_SPLIT_REGIONS`の値は`SHARD_ROW_ID_BITS`の値以下でなければなりません。

例：

```sql
create table t (a int, b int) SHARD_ROW_ID_BITS = 4 PRE_SPLIT_REGIONS=3;
```

-   `SHARD_ROW_ID_BITS = 4` 、 `tidb_rowid`の値が 16 (16=2^4) の範囲にランダムに分散されることを意味します。
-   `PRE_SPLIT_REGIONS=3` 、テーブルが作成後に 8 (2^3) 個のリージョンに事前に分割されることを意味します。

テーブル`t`にデータの書き込みが開始されると、データは事前​​に分割された 8 つのリージョンに書き込まれます。これにより、テーブルの作成後に 1 つのリージョンのみが存在する場合に発生する可能性のあるホットスポットの問題が回避されます。

> **注記：**
>
> [`tidb_scatter_region`](/system-variables.md#tidb_scatter_region)グローバル変数は`PRE_SPLIT_REGIONS`の動作に影響します。
>
> この変数は、テーブル作成後に結果を返す前に、リージョンが事前に分割され、分散されるまで待機するかどうかを制御します。テーブル作成後に書き込みが集中する場合は、この変数の値を`global`に設定する必要があります。そうしないと、TiDBはすべてのリージョンが分割され、分散されるまでクライアントに結果を返しません。そうでない場合、TiDBは分散が完了する前にデータを書き込むため、書き込みパフォーマンスに大きな影響を与えます。

**問題2:**

テーブルの主キーが整数型で、テーブルが主キーの一意性を確保するために`AUTO_INCREMENT`使用している場合 (必ずしも連続または増分ではない)、TiDB は主キーの行値を`_tidb_rowid`として直接使用するため、このテーブルでホットスポットを分散するために`SHARD_ROW_ID_BITS`使用することはできません。

このシナリオの問題に対処するには、データを挿入する際に`AUTO_INCREMENT` [`AUTO_RANDOM`](/auto-random.md) （列属性）に置き換えます。そうすることで、TiDBは整数型の主キー列に自動的に値を割り当て、行IDの連続性が失われ、ホットスポットが分散されます。

## パラメータ設定 {#parameter-configuration}

バージョン2.1では、書き込み競合が頻繁に発生するシナリオにおいて、トランザクションの競合を事前に特定するために、TiDBに[ラッチ機構](/tidb-configuration-file.md#txn-local-latches)が導入されました。これは、書き込み競合によるTiDBおよびTiKVにおけるトランザクションコミットの再試行を削減することを目的としています。通常、バッチタスクはTiDBに既に保存されているデータを使用するため、トランザクションの書き込み競合は発生しません。このような状況では、TiDBのラッチを無効化することで、小さなオブジェクトへのメモリ割り当てを削減できます。

    [txn-local-latches]
    enabled = false
