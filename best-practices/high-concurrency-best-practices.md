---
title: Highly Concurrent Write Best Practices
summary: Learn best practices for highly-concurrent write-intensive workloads in TiDB.
---

# 非常に同時の書き込みのベストプラクティス {#highly-concurrent-write-best-practices}

このドキュメントでは、アプリケーション開発を容易にするのに役立つ、TiDBで書き込みが非常に多いワークロードを処理するためのベストプラクティスについて説明します。

## ターゲットオーディエンス {#target-audience}

このドキュメントは、TiDBの基本を理解していることを前提としています。まず、TiDBの基礎を説明する次の3つのブログ記事と[TiDBのベストプラクティス](https://en.pingcap.com/blog/tidb-best-practice/)を読むことをお勧めします。

-   [データストレージ](https://en.pingcap.com/blog/tidb-internal-data-storage/)
-   [コンピューティング](https://en.pingcap.com/blog/tidb-internal-computing/)
-   [スケジューリング](https://en.pingcap.com/blog/tidb-internal-scheduling/)

## 非常に同時の書き込み集約型シナリオ {#highly-concurrent-write-intensive-scenario}

高度な同時書き込みシナリオは、決済や決済などのアプリケーションでバッチタスクを実行するときによく発生します。このシナリオには、次の機能があります。

-   膨大な量のデータ
-   履歴データを短時間でデータベースにインポートする必要性
-   短時間でデータベースから大量のデータを読み取る必要性

これらの機能は、TiDBに次の課題をもたらします。

-   書き込みまたは読み取りの容量は、線形にスケーラブルである必要があります。
-   データベースのパフォーマンスは安定しており、大量のデータが同時に書き込まれるため、データベースのパフォーマンスが低下することはありません。

分散データベースの場合、すべてのノードの容量を最大限に活用し、単一のノードがボトルネックにならないようにすることが重要です。

## TiDBのデータ配信の原則 {#data-distribution-principles-in-tidb}

上記の課題に対処するには、TiDBのデータセグメンテーションとスケジューリングの原則から始める必要があります。詳細については、 [スケジューリング](https://en.pingcap.com/blog/tidb-internal-scheduling/)を参照してください。

TiDBは、データをリージョンに分割します。各リージョンは、デフォルトでサイズ制限が96Mのデータの範囲を表します。各リージョンには複数のレプリカがあり、レプリカの各グループはラフトグループと呼ばれます。ラフトグループでは、リージョンリーダーがデータ範囲内で読み取りおよび書き込みタスク（TiDBは[フォロワー-読む](/follower-read.md)をサポート）を実行します。リージョンリーダーは、配置ドライバー（PD）コンポーネントによって、読み取りと書き込みの圧力を均等に分散するために、さまざまな物理ノードに自動的にスケジュールされます。

![TiDB Data Overview](/media/best-practices/tidb-data-overview.png)

理論的には、アプリケーションに書き込みホットスポットがない場合、TiDBは、そのアーキテクチャのおかげで、読み取りおよび書き込み容量を線形にスケーリングできるだけでなく、分散リソースを最大限に活用することもできます。この観点から、TiDBは、同時実行性が高く、書き込みが集中するシナリオに特に適しています。

ただし、実際の状況は理論上の仮定とは異なることがよくあります。

> **ノート：**
>
> アプリケーションに書き込みホットスポットがないということは、書き込みシナリオに`AUTO_INCREMENT`の主キーまたは単調に増加するインデックスがないことを意味します。

## ホットスポットケース {#hotspot-case}

次のケースは、ホットスポットがどのように生成されるかを説明しています。以下の表を例として取り上げます。

{{< copyable "" >}}

```sql
CREATE TABLE IF NOT EXISTS TEST_HOTSPOT(
      id         BIGINT PRIMARY KEY,
      age        INT,
      user_name  VARCHAR(32),
      email      VARCHAR(128)
)
```

このテーブルは構造が単純です。主キーとしての`id`に加えて、副次インデックスは存在しません。次のステートメントを実行して、このテーブルにデータを書き込みます。 `id`は乱数として離散的に生成されます。

{{< copyable "" >}}

```sql
INSERT INTO TEST_HOTSPOT(id, age, user_name, email) values(%v, %v, '%v', '%v');
```

負荷は、上記のステートメントを短時間で集中的に実行することから発生します。

理論的には、上記の操作はTiDBのベストプラクティスに準拠しているようであり、アプリケーションでホットスポットは発生しません。 TiDBの分散容量は、適切なマシンで十分に使用できます。それが本当にベストプラクティスに沿っているかどうかを検証するために、次のように説明される実験的環境でテストが実行されます。

クラスタトポロジでは、2つのTiDBノード、3つのPDノード、および6つのTiKVノードが展開されます。このテストはベンチマークではなく原理を明確にするためのものであるため、QPSのパフォーマンスは無視してください。

![QPS1](/media/best-practices/QPS1.png)

クライアントは短時間で「集中的な」書き込み要求を開始します。これは、TiDBが受信する3KQPSです。理論的には、負荷圧力は6つのTiKVノードに均等に分散される必要があります。ただし、各TiKVノードのCPU使用率から、負荷分散は不均一です。 `tikv-3`ノードは書き込みホットスポットです。

![QPS2](/media/best-practices/QPS2.png)

![QPS3](/media/best-practices/QPS3.png)

[ラフトストアCPU](/grafana-tikv-dashboard.md)は`raftstore`スレッドのCPU使用率であり、通常は書き込み負荷を表します。このシナリオでは、 `tikv-3`がこのラフトグループのリーダーです。 `tikv-0`と`tikv-1`はフォロワーです。他のノードの負荷はほとんど空です。

PDの監視メトリックは、ホットスポットが発生したことも確認します。

![QPS4](/media/best-practices/QPS4.png)

## ホットスポットの原因 {#hotspot-causes}

上記のテストでは、操作はベストプラクティスで期待される理想的なパフォーマンスに達していません。これは、新しく作成された各テーブルのデータを次のデータ範囲でTiDBに格納するために、デフォルトで1つのリージョンのみが分割されるためです。

```
[CommonPrefix + TableID, CommonPrefix + TableID + 1)
```

短期間で、大量のデータが同じリージョンに継続的に書き込まれます。

![TiKV Region Split](/media/best-practices/tikv-Region-split.png)

上の図は、リージョン分割プロセスを示しています。データは継続的にTiKVに書き込まれるため、TiKVはリージョンを複数のリージョンに分割します。リーダー選挙は、分割されるリージョンリーダーが配置されている元のストアで開始されるため、新しく分割された2つのリージョンのリーダーが同じストアに残っている可能性があります。この分割プロセスは、新しく分割されたリージョン2とリージョン3でも発生する可能性があります。このように、書き込み圧力はTiKVノード1に集中します。

連続書き込みプロセス中に、ノード1でホットスポットが発生していることを検出した後、PDは集中したリーダーを他のノードに均等に分散します。 TiKVノードの数がリージョンレプリカの数よりも多い場合、TiKVはこれらのリージョンをアイドル状態のノードに移行しようとします。書き込みプロセス中のこれら2つの操作は、PDの監視メトリックにも反映されます。

![QPS5](/media/best-practices/QPS5.png)

継続的な書き込みの期間の後、PDは、圧力が均等に分散される状態にTiKVクラスタ全体を自動的にスケジュールします。その時までに、クラスタ全体の容量を完全に使用することができます。

ほとんどの場合、ホットスポットを発生させる上記のプロセスは正常です。これは、データベースのリージョンウォーミングアップフェーズです。ただし、書き込みが集中するシナリオでは、このフェーズを回避する必要があります。

## ホットスポットソリューション {#hotspot-solution}

理論的に期待される理想的なパフォーマンスを実現するには、リージョンを目的の数のリージョンに直接分割し、クラスタの他のノードに事前にこれらのリージョンをスケジュールすることで、ウォームアップフェーズをスキップできます。

v3.0.x、v2.1.13以降のバージョンでは、TiDBは[スプリットリージョン](/sql-statements/sql-statement-split-region.md)と呼ばれる新機能をサポートします。この新機能は、次の新しい構文を提供します。

{{< copyable "" >}}

```sql
SPLIT TABLE table_name [INDEX index_name] BETWEEN (lower_value) AND (upper_value) REGIONS region_num
```

{{< copyable "" >}}

```sql
SPLIT TABLE table_name [INDEX index_name] BY (value_list) [, (value_list)]
```

ただし、TiDBはこの事前分割操作を自動的に実行しません。その理由は、TiDBでのデータ分散に関連しています。

![Table Region Range](/media/best-practices/table-Region-range.png)

上の図から、行のキーのエンコード規則によれば、 `rowID`が唯一の可変部分です。 TiDBでは、 `rowID`は`Int64`の整数です。ただし、リージョン分割も実際の状況に基づいている必要があるため、 `Int64`の整数範囲を目的の範囲数に均等に分割してから、これらの範囲を異なるノードに分散する必要がない場合があります。

`rowID`の書き込みが完全に離散的である場合、上記の方法ではホットスポットは発生しません。行IDまたはインデックスの範囲またはプレフィックスが固定されている場合（たとえば、データを`[2000w, 5000w)`の範囲に個別に挿入する場合）、ホットスポットも発生しません。ただし、上記の方法を使用してリージョンを分割した場合、データは最初から同じリージョンに書き込まれる可能性があります。

TiDBは一般的な使用のためのデータベースであり、データの分散については想定していません。そのため、テーブルのデータを格納するために最初に1つのリージョンのみを使用し、実際のデータが挿入された後、データ分布に従ってリージョンを自動的に分割します。

この状況とホットスポットの問題を回避する必要があることを考えると、TiDBは、書き込みが非常に多いシナリオのパフォーマンスを最適化するための`Split Region`の構文を提供します。上記のケースに基づいて、 `Split Region`の構文を使用してリージョンを分散し、負荷分散を観察します。

テストで書き込まれるデータは正の範囲内で完全に離散的であるため、次のステートメントを使用して、テーブルを`minInt64`から`maxInt64`の範囲内の128の領域に事前に分割できます。

{{< copyable "" >}}

```sql
SPLIT TABLE TEST_HOTSPOT BETWEEN (0) AND (9223372036854775807) REGIONS 128;
```

事前分割操作の後、 `SHOW TABLE test_hotspot REGIONS;`ステートメントを実行して、領域散乱のステータスを確認します。 `SCATTERING`列の値がすべて`0`の場合、スケジューリングは成功しています。

次のSQLステートメントを使用して、リージョンリーダーの分布を確認することもできます。 `table_name`を実際のテーブル名に置き換える必要があります。

{{< copyable "" >}}

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

この場合、テーブルは単純です。また、インデックスのホットスポットの問題を考慮する必要がある場合もあります。インデックスリージョンを事前に分割する方法の詳細については、 [スプリットリージョン](/sql-statements/sql-statement-split-region.md)を参照してください。

## 複雑なホットスポットの問題 {#complex-hotspot-problems}

**問題1：**

テーブルに主キーがない場合、または主キーが`Int`タイプではなく、ランダムに分散された主キーIDを生成したくない場合、TiDBは行IDとして暗黙の`_tidb_rowid`列を提供します。一般に、 `SHARD_ROW_ID_BITS`パラメーターを使用しない場合、 `_tidb_rowid`列の値も単調に増加し、ホットスポットも発生する可能性があります。詳細については、 [`SHARD_ROW_ID_BITS`](/shard-row-id-bits.md)を参照してください。

この状況でのホットスポットの問題を回避するために、テーブルを作成するときに`SHARD_ROW_ID_BITS`と`PRE_SPLIT_REGIONS`を使用できます。 `PRE_SPLIT_REGIONS`の詳細については、 [分割前の領域](/sql-statements/sql-statement-split-region.md#pre_split_regions)を参照してください。

`SHARD_ROW_ID_BITS`は、 `_tidb_rowid`列で生成された行IDをランダムに分散させるために使用されます。 `PRE_SPLIT_REGIONS`は、テーブルの作成後にリージョンを事前に分割するために使用されます。

> **ノート：**
>
> `PRE_SPLIT_REGIONS`の値は、 `SHARD_ROW_ID_BITS`の値以下である必要があります。

例：

{{< copyable "" >}}

```sql
create table t (a int, b int) SHARD_ROW_ID_BITS = 4 PRE_SPLIT_REGIONS=3;
```

-   `SHARD_ROW_ID_BITS = 4`は、 `tidb_rowid`の値が16（16 = 2 ^ 4）の範囲にランダムに分散されることを意味します。
-   `PRE_SPLIT_REGIONS=3`は、テーブルが作成された後、テーブルが8（2 ^ 3）のリージョンに事前に分割されることを意味します。

データがテーブル`t`に書き込まれ始めると、データは事前に分割された8つのリージョンに書き込まれます。これにより、テーブルの作成後にリージョンが1つしかない場合に発生する可能性のあるホットスポットの問題が回避されます。

> **ノート：**
>
> `tidb_scatter_region`グローバル変数は`PRE_SPLIT_REGIONS`の動作に影響を与えます。
>
> この変数は、テーブルの作成後に結果を返す前に、リージョンが事前に分割および分散されるのを待つかどうかを制御します。テーブルの作成後に集中的な書き込みがある場合は、この変数の値を`1`に設定する必要があります。そうすると、すべてのリージョンが分割されて分散されるまで、TiDBは結果をクライアントに返しません。そうしないと、TiDBはスキャッタリングが完了する前にデータを書き込み、書き込みパフォーマンスに大きな影響を与えます。

**問題2：**

テーブルの主キーが整数型であり、テーブルが主キーの一意性を確保するために`AUTO_INCREMENT`を使用する場合（必ずしも連続または増分である必要はありません）、TiDBは行の値を直接使用するため、 `SHARD_ROW_ID_BITS`を使用してこのテーブルのホットスポットを分散させることはできません。主キーの`_tidb_rowid`として。

このシナリオの問題に対処するために、データを挿入するときに`AUTO_INCREMENT`を[`AUTO_RANDOM`](/auto-random.md) （列属性）に置き換えることができます。次に、TiDBは整数の主キー列に値を自動的に割り当てます。これにより、行IDの連続性が排除され、ホットスポットが分散されます。

## パラメータ設定 {#parameter-configuration}

v2.1では、書き込みの競合が頻繁に発生するシナリオでトランザクションの競合を事前に識別するために、 [ラッチ機構](/tidb-configuration-file.md#txn-local-latches)がTiDBに導入されました。目的は、書き込みの競合によって引き起こされるTiDBおよびTiKVでのトランザクションコミットの再試行を減らすことです。通常、バッチタスクはTiDBにすでに保存されているデータを使用するため、トランザクションの書き込みの競合は存在しません。この状況では、TiDBのラッチを無効にして、小さなオブジェクトへのメモリ割り当てを減らすことができます。

```
[txn-local-latches]
enabled = false
```
