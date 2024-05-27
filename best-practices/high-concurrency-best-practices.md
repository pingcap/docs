---
title: Highly Concurrent Write Best Practices
summary: このドキュメントでは、TiDB で同時書き込みの多いワークロードを処理するためのベスト プラクティスについて説明します。データ分散、ホットスポット ケース、複雑なホットスポットの問題に関する課題と解決策について説明します。また、パフォーマンスを最適化するためのパラメータ構成についても説明します。
---

# 高度な同時書き込みのベストプラクティス {#highly-concurrent-write-best-practices}

このドキュメントでは、TiDB で同時書き込みの多いワークロードを処理するためのベスト プラクティスについて説明します。これにより、アプリケーション開発が容易になります。

## 対象者 {#target-audience}

このドキュメントは、読者が TiDB の基本を理解していることを前提としています。まず、TiDB の基礎を説明する次の 3 つのブログ記事と[TiDB ベストプラクティス](https://en.pingcap.com/blog/tidb-best-practice/)を読むことをお勧めします。

-   [データストレージ](https://en.pingcap.com/blog/tidb-internal-data-storage/)
-   [コンピューティング](https://en.pingcap.com/blog/tidb-internal-computing/)
-   [スケジュール](https://en.pingcap.com/blog/tidb-internal-scheduling/)

## 同時書き込みの多いシナリオ {#highly-concurrent-write-intensive-scenario}

高度な同時書き込みシナリオは、クリアリングや決済などのアプリケーションでバッチ タスクを実行するときによく発生します。このシナリオには、次の特徴があります。

-   膨大な量のデータ
-   履歴データを短時間でデータベースにインポートする必要性
-   短時間でデータベースから大量のデータを読み取る必要がある

これらの機能は、TiDB に次のような課題をもたらします。

-   書き込み容量または読み取り容量は線形に拡張可能である必要があります。
-   大量のデータが同時に書き込まれてもデータベースのパフォーマンスは安定しており、低下しません。

分散データベースでは、すべてのノードの容量を最大限に活用し、単一のノードがボトルネックにならないようにすることが重要です。

## TiDBにおけるデータ分散の原則 {#data-distribution-principles-in-tidb}

上記の課題に対処するには、TiDB のデータ分割とスケジューリングの原則から始める必要があります。詳細については[スケジュール](https://en.pingcap.com/blog/tidb-internal-scheduling/)を参照してください。

TiDB はデータをリージョンに分割します。各リージョンには複数のレプリカがあり、レプリカの各グループはRaftグループと呼ばれます。Raft グループでは、リージョンLeaderがデータ範囲内で読み取りおよび書き込みタスクを実行します (TiDB は[フォロワーを読む](/follower-read.md)をサポートします)。リージョンLeaderは、読み取りおよび書き込みの負荷を均等に分散するために、配置Driver(PD)コンポーネントによって異なる物理ノードに自動的にスケジュールされます。

![TiDB Data Overview](/media/best-practices/tidb-data-overview.png)

理論上、アプリケーションに書き込みホットスポットがない場合、TiDB は、そのアーキテクチャのおかげで、読み取りおよび書き込み容量を線形に拡張できるだけでなく、分散リソースを最大限に活用することもできます。この観点から、TiDB は、同時実行性が高く、書き込みが集中するシナリオに特に適しています。

しかし、実際の状況は理論上の想定とは異なることがよくあります。

> **注記：**
>
> アプリケーションに書き込みホットスポットがないということは、書き込みシナリオに 1 つ`AUTO_INCREMENT`主キーまたは単調に増加するインデックスがないことを意味します。

## ホットスポットケース {#hotspot-case}

次のケースでは、ホットスポットがどのように生成されるかを説明します。以下の表を例に挙げます。

```sql
CREATE TABLE IF NOT EXISTS TEST_HOTSPOT(
      id         BIGINT PRIMARY KEY,
      age        INT,
      user_name  VARCHAR(32),
      email      VARCHAR(128)
)
```

このテーブルは構造が単純です。主キーの`id`以外に、セカンダリ インデックスは存在しません。このテーブルにデータを書き込むには、次のステートメントを実行します。3 `id`ランダムな数値として離散的に生成されます。

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

理論的には、上記の操作は TiDB のベスト プラクティスに準拠しているようで、アプリケーションにホットスポットは発生しません。適切なマシンがあれば、TiDB の分散容量をフルに活用できます。これが本当にベスト プラクティスに準拠しているかどうかを確認するために、実験的環境でテストを実施します。テストの内容は次のとおりです。

クラスター トポロジーには、2 つの TiDB ノード、3 つの PD ノード、および 6 つの TiKV ノードが展開されています。このテストはベンチマークではなく原理を明らかにするためのものであるため、QPS パフォーマンスは無視します。

![QPS1](/media/best-practices/QPS1.png)

クライアントは短時間で「集中的な」書き込み要求を開始します。これは、TiDB によって受信される 3K QPS です。理論上、負荷圧力は 6 つの TiKV ノードに均等に分散されるはずです。ただし、各 TiKV ノードの CPU 使用率から、負荷分散は不均一です。1 `tikv-3`ノードが書き込みホットスポットです。

![QPS2](/media/best-practices/QPS2.png)

![QPS3](/media/best-practices/QPS3.png)

[RaftストアCPU](/grafana-tikv-dashboard.md)は`raftstore`番目のスレッドの CPU 使用率で、通常は書き込み負荷を表します。このシナリオでは、 `tikv-3`がこのRaftグループのLeaderで、 `tikv-0`と`tikv-1`フォロワーです。他のノードの負荷はほぼ空です。

PD の監視メトリックでも、ホットスポットが発生したことが確認されています。

![QPS4](/media/best-practices/QPS4.png)

## ホットスポットの原因 {#hotspot-causes}

上記のテストでは、操作はベスト プラクティスで期待される理想的なパフォーマンスに達していません。これは、TiDB に新しく作成された各テーブルのデータを次のデータ範囲で保存するために、デフォルトで 1 つのリージョンのみが分割されるためです。

    [CommonPrefix + TableID, CommonPrefix + TableID + 1)

短期間のうちに、同じリージョンに大量のデータが継続的に書き込まれます。

![TiKV Region Split](/media/best-practices/tikv-Region-split.png)

上の図は、リージョン分割プロセスを示しています。データが TiKV に継続的に書き込まれると、TiKV はリージョンを複数のリージョンに分割します。リーダー選出は分割されるリージョンLeaderが配置されている元のストアで開始されるため、新しく分割された 2 つのリージョンのリーダーは同じストアに残っている可能性があります。この分割プロセスは、新しく分割されたリージョン2 とリージョン3 でも発生する可能性があります。このように、書き込み圧力は TiKV ノード 1 に集中します。

継続的な書き込みプロセス中に、ノード 1 でホットスポットが発生していることを検出すると、PD は集中しているリーダーを他のノードに均等に分散します。TiKV ノードの数がリージョンレプリカの数より多い場合、TiKV はこれらのリージョンをアイドル ノードに移行しようとします。書き込みプロセス中のこれらの 2 つの操作は、PD の監視メトリックにも反映されます。

![QPS5](/media/best-practices/QPS5.png)

一定期間の連続書き込みの後、PD は TiKV クラスター全体を、圧力が均等に分散される状態に自動的にスケジュールします。その時点で、クラスター全体の容量を完全に使用できます。

ほとんどの場合、ホットスポットを発生させる上記のプロセスは正常であり、データベースのリージョンウォームアップ フェーズです。ただし、同時書き込みが集中するシナリオでは、このフェーズを回避する必要があります。

## ホットスポットソリューション {#hotspot-solution}

理論上期待される理想的なパフォーマンスを実現するには、リージョンを必要な数のリージョンに直接分割し、これらのリージョンをクラスター内の他のノードに事前にスケジュールすることで、ウォームアップ フェーズをスキップできます。

v3.0.x、v2.1.13 以降のバージョンでは、TiDB は[分割リージョン](/sql-statements/sql-statement-split-region.md)と呼ばれる新しい機能をサポートしています。この新しい機能では、次の新しい構文が提供されます。

```sql
SPLIT TABLE table_name [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
```

```sql
SPLIT TABLE table_name [INDEX index_name] BY (value_list) [, (value_list)]
```

ただし、TiDB はこの事前分割操作を自動的に実行しません。その理由は、TiDB 内のデータ分散に関係しています。

![Table Region Range](/media/best-practices/table-Region-range.png)

上の図から、行のキーのエンコード規則によれば、 `rowID`唯一の可変部分です。TiDB では、 `rowID`は`Int64`整数です。ただし、リージョン分割も実際の状況に基づいて行う必要があるため、 `Int64`整数範囲を必要な数の範囲に均等に分割し、これらの範囲を異なるノードに分散する必要がない場合があります。

`rowID`の書き込みが完全に離散的である場合、上記の方法ではホットスポットは発生しません。行 ID またはインデックスが固定範囲またはプレフィックスを持つ場合 (たとえば、 `[2000w, 5000w)`の範囲にデータを離散的に挿入する場合)、ホットスポットも発生しません。ただし、上記の方法を使用してリージョンを分割すると、最初は同じリージョンにデータが書き込まれる可能性があります。

TiDB は一般的な用途のデータベースであり、データ分布について想定していません。そのため、最初はテーブルのデータを格納するために 1 つのリージョンのみを使用し、実際のデータが挿入された後はデータ分布に応じてリージョンを自動的に分割します。

このような状況とホットスポット問題を回避する必要性を考慮して、TiDB は、同時書き込みが頻繁に行われるシナリオでパフォーマンスを最適化するために`Split Region`構文を提供します。上記のケースに基づいて、 `Split Region`構文を使用してリージョンを分散し、負荷分散を観察します。

テストで書き込まれるデータは正の範囲内で完全に離散的であるため、次のステートメントを使用して、テーブルを`minInt64`から`maxInt64`の範囲内の 128 個の領域に事前に分割できます。

```sql
SPLIT TABLE TEST_HOTSPOT BETWEEN (0) AND (9223372036854775807) REGIONS 128;
```

事前分割操作の後、 `SHOW TABLE test_hotspot REGIONS;`ステートメントを実行して、リージョン分散の状態を確認します。3 列`SCATTERING`値がすべて`0`の場合、スケジュールは成功しています。

次の SQL ステートメントを使用して、リージョンリーダーの分布を確認することもできます。1 `table_name`実際のテーブル名に置き換える必要があります。

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

次に、書き込みロードを再度実行します。

![QPS6](/media/best-practices/QPS6.png)

![QPS7](/media/best-practices/QPS7.png)

![QPS8](/media/best-practices/QPS8.png)

明らかなホットスポットの問題が解決されたことがわかります。

この場合、テーブルは単純です。他の場合には、インデックスのホットスポット問題も考慮する必要があります。インデックスリージョンを事前に分割する方法の詳細については、 [分割リージョン](/sql-statements/sql-statement-split-region.md)を参照してください。

## 複雑なホットスポットの問題 {#complex-hotspot-problems}

**問題1:**

テーブルに主キーがない場合、または主キーが`Int`型ではなく、ランダムに分散された主キー ID を生成したくない場合は、TiDB は行 ID として暗黙的に`_tidb_rowid`列を提供します。通常、 `SHARD_ROW_ID_BITS`パラメータを使用しない場合、 `_tidb_rowid`列の値も単調に増加するため、ホットスポットが発生する可能性があります。詳細については、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)を参照してください。

このような状況でホットスポットの問題を回避するには、テーブルを作成するときに`SHARD_ROW_ID_BITS`と`PRE_SPLIT_REGIONS`使用します。 `PRE_SPLIT_REGIONS`の詳細については、 [分割前の地域](/sql-statements/sql-statement-split-region.md#pre_split_regions)を参照してください。

`SHARD_ROW_ID_BITS`は、 `_tidb_rowid`列目に生成された行 ID をランダムに分散するために使用されます。4 `PRE_SPLIT_REGIONS` 、テーブルの作成後にリージョンを事前に分割するために使用されます。

> **注記：**
>
> `PRE_SPLIT_REGIONS`の値は`SHARD_ROW_ID_BITS`の値以下でなければなりません。

例：

```sql
create table t (a int, b int) SHARD_ROW_ID_BITS = 4 PRE_SPLIT_REGIONS=3;
```

-   `SHARD_ROW_ID_BITS = 4` 、 `tidb_rowid`の値が 16 (16=2^4) の範囲にランダムに分散されることを意味します。
-   `PRE_SPLIT_REGIONS=3` 、テーブルが作成後に 8 (2^3) 個のリージョンに事前に分割されることを意味します。

テーブル`t`にデータが書き込まれると、データは事前​​に分割された 8 つのリージョンに書き込まれます。これにより、テーブルの作成後に 1 つのリージョンしか存在しない場合に発生する可能性のあるホットスポットの問題が回避されます。

> **注記：**
>
> `tidb_scatter_region`グローバル変数は`PRE_SPLIT_REGIONS`の動作に影響します。
>
> この変数は、テーブル作成後に結果を返す前に、リージョンが事前に分割され、分散されるまで待機するかどうかを制御します。テーブル作成後に書き込みが集中する場合は、この変数の値を`1`に設定する必要があります。そうすると、すべてのリージョンが分割され、分散されるまで、TiDB は結果をクライアントに返しません。そうしないと、分散が完了する前に TiDB がデータを書き込むため、書き込みパフォーマンスに大きな影響を与えます。

**問題2:**

テーブルの主キーが整数型で、テーブルが主キーの一意性を保証するために`AUTO_INCREMENT`使用している場合 (必ずしも連続または増分である必要はありません)、TiDB は主キーの行値を`_tidb_rowid`として直接使用するため、このテーブルでホットスポットを分散するために`SHARD_ROW_ID_BITS`使用することはできません。

このシナリオの問題に対処するには、データを挿入するときに`AUTO_INCREMENT`を[`AUTO_RANDOM`](/auto-random.md) (列属性) に置き換えます。すると、TiDB は整数の主キー列に値を自動的に割り当て、行 ID の連続性がなくなり、ホットスポットが分散されます。

## パラメータ設定 {#parameter-configuration}

v2.1 では、書き込み競合が頻繁に発生するシナリオでトランザクション競合を事前に識別するために、TiDB に[ラッチ機構](/tidb-configuration-file.md#txn-local-latches)導入されました。その目的は、書き込み競合によって発生する TiDB および TiKV でのトランザクションコミットの再試行を減らすことです。通常、バッチタスクは TiDB にすでに保存されているデータを使用するため、トランザクションの書き込み競合は発生しません。このような状況では、TiDB のラッチを無効にして、小さなオブジェクトのメモリ割り当てを減らすことができます。

    [txn-local-latches]
    enabled = false
