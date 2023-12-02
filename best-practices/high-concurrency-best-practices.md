---
title: Highly Concurrent Write Best Practices
summary: Learn best practices for highly-concurrent write-intensive workloads in TiDB.
---

# 高度な同時書き込みのベスト プラクティス {#highly-concurrent-write-best-practices}

このドキュメントでは、TiDB で同時書き込み負荷の高いワークロードを処理するためのベスト プラクティスについて説明します。これは、アプリケーション開発の促進に役立ちます。

## 対象者 {#target-audience}

このドキュメントは、TiDB の基本を理解していることを前提としています。まず、TiDB の基礎について説明した次の 3 つのブログ記事と[TiDB のベスト プラクティス](https://en.pingcap.com/blog/tidb-best-practice/)を読むことをお勧めします。

-   [データストレージ](https://en.pingcap.com/blog/tidb-internal-data-storage/)
-   [コンピューティング](https://en.pingcap.com/blog/tidb-internal-computing/)
-   [スケジュール設定](https://en.pingcap.com/blog/tidb-internal-scheduling/)

## 同時書き込み集中型のシナリオ {#highly-concurrent-write-intensive-scenario}

高度な同時書き込みシナリオは、清算や決済などのアプリケーションでバッチ タスクを実行するときによく発生します。このシナリオには次の特徴があります。

-   膨大な量のデータ
-   履歴データをデータベースに短時間でインポートする必要がある
-   データベースから大量のデータを短時間で読み取る必要がある

これらの機能により、TiDB に次のような課題が生じます。

-   書き込みまたは読み取り容量は線形に拡張可能である必要があります。
-   データベースのパフォーマンスは安定しており、大量のデータが同時に書き込まれても低下しません。

分散データベースの場合、すべてのノードの容量を最大限に活用し、単一のノードがボトルネックにならないようにすることが重要です。

## TiDB におけるデータ分散の原則 {#data-distribution-principles-in-tidb}

上記の課題に対処するには、TiDB のデータのセグメント化とスケジューリングの原則から始める必要があります。詳細については[スケジュール設定](https://en.pingcap.com/blog/tidb-internal-scheduling/)を参照してください。

TiDB はデータをリージョンに分割し、それぞれがデフォルトで 96M のサイズ制限を持つデータ範囲を表します。各リージョンには複数のレプリカがあり、レプリカの各グループはRaftグループと呼ばれます。 Raftグループでは、リージョンLeaderはデータ範囲内で読み取りおよび書き込みタスク (TiDB は[フォロワー読み取り](/follower-read.md)をサポート) を実行します。リージョンLeaderは、配置Driver(PD)コンポーネントによって自動的に異なる物理ノードに均等にスケジュールされ、読み取りおよび書き込みの圧力が分散されます。

![TiDB Data Overview](/media/best-practices/tidb-data-overview.png)

理論上、アプリケーションに書き込みホットスポットがない場合、TiDB はそのアーキテクチャのおかげで、読み取りおよび書き込み容量を線形に拡張できるだけでなく、分散リソースを最大限に活用することもできます。この観点から、TiDB は、同時実行性が高く、書き込み集中型のシナリオに特に適しています。

しかし、実際の状況は理論上の想定と異なることがよくあります。

> **注記：**
>
> アプリケーションに書き込みホットスポットがないということは、書き込みシナリオに主キーが`AUTO_INCREMENT`も単調増加するインデックスも存在しないことを意味します。

## ホットスポットの場合 {#hotspot-case}

次のケースでは、ホットスポットがどのように生成されるかを説明します。以下の表を例として挙げます。

```sql
CREATE TABLE IF NOT EXISTS TEST_HOTSPOT(
      id         BIGINT PRIMARY KEY,
      age        INT,
      user_name  VARCHAR(32),
      email      VARCHAR(128)
)
```

このテーブルは構造が単純です。主キーとしての`id`のほかに、副インデックスは存在しません。次のステートメントを実行して、このテーブルにデータを書き込みます。 `id`は乱数として離散的に生成される。

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

上記のステートメントを短時間に集中的に実行すると、負荷が発生します。

理論的には、上記の操作は TiDB のベスト プラクティスに準拠していると思われ、アプリケーションでホットスポットは発生しません。 TiDB の分散容量は、適切なマシンを使用すれば最大限に活用できます。本当にベスト プラクティスに従っているかどうかを検証するために、次のように説明される実験的環境でテストが実行されます。

クラスター トポロジには、2 つの TiDB ノード、3 つの PD ノード、および 6 つの TiKV ノードが展開されます。このテストはベンチマークではなく原理を明確にすることを目的としているため、QPS のパフォーマンスは無視してください。

![QPS1](/media/best-practices/QPS1.png)

クライアントは短時間で「集中的な」書き込みリクエストを開始します。これは、TiDB が受信する 3K QPS です。理論的には、負荷圧力は 6 つの TiKV ノードに均等に分散される必要があります。ただし、各 TiKV ノードの CPU 使用率を見ると、負荷分散は不均一です。 `tikv-3`ノードは書き込みホットスポットです。

![QPS2](/media/best-practices/QPS2.png)

![QPS3](/media/best-practices/QPS3.png)

[RaftストアCPU](/grafana-tikv-dashboard.md)は`raftstore`スレッドの CPU 使用率で、通常は書き込み負荷を表します。このシナリオでは、 `tikv-3`がこのRaftグループのLeaderです。 `tikv-0`と`tikv-1`はフォロワーです。他のノードの負荷はほぼ空です。

PD のモニタリング メトリックによっても、ホットスポットが発生していることが確認されます。

![QPS4](/media/best-practices/QPS4.png)

## ホットスポットの原因 {#hotspot-causes}

上記のテストでは、動作はベスト プラクティスで期待される理想的なパフォーマンスに達していません。これは、TiDB に新しく作成された各テーブルのデータを次のデータ範囲で保存するためにデフォルトで 1 つのリージョンのみが分割されるためです。

    [CommonPrefix + TableID, CommonPrefix + TableID + 1)

短期間に、同じリージョンに大量のデータが継続的に書き込まれます。

![TiKV Region Split](/media/best-practices/tikv-Region-split.png)

上の図は、リージョン分割プロセスを示しています。データが継続的に TiKV に書き込まれると、TiKV は 1 つのリージョンを複数のリージョンに分割します。リーダーの選挙は、分割されるリージョンLeaderが配置されている元のストアで開始されるため、新しく分割された 2 つのリージョンのリーダーはまだ同じストアにいる可能性があります。この分割プロセスは、新しく分割されたリージョン2 とリージョン3 でも発生する可能性があります。このようにして、書き込みプレッシャーは TiKV ノード 1 に集中します。

連続書き込み処理中に、ノード 1 でホットスポットが発生していることを検出した後、PD は集中したリーダーを他のノードに均等に分配します。 TiKV ノードの数がリージョンレプリカの数よりも多い場合、TiKV はこれらのリージョンをアイドル ノードに移行しようとします。書き込みプロセス中のこれら 2 つの操作は、PD の監視メトリックにも反映されます。

![QPS5](/media/best-practices/QPS5.png)

一定期間の連続書き込みの後、PD は TiKV クラスター全体を圧力が均等に分散される状態に自動的にスケジュールします。その時点までに、クラスター全体の容量を完全に使用できるようになります。

ほとんどの場合、ホットスポットを引き起こす上記のプロセスは正常であり、データベースのリージョンのウォームアップ フェーズです。ただし、同時書き込み集中型のシナリオでは、このフェーズを回避する必要があります。

## ホットスポット ソリューション {#hotspot-solution}

理論上期待される理想的なパフォーマンスを達成するには、リージョンを必要な数のリージョンに直接分割し、これらのリージョンをクラスター内の他のノードに事前にスケジュールすることで、ウォームアップ フェーズをスキップできます。

v3.0.x、v2.1.13 以降のバージョンでは、TiDB は[分割リージョン](/sql-statements/sql-statement-split-region.md)と呼ばれる新機能をサポートします。この新機能では、次の新しい構文が提供されます。

```sql
SPLIT TABLE table_name [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
```

```sql
SPLIT TABLE table_name [INDEX index_name] BY (value_list) [, (value_list)]
```

ただし、TiDB はこの分割前の操作を自動的に実行しません。その理由は、TiDB 内のデータ分散に関連しています。

![Table Region Range](/media/best-practices/table-Region-range.png)

上の図から、行のキーのエンコード規則によれば、可変部分は`rowID`だけです。 TiDB では、 `rowID`は`Int64`整数です。ただし、リージョン分割も実際の状況に基づいて行う必要があるため、 `Int64`の整数範囲を希望の範囲数に均等に分割してから、これらの範囲を別のノードに分散する必要はない場合があります。

`rowID`の書き込みが完全に離散的であれば、上記の方法ではホットスポットは発生しません。行 ID またはインデックスに固定の範囲またはプレフィックスがある場合 (たとえば、データを`[2000w, 5000w)`の範囲に個別に挿入する)、ホットスポットも発生しません。ただし、上記の方法でリージョンを分割した場合、最初は同じリージョンにデータが書き込まれる可能性があります。

TiDB は一般的な使用を目的としたデータベースであり、データの分散については想定していません。したがって、最初は 1 つのリージョンのみを使用してテーブルのデータを保存し、実際のデータが挿入された後、データの分布に従ってリージョンを自動的に分割します。

この状況とホットスポット問題を回避する必要性を考慮して、TiDB は同時書き込み負荷の高いシナリオのパフォーマンスを最適化する`Split Region`構文を提供します。上記のケースに基づいて、 `Split Region`構文を使用してリージョンを分散し、負荷分散を観察します。

テストで書き込まれるデータは正の範囲内で完全に離散的であるため、次のステートメントを使用して、テーブルを`minInt64`から`maxInt64`の範囲内の 128 個のリージョンに事前分割できます。

```sql
SPLIT TABLE TEST_HOTSPOT BETWEEN (0) AND (9223372036854775807) REGIONS 128;
```

分割前の操作後、 `SHOW TABLE test_hotspot REGIONS;`ステートメントを実行してリージョン分散のステータスを確認します。 `SCATTERING`列の値がすべて`0`であれば、スケジュールは成功です。

次の SQL ステートメントを使用して、リージョンリーダーの分布を確認することもできます。 `table_name`実際のテーブル名に置き換える必要があります。

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

明らかなホットスポットの問題が解決されたことがわかります。

この場合、テーブルは単純です。他の場合には、インデックスのホットスポットの問題も考慮する必要があるかもしれません。インデックスリージョン を事前に分割する方法の詳細については、 [分割リージョン](/sql-statements/sql-statement-split-region.md)を参照してください。

## 複雑なホットスポットの問題 {#complex-hotspot-problems}

**問題 1:**

テーブルに主キーがない場合、または主キーが`Int`タイプではなく、ランダムに分散された主キー ID を生成したくない場合、TiDB は暗黙的な`_tidb_rowid`列を行 ID として提供します。一般に、 `SHARD_ROW_ID_BITS`パラメータを使用しない場合、 `_tidb_rowid`列の値も単調増加するため、ホットスポットが発生する可能性があります。詳細については[`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)を参照してください。

この状況でのホットスポットの問題を回避するには、テーブルを作成するときに`SHARD_ROW_ID_BITS`と`PRE_SPLIT_REGIONS`を使用します。 `PRE_SPLIT_REGIONS`の詳細については、 [分割前のリージョン](/sql-statements/sql-statement-split-region.md#pre_split_regions)を参照してください。

`SHARD_ROW_ID_BITS`は、 `_tidb_rowid`列で生成される行 ID をランダムに分散するために使用されます。 `PRE_SPLIT_REGIONS`は、テーブルの作成後にリージョンを事前に分割するために使用されます。

> **注記：**
>
> `PRE_SPLIT_REGIONS`の値は`SHARD_ROW_ID_BITS`の値以下である必要があります。

例：

```sql
create table t (a int, b int) SHARD_ROW_ID_BITS = 4 PRE_SPLIT_REGIONS=3;
```

-   `SHARD_ROW_ID_BITS = 4` `tidb_rowid`の値が 16 (16=2^4) の範囲にランダムに分散されることを意味します。
-   `PRE_SPLIT_REGIONS=3` 、テーブルの作成後にテーブルが 8 (2^3) 個の領域に事前に分割されることを意味します。

table `t`へのデータの書き込みが開始されると、データは分割前の 8 つのリージョンに書き込まれます。これにより、テーブルの作成後にリージョンが1 つしか存在しない場合に発生する可能性のあるホットスポットの問題が回避されます。

> **注記：**
>
> `tidb_scatter_region`グローバル変数は`PRE_SPLIT_REGIONS`の動作に影響を与えます。
>
> この変数は、テーブルの作成後に結果を返す前に、リージョンが事前に分割されて分散されるまで待機するかどうかを制御します。テーブルの作成後に集中的な書き込みがあった場合は、この変数の値を`1`に設定する必要があります。そうすれば、すべてのリージョンが分割されて分散されるまで、TiDB はクライアントに結果を返しません。そうしないと、TiDB は分散が完了する前にデータを書き込み、書き込みパフォーマンスに重大な影響を与えます。

**問題 2:**

テーブルの主キーが整数型で、テーブルが主キーの一意性を保証するために`AUTO_INCREMENT`を使用する場合 (必ずしも連続または増分である必要はありません)、TiDB は行の値を直接使用するため、このテーブルにホットスポットを分散するために`SHARD_ROW_ID_BITS`を使用することはできません。主キーの`_tidb_rowid` 。

このシナリオの問題に対処するには、データを挿入するときに`AUTO_INCREMENT`を[`AUTO_RANDOM`](/auto-random.md) (列属性) に置き換えます。次に、TiDB は整数の主キー列に値を自動的に割り当てます。これにより、行 ID の連続性がなくなり、ホットスポットが分散されます。

## パラメータ設定 {#parameter-configuration}

v2.1 では、書き込み競合が頻繁に発生するシナリオでトランザクション競合を事前に特定するために、TiDB に[ラッチ機構](/tidb-configuration-file.md#txn-local-latches)が導入されました。目的は、書き込み競合によって引き起こされる TiDB および TiKV でのトランザクション コミットの再試行を減らすことです。一般に、バッチ タスクは TiDB に既に保存されているデータを使用するため、トランザクションの書き込み競合は存在しません。この状況では、TiDB のラッチを無効にして、小さなオブジェクトへのメモリ割り当てを減らすことができます。

    [txn-local-latches]
    enabled = false
