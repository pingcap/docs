---
title: TiFlash MinTSO Scheduler
summary: TiFlash MinTSO Scheduler の実装原則を学びます。
---

# TiFlash MinTSO スケジューラ {#tiflash-mintso-scheduler}

TiFlash MinTSO スケジューラは、 TiFlashの[マルチレベル](/glossary.md#mpp)タスク用の分散スケジューラです。このドキュメントでは、 TiFlash MinTSO スケジューラの実装原理について説明します。

## 背景 {#background}

MPP クエリを処理する際、TiDB はクエリを 1 つ以上の MPP タスクに分割し、これらの MPP タスクを対応するTiFlashノードに送信してコンパイルおよび実行します。TiFlashが[パイプライン実行モデル](/tiflash/tiflash-pipeline-model.md)使用する前に、 TiFlash は各 MPP タスクを実行するために複数のスレッドを使用する必要があります。スレッドの具体的な数は、MPP タスクの複雑さとTiFlashで設定された同時実行パラメータによって異なります。

同時実行性の高いシナリオでは、 TiFlashノードは複数の MPP タスクを同時に受信します。MPP タスクの実行が制御されていない場合、 TiFlash がシステムに要求する必要があるスレッドの数は、MPP タスクの数の増加とともに直線的に増加します。スレッドが多すぎるとTiFlashの実行効率に影響する可能性があります。また、オペレーティング システム自体がサポートするスレッドの数には制限があるため、オペレーティング システムが提供できる数よりも多くのスレッドを要求すると、 TiFlashでエラーが発生します。

高い同時実行性が必要なシナリオで TiFlash の処理能力を向上させるには、 TiFlashに MPP タスク スケジューラを導入する必要があります。

## 実施原則 {#implementation-principles}

[背景](#background)で述べたように、 TiFlashタスク スケジューラを導入する当初の目的は、MPP クエリ実行中に使用されるスレッドの数を制御することです。簡単なスケジューリング戦略は、 TiFlash が要求できるスレッドの最大数を指定することです。各 MPP タスクについて、スケジューラは、システムで現在使用されているスレッドの数と、MPP タスクが使用すると予想されるスレッドの数に基づいて、MPP タスクをスケジュールできるかどうかを決定します。

![TiFlash MinTSO Scheduler v1](/media/tiflash/tiflash_mintso_v1.png)

前述のスケジューリング戦略ではシステム スレッドの数を効果的に制御できますが、MPP タスクは最小の独立した実行単位ではなく、異なる MPP タスク間には依存関係が存在します。

```sql
EXPLAIN SELECT count(*) FROM t0 a JOIN t0 b ON a.id = b.id;
```

    +--------------------------------------------+----------+--------------+---------------+----------------------------------------------------------+
    | id                                         | estRows  | task         | access object | operator info                                            |
    +--------------------------------------------+----------+--------------+---------------+----------------------------------------------------------+
    | HashAgg_44                                 | 1.00     | root         |               | funcs:count(Column#8)->Column#7                          |
    | └─TableReader_46                           | 1.00     | root         |               | MppVersion: 2, data:ExchangeSender_45                    |
    |   └─ExchangeSender_45                      | 1.00     | mpp[tiflash] |               | ExchangeType: PassThrough                                |
    |     └─HashAgg_13                           | 1.00     | mpp[tiflash] |               | funcs:count(1)->Column#8                                 |
    |       └─Projection_43                      | 12487.50 | mpp[tiflash] |               | test.t0.id                                               |
    |         └─HashJoin_42                      | 12487.50 | mpp[tiflash] |               | inner join, equal:[eq(test.t0.id, test.t0.id)]           |
    |           ├─ExchangeReceiver_22(Build)     | 9990.00  | mpp[tiflash] |               |                                                          |
    |           │ └─ExchangeSender_21            | 9990.00  | mpp[tiflash] |               | ExchangeType: Broadcast, Compression: FAST               |
    |           │   └─Selection_20               | 9990.00  | mpp[tiflash] |               | not(isnull(test.t0.id))                                  |
    |           │     └─TableFullScan_19         | 10000.00 | mpp[tiflash] | table:a       | pushed down filter:empty, keep order:false, stats:pseudo |
    |           └─Selection_24(Probe)            | 9990.00  | mpp[tiflash] |               | not(isnull(test.t0.id))                                  |
    |             └─TableFullScan_23             | 10000.00 | mpp[tiflash] | table:b       | pushed down filter:empty, keep order:false, stats:pseudo |
    +--------------------------------------------+----------+--------------+---------------+----------------------------------------------------------+

たとえば、上記のクエリは各TiFlashノードに 2 つの MPP タスクを生成し、 `ExchangeSender_45`エグゼキュータを含む MPP タスクは`ExchangeSender_21`エグゼキュータを含む MPP タスクに依存します。同時実行性の高いシナリオでは、スケジューラがクエリごとに`ExchangeSender_45`を含む MPP タスクをスケジュールすると、システムはデッドロック状態になります。

デッドロックを回避するために、 TiFlash次の 2 つのレベルのスレッド制限が導入されています。

-   thread_soft_limit: システムで使用されるスレッドの数を制限するために使用されます。特定の MPP タスクでは、デッドロックを回避するためにこの制限を破ることができます。
-   thread_hard_limit: システムを保護するために使用されます。システムで使用されるスレッド数がハード制限を超えると、 TiFlash はデッドロックを回避するためにエラーを報告します。

ソフト リミットとハード リミットは、デッドロックを回避するために次のように連携して機能します。ソフト リミットは、すべてのクエリで使用されるスレッドの合計数を制限し、スレッド リソースの枯渇を回避しながらリソースを最大限に活用できるようにします。ハード リミットは、どのような状況でも、システム内の少なくとも 1 つのクエリがソフト リミットを破り、スレッド リソースを取得して実行し続けることができるようにすることで、デッドロックを回避します。スレッド数がハード リミットを超えない限り、システム内には常に 1 つのクエリがあり、そのクエリのすべての MPP タスクを正常に実行できるため、デッドロックを回避できます。

MinTSO スケジューラの目標は、システム スレッドの数を制御しながら、システム内のすべての MPP タスクをスケジュールできる特別なクエリが常に 1 つだけ存在するようにすることです。MinTSO スケジューラは完全に分散されたスケジューラであり、各TiFlashノードは独自の情報のみに基づいて MPP タスクをスケジュールします。したがって、 TiFlashノード上のすべての MinTSO スケジューラは、同じ「特別な」クエリを識別する必要があります。TiDB では、各クエリに読み取りタイムスタンプ ( `start_ts` ) が付いており、MinTSO スケジューラは、現在のTiFlashノードで最小の`start_ts`持つクエリを「特別な」クエリとして定義します。グローバル最小値はローカル最小値でもあるという原則に基づいて、すべてのTiFlashノードによって選択される「特別な」クエリは同じである必要があり、これを MinTSO クエリと呼びます。

MinTSO スケジューラのスケジューリング プロセスは次のとおりです。

![TiFlash MinTSO Scheduler v2](/media/tiflash/tiflash_mintso_v2.png)

ソフト リミットとハード リミットを導入することで、MinTSO スケジューラはシステム スレッドの数を制御しながらシステム デッドロックを効果的に回避します。ただし、同時実行性の高いシナリオでは、ほとんどのクエリで MPP タスクの一部のみがスケジュールされる可能性があります。MPP タスクの一部のみがスケジュールされているクエリは正常に実行できず、システム実行効率が低下します。この状況を回避するために、 TiFlash は、active_set_soft_limit と呼ばれる MinTSO スケジューラのクエリ レベルの制限を導入しています。この制限により、active_set_soft_limit クエリまでの MPP タスクのみがスケジュールに参加できます。他のクエリの MPP タスクはスケジュールに参加せず、現在のクエリが終了した後にのみ新しいクエリがスケジュールに参加できます。この制限はソフト リミットに過ぎません。MinTSO クエリの場合、システム スレッドの数がハード リミットを超えない限り、すべての MPP タスクを直接スケジュールできるためです。

## 参照 {#see-also}

-   [TiFlashを設定する](/tiflash/tiflash-configuration.md) : MinTSO スケジューラを構成する方法を学習します。
